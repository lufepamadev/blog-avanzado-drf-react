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
                                                     thumbnail='https://cdn.shopify.com/s/files/1/0648/0124/3361/files/logo-light.png?v=1656315496&width=100'
                                                     )
        self.subcategory_of_a_category = Category.objects.create(parent=self.category_test, name='Subcategory_name', description='Subcategory_Description',
                                                                 thumbnail='https://cdn.shopify.com/s/files/1/0648/0124/3361/files/logo-light.png?v=1656315496&width=100'
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
            Check if the returned parameters in category list request are correct,
            they must include id, name, thumbnail, description and sub_categories
        '''
        category_list = self.response.json()['categories']

        for cat in category_list:
            self.assertIsNotNone(cat['id'])
            self.assertIsNotNone(cat['name'])
            self.assertIsNotNone(cat['thumbnail'])
            self.assertIsNotNone(cat['description'])
            self.assertIsNotNone(cat['sub_categories'])

    def test_parameters_in_sub_categories_key_in_get_category_list_request(self):
        '''
            Check if the subcategory key of the returned category list contains 
            the needed parameters which are id, name, thumbnail and description.
        '''
        # Obtain category list
        category_list = self.response.json()['categories']

        for cat in category_list:
            if (len(cat['sub_categories']) > 0):
                for sub_cat in cat['sub_categories']:
                    self.assertIsNotNone(sub_cat['id'])
                    self.assertIsNotNone(sub_cat['name'])
                    self.assertIsNotNone(sub_cat['thumbnail'])
                    self.assertIsNotNone(sub_cat['description'])

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
