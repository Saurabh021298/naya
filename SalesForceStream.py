from KafkaProducerStream import *

import asyncio

from aiosfstream import SalesforceStreamingClient,RefreshTokenAuthenticator

async def stream_events():
    # connect to Streaming API
    
    async with SalesforceStreamingClient(
            consumer_key=configdata['SALESFORCE']['AUTHENTICATION']['ClientID'],
            consumer_secret=configdata['SALESFORCE']['AUTHENTICATION']['ClientSecret'],
            username=configdata['SALESFORCE']['AUTHENTICATION']['UserName'],
            password=configdata['SALESFORCE']['AUTHENTICATION']['Password']) as client:

        # subscribe to topics  
        for topicName in configdata['SALESFORCE']['STREAMAPI']['SALESFORCE_PUSHTOPICS']:
            await client.subscribe("/topic/"+topicName)          
            #await client.subscribe("/topic/TCRMAccount")
            #await client.subscribe("/topic/TCRMContact")

        # listen for incoming messages
        async for message in client:
            topic = message["channel"]
            data = message["data"]
            LogMessageInProcessLog(f"Topic..{topic}: Data  {data}")
        ###Insert Into Table    
            SQLTableFormattedDataValues="('"+str(data['event']['createdDate']).replace("T"," ").replace("Z","")+"','"+str(data['event']['type'])+"','"+str(data['sobject']).replace("None",'""').replace("'",'"')+"')"            
            #print(SQLTableFormattedDataValues)"
            SalesForceCDCInject(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']),SQLTableFormattedDataValues,topic.split("/")[2])
        ###Push To Kafka Topic    
            PushSalesForceTopicDataToKafkaTopic(topic,data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_events())
    