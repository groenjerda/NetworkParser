import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class TasksConsumer(WebsocketConsumer):
    def connect(self):
        try:
            async_to_sync(self.channel_layer.group_add)(
                'tasks_status_updates',
                self.channel_name
            )
            self.accept()
        except Exception as er:
            print('Error while connect: ', er)

    def disconnect(self, code):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                'tasks_status_updates',
                self.channel_name
            )
        except Exception as er:
            print('Error while disconnect: ', er)

    def send_status_updates(self, event):
        self.send(text_data=json.dumps(event))

    def send_new_task(self, event):
        self.send(text_data=json.dumps(event))
