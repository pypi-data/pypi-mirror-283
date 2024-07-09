from datetime import datetime

from ..custom.execute import Execute
from ..domain.data_dto import DataEntity
from ..utils.kafka_component_util import kafkaComponent
from ..utils.log_util import send_task_log


class KafkaProcessor:
    def __init__(self, serverName, headers):
        self.serverName = serverName
        self.headers = headers
        self.group_id = 'data-central-group'
        self.kafka_component = kafkaComponent(topic=serverName, group_id=self.group_id)

    def processor(self, execute: Execute):
        topic = 'task-distribute-center'
        kafka_consumer = self.kafka_component
        while True:
            start_time = datetime.now()
            data = kafka_consumer.receive()
            dataDto = DataEntity(preData=data['data'], pluginDataConfig=data['pluginDataConfig'],
                                 taskInstanceId=data['taskInstanceId'], taskId=data['taskId'], nodeId=data['nodeId'],
                                 logId=data['logId'], headers=self.headers, serverName=self.serverName,
                                 prjId=data['prjId'],
                                 tenantId=data['tenantId'])
            custom = execute
            result = custom.execute_custom(dataDto)
            message = {'data': result, 'taskId': dataDto.taskId, 'logId': dataDto.logId, 'nodeId': dataDto.nodeId,
                       'prjId': dataDto.prjId, 'taskInstanceId': dataDto.taskInstanceId,
                       'tenantId': data.get('tenantId', '')}
            self.kafka_component.send(topic, message)
            end_time = datetime.now()
            upSecond = (end_time - start_time).total_seconds()
            message_1 = {'importData': data, 'upSecond': upSecond, 'outputData': result, 'statuDesc': '状态描述',
                         'exceptionInfo': '异常信息'}
            print(message_1)
            send_task_log(message_1, dataDto)
