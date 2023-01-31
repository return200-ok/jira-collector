import logging

import jira_client
from influx_client import InfluxPoint

logger = logging.getLogger(__name__)
class IssueInfo:
    def __init__(self, board_id, project_id, sprint_id, issue_key, issue_id, issue_assignee, 
    issue_created, issue_creator, issue_duedate, issue_type, issue_reporter, issue_status, 
    issue_summary, issue_timeestimate, issue_timespent, issue_worklog):
        self.board_id = board_id
        self.project_id = project_id
        self.sprint_id = sprint_id
        self.issue_key = issue_key
        self.issue_id = issue_id
        self.issue_assignee = issue_assignee
        self.issue_created = issue_created
        self.issue_creator = issue_creator
        self.issue_duedate = issue_duedate
        self.issue_type = issue_type
        self.issue_reporter = issue_reporter
        self.issue_status = issue_status
        self.issue_summary = issue_summary
        self.issue_timeestimate = issue_timeestimate
        self.issue_timespent = issue_timespent
        self.issue_worklog = issue_worklog

# def check_attr(a):
#     if hasattr(a, 'property'):
#         a.property

def gen_data(issue, board, sprint):

    project_id = ''
    if hasattr(issue.fields, 'project'):
        project_id = issue.fields.project

    issue_assignee = ''
    if hasattr(issue.fields.assignee, 'name'):
        issue_assignee = issue.fields.assignee.name

    issue_created = ''
    if hasattr(issue.fields, 'created'):
        issue_created = issue.fields.created

    issue_creator = ''
    if hasattr(issue.fields.creator, 'name'):
        issue_creator = issue.fields.creator.name

    issue_duedate = ''
    if hasattr(issue.fields, 'duedate'):
        issue_duedate = issue.fields.duedate

    issue_type = ''
    if hasattr(issue.fields.issuetype, 'name'):
        issue_type = issue.fields.issuetype.name

    issue_reporter = ''
    if hasattr(issue.fields.reporter, 'name'):
        issue_reporter = issue.fields.reporter.name

    issue_status = '' 
    if hasattr(issue.fields.status, 'name'):
        issue_status = issue.fields.status.name

    issue_summary = ''
    if hasattr(issue.fields, 'summary'):
        issue_summary = issue.fields.summary

    issue_timeestimate = ''
    if hasattr(issue.fields, 'timeestimate'):
        issue_timeestimate = issue.fields.timeestimate

    issue_timespent = ''
    if hasattr(issue.fields, 'timespent'):
        issue_timespent = issue.fields.timespent

    issue_worklog = ''
    if hasattr(issue.fields.worklog, 'total'):
        issue_worklog = issue.fields.worklog.total
    
    data = IssueInfo(
        board.id,
        project_id,
        sprint.id,
        issue.key,
        issue.id,
        issue_assignee,
        issue_created,
        issue_creator,
        issue_duedate,
        issue_type,
        issue_reporter,
        issue_status,
        issue_summary,
        issue_timeestimate,
        issue_timespent,
        issue_worklog
        
    )
    return data

def gen_datapoint(data):
    measurement = 'jira'
    tags = {
        "board_id": data.board_id,
        "sprint_id": data.sprint_id,
        "project_key": data.project_id,
        "issue_id": data.issue_id,
        "issue_key": data.issue_key,
        "summary": data.issue_summary,

        }
    timestamp = data.issue_created
    fields = {
        "assignee": data.issue_assignee,
        "creator": data.issue_creator,
        "duedate": data.issue_duedate,
        "issuetype": data.issue_type ,
        "reporter": data.issue_reporter ,
        "status": data.issue_status ,
        "timeestimate": data.issue_timeestimate ,
        "timespent": data.issue_timespent ,
        "worklog": data.issue_worklog

        }
    data_point = InfluxPoint(measurement, tags, fields, timestamp)._point
    return data_point

def push_data(data, influx_client):  
    data_point = gen_datapoint(data)
    try:
        influx_client.write_data(data_point)
        logging.info("Wrote "+str(data_point)+" to bucket "+influx_client._bucket)
    except Exception as e:
        logging.info("Problem inserting points for current batch")
        raise e

def collector(jira_client, influx_client):
    list_board = jira_client.get_boards()
    for board in list_board:
        # print(board.type)
        if (board.type == 'kanban'):
            break
        else:
            # print('board:',board.id)
            list_sprint = jira_client.get_sprints(board.id)
            for sprint in list_sprint:
                # print('     sprint:',sprint.id)
                list_issue = jira_client.get_all_issues(sprint.id)
                # print(list_issue)
                for issue in list_issue:
                    data = gen_data(issue, board, sprint)
                    # print(data)
                    push_data(data, influx_client)

    # list_project = jira_client.get_projects()
    # for project in list_project:
    #     print(project.projectTypeKey)






        # list_project = jira_client.get_list_build(job)
        # try:
        #     for build in list_build:
        #         build_info = jira_client.build_info(job, build)
        #         data = gen_build_data(build_info, job, build)
        #         push_data(data, influx_client)
        # except TypeError:
        #     logging.info("Job {} has no build data, {}  is not iterable".format(job, list_build))