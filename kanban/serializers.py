from rest_framework import serializers
from .models import *


class KanbanListItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = KanbanListItem
        fields = "__all__"

class KanbanListSerializers(serializers.ModelSerializer):
    items = KanbanListItemSerializers(many = True)
    class Meta:
        model = KanbanList
        fields = "__all__"

class KanbanSerializers(serializers.ModelSerializer):
    lists = KanbanListSerializers(many=True, required=False)

    class Meta:
        model = Kanban
        fields = "__all__"

