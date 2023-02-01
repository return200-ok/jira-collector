import logging

from influx_client import InfluxPoint

logger = logging.getLogger(__name__)

class IssueInfo:
    """
    The constructor for the class Issue. It takes in the following parameters:
    board_id, project_id, sprint_id, issue_key, issue_id, issue_assignee, issue_created, issue_creator,
    issue_duedate, issue_type, issue_reporter, issue_status, issue_summary, issue_timeestimate,
    issue_timespent, issue_worklog
    
    :param board_id: The ID of the board that the issue is on
    :param project_id: The ID of the project that the issue belongs to
    :param sprint_id: The ID of the sprint
    :param issue_key: The issue key, e.g. "TEST-1"
    :param issue_id: The unique ID of the issue
    :param issue_assignee: The user to whom the issue is assigned
    :param issue_created: The date the issue was created
    :param issue_creator: The user who created the issue
    :param issue_duedate: The date the issue is due
    :param issue_type: The type of issue (e.g. Story, Bug, etc.)
    :param issue_reporter: The user who reported the issue
    :param issue_status: The status of the issue
    :param issue_summary: The summary of the issue
    :param issue_timeestimate: The time estimate in seconds
    :param issue_timespent: The time spent on the issue in seconds
    :param issue_worklog: a list of worklogs for the issue
    """
    def __init__(self, board_id, board_name, project_id, sprint_id, issue_key, issue_id, issue_assignee, 
    issue_created, issue_creator, issue_duedate, issue_type, issue_reporter, issue_status, 
    issue_summary, issue_timeestimate, issue_timespent, issue_worklog):
        self.board_id = board_id
        self.board_name = board_name
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

def gen_data(issue, board, sprint_id):
    """
    It takes in an issue, a board id, and a sprint id, and returns an IssueInfo object with all the
    relevant information about the issue
    
    :param issue: the issue object
    :param board_id: The ID of the board that the issue is on
    :param sprint_id: The ID of the sprint
    :return: A list of IssueInfo objects
    """

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
        board.name,
        project_id,
        sprint_id,
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
    """
    It takes a dataframe row as input, and returns a data point in the format that InfluxDB expects
    
    :param data: the data object that we created in the previous step
    :return: A dictionary
    """
    measurement = 'jira'
    tags = {
        "board_id": data.board_id,
        "board_name": data.board_name,
        "sprint_id": data.sprint_id,
        "project_key": data.project_id,
        "issue_id": data.issue_id,
        "issue_key": data.issue_key,
        "summary": data.issue_summary,
        "assignee": data.issue_assignee,
        "creator": data.issue_creator,
        "reporter": data.issue_reporter,
        "issuetype": data.issue_type,

        }
    timestamp = data.issue_created
    fields = {
        "duedate": data.issue_duedate,
        "status": data.issue_status,
        "timeestimate": data.issue_timeestimate,
        "timespent": data.issue_timespent,
        "worklog": data.issue_worklog
        }
    data_point = InfluxPoint(measurement, tags, fields, timestamp)._point
    return data_point

def push_data(data, influx_client):  
    """
    It takes a dataframe and an InfluxDB client as input, and writes the dataframe to the InfluxDB
    client
    
    :param data: This is the data that you want to push to InfluxDB
    :param influx_client: The InfluxDB client object
    """
    data_point = gen_datapoint(data)
    try:
        influx_client.write_data(data_point)
        logging.info("Wrote "+str(data_point)+" to bucket "+influx_client._bucket)
    except Exception as e:
        logging.info("Problem inserting points for current batch")
        raise e

def collector(jira_client, influx_client):
    """
    For each board, get all the sprints, get all the issues in each sprint, and push the data to
    InfluxDB
    
    :param jira_client: the Jira client object
    :param influx_client: the client object that we created in the previous step
    """
    list_board = jira_client.get_boards()
    for board in list_board:
        board_type = board.type
        board_id = board.id
        if (board_type == 'kanban'):
            continue
        else:
            list_sprint = jira_client.get_sprints(board_id)
            for sprint in list_sprint:
                sprint_id = sprint.id
                list_issue = jira_client.get_all_issues(sprint.id)
                for issue in list_issue:
                    data = gen_data(issue, board, sprint_id)
                    push_data(data, influx_client)

