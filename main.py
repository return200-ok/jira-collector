# This script shows how to use the client in anonymous mode
# against jira.atlassian.com.
import re

from jira import JIRA

# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK
# (see https://developer.atlassian.com/display/DOCS/Installing+the+Atlassian+Plugin+SDK for details).
jira = JIRA(server="http://192.168.3.56:8089", basic_auth=('thuandd', 'Biplus@2021'))


# Get all projects viewable by anonymous users.
projects = jira.projects()
print(dir(projects[0]))
# print(projects[0].raw)
boards = jira.boards()
# print(boards)

# # Sort available project keys, then return the second, third, and fourth keys.
# keys = sorted(project.key for project in projects)[2:5]



