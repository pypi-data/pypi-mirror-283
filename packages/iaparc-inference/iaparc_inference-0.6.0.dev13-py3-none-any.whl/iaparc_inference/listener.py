"""
IA Parc Inference service
Support for inference of IA Parc models
"""
from json import dumps
from math import e
import os
import time
import asyncio
from re import T
import time
import uuid
from inspect import signature
import logging
import logging.config
import nats
from nats import errors as nats_errors
from iaparc_inference.config import Config
from iaparc_inference.data_decoder import decode
from iaparc_inference.data_encoder import DataEncoder
from iaparc_inference.subscription import BatchSubscription
import iaparc_inference.messaging as messaging

Error = ValueError | None

LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=LEVEL,
    force=True,
    format="%(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
LOGGER = logging.getLogger("Inference")
LOGGER.propagate = True


class IAPListener():
    """
    Inference Listener class
    """

    def __init__(self,
                 callback,
                 decode=True,
                 batch:int=-1,
                 inputs:str = "",
                 outputs:str = "",
                 config_path:str= "/opt/pipeline/pipeline.json",
                 url:str="",
                 queue:str=""
                 ):
        """
        Constructor
        Arguments:
        - callback:     Callback function to proccess data
                        callback(data: Any | list[Any], parameters: Optional[dict])
        Optional arguments:
        - inputs:       Input queue name
        - outputs:      Output queue name
        - decode:       Set wether data should be decoded before calling the callback function (default: True)
        - batch:        Batch size for inference (default: -1)
                        If your model do not support batched input, set batch to 1
                        If set to -1, batch size will be determined by the BATCH_SIZE 
                        environment variable
        - config_path:  Path to config file (default: /opt/pipeline/pipeline.json)
        - url:          Url of inference server (default: None)
                        By default determined by the NATS_URL environment variable,
                        however you can orverride it here
        - queue:        Name of queue (default: None)
                        By default determined by the NATS_QUEUE environment variable,
                        however you can orverride it here
        """
        # Init internal variables
        self.decode = decode
        self.timeout = 0.002
        self.exec_time = 0
        self._subs_in = []
        self._subs_out = []
        self._dag = Config(config_path)
        if inputs:
            self._dag.inputs = inputs
        self._inputs_name = self._dag.inputs.split(",")
        self._outputs_name = self._dag.outputs.split(",")
        
        self.lock = asyncio.Lock()
        self.callback = callback
        sig = signature(callback)
        self.callback_args = sig.parameters
        nb_params = len(self.callback_args)
        if nb_params == 1:
            self.callback_has_parameters = False
        else:
            self.callback_has_parameters = True
        
        if url:
            self.url = url
        else:
            self.url = os.environ.get("NATS_URL", "nats://localhost:4222")
        if queue:
            self.queue = queue.replace("/", "-")
        else:
            self.queue = os.environ.get(
                "NATS_QUEUE", "inference").replace("/", "-")
        if batch > 0:
            self.batch = batch
        else:
            self.batch = int(os.environ.get("BATCH_SIZE", 1))
        if self.batch > 1:
            self.is_batch = True
        else:
            self.is_batch = False
        
        self.inputs = {}
        self.outputs = {}
        self.encoders = {}        
        for entity in self._dag.pipeline:
            for item in entity.input_def:
                if "name" in item and item["name"] in self._inputs_name:
                    self.inputs[item["name"]] = item
            for item in entity.output_def:
                if "name" in item and item["name"] in self._outputs_name:
                    self.outputs[item["name"]] = item
                    self.encoders[item["name"]] = DataEncoder(item)
        if outputs and outputs in self._outputs_name:
            self.default_output = self.outputs[outputs]["link"]
        else:
            self.default_output = self.outputs[self._outputs_name[0]]["link"]
        
        # Init go messaging
        messaging.Init(self.queue, self._outputs_name, self._inputs_name, self.url, self.queue, self.batch)

    @property
    def dag(self) -> Config:
        """ Input property """
        return self._dag

    @property
    def inputs_name(self) -> list:
        """ Input property """
        return self._inputs_name

    @property
    def outputs_name(self) -> list:
        return self._outputs_name

    def run(self):
        """
        Run inference service
        """
        timeout: int = 4
        exec_time = 0
        while True:
            input_names, uids, sources, datas, params, content_types = messaging.GetDatas(timeout)
            if len(uids) == 0:
                break
            t0 = time.time()
            self._process_data(input_names, uids, sources,
                               datas, params, content_types)
            t1 = time.time()
            if exec_time == 0:
                exec_time = t1 - t0
            exec_time = (exec_time + t1 - t0) / 2
            if exec_time < 0.02:
                timeout = 2
            else:
                timeout = int(exec_time * 0.15 * 1000)
            
    async def send_msg(self, out, uid, source, data, parameters={}, error=""):
        bdata = "".encode()
        content_type = ""
        if out == "ERROR":
            bdata = data.encode()
        else:
            bdata, content_type, error = self.encoders[out].encode(data)
            if error:
                out = "ERROR"
                bdata = str(error).encode()
                error = "Error encoding data"
        
        messaging.SendData(out, uid, source, bdata,
                           parameters, content_type, error)
            
    def _process_data(self, 
                        names: list[str],
                        uids: list[str],
                        sources: list[str],
                        raw_datas: list[bytes],
                        reqs_parameters: list[str],
                        content_types: list[str]):
        """
        Process data
        Arguments:
        - requests:   list of data to process
        - is_batch:   is batched data
        """
        LOGGER.debug("handle request")
        queue_out = self.default_output
        p_datas = []
        p_sources = []
        p_uids = []
        p_params = []
        for name, uid, src, raw, ctype, params in zip(names, uids, sources, raw_datas, content_types, reqs_parameters):
            if self.decode:
                data, error = decode(raw, ctype, self.inputs[name])
                if error:
                    asyncio.create_task(self.send_msg("ERROR", 
                                                      uid, 
                                                      src,
                                                      str(error), 
                                                      params, 
                                                      "Wrong input"))
                    continue
                p_datas.append(data)
            else:
                p_datas.append(raw)
            p_sources.append(src)
            p_uids.append(uid)
            p_params.append(params)
        
        try_error = ""      
        if len(p_datas) > 0:
            try:
                error = ""
                if self.is_batch:
                    if self.callback_has_parameters:
                        res = self.callback(p_datas, p_params)
                    else:
                        res = self.callback(p_datas)           
                    if isinstance(res, tuple):
                        if len(res) == 2:
                            result, error = res
                        if len(res) == 3:
                            result, out, error = res
                            if out in self.outputs_name:
                                queue_out = self.outputs_name[out]['link']
                    else:
                        result = res
                    if not isinstance(result, list):    
                        error = "batch reply is not a list"
                    if len(p_datas) != len(result):
                        error = "batch reply has wrong size"
                    if error:
                        for uid, source, params in zip(p_uids, p_sources, p_params):
                            asyncio.create_task(self.send_msg(queue_out, 
                                                              uid, 
                                                              source, 
                                                              error, 
                                                              params, 
                                                              error))
                    else:
                        for uid, source, res, params in zip(p_uids, p_sources, result, p_params):
                            asyncio.create_task(self.send_msg(queue_out, 
                                                              uid, 
                                                              source, 
                                                              res,
                                                              params))
                else:
                    if len(p_params) > 0:
                        _params = p_params[0]
                    else:
                        _params = {}
                    if self.callback_has_parameters:
                        res = self.callback(p_datas[0], _params)
                    else:
                        res = self.callback(p_datas[0])
                    if isinstance(res, tuple):
                        if len(res) == 2:
                            result, error = res
                        if len(res) == 3:
                            result, out, error = res
                            if out in self.outputs_name:
                                queue_out = out
                    else:
                        result = res
                    asyncio.create_task(self.send_msg(queue_out, 
                                                      p_uids[0], 
                                                      p_sources[0], 
                                                      result, 
                                                      _params,
                                                      error=error))
                
            except ValueError:
                LOGGER.error("Fatal error message handler", exc_info=True)
                try_error  = "Wrong input"
            except Exception as e: # pylint: disable=W0703
                LOGGER.error("Fatal error message handler", exc_info=True)
                try_error = f'Fatal error: {str(e)}'
            if try_error:
                for uid, source in zip(p_uids, p_sources):
                    asyncio.create_task(self.send_msg(
                        "ERROR", uid, src, try_error, "Wrong input"))
                    
