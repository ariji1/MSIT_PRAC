# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

import random
import string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # slug = models.SlugField(default=False, null=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# Database model for Chat Room
class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)

    def contains_user(self, id):
        if self.label == 'global':
            try:
                uname = User.objects.get(id=id)
                my_msgs = self.messages.filter(sender__username__iexact=uname.username)
                if my_msgs:
                    return True
                else:
                    return False
            except User.DoesNotExist:
                return False

        one, other = self.label.split('_')
        return str(one) == str(id) or str(other) == str(id)

    def get_room_name(self, user_id):
        """
        Returns the room name, usually the name of the other person.
        :return: Name
        """
        if self.label == 'global':
            return 'Global'

        other = self.get_other_participant(user_id)
        other_obj = User.objects.get(id=other)

        if len(other_obj.first_name) != 0 and len(other_obj.last_name) != 0:
            return other_obj.first_name + ' ' + other_obj.last_name
        else:
            return other_obj.username

    def get_other_participant(self, user_id):
        one, other = self.label.split('_')
        one = str(one)
        other = str(other)

        if one == user_id:
            return other

        return one

    def get_room_link(self, user_id):
        """
        Returns the "room link". This basically means the method returns either the string 'all',
        or the ID of the other participant.
        :param user_id:
        :return:
        """

        if self.label == 'global':
            return 'all'

        return self.get_other_participant(user_id)


# Database model for Chat Message
class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=CASCADE, null=True)
    message = models.TextField()
    timestamp = models.DateTimeField(default=datetime.now(), db_index=True)


# def prof_pre_save(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)
# pre_save.connect(prof_pre_save, sender=Profile)

# def unique_slug_generator(instance, new_slug=None):
#     """
#     This is for a Django project and it assumes your instance
#     has a model with a slug field and a title character (char) field.
#     """
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.title)
#
#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#                     slug=slug,
#                     randstr=random_string_generator(size=4)
#                 )
#         return unique_slug_generator(instance, new_slug=new_slug)
#     return slug
#
#
# def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))