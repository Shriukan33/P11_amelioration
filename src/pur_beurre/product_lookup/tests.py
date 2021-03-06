from django.contrib.auth.models import User
from django.http import HttpResponse
from django.test import Client, TestCase
from django.urls import reverse
from .models import Products, Favorites, Category


class ProductLookupTests(TestCase):
    def setUp(self):
        """
        Create a user and a product to test the product_lookup view
        """
        self.user = User.objects.create_user(
            username='testuser', password='12345')
        self.category = Category.objects.create(category_name='test_category')
        self.product = Products.objects.create(
            product_name='test_product',
            product_url='http://test_url.com',
            product_image='https://via.placeholder.com/400',
            product_nutriscore='a',
            product_category=self.category,
            nutritional_information='https://via.placeholder.com/200'
        )
        self.second_product = Products.objects.create(
            product_name='test_product2',
            product_url='http://test_url2.com',
            product_image='https://via.placeholder.com/400',
            product_nutriscore='b',
            product_category=self.category,
            nutritional_information='https://via.placeholder.com/200'
        )
        self.third_product = Products.objects.create(
            product_name='test_product3',
            product_url='http://test_url3.com',
            product_image='https://via.placeholder.com/400',
            product_nutriscore='c',
            product_category=self.category,
            nutritional_information='https://via.placeholder.com/200'
        )
        self.favorite = Favorites.objects.create(
            user=self.user,
            product=self.third_product
        )
        self.connected_client = Client()
        self.connected_client.force_login(self.user)

    def test_product_lookup_view_status_code(self):
        """
        Test that the product_lookup view returns a 200 status code
        """
        url = reverse('product_lookup:product_lookup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_lookup_search_status_code(self):
        """
        Test that the product_lookup_search view returns a 200 status code
        """
        url = reverse('product_lookup:product_lookup_results',
                      kwargs={'product_name': 'test_product'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.connected_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_lookup_search_results(self):
        """
        Test that the product_lookup_search view returns the correct product
        """
        url = reverse('product_lookup:product_lookup_results',
                      kwargs={'product_name': 'test_product'})
        response = self.client.get(url)
        self.assertEqual(response.context['searched_product'], self.product)

    def test_product_lookup_search_results_no_results(self):
        """
        Test that the product_lookup_search view returns an empty list if no
        product is found
        """
        url = reverse('product_lookup:product_lookup_results',
                      kwargs={'product_name': 'test_product4'})
        response = self.client.get(url)
        self.assertEqual(response.context['searched_product'], None)

    def test_favorites_status_code(self):
        """
        Test that the favorites view returns a 302 status code
        The user must be connected.
        """
        url = reverse('product_lookup:my_favorites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_favorites_status_code_connected(self):
        """
        Test that the favorites view returns a 200 status code
        The user must be connected.
        """
        url = reverse('product_lookup:my_favorites')
        response = self.connected_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_details_status_code_connected(self):
        """
        Test that the product_details view returns a 200 status code
        The user must be connected.
        """
        url = reverse('product_lookup:product_details',
                      kwargs={'pk': self.product.pk})
        response = self.connected_client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_model_names(self):
        """
        Test that the model names are correct
        """
        self.assertEqual(str(self.user), 'testuser')
        self.assertEqual(str(self.category), 'test_category')
        self.assertEqual(str(self.product), 'test_product')
        self.assertEqual(str(self.favorite), 'test_product3')

    def lookup_by_name_response(
            self, product_name: str, client: Client = None) -> HttpResponse:
        """
        Test that the lookup_by_name returns a 200 response and return
        said response.
        """
        url = reverse('product_lookup:product_lookup_by_name',
                      kwargs={'product_name': product_name})
        if not client:
            response = self.client.get(url)
        else:
            response = client.get(url)

        self.assertEqual(response.status_code, 200)
        return response

    def test_ProductLookupByNameView(self):
        """
        Test that lookupbyname view returns the correct number of products
        """

        response = self.lookup_by_name_response('test_product')
        # All 3 products contain the word "test_product"
        self.assertEqual(len(response.context['alternatives']), 3)

        self.third_product.product_name = "something else"
        self.third_product.save()
        response = self.lookup_by_name_response('test_product')
        # Only 2 products contain the word "test_product"
        self.assertEqual(len(response.context['alternatives']), 2)

        # We look up the third_product with its terms in a different order
        response = self.lookup_by_name_response("else something")

        # Only third_product contains the word "else something"
        # Note : third_product.product_name is "something else"
        self.assertEqual(len(response.context['alternatives']), 1)

        self.lookup_by_name_response("else something", self.connected_client)
        self.assertEqual(len(response.context['alternatives']), 1)
