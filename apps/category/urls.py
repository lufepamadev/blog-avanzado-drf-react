from django.urls import path

from .views import *


urlpatterns = [
    path('categories', ListCategoriesView.as_view()),
    # Add new endpoint to the resource creation
    path('category', CategoryView.as_view()),
]
