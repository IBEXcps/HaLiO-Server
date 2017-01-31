from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class House(models.Model):
    user = models.ForeignKey(User, default=None)
    nome = models.CharField(max_length=128)

    def __str__(self):
        return "{0}'s {1}".format(self.user, self.nome)


class Node(models.Model):
    house = models.ForeignKey(House,related_name='nodes')
    nome = models.CharField(max_length=128)
    relayState = models.BooleanField(default=False)

    def __str__(self):
        return "{0}'s {1} @ {2}".format(self.house.user, self.nome, self.house.nome)

    def get_last_reading(self):
        return ConsumptionData.objects.filter(node=self).order_by('-timestamp')[0].value

    def lastPoints(self):
        return ConsumptionData.objects.filter(node=self).order_by('-timestamp')[:500][::-1]

    def getDataSince(self, startTime, interval=None): #start forcing interval soon
        data = ConsumptionData.objects.filter(node=self, timestamp__gt=startTime)
        return data

    def getFormattedLastData(self):
        timeback = 60
        data = self.getDataSince(datetime.datetime.now() - datetime.timedelta(minutes=timeback))
        ret = []
        now = datetime.datetime.now()
        for point in data:
            since = (now - point.timestamp).seconds
            ret.append([-since, point.value])
        return ret

class ConsumptionData(models.Model):
    node = models.ForeignKey(Node)
    timestamp = models.DateTimeField(auto_now=True)
    value = models.FloatField()

