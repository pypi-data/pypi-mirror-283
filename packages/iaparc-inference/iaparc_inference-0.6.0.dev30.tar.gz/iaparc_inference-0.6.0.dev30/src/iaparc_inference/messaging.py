from typing import List

import iaparc_inference.messenger.messenger as messenger
import iaparc_inference.messenger.go as go

# type DataMsg struct {
#     Uid         string
#     Source      string
#     Data[]byte
#     Params      map[string]string
#     ContentType string
# }

def Init(uid: str, out_links: List[str], in_links: List[str], nats_url: str, queue: str, batch: int):
    _outputs = go.Slice_string(out_links)
    _inputs = go.Slice_string(in_links)
    messenger.MessengerInit(_outputs, _inputs, nats_url, queue, batch)
    
def GetDatas(timeout: int):
    msgs = messenger.MessengerGetMsgs(timeout)
    input_names = []
    uids = []
    sources = []
    datas = []
    params = []
    content_types = []
    for msg in msgs:
        input_names.append(msg.InputName)
        uids.append(msg.Uid)
        sources.append(msg.Source)
        datas.append(bytes(msg.Data))
        params.append({k:v for k,v in msg.Params.items()})
        content_types.append(msg.ContentType)
    
    return input_names, uids, sources, datas, params, content_types

def SendData(dest: str, uid: str, source: str, data: bytes, params: dict, content_type: str, err_str: str=""):
    _data = go.Slice_byte(data)
    _params = messenger.Map_string_string(params)
    if err_str == None:
        err_str = ""
    messenger.MessengerSendReply(dest, uid, source, _data, _params, content_type, err_str)
