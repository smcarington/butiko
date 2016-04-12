from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class ItemList(models.Model):
    owner        = models.ForeignKey(User)
    users        = models.ManyToManyField(User, related_name='lists')
    title        = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    modified     = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

class Item(models.Model):
    itemList = models.ForeignKey(ItemList)
    title    = models.CharField(max_length=50)
    store    = models.CharField(max_length=50)
    number   = models.IntegerField(default=0)
    price    = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    update   = models.DateTimeField(default=timezone.now)

    def change_number(self, diff=1):
        self.number = self.number + diff;
        if self.number < 0:
            self.number = 0
        self.update = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class PermRequest(models.Model):
    itemList = models.ForeignKey(ItemList, related_name="user_requests")
    user     = models.ForeignKey(User, related_name="list_requests")

    def __str__(self):
        return [self.itemList + " from " + self.user]

# Create your models here.
