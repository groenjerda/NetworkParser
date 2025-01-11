from django import template

register = template.Library()


@register.filter
def status_class(status):
    if status == 'pending':
        return 'task-pending'
    elif status == 'running':
        return 'task-running'
    elif status == 'finished':
        return 'task-finished'
    else:
        return 'task-error'
