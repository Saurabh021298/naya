from KafkaProducerStream import *

import asyncio

from aiosfstream import SalesforceStreamingClient,RefreshTokenAuthenticator,Client

    
async def stream_events():
    # connect to Streaming API
    auth= RefreshTokenAuthenticator(
    consumer_key=configdata['SALESFORCE']['AUTHENTICATION']['ClientID'],
    consumer_secret=configdata['SALESFORCE']['AUTHENTICATION']['ClientSecret'],
    refresh_token=configdata['SALESFORCE']['AUTHENTICATION']['RefreshToken'],)
    client = Client(auth)
    
    #print('client...',client, flush=True)
    ### Open SF Server Connection with below operation
    await client.open()

    # subscribe to topics
    await client.subscribe("/data/ChangeEvents")  
    # listen for incoming messages
    async for message in client:
        topic = message["channel"]
        data = message["data"]
        #data['payload']['ProfileId']="00e3h000001Yti4AAC"
        #data['payload']['UserRoleId']="00E3h000000l5WREAY"
        #data['payload']['UserId']="0053h000006fn0hAAA"
        #data['payload']['ContactId']="0033h000009ANBcAAO"
        #################################################### Additional Capabilities if we need detailed Data 
        for sobjectData in configdata['SALESFORCE']['GETAPI']['SOBJECTS_DETAILED_DATA']['SOBJECTS']:            
            if sobjectData+"Id" in data['payload'].keys() and data['payload'][sobjectData+"Id"]!='null':
                sobjectDetailData=GetApiSalesForce(configdata['SALESFORCE']['GETAPI']['SOBJECTS_DETAILED_DATA']['EndPointURL']+sobjectData+"/"+data['payload'][sobjectData+"Id"])
                data['payload'][sobjectData]=sobjectDetailData

        ''''
        if 'ProfileId' in data['payload'].keys() and data['payload']['ProfileId']!='null':
            ProfileData=GetApiSalesForce(configdata['SALESFORCE']['GETAPI']['GetUserProfile']['EndPointURL']+data['payload']['ProfileId'])
            data['payload']['Profile']=ProfileData
        if 'UserRoleId' in data['payload'].keys()and data['payload']['UserRoleId']!='null':
            RoleData=GetApiSalesForce(configdata['SALESFORCE']['GETAPI']['GetUserRole']['EndPointURL']+data['payload']['UserRoleId'])
            data['payload']['UserRole']=RoleData
        '''
        #####################################################    
        LogMessageInProcessLog(f"Topic..{topic}: Data  "+str(data).replace("None",'null').replace("'",'"').replace("True",'true').replace("False",'false'))
        #print(message)
        if data['payload']['ChangeEventHeader']['changeType'].upper()=="DELETE":
            data['payload']['LastModifiedDate']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') ### Dummy Field Added As this Field is Missing in Delete Operation
    ###Insert Into Table    
        SQLTableFormattedDataValues="('"+str(data['payload']['LastModifiedDate']).replace("T"," ").replace("Z","")+"','"+str(data['payload']['ChangeEventHeader']['changeType'])+"','"+str(data['payload']).replace("None",'null').replace("'",'"').replace("True",'true').replace("False",'false')+"')"         
        print(SQLTableFormattedDataValues, flush=True)
        tableName='CDC_'+str(data['payload']['ChangeEventHeader']['entityName'])
        SalesForceCDCInject(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']),SQLTableFormattedDataValues,tableName)
    ###Push To Kafka Topic    
        PushSalesForceTopicDataToKafkaTopic(tableName,data)
    await client.close()    

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_events())


#SQL Query to extract json column
#SELECT    ActionType, replace(ActionDetailsJson->"$.Name",'"',''),ActionDetailsJson->"$.Site",ActionDetailsJson->"$.FinServ__MarketingOptOut__pc"  FROM tcrm.cdc_account;
#SELECT    ActionType, replace(ActionDetailsJson->"$.Name.FirstName",'"','') ,replace(ActionDetailsJson->"$.Profile.Name",'"','')  FROM tcrm.cdc_user;
