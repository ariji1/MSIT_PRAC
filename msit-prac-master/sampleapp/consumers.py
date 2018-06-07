import json
import logging
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from .models import Message, Room

log = logging.getLogger(__name__)


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['u']
        self.room_group_name = 'chat-%s' % self.room_name

        self.accept()

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        message = text_data_json['message']
        label = text_data_json['room_label']
        sender_username = text_data_json['sender']

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'label': label,
                'sender_username': sender_username
            }
        )

    def chat_message(self, event):

        message = event['message']
        label = event['label']
        sender_username = event['sender_username']

        try:
            room = Room.objects.get(label=label)
            sender = User.objects.get(username=sender_username)
            new_msg = Message.objects.create(room=room, message=message, sender=sender, timestamp=datetime.now())
            print('inserted new message: ' + new_msg.message)

            self.send(text_data=json.dumps({
                'message': message,
                'sender': sender_username,
                'first_name': sender.first_name,
                'last_name': sender.last_name,
                'timestamp': json.dumps(new_msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                                        indent=4, sort_keys=True, default=str)
            }))

        except Room.DoesNotExist:
            log.debug('Room with label %s does not exist!' % label)
            print('Room with label %s does not exist!' % label)
            return
        except User.DoesNotExist:
            log.debug('User with username %s does not exist!' % sender_username)
            print('User with username %s does not exist!' % sender_username)
            return