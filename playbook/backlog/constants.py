ACCEPT_ISSUE_LABEL = 'owner acceptance'

GH_STATE = 'gh_state'
DB_STATUS = 'db_status'

DB_OPEN_STATUS_NAME = 'open'
DB_SELECTED_STATUS_NAME = 'selected'
DB_QUEUED_STATUS_NAME = 'queued'
DB_ACCEPTED_STATUS_NAME = 'accepted'

GH_ACTION = {
    'closed': {
        DB_STATUS: DB_ACCEPTED_STATUS_NAME,
        GH_STATE: 'closed'
    },
    'reopened': {
        DB_STATUS: DB_QUEUED_STATUS_NAME,
        GH_STATE: 'open'
    }
}
