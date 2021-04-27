import requests
import json
from tabulate import tabulate
from requests.auth import HTTPBasicAuth
from dnac_config import DNAC, DNAC_PORT, DNAC_USER, DNAC_PASSWORD

DnacURL = "10.91.43.70"

def get_device_list():
    """
    Building out function to retrieve list of devices and formats with tabulate.
    """
    token = get_auth_token() # Get Token
    url = "https://"+DnacURL+"/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    device_list = resp.json()

    DnaList = []

    for i, device in enumerate(device_list['response']):
        DnaList.append([device["hostname"],device['managementIpAddress'],device['serialNumber'],device['platformId'],device['upTime']])
    dnacDeviceTable = "```                            DNA Center Device List\n\n" + str(tabulate(DnaList, headers=['hostname','IP Address','Serial Number','Platform ID','Up Time']))
    print(dnacDeviceTable)
    return dnacDeviceTable

def get_device_config():
    """
    Building out function to retrieve list of devices and formats with tabulate.
    """
    token = get_auth_token() # Get Token
    url = "https://"+DnacURL+"/api/v1/network-device"
    hdr = {'x-auth-token': token, 'content-type' : 'application/json'}
    resp = requests.get(url, headers=hdr, verify=False)  # Make the Get Request
    device_list = resp.json()


    for id in device_list['response']:
        device_id = id['id']
        if device_id == '498812f8-b813-4ca2-ab74-b11c44c42600':
            #print "\nDevice ID=", device_id, ",Hostname=", id['hostname'], "\n"
            resp_config = requests.get(url + "/" + device_id + "/config", headers=hdr, verify=False)
            device_config = resp_config.json()
            f_config = device_config['response']
            #print f_config
            f_config2 = str(f_config)
            deviceName = "Configuration File For " + id['hostname']

    with open("/tmp/Switch_Config.txt", "w") as file1:
        print ("\n\nPrinted", deviceName, "\n")
        file1.write(f_config)
        file1.close()

    return deviceName

def get_compliance_list():
    """
    Building out function to retrieve list of devices and formats with tabulate.
    """
    token = get_auth_token() # Get Token
    networkDeviceURL = "https://"+DnacURL+"/api/v1/network-device"

    hdr = {
        'x-auth-token': token,
        'content-type' : 'application/json'
    }
    deviceResp = requests.get(networkDeviceURL, headers=hdr, verify=False)  # Make the Get Request
    deviceListResp = deviceResp.json()
    deviceList = deviceListResp['response']


    DnaList = []
    DeviceID = []


    for i, device in enumerate(deviceList):
        deviceUID = device['id']
        complianceURL = "https://"+DnacURL+"/dna/intent/api/v1/compliance/"+deviceUID+"/detail?complianceType=IMAGE"
        complianceResp = requests.get(complianceURL, headers=hdr, verify=False)
        complianceListResp = complianceResp.json()
        complianceList = complianceListResp['response']
        for i, compliance in enumerate(complianceList):
            id = compliance['status']
        DnaList.append([device['hostname'],device['managementIpAddress'],device['platformId'],device['serialNumber'],device['softwareVersion'],id])
    dnacDeviceTable = "```\n                            DNA Center Device List\n\n" + str(tabulate(DnaList, headers=['hostname','IP Address','Platform ID','Serial Number','Software Version','Software Compliance Status']))


    ImageVersion = []
    goldenImageURL = "https://"+DnacURL+"/dna/intent/api/v1/image/importation?isTaggedGolden=true"
    goldenImageResp = requests.get(goldenImageURL, headers=hdr, verify=False)
    goldenImageListResp = goldenImageResp.json()
    goldenImageList = goldenImageListResp['response']
    for i, image in enumerate(goldenImageList):
        ImageVersion.append([image['family'],image['displayVersion']])
    imageVersionTable = "\n    Golden Images\n\n" + str(tabulate(ImageVersion, headers=['Family','Golden Image']))

    complaince_table = dnacDeviceTable+"\n"+imageVersionTable+"\n"
    print (complaince_table)
    return complaince_table

def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = "https://"+DnacURL+"/dna/system/api/v1/auth/token"       # Endpoint URL
    #resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)  # Make the POST Request
    resp = requests.post(url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    token = resp.json()['Token']    # Retrieve the Token from the returned JSONhahhah
    return token    # Create a return statement to send the token back for later use


if __name__ == "__main__":
    get_device_list()
    get_device_config()
    get_compliance_list()
