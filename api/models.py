from django.db import models
from datetime import datetime
import time


class App(models.Model):
    class Meta:
        db_table = 'app'

    name = models.CharField(max_length=128)
    host_id = models.IntegerField()
    group_id = models.IntegerField()
    configuration = models.TextField()
    status = models.CharField(max_length=12) 
    message = models.TextField()
    enable = models.IntegerField(default=1)
    last_update = models.DateTimeField()

    @classmethod
    def create(cls, name, host_id, status, message, enable, group_id):
        app = cls(name=name,
                  host_id=host_id,
                  group_id=group_id,
                  status=status,
                  message=message,
                  enable=enable,
                  last_update=datetime.now())
        return app

    def convert_to_epoc(self):
        return self.last_update.strftime("%Y-%m-%d %H:%M:%S")


class AppStatistics(models.Model):
    class Meta:
        db_table = 'app_statistics'

    app_id = models.IntegerField()
    statistics = models.CharField(max_length=256)
    time = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, statistics, app_id):
        appStatistics = cls(statistics=statistics, app_id=app_id)
        return appStatistics

    def convert_to_epoc(self):
        return time.mktime(self.time.timetuple())


class Group(models.Model):
    class Meta:
        db_table = 'app_group'

    unique_name = models.CharField(max_length=32)
    display_name = models.CharField(max_length=32)

    @classmethod
    def create(cls, unique_name, display_name):
        group = cls(unique_name=unique_name, display_name=display_name)
        return group


class AppHistory(models.Model):
    class Meta:
        db_table = 'app_history'

    app_id = models.IntegerField()
    status = models.CharField(max_length=32)
    message = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)

    def convert_to_epoc(self):
        return self.time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def create(cls, app_id, status, message):
        group = cls(app_id=app_id, status=status, message=message, time=datetime.now())
        return group


class Host(models.Model):
    class Meta:
        db_table = 'app_host'

    name = models.CharField(max_length=32)
    ip = models.CharField(max_length=64)
    description = models.CharField(max_length=256, null=True)

    @classmethod
    def create(cls, ip, name=''):
        group = cls(ip=ip, name=name)
        return group
