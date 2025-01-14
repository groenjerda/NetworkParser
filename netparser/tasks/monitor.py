import asyncio
from time import sleep

from celery import shared_task
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from scrapyd_api import ScrapydAPI

from .models import Task

PROJECT_NAME = 'ip_networks'
FINISHED = 'finished'
PENDING = 'pending'
MAX_TIME = 90


@shared_task
def monitor_task(taskid, user_id):
    """
    Опрос scrapyd на предмет статуса задачи.
    Завершение работы при получении статуса finished
    """
    task = Task.objects.get(id=taskid)

    scrapyd = ScrapydAPI(settings.SCRAPYD_HOST)
    status = scrapyd.job_status(PROJECT_NAME, task.description)
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    initial_status = PENDING
    seconds_passed = 0
    while status != FINISHED:
        if seconds_passed > MAX_TIME:
            loop.run_until_complete(
                channel_layer.group_send(
                    f'task_from_user_{user_id}',
                    {
                        'type': 'send_status_updates',
                        'task_id': task.id,
                        'status': 'timeout'
                    }
                )
            )
            break
        sleep(1)
        status = scrapyd.job_status(PROJECT_NAME, task.description)
        if status != initial_status:
            try:
                # В процессе мониторинга выполнения задачи
                # пользователь может удалить задачу
                task = Task.objects.get(id=taskid)
            except ObjectDoesNotExist:
                break
            initial_status = status
            task.status = status
            task.save()
            loop.run_until_complete(
                channel_layer.group_send(
                    f'task_from_user_{user_id}',
                    {
                        'type': 'send_status_updates',
                        'task_id': task.id,
                        'status': status
                    }
                )
            )
        seconds_passed += 1
