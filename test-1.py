from jira.client import JIRA
from jira.resources import Issue

username = 'thuandd'
ldp_password = 'Biplus@2021'
sprint_name = 'CAOL Sprint 2'

def sprints(username, 
            ldp_password,
            sprint_name,
            type_of_issues_to_pull=[
                  'completedIssues', 
                  'incompletedIssues',
                  'issuesNotCompletedInCurrentSprint',
                  'issuesCompletedInAnotherSprint']):
    def sprint_issues(cls, board_id, sprint_id):
        r_json = cls._get_json(
            'rapid/charts/sprintreport?rapidViewId=%s&sprintId=%s' % (
                board_id, sprint_id),
            base=cls.AGILE_BASE_URL)

        issues = []
        for t in type_of_issues_to_pull:
            if t in r_json['contents']:
                issues += [Issue(cls._options, cls._session, raw_issues_json)
                           for raw_issues_json in
                           r_json['contents'][t]]
        return {x.key: x for x in issues}.values()

    fmt_full = 'Sprint: {} \n\nIssues:{}'
    fmt_issues = '\n- {}: {}'
    issues_str = ''
    milestone_str = ''

    options = {
        'server': 'http://192.168.3.56:8089/',
        'verify': True,
        'basic_auth': (username, ldp_password),
    }
    gh = JIRA(options=options, basic_auth=(username, ldp_password))

    # Get all boards viewable by anonymous users.
    boards = gh.boards()
    # board = [b for b in boards if b.name == sprint_name][0]

    sprints = gh.sprints('42')

    for sprint in sorted([s for s in sprints
                   if s.raw[u'state'] == u'ACTIVE'],
                key = lambda x: x.raw[u'sequence']):
        milestone_str = str(sprint)
        issues = sprint_issues(gh, '42', sprint.id)
        for issue in issues:
            issues_str += fmt_issues.format(issue.key, issue.summary)

    result = fmt_full.format(
        milestone_str,
        issues_str
    )
    print(result)
    return result

sprints(username, ldp_password, sprint_name)