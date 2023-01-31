# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
import logging
import re

from jira import JIRA


class JiraClient:
    def __init__(self, jira_base_url, username=None, password=None, token=None):
        self._password = password
        self._token = token
        self._username = username
        self._jira_base_url = jira_base_url
        self.get_server_instance()

    def get_server_instance(self):
        """
        If the user has provided a username and password, use those to connect to JIRA. If the user has
        provided a username and token, use those to connect to JIRA. If the user has provided a username
        but no password or token, use the username to connect to JIRA. If the user has not provided a
        username, connect to JIRA without a username
        :return: JIRA object
        """
        try:
            if (self._username and self._password):
                return JIRA(server=self._jira_base_url, basic_auth=(self._username, self._password))
            elif (self._username and self._token):
                return JIRA(server=self._jira_base_url, basic_auth=(self._username, self._token))
            elif (self._username and not (self._password or self._token)):
                return JIRA(server=self._jira_base_url, basic_auth=(self._username))
            else:
                return JIRA(self._jira_base_url)
        except Exception as e:
            logging.info(msg='Unable to connect to Jira server')
            raise e

    def get_projects(self):
        """
        It returns a list of projects from the server
        :return: A list of projects
        """
        projects = self.get_server_instance().projects()
        return projects

    def get_boards(self):
        """
        It returns a list of boards
        :return: A list of boards
        """
        boards = self.get_server_instance().boards()
        return boards

    def get_sprints(self, board_id):
        """
        This function returns a list of sprints for a given board
        
        :param board_id: The ID of the board you want to get the sprints for
        :return: A list of sprints
        """
        sprints = self.get_server_instance().sprints(board_id)
        return sprints

    def get_server_info(self):
        """
        It returns the server information of the server instance
        :return: The server_info() method returns a dictionary containing information about the server.
        """
        server_info = self.get_server_instance().server_info()
        return server_info

    def get_statuses(self):
        """
        It returns a list of statuses from the server
        :return: A list of statuses.
        """
        statuses = self.get_server_instance().statuses()
        return statuses

    def get_status_resource(self, resource_id):
        """
        This function gets the status of a resource
        
        :param resource_id: The ID of the resource you want to get the status of
        :return: The status of the resource.
        """
        status = self.get_server_instance().status(resource_id)
        return status

    def get_all_issues(self, sprint_id):
        """
        It gets all the issues in a sprint by using the Jira search API to get 100 issues at a time, and
        then iterating through the results until it has all the issues
        
        :param project_name: The name of the project you want to get the issues from
        :param sprint_id: The ID of the sprint you want to get the issues for
        :return: A list of issues
        """
        issues = []
        i = 0
        chunk_size = 200
        while True:
            chunk = self.get_server_instance().search_issues(f'Sprint = {sprint_id}', startAt=i, maxResults=chunk_size)
            i += chunk_size
            issues += chunk.iterable
            if i >= chunk.total:
                break
        return issues
