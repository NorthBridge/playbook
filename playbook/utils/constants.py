ACCEPT_ISSUE_LABEL = 'owner acceptance'
ACCEPT_ISSUE_TITLE = 'Accept the story (milestone)'
STATIC_LABEL_VALUE = 'acceptance criteria'

SELECTED_STATUS = 14
IN_PROGRESS_STATUS = 15
ACCEPTED_STATUS = 16

ACTION = {'closed': {
                     'status': ACCEPTED_STATUS,
                     'state': 'closed'
                     },
          'reopened': {
                       'status': IN_PROGRESS_STATUS,
                       'state': 'open'
                       }
          }