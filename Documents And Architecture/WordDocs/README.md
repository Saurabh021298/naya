

Sales-force Streaming Events and Kafka Integration
![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.001.png)


# **Document History**

|**Date**|**Version**|**Created By**|**Reviewed By**|
| :- | :- | :- | :- |
|2021-08-16|V5|Nikhil|Kamlesh Kumar Pant|
|||||
|||||
|||||
|||||
|||||
|||||



# **Contents**

` `TOC \o "1-3" \h \z \u [**Solution Architecture**	 PAGEREF _Toc88497729 \h 3](#_Toc88497729)

[**Solution Design/Approach**	 PAGEREF _Toc88497730 \h 3](#_Toc88497730)

[**Setting up Salesforce for Streaming Events:**	 PAGEREF _Toc88497731 \h 4](#_Toc88497731)

[·	Create Connected App:	 PAGEREF _Toc88497732 \h 4](#_Toc88497732)

[·	Acquire Consumer Key and Secret Key:	 PAGEREF _Toc88497733 \h 6](#_Toc88497733)

[·	Acquire refresh token:	 PAGEREF _Toc88497734 \h 7](#_Toc88497734)

[·	Enable Salesforce for CDC:	 PAGEREF _Toc88497735 \h 9](#_Toc88497735)

[·	Enable Salesforce for PushTopic:	 PAGEREF _Toc88497736 \h 9](#_Toc88497736)

[**Application Development:**	 PAGEREF _Toc88497737 \h 11](#_Toc88497737)

[·	Software Requirements:	 PAGEREF _Toc88497738 \h 11](#_Toc88497738)

[·	Installation Details:	 PAGEREF _Toc88497739 \h 12](#_Toc88497739)

[·	Start Gitbash	 PAGEREF _Toc88497740 \h 13](#_Toc88497740)

[·	Start Zookeeper	 PAGEREF _Toc88497741 \h 14](#_Toc88497741)

[·	Start Kafka Server	 PAGEREF _Toc88497742 \h 15](#_Toc88497742)

[·	Create Topics	 PAGEREF _Toc88497743 \h 15](#_Toc88497743)

[·	Application Configuration Details:	 PAGEREF _Toc88497744 \h 16](#_Toc88497744)

[·	Application Development Details:	 PAGEREF _Toc88497745 \h 21](#_Toc88497745)

[**Application Deployment and Testing:**	 PAGEREF _Toc88497746 \h 21](#_Toc88497746)









SALESFORCE - CDC & KAFKA CONNECTOR

This solution is primarily intended for Citibank, where Citi bank requires all the changes related to users -any addition/modification or role changes etc should be reflected in real time to consuming applications.

To Achieve this, application capitalizing salesforce event bus mechanism to capture the CDC Data.
# **Solution Architecture**


![Diagram

Description automatically generated](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.002.png)

# **Solution Design/Approach**

To capture CDC data and storing or redirecting them to HDFS/Databases (Mysql) or Kafka Topics, application (Python) needs to capitalize Salesforce Streaming Events service for capturing real time changing data via SF event bus.

Following steps to be executed across platforms

# **Setting up Salesforce for Streaming Events:**
##
- ## Create Connected App:
\- To create a connected Salesforce app, follow these steps:

\-  Log in to Salesforce with your developer account

\-   In the drop-down list of the account (in the upper-right corner), select **Setup**

\-   In the left-hand pane, search for: **App Manager** and open it

\-   Click on **“New connected App”**

![Create new connected app](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.003.png)



- On the New Connected App page, fill the following required fields under Basic Information:
- **Connected App Name.** For example, "test". The connected app name must be unique within your org. If the connected app was created in the Spring ‘14 release or later, you can reuse the name of a deleted connected app. Only letters, numbers, and underscores are allowed, also avoid using names which ends with "builder".

- **API name.** For example, "test".

- **Contact Email.** your email.

![New connected app form](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.004.png)

- Go to **API (Enable OAuth Settings)** and select Enable OAuth Settings.

- In the **Call back URL** field, enter **https://login.salesforce.com/services/oauth2/token** for a production Org and **https://test.salesforce.com/services/oauth2/token** for a Sandbox Org.
  If you have a custom domain enabled on your org, you must use the custom URL [**https://yourcustomdomain.my.salesforce.com/services/oauth2/token**](https://yourcustomdomain.my.salesforce.com/services/oauth2/token)

- In the **Selected OAuth Scopes** field, select **Access and manage your data (api)**, and then click **Add**.

- Click the **Save** button to save the new Connected App.

![Selected OAuth Scopes](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.005.png)






- On the new app that you just created, click **Manage**


![Manage connected app](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.006.png)

\-     On the page that opens, click the Edit Policies button.

\-    Set **IP Relaxation** to: Relax IP Restrictions

\-    Set **Permitted Users** to: All users may self-authorize

![Manage Salesforce connected app](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.007.png)
##
- ## Acquire Consumer Key and Secret Key:

- Go to the **API (Enable OAuth Settings)** section, and note down the **Consumer Key** and **Consumer Secret**.

![Consumer and secret key](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.008.png)

- Get Your Consumer Key and Client Secrete and Save it in Notepad.
##
- ## Acquire refresh token:
- Log in to Salesforce using your favourite browser, then enter the following request Url in a new tab to get the code. <CONSUMER\_KEY> should be replaced with the obtained Consumer Key in the above step. <YOUR\_INSTANCE> should be replaced with your instance name, in my case it is **ap15**.

https://**<YOUR\_INSTANCE>**.salesforce.com/services/oauth2/authorize?response\_type=code&client\_id=**<CONSUMER\_KEY>**&redirect\_uri=https://login.salesforce.com/

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.009.png)

- Enter request Url in the browser
- Allow access if any alert popup. Then you will see browser is redirecting to a Url like this. You can obtain the code using that Url.

[https://login.salesforce.com/?code=**aPrxYXyxzkuBzbDGdwv67qekAQredtrsWqty38LsdhfREyTRbvdjvTqdbvxPVC__4Cb9xGKDGErtOw%3D%3D**](https://login.salesforce.com/?code=aPrxYXyxzkuBzbj78FV67qekAQpAHyzh9Ry38LsyinKxPVC__Wzov6j6OBFx74Cb9xGKI60AOw%3D%3D)

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.010.png)

\-  The browser will redirect to a Url with the code

\- Get Access token & Refresh token

\-  Send the following curl request to obtain the tokens. <CODE> should be replaced with the      code you obtained in the above step. <CONSUMER\_KEY> and <CONSUMER\_SECRET> should be replaced with obtained keys with the created Connected App.

curl -X POST [https://**<YOUR_INSTANCE>**.salesforce.com/services/oauth2/token?code=**<CODE>**&grant_type=authorization_code&client_id=**<CONSUMER_KEY>**&client_secret=**<CONSUMER_SECRET>**&redirect_uri=https://login.salesforce.com/]()

- You can obtain the **access token** and **refresh token** from the response.

{
**"access\_token":"00D2v000001XKxi\_\_SOMETHING"**,
**"refresh\_token":"5Aep861dlMxAL.LhVTuPRa\_\_SOMETHING"**,
"signature":"MK/YGMNQhPSSnKtYicXlaU\_\_SOMETHING",
"scope":"refresh\_token web api",
"instance\_url":"[https://ap15.salesforce.com](https://ap15.salesforce.com/)",
"id":"[https://login.salesforce.com/id/00D2vKxiEAG/0045Q09vAAL](https://login.salesforce.com/id/00D2v000001XKxiEAG/0052v00000ZQ9OvAAL)",
"token\_type":"Bearer",
"issued\_at":"1570030000198"
}

- If you are not familiar with curl you can use Postman to send the request.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.011.png)



- ## Enable Salesforce for CDC:

- Go in your Salesforce Dev Org. Click on set up.
- Then search Change Data Capture in Quick Find Box.
- Click on change data capture and You will find two boxes in one box all salesforce objects are there and one box is empty.
- So, select the object which changed data event you want.
- In Our case We are selecting Users.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.012.png)
- ## Enable Salesforce for PushTopic:

- The pushTopic record contains a SOQL query. Event notifications are generated for updates that match the query. Alternatively, you can also use Workbench to create a PushTopic. In this sample we using Salesforce Developer Console to create a Push Topic.

- **Login** to the **Salesforce Account**. Navigate to the top right corner of the **Home page** and click the **Setup** icon. Then select **Developer Console**.

![Open the Developer Console.](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.013.png)

- After populating the Developer console, click **Debug** -> Open **Execute Anonymous Window**.

![Open the Anonymous Window.](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.014.png)

- Add the following entry in the **Enter Apex Code** window and click **Execute**.

![Enter Apex code.](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.015.png)

PushTopic pushTopic = **new** PushTopic();

pushTopic.Name = 'Account';

pushTopic.Query = 'SELECT Id, Name FROM Account';

pushTopic.ApiVersion = 37.0;

pushTopic.NotifyForOperationCreate = true;

pushTopic.NotifyForOperationUpdate = true;

pushTopic.NotifyForOperationUndelete = true;

pushTopic.NotifyForOperationDelete = true;

pushTopic.NotifyForFields = 'Referenced';

insert pushTopic;

- We are essentially creating a SOQL query with a few extra parameters that watch for changes in a specified object. If the Push Topic is executed successfully then Salesforce is ready to post notification to WSO2 Salesforce Inbound Endpoint, if any changes are made in the Account object in Salesforce. This is because the below Push Topic has been created for Salesforce's Account object.

# **Application Development:**

- ## Software Requirements:


|**Requirements**|**Version**|**Libraries**|
| :- | :- | :- |
|Python|3.7|<p>Pyodbc,</p><p>Requests,</p><p>Pytz,</p><p>kafka-python,</p><p>mysql-connector,</p><p>aiosfstream</p>|
|Git hub|**-**||
|java|jdk 8||
|Kafka|2.13-2.8||
|PostmanAPI|**-**||
|Salesforce account|Developer account||
||||
||||


- ## Installation Details:

Step 1. Install Python and Required Libraries:

- Consider this process in Windows
- Firstly, install python 3.7 and install all required libraries which mentioned in the starting of this document.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.016.png)

Step 2. Install git hub and git bash in your system.

- Install git 2.33.1 in your system
- See its all command

Step 3. Install Kafka

- Then download kafka 2.13-2.8.0 tar file in your system.
- Move that tar file into C drive and Unzip into it.
- Since it’s based on JVM languages like Scala and Java, you must make sure that you are using Java 7 or greater.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.017.png)

After installing kafka Follow these steps to start kafka server:
- ## Start Gitbash

- Go in Kafka Folder and Right click on any white space. Then click on git bash.
- Minimise First git bash and again follow the first step to open one more git bash.
- Note: check previous git bash and cmd prompt aren’t open at the same time.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.016.png)

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.018.png)![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.019.png)

The easiest way to install Kafka is to download binaries and run it. Since it’s based on JVM languages like Scala and Java, you must make sure that you are using Java 7 or greater.

Kafka is available in two different flavours: One by [Apache foundation](https://kafka.apache.org/downloads) and other by [Confluent](https://www.confluent.io/about/) as a [package](https://www.confluent.io/download/). For this tutorial, I will go with the one provided by Apache foundation. By the way, Confluent was founded by the [original developers](https://www.confluent.io/about/) of Kafka.
##
- ## Start Zookeeper
Kafka relies on Zookeeper, in order to make it run we will have to run Zookeeper first. Write this Command in First git bash.

bin/zookeeper-server-start.sh config/zookeeper.properties

it will display lots of text on the screen, if see the following it means it’s up properly.

2018-06-10 06:36:15,023] INFO maxSessionTimeout set to -1 (org.apache.zookeeper.server.ZooKeeperServer)
[2018-06-10 06:36:15,044] INFO binding to port 0.0.0.0/0.0.0.0:2181 (org.apache.zookeeper.server.NIOServerCnxnFactory)

##
- ## Start Kafka Server
Next, we have to start Kafka broker server in the second git bash:

bin/kafka-server-start.sh config/server.properties

And if you see the following text on the console, it means it’s up.

2018-06-10 06:38:44,477] INFO Kafka commitId: fdcf75ea326b8e07 (org.apache.kafka.common.utils.AppInfoParser)
[2018-06-10 06:38:44,478] INFO [KafkaServer id=0] started (kafka.server.KafkaServer)
##
- ## Create Topics
Messages are published in topics. Use this command to create a new topic.

➜ kafka\_2.11-1.1.0 bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic test
Created topic "test".

You can also list all available topics by running the following command.

➜ kafka\_2.11-1.1.0 bin/kafka-topics.sh --list --zookeeper localhost:2181
test

Step 4. Clone or Download the Python Code.

- Clone or download the python codes from git hub repo
- Unzip that file on desktop

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.016.png)
- ## Application Configuration Details:

Clone or Download the Python Code.

- Clone or download the python codes from git hub repo
- Unzip that file on desktop

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.016.png)

- Set Up Your Configuration in Configuration File:
- Go to the file where all python codes are there.
- Look for a configuration file where all configurations are pre-written in json format.
- You just need to change the configuration as per your requirement.
- Now, Let’s Look into the config file.

**Configuration file (json code):**

|<p>{</p><p>"DATABASE": {</p><p>"MSSQL": [</p><p>{</p><p>"SERVER": "mssqlldb",</p><p>"NAME": "**database\_name**",</p><p>"SCHEMA": "DBO",</p><p>"TABLE\_PREFIX": "**table\_prefix”**</p><p>"DRIVER": "{SQL Server}",</p><p>"AUTH\_TYPE": "WINLOGIN",</p><p>"USERNAME": "**your\_username**",</p><p>"PASSWORD": "**your\_pwd**"</p><p>}</p><p>],</p><p>"MYSQL": [</p><p>{</p><p>"SERVER": "127.0.0.1”,              - **Localhost sever**</p><p>"NAME": "XYZ”,                          - **Database Name**</p><p>"SCHEMA": "“,                            -  **Schema Name**</p><p>"TABLE\_PREFIX": "XYZ”,            -  **Table Prefix**</p><p>"DRIVER": "",                                - **Driver name**</p><p>"AUTH\_TYPE": "WINLOGIN",     - **Authentication Type**</p><p>"USERNAME": "XXXX",                - **your Username**</p><p>"PASSWORD": "XXXX"                 - **your password**</p><p>}</p><p>],</p><p>"SNOWFLAKE": [</p><p>{</p><p>"WAREHOUSE": "PC\_ALTERYX\_WH",</p><p>"DSN": "SnowFlake32",</p><p>"CONNECTION\_URI": "pua75685.snowflakecomputing.com",</p><p>"NAME": "**database\_name**",</p><p>"SCHEMA": "**schema\_name**",</p><p>"TABLE\_NAME": "**table\_name**",</p><p>"STAGE\_NAME": "**Your\_stage\_name**",</p><p>"FILE\_FORMAT\_NAME": "**Filene name**",</p><p>"FILE\_FORMAT\_TYPE": "CSV",</p><p>"FILE\_FIELD\_DELIMITER": ",",</p><p>"SNOWSQL\_CMD": "C:\\\"Program Files\"\\\"Snowflake SnowSQL\"\\snowsql",</p><p>"TABLE\_PREFIX": "Snowflake\_Table\_",</p><p>"DRIVER": "SnowflakeDSIIDriver",</p><p>"USERNAME": "**Your\_Username**",</p><p>"PASSWORD": "**your\_pwd**"</p><p>},</p><p>{</p><p>"WAREHOUSE": "COMPUTE\_WH",</p><p>"DSN": "SnowFlake32",</p><p>"CONNECTION\_URI": "mpa43641.snowflakecomputing.com",</p><p>"NAME": "SNOWDBKK",</p><p>"SCHEMA": "SNOWSCHEMAKK",</p><p>"TABLE\_NAME": "SNOWTABLEKK",</p><p>"STAGE\_NAME": "PY\_MYSQL\_STAGE",</p><p>"FILE\_FORMAT\_NAME": "PYCSV\_FORMAT",</p><p>"FILE\_FORMAT\_TYPE": "CSV",</p><p>"FILE\_FIELD\_DELIMITER": ",",</p><p>"SNOWSQL\_CMD": "C:\\\"Program Files\"\\\"Snowflake SnowSQL\"\\snowsql",</p><p>"TABLE\_PREFIX": "SnowTableKK\_",</p><p>"DRIVER": "SnowflakeDSIIDriver",</p><p>"USERNAME": "**your\_username**",</p><p>"PASSWORD": "**your\_pwd**"</p><p>}</p><p>]</p><p>},</p><p>"CLOUD\_PLATFORM": "AWS",</p><p>"AWS": {</p><p>"AWS\_REGION": "us-west-2",</p><p>"SNS\_NAME\_OR\_ARN": "",</p><p>"SQS\_NAME\_OR\_ARN": "",</p><p>"S3\_BUCKET\_NAME": "",</p><p>"S3\_OBJECT\_NAME": "",</p><p>"AWS\_SNS\_ARN": ""</p><p>},</p><p>"WAREHOUSE\_PLATFORM": "SNOWFLAKE",</p><p>"STREAMING\_SERVICE": "KAFKA",</p><p>"KAFKA": [</p><p>{</p><p>"TOPIC": " **Topic Name** ",</p><p>"SOURCE\_SYSTEM": "SALESFORCE",                - **Source**</p><p>"TARGET\_SYSTEM": "HDFS",                              - **Target**</p><p>"BOOTSTRAP\_SERVERS": "['localhost:9092']"</p><p>}</p><p>],</p><p>"SFTP": [</p><p>{</p><p>"SERVER": "192.168.1.116",</p><p>"PUT\_PATH": "D:\\SnowFlake-UR\\SNOWFLAKE\\Processed\\",</p><p>"GET\_PATH": "D:\\SnowFlake-UR\\SNOWFLAKE\\",</p><p>"USERNAME": "ftpuser",</p><p>"PASSWORD": "password",</p><p>"FILE\_PATTERN": ".\*\\.csv"</p><p>}</p><p>],</p><p>"FTP": [</p><p>{</p><p>"SERVER": "192.168.1.16",</p><p>"PUT\_PATH": "/Processed/",</p><p>"GET\_PATH": "/",</p><p>"USERNAME": "ftpuser",</p><p>"PASSWORD": "password",</p><p>"FILE\_PATTERN": "^[aA0-zZ1]\*\\.csv"</p><p>}</p><p>],</p><p>"PROCESS\_LOG": {</p><p>"LOG\_FILE\_RETENTION\_PERIOD": 10,</p><p>"LOG\_FILE\_MAX\_FILE\_SIZE": 50000000,</p><p>"PRINT\_LOG\_MESSGAE\_ON\_CONSOLE": "YES",</p><p>"ENABLE\_FILE\_LOGGING": "YES",</p><p>"LOG\_LEVEL": "WARNING",</p><p>"LOG\_FILE\_NAME": "LogForSalesForce\_"</p><p>},</p><p>"SYSTEM\_PARAMETERS": {</p><p>"LOCAL\_FILE\_PATH": "C:\\SalesForce-UR\\",</p><p>"CLEANUP\_HISTORICAL\_FILES": "NO",</p><p>"TIMEZONE": "Etc/UTC",</p><p>"CREDENTIAL": "SECRET\_MANAGER\_NO",</p><p>"ENTITY\_NAME": "SNOWFLAKE"</p><p>},</p><p>"SEARCH\_STRING\_FOR\_INDEX": {</p><p>"SNOWFLAKE1": "mpa43641",</p><p>"MSSQL1": "mssqlldb",</p><p>"MYSQL1": "mysql",</p><p>"KAFKA\_TOPIC\_SNOWDB": "salesforceTCRM",</p><p>"FTP\_LOCAL": "192.168.1.16"</p><p>},</p><p>"WEBAPI": {</p><p>"EnableDataSerachWithLIKE": "yes",</p><p>"WebPort": "800",</p><p>"EnableDataSearchAcrossAttributes": "yes",</p><p>"WebContentDisplayType": "TABLE",</p><p>"EnableUserToControlSearch": "Yes",</p><p>"EnableUserFullAccessToSearch": "yes"</p><p>},</p><p>"SALESFORCE": {</p><p>"AUTHENTICATION": {</p><p>"AuthURL": "https://login.salesforce.com/services/oauth2/token",</p><p>"UserName": " **Salesforce Username** ",</p><p>"Password": " **Salesforce Password** ",</p><p>"GrantType": "password",                                         - **Keep it as same**</p><p>"ClientID": " **Your Client Id**",</p><p>"ClientSecret": " **Your Client Secrete** "</p><p>},</p><p>"GETAPI": {</p><p>"GetAccountDetail": {</p><p>"EndPointURL": "https:// <**Your\_Instance\_Url**>.salesforce.com/services/data/v52.0/query/?q=",</p><p>"QueryOrHeaderParameters": "SELECT+Name,Type+FROM+Account"</p><p>},</p><p>"GetUserDetail": {</p><p>"EndPointURL": "https:// <**Your\_Instance\_Url**>.salesforce.com/services/data/v52.0/query/?q=",</p><p>"QueryOrHeaderParameters": "SELECT+Name,Email,UserRoleId,ProfileId,Phone+FROM+User "</p><p>},</p><p>"GetUserProfile": {</p><p>"EndPointURL": "https://<**Your\_Instance\_Url**>.salesforce.com/services/data/v52.0/query/?q=",</p><p>"QueryOrHeaderParameters": "SELECT+Name,Email+FROM+Profile"</p><p>}</p><p>},</p><p>"POSTAPI": {</p><p>"PostAccountDetail": {</p><p>"EndPointURL": "",</p><p>"HeaderParameters": "",</p><p>"BodyParameters": ""</p><p>}</p><p>},</p><p>"STREAMAPI": {</p><p>"SALESFORCE\_PUSHTOPICS": [</p><p>"pushtopic\_name1”,                      - **Your PushTopic Name**</p><p>"Pushtopic\_name2"                        - **Your PushTopic Name**</p><p>]</p><p>}</p><p>}</p><p>}</p>|
| :- |

**SalesForce auth configuration details:**

- Go in configuration file change all the configuration for salesforce Auth.
- Auth url is same as mentioned but write your salesforce instance and write correct Version.
- Paste your username, password, ClientID and client secrete. Get client id and client secrete from Your salesforce connected app which we have done in First Step.

**database configuration details:**

- So, after the salesforce auth now we configure and set up Mysql
- Just Install MySql in your system and then configure it,
- Name the database engine under the database key in json format.
- Then mention server, Name, schema, table\_prefix, driver, auth\_type, Username and password done.

**kafka configuration details:**

- In kafka configuration firstly create the topic while writing the command in git bash. You can follow Third step of this document for it.
- After creating the topic now configure in the json configuration file for kafka setup.
- Under the KAFKA key mention topic name, source system, targeted system and server.
- You also can use SFTP and FTP file protocol services if you have requirement of it. Just set up the file according to your requirement.
- In our case Our source is “Salesforce” and Destination is “Mysql” or any other database and cloud platform.
- You can adjust source and target as per your requirement. This is the complete code for the integration and data migration between any cloud and desktop platform.
- ## Application Development Details:


|**File name**|**File type**|**Working**|
| :- | :- | :- |
|configuration|json|It holds all the configuration of this process.|
|SalesForceStreamCDC|py|This code would subscribe the CDC event channel by using ‘aiosfstream’ library. At the same it will produce the changed data event information in kafka producer and it will store the data in MySql.|
|KafkaConsumerStreamCDC|py|This code is for kafka consumer. It would consume all the changed data.|
|SalesForceStream|py|This code would subscribe the pushTopic by using ‘aiosfstream’ liberary. At the same it will produce the changed data event information in kafka producer and it will store the data in MySql.|
|KafkaConsumerStream|py|This code is for kafka consumer. It would consume all the changed data.|
|SalesForce|py|This file integrates salesforce and python to get all the data from salesforce org.|
|Utilities|py|This file is for general formatting and functional part of configuration file.|
||||

# **Application Deployment and Testing:**

**Now, we are ready with our configuration and the set up.**

**Let’s Implement that how it looks:**

**Note:** when you will download the python code file you will get configuration file as well that you can change in.

Here, our objective is to pull the Changed data information from salesforce using Change data capture and store all the data into MySql.

This is the salesforce streaming data so we are using python liberary called “aiosfstream”.

To run this python code you need to install aiosfstream using this command “pip install aiosfstream”.

Import all other supported libraries which are mentioned in the code itself. Just “pip install” it.

Step 7. Implementation:

- Start the kafka zookeeper and server.  (Follow Third step’s step 3)
- Then Open two command prompts and go into the python codes file using this command: **“cd C:\Users\Username\Desktop\\*python\_codes\_filename\*”**   then enter it.
- Use this command in both cmd prompts.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.020.png)

- Now kafka server is running. So, let’s run python codes in cmd.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)

- In one cmd prompt, type “python SalesForceStreamCDC.py” to run the python file.
- In second cmd prompt, type “python SalesForceConsumerCDC.py”.
- In first code, we are pulling the changed data information from Salesforce and producing it from kafka. At the same time, we are dumping this data into MySql. how we will get the information we will look ahead.
- In second code we are consuming the information in the kafka.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)

- Now Go to salesforce Org and Change some data or add new User in the Users section. (Refer Third Step’s step 5)
- Let’s add New User.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.022.png)

- Type Users in Quick find box.
- Click on Users and then Click on New User
- Fill all the details and save it.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)

- After adding a new user check your cmd prompt for the changed data information.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)

- so, we have got the data here.
- You can get all the information related to create, delete and update data of the salesforce Object.

**Note:**  even you can get all objects data by get request and soql query.

- We have one more python file named “Salesforce.py” for getting all objects data.
- Just go to the cmd prompt and type “python Salesforce.py”.
- You will get all the data from the object you have queried in configuration file.

![](references/Aspose.Words.be9bfa77-d374-4285-a501-ac90684d75a5.021.png)











` `PAGE   \\* MERGEFORMAT 28

