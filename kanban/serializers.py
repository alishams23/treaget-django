from rest_framework import serializers
from .models import *
from extensions.utils import jalali_converter


class KanbanListItemSerializers(serializers.ModelSerializer):
    def created_at_function(self,obj):
        date = jalali_converter(obj.created_at)
        return  f"{date[0]}/{date[1]}/{date[2]}"
    def updated_at_function(self,obj):
        date = jalali_converter(obj.updated_at)
        return  f"{date[0]}/{date[1]}/{date[2]}"

    created_at = serializers.SerializerMethodField("created_at_function")
    updated_at = serializers.SerializerMethodField("updated_at_function")
    class Meta:
        model = KanbanListItem
        fields = "__all__"

class KanbanListSerializers(serializers.ModelSerializer):
    items = KanbanListItemSerializers(many = True)
    class Meta:
        model = KanbanList
        fields = "__all__"

class KanbanSerializers(serializers.ModelSerializer):
    def created_at_function(self,obj):
        return  f"{jalali_converter(obj.created_at)}"

    created_at = serializers.SerializerMethodField("created_at_function")
    
    lists = KanbanListSerializers(many=True, required=False)

    class Meta:
        model = Kanban
        fields = "__all__"

