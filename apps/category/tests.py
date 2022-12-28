from django.test import TestCase
from django.test import Client
from .models import Category
# Create your tests here.


class CategoryTestCase(TestCase):

    def setUp(self):
        '''
            Setup the basic attributes used in this class
        '''
        self.category_test = Category.objects.create(name='Test_name', description='Test_Description',
                                                     thumbnail='/media/media/categories/WhatsApp_Image_2022-10-26_at_15.09.05_2_wcK09Jr.jpeg')
        self.category_demo = Category.objects.create(name='Demo_name', description='Demo_Description',
                                                     thumbnail='/media/media/categories/WhatsApp_Image_2022-10-26_at_15.09.05_2_wcK09Jr.jpeg'
                                                     )
        self.subcategory_of_a_category = Category.objects.create(parent=self.category_test, name='Subcategory_name', description='Subcategory_Description',
                                                                 thumbnail='/media/media/categories/WhatsApp_Image_2022-10-26_at_15.09.05_2_wcK09Jr.jpeg'
                                                                 )

        self.client = Client()
        self.response = self.client.get('/api/category/categories')

    def test_get_category_list(self):
        '''
            Check if category list is fetched
        '''
        # The status code already set in ListCategoriesView is 200
        self.assertEqual(self.response.status_code, 200)

    def test_parameters_in_get_category_list_request(self):
        '''
            Check if the returned parameters in category list request are correct
        '''
        category_list = self.response.json()['categories']
        # If one item accomplish the requirements, all items will do too
        if (len(category_list) > 0):
            first_item = category_list[0]
            self.assertIsNotNone(first_item['id'])
            self.assertIsNotNone(first_item['name'])
            self.assertIsNotNone(first_item['thumbnail'])
            self.assertIsNotNone(first_item['description'])
            self.assertIsNotNone(first_item['sub_categories'])

    def test_parameters_in_sub_categories_key_in_get_category_list_request(self):
        '''
            Check if the subcategory key of the returned category list contains 
            the needed parameters.
        '''
        # Obtain category list
        category_list = self.response.json()['categories']

        for cat in category_list:
            if (len(cat['sub_categories']) > 0):
                # If one item accomplish the requirements, all items will do too

                self.assertIsNotNone(cat['sub_categories'][0]['id'])
                self.assertIsNotNone(cat['sub_categories'][0]['name'])
                self.assertIsNotNone(cat['sub_categories'][0]['thumbnail'])
                self.assertIsNotNone(cat['sub_categories'][0]['description'])

    def test_creation_new_category(self):
        '''
            Check if category is created sending post request
        '''
        context = {
            'name': 'post_test_name',
            'description': 'post_test_description'
        }
        # Send post request
        response_post = self.client.post('/api/category/category', context)
        query = Category.objects.filter(name='post_test_name')

        # Make validations
        # The status code already set in CategoryView is 201
        self.assertEqual(query[0].name, 'post_test_name')
        self.assertEqual(query[0].description, 'post_test_description')
        self.assertEqual(response_post.status_code, 201)
