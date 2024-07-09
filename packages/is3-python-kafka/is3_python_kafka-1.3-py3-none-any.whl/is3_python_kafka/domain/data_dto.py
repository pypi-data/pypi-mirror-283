from typing import List


class DataEntity:
    def __init__(self, preData: List[int], pluginDataConfig: str, taskInstanceId: int, taskId: int, nodeId: int,
                 logId: int, headers: str, serverName: str, prjId: int, tenantId: int):
        self.preData = preData
        self.pluginDataConfig = pluginDataConfig
        self.taskInstanceId = taskInstanceId
        self.taskId = taskId
        self.nodeId = nodeId
        self.logId = logId
        self.headers = headers
        self.serverName = serverName
        self.prjId = prjId
        self.tenantId = tenantId
