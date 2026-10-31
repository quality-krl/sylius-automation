from config.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from playwright.sync_api import expect

class TestCartPage:
    def test_add_product_to_cart(self,page):
        home_page = HomePage(page)
        home_page.open()
        home_page.open_radiant_reflection_cap()

        product_page = ProductPage(page)
        product_page.add_to_cart()

        cart_page = CartPage(page)

        expect(cart_page.get_added_message()).to_contain_text("Item has been added to cart")
        expect(cart_page.get_product_by_name("Radiant Reflection Cap")).to_be_visible()

    def test_add_to_cart_logged_in(self, page):
        home_page = HomePage(page)
        home_page.open()
        home_page.open_login()

        username = ConfigReader.get_username()
        password = ConfigReader.get_password()

        login_page = LoginPage(page)
        login_page.login(username, password)
        expect(home_page.get_logout_button()).to_be_visible()
        home_page.open_radiant_reflection_cap()

        product_page = ProductPage(page)
        product_page.add_to_cart()

        cart_page = CartPage(page)
        expect(cart_page.get_added_message()).to_contain_text("Item has been added to cart")
        expect(cart_page.get_product_by_name("Radiant Reflection Cap")).to_be_visible()