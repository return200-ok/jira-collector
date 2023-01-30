import logging

import jira_client
from influx_client import InfluxPoint

logger = logging.getLogger(__name__)
class IssueInfo:
    def __init__(self, board_id, project_id, project_name, sprint_id, issue_name, issue_type, issue_id, issue_status):
        self.board_id = board_id
        self.project_id = project_id
        self.project_name = project_name
        self.sprint_id = sprint_id
        self.issue_name = issue_name
        self.issue_type = issue_type
        self.issue_id = issue_id
        self.issue_status = issue_status

def gen_build_data(build_info, job, build_id):
    data = IssueInfo(
        job,
        build_id,
        build_info['url'],
        round(build_info['timestamp']/1000),
        build_info['duration'],
        build_info['estimatedDuration'],
        build_info['queueId'],
        build_info['result'],
        build_info['displayName'],
    )
    return data


def gen_datapoint(data):
    measurement = 'jenkins'
    tags = {
        "jobname": data.jobname,
        "build_id": data.build_id,
        "url": data.url,
        }
    timestamp = data.timestamp
    fields = {
        "duration": data.duration,
        "estimatedDuration": data.estimatedDuration,
        "result": data.result,
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
        if (board.type == 'kanban'):
            break
        else:
            print('board:',board.id)
            list_sprint = jira_client.get_sprints(board.id)
            for sprint in list_sprint:
                print('     sprint:',sprint)






        # list_project = jira_client.get_list_build(job)
        # try:
        #     for build in list_build:
        #         build_info = jira_client.build_info(job, build)
        #         data = gen_build_data(build_info, job, build)
        #         push_data(data, influx_client)
        # except TypeError:
        #     logging.info("Job {} has no build data, {}  is not iterable".format(job, list_build))