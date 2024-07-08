 
## Open IoE

Open IoE is a simple IoT platform to operate IoT devices.

There are two options available,

1. Python Library (Client)

2. Web services (REST APIs)

---

### 1\. Python Library

Users are expected to take these steps,

1. Install Python Library
	`pip install openioe`

2. Write the client code using the following methods

 
#### Method List:

<table><tbody><tr><td><strong>No</strong></td><td><strong>Method</strong></td><td><strong>Description</strong></td><td><strong>Example</strong></td></tr><tr><td>1</td><td>ReadValue</td><td>To read the sensor data from single nodes. Type of data is "Numeric/String"</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xxx
SensorData,ResposeCode=oi.ReadValue()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>2</td><td>WriteValue</td><td>To modify the control signal at single nodes. Type of data is "Numeric/String".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xx
oi.Data=10
SensorData,ResposeCode=oi.WriteValue()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>3</td><td>ReadJSON</td><td>To read the sensor data from single nodes. Type of data is "JSON".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xxx
SensorData,ResposeCode=oi.ReadJSON()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>4</td><td>WriteJSON</td><td>To modify the control signal at single nodes. Type of data is "JSON".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xxx
oi.DataJSON={'Value': '10'}
SensorData,ResposeCode=oi.WriteJSON()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>5</td><td>ReadXML</td><td>To read the sensor data from single nodes. Type of data is "XML".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xxx
SensorData,ResposeCode=oi.ReadXML()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>6</td><td>WriteXML</td><td>To modify the control signal at single nodes. Type of data is "XML".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.DeviceID=xx
oi.DevicePin=xxx
oi.DataXML='<Name>OpenIoE</Name>'
SensorData,ResposeCode=oi.WriteXML()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>7</td><td>Read</td><td>To read the sensor data from multiple nodes. Type of data is "Numeric/String".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.UserIDPinAPIKeys=[[xx, xxx], [x, xxx]]
SensorData,ResposeCode=oi.Read()
print(SensorData)
print(ResposeCode)</code></pre></td></tr>
<tr><td>8</td><td>Write</td><td>To modify the control signal at multiple nodes. Type of data is "Numeric/String".</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='xxxxxxxxxxxxxxxxxxxx';
oi.UserIDPinAPIKeys=[[xx, xxx], [xx, xxx]]
oi.Data=[xx,xx]
Confirmation,ResposeCode=oi.ReadAPI()
print(Confirmation)
print(ResposeCode)</code></pre></td></tr>
<tr><td>9</td><td>Generate API Key</td><td>To generate new API key for a given email and password.</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.UserEmail='xxxxxxxxxx'
oi.UserPassword='xxxxxxxxxxx'
ResponseJson,ResponseCode=oi.GenerateAPIKey()
print(ResponseJson['User ID'])
print(ResponseJson['API Key'])
print(ResponseJson['Message'])
print(ResponseCode)</code></pre></td></tr>
<tr><td>10</td><td>Create New Device</td><td>To add new IoT device for a given API key, name, cryptotype and data format.</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.APIKey='pnHEmHgjFl0PT247Eae9'
oi.DeviceName='Test000'
oi.CryptoName='None'
oi.DataFormat='Value' # 'XML' or 'JSON'
ResponseTest,ResponseCode=oi.CreateDevice()
print(ResponseTest)
print(ResponseCode)</code></pre></td></tr>
<tr><td>11</td><td>Get API Key</td><td>To get API key from user email and password.</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi.UserEmail='v@v.com'
oi.UserPassword='v'
ResponseText,ResponseCode=oi.ReadAPIKey()
print(ResponseText)
print(ResponseCode)</code></pre></td></tr>
<tr><td>12</td><td>Get Data Set</td><td>To get Dataset stored for device.</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi.DeviceID='xxx'
ResponseTest,ResponseCode=oi.DownloadDeviceData()
print(ResponseTest)
print(ResponseCode)</code></pre></td></tr>
<tr><td>13</td><td>Developer</td><td>To display the developer information</td><td><pre><code  class="language-python">from openioe.openioe_apis import *
oi=openioe_apis()
oi.Developer()</code></pre></td></tr></tbody></table>

---  

### 2\. Web Services

Users are expected to take these steps,
1. Register and login to OpenIoE- [Register/Login](https://openioe.gnanodaya.org/)
2. Create API Key/ Get API Key from OpenIoE.
3. Embed the API Key, Device ID and Pin into the client code.

#### Visit the OpenIoE 3.0 web portal at [https://openioe.gnanodaya.org](https://openioe.gnanodaya.org)


#### Visit the OpenIoE 3.0 Help Portal at [https://openioedoc.gnanodaya.org](https://openioedoc.gnanodaya.org)

 
#### API List:

<table><tbody><tr><td><strong>No</strong></td><td><strong>API</strong></td><td><strong>Description</strong></td><td><strong>Type</strong></td><td><strong>Example</strong></td></tr><tr><td>1</td><td>showdevicevalue</td><td>To get hardware value from web service.</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/showdevicevalue/&lt;apikey&gt;/2/433</code></pre></td></tr><tr><td>2</td><td>updatedevicevalue</td><td>Update the hardware value passed as a parameter</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/updatedevievalue/&lt;apikey&gt;/2/433/2</code></pre></td></tr><tr><td>3</td><td>showdevicejson</td><td>To get hardware JSON from web service.</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/showdevicejson/&lt;apikey&gt;/2/433</code></pre></td></tr><tr><td>4</td><td>updatedevicejson</td><td>Update the hardware JSON passed as parameter</td><td>http post</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/updatedevicejson/&lt;apikey&gt;/2/433 &lt;Data&gt;</code></pre></td></tr><tr><td>5</td><td>showdevicexml</td><td>To get hardware XML file from web service.</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/showdevicexml/&lt;apikey&gt;/2/433</code></pre></td></tr><tr><td>6</td><td>updatedevicexml</td><td>Update the hardware XML passed as parameter</td><td>http post</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/updatedevicexml/&lt;apikey&gt;/2/433 &lt;Data&gt;</code></pre></td></tr>
<tr><td>7</td><td>generateapikey</td><td>Generate new API Key by providing user creds</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/generateapikey/&lt;emailid&gt;/&lt;password&gt;</code></pre></td></tr>
<tr><td>8</td><td>createuserdevice</td><td>Add new IoT device to your account</td><td>http get</td><td><pre><code  class="language-plaintext">&lt;endpoint&gt;/createuserdevice/&lt;APIKey&gt;/&lt;DeviceName&gt;/&lt;CryptoName&gt;/&lt;DataFormat&gt;</code></pre></td></tr>
</tbody></table>

---

### Developers 
<p>
<img  src="https://venkataswamy.in/images/img1.jpg"  alt="Dr. Venkataswamy R"  width="100"/>
</p>
<div>Thanks and Regards</div>
<div><strong>Venkataswamy R</strong></div>
<div>Assistant Professor</div>
<div>Department of Electrical and Electronics Engineering,</div>
<div>School of Engineering and Technology</div>
<div>Christ (Deemed to be University)</div>
<div>Bengaluru-560074, India</div>
<br>
<img  src="https://lh4.googleusercontent.com/-FqpLVHU8eMw/AAAAAAAAAAI/AAAAAAAAABM/ivbX55TtoV4/photo.jpg"  alt="Related image"  style="margin-top:0px"  width="21"  height="21"> <span><b  style="color:rgb(7,55,99);font-family:'trebuchet ms',sans-serif"><i>  <a  href="http://venkataswamy.in"  target="_blank">venkatswamy.in</a><br><br><br></i></b></span></div></div></div>
