import requests
import json
import config
import urllib3
from requests.auth import HTTPBasicAuth

#Sample App File Paths
APP_FILE_PATH = 'H:\\Jira\\PluginList\\jira-slack-server-integration-plugin-3.0.1.jar'
APP_FILE_PATH_TWO = 'H:\\Jira\\PluginList\\automation-for-jira-lite-8.0.2.jar'
APP_FILE_PATH_THREE = 'H:\\Jira\\PluginList\\confluence-markdown-macro-1.6.12.jar'
APP_FILE_PATH_FOUR = 'H:\\Jira\\PluginList\\microsoft-teams-2021.12.85.jar'
APP_FILE_PATH_FIVE = 'H:\\Jira\\PluginList\\rest-api-browser-3.2.3.jar'
testDownload = [APP_FILE_PATH, APP_FILE_PATH_TWO, APP_FILE_PATH_THREE, APP_FILE_PATH_FOUR, APP_FILE_PATH_FIVE]

jira_EDN = '' #Domain for a JIRA server
plugin_list_endpoint = '/rest/plugins/latest/'

list_of_plugins = []
list_of_plugins_formatted= {}

#Login information
username = config.username #string containing EDN username for user
password = config.password #string containing EDN password for user
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

#Function that will populate the list of plugins and the formatted list
def grabPlugins():
    headersForPluginGrab = {
        'Authorization': 'Admin'
    }
    #Get request for getting the list of plugins
    response = requests.get(
        jira_EDN + plugin_list_endpoint,
        headers = headersForPluginGrab,
        auth = HTTPBasicAuth(username, password), #Basic Authentication. Encodes username and password into Base64
        verify = False #Requests ignores verifying the SSl certificate
    )
    results = response.json() 
    #Appends all of the plugins to a list
    for i in range(len(results['plugins'])):
        list_of_plugins.append(results['plugins'][i])
    #Formats and maps the plugins
        pluginInfo = ""
        if "name" in results['plugins'][i]:
            pluginInfo += "Name: " + results['plugins'][i]['name'] + '\n'
        if "description" in results['plugins'][i]:
            pluginInfo += "Description: " + results['plugins'][i]['description'] + '\n'
        if "vendor" in results['plugins'][i]:
            if "marketplaceLink" in results['plugins'][i]['vendor']:
                pluginInfo += "Link: " + results['plugins'][i]['vendor']['marketplaceLink'] + '\n'
        list_of_plugins_formatted[i] = pluginInfo

#Grabs the Universal Plugin Manager Token
def grabUPMToken():
    headersForUPMToken = {
    'Accept': 'application/vnd.atl.plugins.installed+json'
    }
    #Gets request for the token
    response = requests.get(
        jira_EDN + '/rest/plugins/latest/?os_authType=basic',
        headers = headersForUPMToken,
        auth = HTTPBasicAuth(username, password),
        verify = False
    )
    return response.headers['upm-token']

#Downloads a plugin to the server from a .jar file path.
def downloadPluginToServer(filepath):
    headersForUPMPost = {
    'Accept': 'application/json',
    }
    #Gathering the .jar file to download to the server
    file = {"plugin": open(filepath, "rb")}
    upmToken = grabUPMToken()
    #Making post-request to download
    response = requests.post(
        jira_EDN + '/rest/plugins/latest/?token='+upmToken,
        files = file,
        headers = headersForUPMPost,
        auth = HTTPBasicAuth(username, password),
        verify = False
    )
    #Check for successful download or failure
    if response.json()['status']['statusCode'] == 200:
        print("Plugin from " + filepath + " successfully downloaded!")
    else:
        print("Plugin insertion failed. Check file path: " + response.text)

#Delete a plugin from the server with the pugin key
def deletePluginFromServer(pluginKey):
    response = requests.delete(
        jira_EDN + '/rest/plugins/1.0/'+pluginKey+'-key',
        auth = HTTPBasicAuth(username, password),
        verify = False
    )
    if(response.text == ''):
        print("Plugin " + pluginKey + " successfully deleted!")
    else:
        print("Plugin deletion failed: " + response.text)
     









