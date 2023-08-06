from rest_framework import serializers
from server.models import Server, Category, Channel


class ChannelSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    # SerilaizerMethodField used for adding derived fields
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerilaizer(many=True)
    # channel_server is related name

    class Meta:
        model = Server
        exclude = ("member",)

    # telling django to serialize that
    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        else:
            None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("num_members")
        if not num_members:
            data.pop("num_members")
        return data
