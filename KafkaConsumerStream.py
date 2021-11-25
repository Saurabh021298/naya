from kafka import TopicPartition, KafkaConsumer,KafkaProducer
from Utilities import *
#consumer = KafkaConsumer('snowtopic',bootstrap_servers=['localhost:9092'])
Index=GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['KAFKA_TOPIC_SNOWDB'])
consumer = KafkaConsumer(configdata['KAFKA'][Index]['TOPIC'],bootstrap_servers=eval(configdata['KAFKA'][Index]['BOOTSTRAP_SERVERS']))	
for message in consumer:	
    print(message.key.decode('utf-8'))
    print(message.value.decode('utf-8'))
    topic=message.key.decode('utf-8')
    data=json.loads(message.value.decode('utf-8').replace("'",'"').replace("None",'""').replace("True",'true').replace("False",'false'))
    print(type(data))
    SQLTableFormattedDataValues="('"+str(data['event']['createdDate']).replace("T"," ").replace("Z","")+"','"+str(data['event']['type'])+"','"+str(data['sobject']).replace("None",'""').replace("'",'"').replace("True",'true').replace("False",'false')+"')"            
    SalesForceCDCInject(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']),SQLTableFormattedDataValues,topic.split("/")[2])
