from apps.category.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category
from rest_framework.pagination import PageNumberPagination
from .serializers import CreateCategorySerializer


'''
    The test classes for this Views can be found in tests.py file of this Django app.
'''


class ListCategoriesView(APIView):

    def get(self, request, format=None):
        '''
            In order to simplify this view, I would rather move this logic into serializer class
        '''
        if Category.objects.all().exists():
            categories = Category.objects.all()

            result = []

            for category in categories:
                if not category.parent:
                    item = {}
                    item['id'] = category.id
                    item['name'] = category.name
                    item['thumbnail'] = category.get_thumbnail
                    item['description'] = category.description
                    item['sub_categories'] = []

                    for cat in categories:
                        sub_item = {}
                        if cat.parent and cat.parent.id == category.id:
                            sub_item['id'] = cat.id
                            sub_item['name'] = cat.name
                            sub_item['thumbnail'] = cat.get_thumbnail
                            sub_item['description'] = cat.description
                            item['sub_categories'].append(sub_item)

                    result.append(item)

            return Response({'categories': result}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No categories found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryView(APIView):

    def post(self, request, format=None):
        '''
            Manages the creation of new Categories
        '''
        try:
            category_serializer = CreateCategorySerializer(data=request.data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response({'success': True}, status=status.HTTP_201_CREATED)
            else:
                return Response({'success': False, 'error': category_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success': False, 'error': 'Something went wrong, try again'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
