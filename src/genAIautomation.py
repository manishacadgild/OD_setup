# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 11:13:40 2023

@author: tiwarric
"""

import requests
import json
from datetime import datetime, date
import logging
import os,sys
from github import Github

class GenAI:
    day = date.today()
    day = str(day)
    log_filename = 'gen AI -log'+day+'.log'
    logger = logging.getLogger('logger')
    logger.setLevel(logging.INFO)
    
    # Create a formatter to include a timestamp
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Create a file handler to log to a file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setFormatter(formatter)
    
    # Add the file handler to the logger
    logger.addHandler(file_handler)   

    def get_token(self):
        consumer_key = 'mkqMfPPSucUPfrk94NDraqMNvYCrVFeE'
        client_secret = 'aa7jJHJ8cbnrGsPFGsvCh6cPz4PRg3YsNqqgdtWUFNafYSbPtx9sChs63fGCMuTD'
        
        headersAuth = {
        'Content-Type': 'application/x-www-form-urlencoded ',
        'Accept': 'application/json'
        }
        
        print("token called")
        
        data = {
        'grant_type': 'client_credentials',
        'client_id': consumer_key,
        'client_secret': client_secret
        }
        url = 'https://tietoevry.api.opsramp.com/tenancy/auth/oauth/token'
        response = requests.post(url, headers=headersAuth, data=data, verify=True)
        j = response.json()
        return j
    
    def createfile(self):
        day = date.today()
        day = str(day)
        name = 'open AI'+day+'.txt'
        file1=open(name,'w')
        var1= "id,metric,component,created date,Subject,response"               
        file1.write(var1 + '\n')  
        file1.close() 
        return name

    def write(self,name,writevar):
         file1=open(name,'a+')
         file1.write(writevar + '\n')
         file1.close() 
    
    def get_alerts(self,token):
        file = self.createfile()
        
        val = 'true'
        metric_list = [ "SE-MSSQL_AgentJobFailed_Metric-V4","EVENTLOGS","PROCESS","system.process.stats.count","System_Windows_Service_Status_Ext","system.cpu.usage.utilization","Agent Status","system.ping.pl","system.memory.usage.utilization","system.cpu.usage.utilization","system.os.uptime","system.disk.usage.utilization","system_linux_swapMemory_Utilization"]
        
            
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer '+token['access_token'],
        }
        data={
            "objectType": "alert",
            "fields": [
              "dnsName",
              "createdTime",
              "metric",
              "component",
              "currentState",
              "incidentId",
              "isInferenceAlert"
            ],
          "filterCriteria": "createdTime > '-1d'  AND isInferenceAlert = 'False' ",
          "pageNo": 1,
          "pageSize": 1000,
          "nextPage": val,
          "descendingOrder": val
                }
        url = 'https://tietoevry.app.opsramp.com/opsql/api/v3/tenants/d7c1dfec-4075-4f5d-b1d6-73cde9fb313e/queries'
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            logging.info("Get Alert status code is "+str(response.status_code))
            output = response.json()
            details = output['results']
            total_alerts= len(details)
            for ins in range(total_alerts):
                metric=details[ins]['metric']
                
                if metric in metric_list:
                    logging.info(" Automation is avaliable for this metric "+ metric)
                    
                
                else:
                    id = details[ins]['id']
                    component = details[ins]['component']
                    createdTime = details[ins]['createdTime']
                    createdtime = createdTime.replace("T"," ")
                    subject = details[ins]['subject']
                    finalout = self.call_openai(subject)
                    
                    string = str(id)+ "," + metric+ "," + component+ "," + createdtime+ "," + subject + ","+ finalout
                    ROOT_DIR = os.getcwd()
                    DIRR_FILE="genAI"
                    # g=Github("manishjha","Kisdin123$")
                    # repo=g.get_repo("manishacadgild/OD_setup")
                    os.makedirs(DIRR_FILE,exist_ok=True)
                    file=os.path.join(ROOT_DIR,DIRR_FILE,file)
                    self.write(file,string)
                                           
                
        else:
            logging.debug(" fetch alert failed Alert "+str(response.status_code))
            
    
    def call_openai(self,metric):
        url = "https://test-open-ai-chatbot-itegration-01.openai.azure.com/openai/deployments/testchatbotdeployment/chat/completions?api-version=2023-03-15-preview"
        headers = {
            'Accept': 'application/json',
            'api-key': '54b7b3eebb6a437c8b890e0aee8d9991',
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
            {
              "role": "system",
              "content": "You are a helpful assistant that provides information."
            },
            {
              "role": "user",
              "content": metric + " Can you write code for this?"}
          ]
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            output = response.json()
            value = output['choices'][0]['message']['content']
            return value
        else:
            logging.DEBUG(" Open AI call failed with status code : "+response.status_code)
        
    def __init__(self):
        
        token =self.get_token()
        
        self.get_alerts(token)
        

if __name__ == "__main__":
    call_class=GenAI()
        
    
        
