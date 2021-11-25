from KafkaProducerStream import *

import asyncio

from aiosfstream import SalesforceStreamingClient,RefreshTokenAuthenticator,Client

async def stream_events():
    # connect to Streaming API
    
    async with SalesforceStreamingClient(
            consumer_key=configdata['SALESFORCE']['AUTHENTICATION']['ClientID'],
            consumer_secret=configdata['SALESFORCE']['AUTHENTICATION']['ClientSecret'],
            username=configdata['SALESFORCE']['AUTHENTICATION']['UserName'],
            password=configdata['SALESFORCE']['AUTHENTICATION']['Password']) as client:

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
            print(SQLTableFormattedDataValues)
            tableName='CDC_'+str(data['payload']['ChangeEventHeader']['entityName'])
            SalesForceCDCInject(GetItemIndex(configdata['SEARCH_STRING_FOR_INDEX']['MYSQL1']),SQLTableFormattedDataValues,tableName)
        ###Push To Kafka Topic    
            PushSalesForceTopicDataToKafkaTopic(tableName,data)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(stream_events())


#SQL Query to extract json column
#SELECT    ActionType, replace(ActionDetailsJson->"$.Name",'"',''),ActionDetailsJson->"$.Site",ActionDetailsJson->"$.FinServ__MarketingOptOut__pc"  FROM tcrm.cdc_account;
#SELECT    ActionType, replace(ActionDetailsJson->"$.Name.FirstName",'"','') ,replace(ActionDetailsJson->"$.Profile.Name",'"','')  FROM tcrm.cdc_user;


'''
testdata='{"Name": {"LastName": "sharma", "FirstName": "sourabh"}, "Alias": "sshar", "Email": "saurabhdadhich100@gmail.com", "IsActive": true, "UserType": "Standard", "Username": "saurabhdadhich11200@gmail.com", "UserRoleId": "00E3h000000l5WREAY","ProfileId": "00e3h000001Yti4AAC", "CreatedById": "0053h000006MZdhAAG", "CreatedDate": "2021-11-04T06:56:07.000Z", "LocaleSidKey": "en_IN", "TimeZoneSidKey": "America/Los_Angeles", "CurrencyIsoCode": "INR", "DigestFrequency": "D", "ForecastEnabled": false, "UserPermissions": ["SFContentUser"], "UserPreferences": ["ActivityRemindersPopup", "EventRemindersCheckboxDefault", "TaskRemindersCheckboxDefault", "ShowTitleToExternalUsers", "HideS1BrowserUI", "LightningExperiencePreferred", "HideSfxWelcomeMat"], "EmailEncodingKey": "ISO-8859-1", "EmailPreferences": ["AutoBcc", "StayInTouchReminder"], "LastModifiedById": "0053h000006MZdhAAG", "LastModifiedDate": "2021-11-04T06:56:07.000Z", "ChangeEventHeader": {"recordIds": ["0053h000006goauAAA"], "changeType": "CREATE", "commitUser": "0053h000006MZdhAAG", "entityName": "User", "changeOrigin": "", "commitNumber": 504513558197, "changedFields": [], "sequenceNumber": 1, "transactionKey": "0001e962-2a4d-a86f-3914-5e16953f0057", "commitTimestamp": 1636008967000}, "CommunityNickname": "User16360089459647349714", "LanguageLocaleKey": "en_US", "IsSystemControlled": false, "ReceivesInfoEmails": false, "IsProfilePhotoActive": false, "DefaultCurrencyIsoCode": "INR", "ReceivesAdminInfoEmails": true, "FinServ__ReferrerScore__c": 0.0, "JigsawImportLimitOverride": 300, "DefaultGroupNotificationFrequency": "D"}'

jsonData=json.loads(testdata)
if 'ProfileId1' in jsonData.keys():
    ProfileData=GetApiSalesForce(configdata['SALESFORCE']['GETAPI']['GetUserProfile']['EndPointURL']+jsonData['ProfileId'])
    jsonData['Profile']=ProfileData
if 'UserRoleId' in jsonData.keys():
    RoleData=GetApiSalesForce(configdata['SALESFORCE']['GETAPI']['GetUserRole']['EndPointURL']+jsonData['UserRoleId'])
    jsonData['UserRole']=RoleData

LogMessageInProcessLog(str(jsonData).replace("None",'null').replace("'",'"').replace("True",'true').replace("False",'false'))
exit(0)

'''