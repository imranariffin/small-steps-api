from tasks.models import Task


def setup_tasks(input_list):
    """
    >>> setup_tasks(
        '''id,parent_id,text,status
        e2ea6821-9298-41cc-b970-9bf299c63e37,78f15712-371f-4b1d-b60e-4c9f4c89f642,some-task-text-0,not_started
        a0df4108-fd0a-4deb-aec7-d284ac33cf92,78f15712-371f-4b1d-b60e-4c9f4c89f642,some-task-text-1,in_progress
        a61f8e97-ebd9-43f5-b72c-58017e89b6f8,78f15712-371f-4b1d-b60e-4c9f4c89f642,some-task-text-2,completed
        '''
    )
    [<Task: Task ...>, <Task: Task ...>, <Task: Task ...>]
    """
    tasks_list = []
    for ln, line in enumerate(input_list.split('\n')):
        if ln == 0 or len(line.split(',')) != 4:
            continue
        id, parent_id, text, status = line.strip().split(',')
        tasks_list.append(
            Task.objects.create(
                id=id,
                parent_id=parent_id,
                status=status,
                text=text,
            ),
        )
    return tasks_list
