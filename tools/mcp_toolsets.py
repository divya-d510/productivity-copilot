from tools.calendar_tools import create_event, list_events, check_availability
from tools.task_tools import create_task, list_tasks, update_task_status, get_task
from tools.notes_tools import create_note, list_notes
from tools.search_tools import semantic_search_notes, semantic_search_tasks


def get_calendar_toolset():
    return [
        create_event,
        list_events,
        check_availability,
    ]


def get_task_notes_toolset():
    return [
        create_task,
        list_tasks,
        update_task_status,
        get_task,
        create_note,
        list_notes,
    ]


def get_memory_toolset():
    return [
        semantic_search_notes,
        semantic_search_tasks,
    ]