from rest_framework import serializers
from api.models import Group, App, Host, AppHistory, AppStatistics


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('unique_name', 'display_name', 'id')


class AppSerializer(serializers.ModelSerializer):
    last_update = serializers.ReadOnlyField(source='convert_to_epoc')

    class Meta:
        model = App
        fields = ('id', 'name', 'host_id', 'group_id',
                  'status', 'message', 'last_update')


class host_serializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ("id", "name", "ip", "description")


class manager_app_serializer(serializers.ModelSerializer):
    last_update = serializers.ReadOnlyField(source='convert_to_epoc')

    class Meta:
        model = App
        fields = ("id", "name", "host_id", "group_id",
                  "configuration", "status", "message",
                  "enable", "last_update")


class app_history_serializer(serializers.ModelSerializer):
    time = serializers.ReadOnlyField(source='convert_to_epoc')

    class Meta:
        model = AppHistory
        fields = ("id", "app_id", "status", "time")


class app_statistics_serializer(serializers.ModelSerializer):
    time = serializers.ReadOnlyField(source='convert_to_epoc')

    class Meta:
        model = AppStatistics
        fields = ("id", "app_id", "statistics", "time")
