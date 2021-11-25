from Utilities import *
from SalesForce import *
from kafka import TopicPartition, KafkaConsumer,KafkaProducer

##### Get Index
Index=GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['KAFKA_TOPIC_SNOWDB'])
producer=KafkaProducer(bootstrap_servers=eval(configdata['KAFKA'][Index]['BOOTSTRAP_SERVERS']))

def PushSalesForceTopicDataToKafkaTopic(TopicName,DataFromSalesForce):
    future=producer.send(configdata['KAFKA'][Index]['TOPIC'],key=str(TopicName).encode('utf-8'),value=str(DataFromSalesForce).encode('utf-8'))
    future.get(timeout=10)

#producer.flush()
