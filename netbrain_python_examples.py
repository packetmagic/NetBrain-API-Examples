import requests
import json
import base64
from getpass import getpass

user = getpass("Username: ")       
pwd = getpass()       
server_url = "http://netbrain.domain.com/ServicesAPI/"              
headers = {"Content-Type": "application/json", "Accept": "application/json"}

 
def Login():
    token_url= server_url + "API/V1/Session"
    #get token
    basic_data = user + ":" + pwd
    basic_data = basic_data.encode("ascii")
    auth_data = base64.b64encode(basic_data)
    headers["Authorization"] = "Basic " + auth_data.decode()
 
    token = requests.post(token_url,headers=headers,verify=False).json()["token"]
    return token

def Logout(token):
    full_url= server_url + "API/V1/Session" 
    headers["Token"]=token   
    response = requests.delete(full_url,data=json.dumps({"token": token}),headers=headers,verify=False)
    return response.json()['statusDescription']

def GetTenantID(token):
    full_url = server_url + "API/V1/CMDB/Tenants"
    headers["Token"]=token
    tenants = requests.get(full_url,headers=headers)
    return tenants.json()['tenants'][0]['tenantId']

def GetDomainID(token, tenantId):
    full_url = server_url + "API/V1/CMDB/Domains"
    headers["Token"]=token
    data = {
        "tenantId": tenantId,
    }
    domains = requests.get(full_url,params=data,headers=headers)
    return domains.json()['domains'][0]['domainId']

def SetDomain(token, tenantId, domainId):
    full_url = server_url + "API/V1/Session/CurrentDomain"
    headers["Token"]=token
    response = requests.put(full_url,data=json.dumps({"tenantId": tenantId,"domainId": domainId}),headers=headers,verify=False)
    return response.json()['statusDescription']

if __name__ == "__main__":
   token = Login()
   print(token)
   tenantId = GetTenantID(token=token)
   print(tenantId)
   domainId = GetDomainID(token=token,tenantId=tenantId)
   print(domainId)
   currentDomain = SetDomain(token=token,domainId=domainId,tenantId=tenantId)
   print(currentDomain)
   logoff = Logout(token=token)
   print(logoff)