from .models import *
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    thumbnail = serializers.CharField(source='get_thumbnail')

    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'thumbnail',
        ]


class CreateCategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()

    def validate_name(self, value):
        '''
            Validates if name from body request is unique
        '''
        category_query = Category.objects.filter(name=value)
        if (len(category_query) > 0):
            raise serializers.ValidationError(
                'The category name is already in use, please try again')
        return value

    def create(self, validated_data):
        '''
            Once the validations are passed, the resource is created
        '''
        new_category = Category(**validated_data)
        new_category.save()
        return new_category
