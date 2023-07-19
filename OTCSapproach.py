#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import os
import json
import xxx_certifi

# Define Proxies
proxies = {'https':"",'http':""} 

# Header for REST API
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

# SSL Cert: that's in case you are using ssl cert, then you have to set a value for this env attribute
os.environ["REQUESTS_CA_BUNDLE"] = xxx_certifi.where()

# Ask user to provide Windows Credentials
from getpass import getpass
username = getpass(prompt= "Username: ")
password = getpass(prompt= "Password: ")

payload = "username="+username+"&password="+password
url = "https://<your-domain-here>/livelink/livelink/api/v1/auth/"
session = requests.Session()
response = session.post(url, headers=headers, data=payload,proxies=proxies, verify=xxx_certifi.where() )

token = json.loads(response.text)['ticket']

headers = {
    'OTCSTICKET': token
}

# Get the content of a node
content_url = "https://<your-domain-here>/livelink/livelink/api/v1/nodes/{0}/content"
node_id = <define-id>
url = content_url.format(str(node_id))
# url
response = session.get(url, headers=headers)
# print(response)
# print(response.text)

# Get subnodes
parent_id = <define-id>
url = "https://<your-domain-here>/livelink/livelink/api/v1/nodes/" + str(parent_id) + "/nodes"
response = session.get(url, headers=headers, proxies=proxies, verify=xxx_certifi.where())
data = json.loads(response.text)
parent_node = json.loads(json.dumps(data))
PARNODE_KEY = parent_node
# print("Folder's content: ", PARNODE_KEY)

# Create a node (folder)
url = "https://<your-domain-here>/livelink/livelink/api/v2/nodes"
files=[
    ('type', (None, 0)), # 0 stands for folder
    ('parent_id', (None, <define-id>)),
    ('name', (None, 'TestFolder'))
]
response = session.post(url, headers=headers, files=files)

# Create a node (file)
url = "https://<your-domain-here>/livelink/livelink/api/v2/nodes"
files=[
    ('type', (None, 144)), # 144 stands for file
    ('parent_id', (None, <define-id>)),
    ('name', (None, 'TestFile')),
    ('file',('TestFile.txt',open(r"C:\TestFile.txt",'rb'),'text/plain'))
]
response = session.post(url, headers=headers, files=files)
# print(response.text)

# List the content of a node (folder)
parent_id = <define-id>
url = "https://<your-domain-here>/livelink/livelink/api/v1/nodes/" + str(parent_id) + "/nodes"
response = session.get(url, headers=headers, proxies=proxies, verify=xxx_certifi.where())
print(response.text)

rslt = json.loads(response.text)['data']
print (rslt)

# Check if the local file exists already in the list: if yes, add a new version; if no, upload it
# Local file
fileName = "TestFile.txt"
fileNameS = fileName[0:-4]
print(fileNameS)

for item in rslt:
    print(item['name'])
    if fileNameS == item['name']:
        update_node(str(item['id']), 144, item['parent_id'], item['name'], item['name']+ '.txt', r"C:\TestFile.txt")
        break
    else:
        create_node(144, <define-id>, 'TestFile01', 'TestFile01.txt', r"C:\TestFile.txt")

# Create a node (file)
def create_node(node_type, parent_id, node_name, file_type, file_location):
    url = "https://<your-domain-here>/livelink/livelink/api/v2/nodes"
    files=[
        ('type', (None, node_type)),
        ('parent_id', (None, parent_id)),
        ('name', (None, node_name)),
        ('file',(file_type,open(file_location,'rb'),'text/plain'))
    ]
    response = session.post(url, headers=headers, files=files)

# Update a node (file)
def update_node(node_id, node_type, parent_id, node_name, file_type, file_location):
    url = "https://<your-domain-here>/livelink/livelink/api/v2/nodes/" + node_id + "/versions"
    files=[
        ('type', (None, node_type)),
        ('parent_id', (None, parent_id)),
        ('name', (None, node_name)),
        ('file',(file_type,open(file_location,'rb'),'text/plain'))
    ]
    response = session.post(url, headers=headers, files=files)
    print(response.text)
