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

    # issue = jira_client.get_all_issues('27')
    # print ('issue_id:', issue[0].id)
    # print ('issue_key:', issue[0].key)
    # print ('issue_assignee:', issue[0].fields.assignee)
    # print ('issue_components:', issue[0].fields.components)
    # print ('issue_created:', issue[0].fields.created)
    # print(dir(issue[0].fields.creator))
    # print ('issue_creator:', issue[0].fields.creator.name)
    # print ('issue_duedate:', issue[0].fields.duedate)
    # print ('issue_fixVersions:', issue[0].fields.fixVersions)
    # print ('issue_description:', issue[0].fields.description)
    # print (dir(issue[0].fields.issuetype))
    # print ('issue_issuetype:', issue[0].fields.issuetype.name)
    # print ('issue_labels:', issue[0].fields.labels)
    # print ('issue_progress:', issue[0].fields.progress)
    # print ('issue_project:', issue[0].fields.project)
    # print ('issue_reporter:', issue[0].fields.reporter.name)
    # print ('issue_resolution:', issue[0].fields.resolution)
    # print ('issue_resolutiondate:', issue[0].fields.resolutiondate)
    # print ('issue_status:', issue[0].fields.status.name)
    # print ('issue_subtasks:', issue[0].fields.subtasks)
    # print ('issue_summary:', issue[0].fields.summary)
    # print ('issue_timeestimate:', issue[0].fields.timeestimate)
    # print ('issue_timespent:', issue[0].fields.timespent)
    # print ('issue_timetracking:', issue[0].fields.timetracking)
    # print ('issue_updated:', issue[0].fields.updated)
    # print ('issue_votes:', issue[0].fields.votes)
    # print ('issue_watches:', issue[0].fields.watches)
    # print ('issue_worklog:', issue[0].fields.worklog)
    # print(issue[0].fields.worklog.total)
    # print ('issue_workratio:', issue[0].fields.workratio)


if __name__ == "__main__":
    main()
