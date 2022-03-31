from pathlib import Path

from .tests import ProductLookupTests
from .models import Favorites, Products
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


from django.urls import reverse


class ProductLookupSeleniumTest(StaticLiveServerTestCase):
    """Selenium tests for Product_lookup"""

    def setUp(self):
        """
        Create a user and a product to test the product_lookup view
        """
        ProductLookupTests.setUp(self)

        self.connected_client = Client()
        self.connected_client.login(
            username='testuser', password='12345')
        self.connected_client_cookie = \
            self.connected_client.cookies['sessionid'].value
        self.this_dir = Path(__file__).parent.absolute()
        self.options = Options()
        self.options.add_argument("--enable-javascript")
        self.options.add_argument(
            '--disable-blink-features=AutomationControlled')
        # self.options.add_argument('--headless')
        self.browser = WebDriver(ChromeDriverManager().install(),
                                 chrome_options=self.options)
        self.browser.implicitly_wait(60)

    def tearDown(self) -> None:
        self.browser.quit()
        super().tearDown()

    def test_save_product_to_favorites(self):
        """
        Test that the add to favorite feature adds to favorites
        """

        url = reverse('product_lookup:product_lookup_results',
                      args=["test_product3"])
        self.browser.get(self.live_server_url + url)
        # Add a cookie to be logged in
        self.browser.add_cookie(
            {'name': 'sessionid', 'value': self.connected_client_cookie,
             'secure': False, 'path': '/'})
        # Refresh the page to have the proper javascript run
        self.browser.refresh()
        # Look for the add to favorite button
        to_be_added_product_id = Products.objects.get(
            product_name="test_product2").id
        self.browser.find_element_by_id(
            f'product_add_{to_be_added_product_id}').click()
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of_element_located(
                (By.ID, f"product_remove_{to_be_added_product_id}")))
        # 2 items in favorites, 1 from setup, and the one we added.
        self.assertEqual(Favorites.objects.count(), 2)

        # We then re-click the button to remove the item from favorites
        self.browser.find_element_by_id(
            f'product_remove_{to_be_added_product_id}').click()
        WebDriverWait(self.browser, 30).until(
            EC.visibility_of_element_located(
                (By.ID, f"product_add_{to_be_added_product_id}")))

        # We should have only 1 item in favorites
        self.assertEqual(Favorites.objects.count(), 1)

        self.tearDown()

    def test_homepage_search(self):
        url = reverse('product_lookup:product_lookup')
        self.browser.get(self.live_server_url + url)
        self.browser.find_element_by_css_selector(
            'input.form-control:nth-child(2)').send_keys('test_product')
        self.browser.find_element_by_css_selector(
            'div.input-group-append:nth-child(3) > button:nth-child(1)'
            ).click()
        search_done = WebDriverWait(self.browser, 3).until(
            EC.url_contains('search'))
        self.assertTrue(search_done)
