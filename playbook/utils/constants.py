ACCEPT_ISSUE_LABEL = 'owner acceptance'
ACCEPT_ISSUE_TITLE = 'Accept the story (milestone)'
STATIC_LABEL_VALUE = 'acceptance criteria'

SELECTED_STATUS = 14
IN_PROGRESS_STATUS = 15
ACCEPTED_STATUS = 16

GH_CLOSED_STATE='closed'
GH_OPEN_STATE='open'

GH_CLOSED_ACTION='closed'
GH_REOPENED_ACTION='reopened'

GH_ACTION = {
    GH_CLOSED_ACTION: {
        'db_status': ACCEPTED_STATUS,
        'gh_state': GH_CLOSED_STATE
    },
    GH_REOPENED_ACTION: {
        'db_status': IN_PROGRESS_STATUS,
        'gh_state': GH_OPEN_STATE
    }
}