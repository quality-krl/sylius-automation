import pytest
from playwright.sync_api import expect

from config.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


class TestCartPage:
    def test_add_product_to_cart(self, page, radiant_product_page):
        radiant_product_page.add_to_cart()
        cart_page = CartPage(page)
        expect(cart_page.get_added_message()).to_contain_text("Item has been added to cart")
        expect(cart_page.get_product_by_name("Radiant Reflection Cap")).to_be_visible()

    def test_add_to_cart_logged_in(self, page):
        home_page = HomePage(page)
        page.goto(f"{ConfigReader.get_ui_base_url()}login")
        username = ConfigReader.get_username()
        password = ConfigReader.get_password()

        login_page = LoginPage(page)
        login_page.login(username, password)
        expect(home_page.get_logout_button()).to_be_visible()
        response = page.goto(f"{ConfigReader.get_ui_base_url()}products/radiant-reflection-cap")
        if response is None or response.status >= 500:
            pytest.skip("External Sylius product page is unavailable")
        product_page = ProductPage(page)
        product_page.add_to_cart()

        cart_page = CartPage(page)
        expect(cart_page.get_added_message()).to_contain_text("Item has been added to cart")
        expect(cart_page.get_product_by_name("Radiant Reflection Cap")).to_be_visible()

    def test_correct_quantity(self, page, radiant_product_page):
        radiant_product_page.add_to_cart()
        cart_page = CartPage(page)
        initial_price = cart_page.get_total_price_value("Radiant Reflection Cap")
        cart_page.set_quantity(2)
        expect(cart_page.get_current_quantity()).to_have_value("2")
        expected_total = initial_price * 2
        expect(cart_page.get_total_price("Radiant Reflection Cap")).to_contain_text(f"€{expected_total:.2f}")

    def test_remove_product(self, page, radiant_product_page):
        radiant_product_page.add_to_cart()
        product_name = "Radiant Reflection Cap"

        cart_page = CartPage(page)
        cart_page.remove_product(product_name)

        expect(
            cart_page.get_product_by_name(product_name)
        ).to_have_count(0)
        expect(cart_page.get_empty_cart_message()).to_contain_text("Your cart is empty")