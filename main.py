#!/usr/bin/python
import os

from dotenv import load_dotenv
from influx_client import InfluxClient
from jira_client import JiraClient
from jira_collector import collector

'''
    Load env
'''
load_dotenv()
jira_url = os.getenv('JIRA_URL')
jira_user = os.getenv('JIRA_USER')
jira_password = os.getenv('JIRA_PASSWORD')

influx_token = os.getenv('INFLUX_TOKEN')
influx_server = os.getenv('INFLUX_DB')
org_name = os.getenv('INFLUX_ORG')
bucket_name = os.getenv('BUCKET_NAME')
logPath = os.getenv('COLLECTOR_LOG_PATH')

def main():
    jira_client = JiraClient(
        jira_url, jira_user, jira_password
    )
    influx_client = InfluxClient(
        influx_server, influx_token, org_name, bucket_name
    )
    collector(jira_client, influx_client)

if __name__ == "__main__":
    main()
