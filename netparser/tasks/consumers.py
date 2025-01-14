import json

# from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class TasksConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.channel_layer.group_add(
            f'task_from_user_{self.user.id}',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            f'task_from_user_{self.user.id}',
            self.channel_name
        )

    # def disconnect(self, code):
    #     try:
    #         async_to_sync(self.channel_layer.group_discard)(
    #             'tasks_status_updates',
    #             self.channel_name
    #         )
    #     except Exception as er:
    #         print('Error while disconnect: ', er)

    async def send_status_updates(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_new_task(self, event):
        await self.send(text_data=json.dumps(event))
