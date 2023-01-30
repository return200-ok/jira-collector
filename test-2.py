# By default, the client will connect to a Jira instance started from the Atlassian Plugin SDK

jira = JIRA(server="http://192.168.3.56:8089", basic_auth=('thuandd', 'Biplus@2021'))
# MDY0MjMxOTg5OTY2OsJ7rWa/MzDopxzdbtTNZrjGwnil

# Getting all the projects that are available to the user.
projects = jira.projects()

# Getting all the boards that are available to the user.
boards = jira.boards()

board_id = 42
# Getting all the sprints that are available to the user.
sprints = jira.sprints(board_id)

# Getting all the dashboards that are available to the user.
dashboard = jira.dashboards()

sprint_id = 27
# Getting the sprint information for the sprint with the given id.
sprint_info = jira.sprint_info(board_id, sprint_id)

sprint = jira.sprint(sprint_id)


# Getting the server information.
server_info = jira.server_info()

# Getting all the statuses that are available to the user.
statuses = jira.statuses()

resource_id = 1
# Getting the status information for the status with the given id.
status = jira.status(resource_id)

# issue = jira.issue()

# size = 100
# initial = 0
# while True:
#     start= initial*size
#     issues = jira.search_issues('project=CAOL AND Sprint=27',  start,size)
#     print(issues)
#     if len(issues) == 0:
#         break
#     initial += 1
#     for issue in issues:
#         print(issue)
        # print ('ticket-no=',issue)
        # print ('IssueType=',issue.fields.issuetype.name)
        # print ('Status=',issue.fields.status.name)
        # print ('Summary=',issue.fields.summary)


def get_all_issues(jira_client, project_name, sprint_id):
    issues = []
    i = 0
    chunk_size = 100
    while True:
        chunk = jira_client.search_issues(f'project = {project_name} AND Sprint = {sprint_id}', startAt=i, maxResults=chunk_size)
        i += chunk_size
        issues += chunk.iterable
        if i >= chunk.total:
            break
    return issues
issues = get_all_issues(jira, 'CAOL', '27')
print(issues[0].fields.status.name)
# print(sprint)