from kafka import TopicPartition, KafkaConsumer,KafkaProducer
from Utilities import *
#consumer = KafkaConsumer('snowtopic',bootstrap_servers=['localhost:9092'])
Index=GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['KAFKA_TOPIC_SNOWDB'])
consumer = KafkaConsumer(configdata['KAFKA'][Index]['TOPIC'],bootstrap_servers=eval(configdata['KAFKA'][Index]['BOOTSTRAP_SERVERS']))	
for message in consumer:	
    print(message.key.decode('utf-8'))
    print(message.value.decode('utf-8'))
    topic=message.key.decode('utf-8')
    data=json.loads(message.value.decode('utf-8').replace("'",'"').replace("None",'null').replace("True",'true').replace("False",'false'))
    #print(type(data))
    SQLTableFormattedDataValues="('"+str(data['payload']['LastModifiedDate']).replace("T"," ").replace("Z","")+"','"+str(data['payload']['ChangeEventHeader']['changeType'])+"','"+str(data['payload']).replace("None",'null').replace("'",'"').replace("True",'true').replace("False",'false')+"')"         
    print(SQLTableFormattedDataValues)
    tableName='CDC_'+str(data['payload']['ChangeEventHeader']['entityName'])
    SalesForceCDCInject(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']),SQLTableFormattedDataValues,tableName)