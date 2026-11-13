import pytest
from playwright.sync_api import expect


from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


class TestCheckoutPage:
    @pytest.mark.parametrize("payment_method",
        [
            "cash_on_delivery",
            "bank_transfer"
        ],
        ids=[
            "cash_on_delivery",
            "bank_transfer"
        ]
    )
    def test_guest_complete_checkout(self, page, radiant_product_page, payment_method):
        radiant_product_page.add_to_cart()
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(page)

        checkout_page.fill_billing_address(
            email="test.qa@example.com",
            first_name="test",
            last_name="Testing",
            street="123 Main Street",
            country="United States",
            city="New York",
            postcode="10001",
            phone_number="1234567890"
        )

        checkout_page.continue_to_shipping()
        checkout_page.select_shipping_method()
        checkout_page.continue_to_payment()

        if payment_method == "cash_on_delivery":
            checkout_page.select_cash_on_delivery()
        else:
            checkout_page.select_bank_transfer()

        checkout_page.continue_from_payment()
        checkout_page.place_order()
        expect(checkout_page.get_thank_you_title()).to_be_visible()
        assert "order/thank-you" in page.url

    def test_checkout_required_address_fields(self, page, radiant_product_page):
        radiant_product_page.add_to_cart()
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(page)
        checkout_page.submit_address()
        errors = checkout_page.get_address_validation_errors()

        assert "Please enter your email." in errors
        assert "Please enter first name." in errors
        assert "Please enter last name." in errors
        assert "Please enter street." in errors
        assert "Please select country." in errors
        assert "Please enter city." in errors
        assert "Please enter postcode." in errors
        assert "checkout/address" in page.url

    def test_checkout_invalid_email(self, page, radiant_product_page):
        radiant_product_page.add_to_cart()
        cart_page = CartPage(page)
        cart_page.proceed_to_checkout()
        checkout_page = CheckoutPage(page)

        checkout_page.fill_billing_address(
            email="invalid-email",
            first_name="Test",
            last_name="Testing",
            street="123 Main Street",
            country="United States",
            city="New York",
            postcode="10001",
            phone_number="1234567890"
        )

        checkout_page.submit_address()
        errors = checkout_page.get_address_validation_errors()

        assert "This email is invalid." in errors
        assert "checkout/address" in page.url
