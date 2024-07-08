from typing import List

import iaparc_inference.messenger.messenger as messenger


# type DataMsg struct {
#     Uid         string
#     Source      string
#     Data[]byte
#     Params      map[string]string
#     ContentType string
# }

def Init(uid: str, out_links: List[str], in_links: List[str], nats_url: str, queue: str, batch: int):
    _outputs = messenger.StringArray(out_links)
    _inputs = messenger.StringArray(in_links)
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
        datas.append(msg.Data)
        params.append(msg.Params)
        content_types.append(msg.ContentType)
    
    return input_names, uids, sources, datas, params, content_types

def SendData(dest: str, uid: str, source: str, data: bytes, params: dict, content_type: str, err_str: str):
    messenger.MessengerSendReply(dest, uid, source, data, params, content_type, err_str)
    