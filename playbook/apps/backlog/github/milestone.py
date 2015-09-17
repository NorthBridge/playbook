def create_milestone_data(backlog, state='open'):
    data = {'title': backlog.story_title}
    data['state'] = state
    data['description'] = backlog.story_descr
    data['due_on'] = backlog.sprint.end_dttm
    return data
