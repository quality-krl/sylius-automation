from pages.base_page import BasePage
from utils.demo_helper import DemoHelper

class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__EMAIL = self.page.locator("#sylius_shop_checkout_address_customer_email")
        self.__FIRST_NAME = self.page.locator("#sylius_shop_checkout_address_billingAddress_firstName")
        self.__LAST_NAME = self.page.locator("#sylius_shop_checkout_address_billingAddress_lastName")
        self.__STREET = self.page.locator("#sylius_shop_checkout_address_billingAddress_street")
        self.__COUNTRY = self.page.locator("#sylius_shop_checkout_address_billingAddress_countryCode")
        self.__CITY = self.page.locator("#sylius_shop_checkout_address_billingAddress_city")
        self.__POSTCODE = self.page.locator("#sylius_shop_checkout_address_billingAddress_postcode")
        self.__PHONE_NUMBER = self.page.locator("#sylius_shop_checkout_address_billingAddress_phoneNumber")
        self.__NEXT_BUTTON = self.page.get_by_role("button", name="Next", exact=True)
        self.__SHIPPING_METHOD = self.page.get_by_role("radio", name="UPS")
        self.__CASH_ON_DELIVERY = self.page.get_by_role("radio", name="Cash on delivery")
        self.__PLACE_ORDER_BUTTON = self.page.locator("#confirmation-button")
        self.__THANK_YOU_TITLE = self.page.get_by_role("heading", name="Thank you!", exact=True)
        self.__BANK_TRANSFER = self.page.get_by_role("radio", name="Bank transfer")
        self.__ADDRESS_ERRORS = self.page.locator(".invalid-feedback")

    def fill_billing_address(
            self,
            email,
            first_name,
            last_name,
            street,
            country,
            city,
            postcode,
            phone_number
    ):
        DemoHelper.select_option(
            self.page,
            self.__COUNTRY,
            label=country
        )

        DemoHelper.fill_field(
            self.page,
            self.__EMAIL,
            email
        )

        DemoHelper.fill_field(
            self.page,
            self.__FIRST_NAME,
            first_name
        )

        DemoHelper.fill_field(
            self.page,
            self.__LAST_NAME,
            last_name
        )

        DemoHelper.fill_field(
            self.page,
            self.__STREET,
            street
        )

        DemoHelper.fill_field(
            self.page,
            self.__CITY,
            city
        )

        DemoHelper.fill_field(
            self.page,
            self.__POSTCODE,
            postcode
        )

        DemoHelper.fill_field(
            self.page,
            self.__PHONE_NUMBER,
            phone_number
        )

    def continue_to_shipping(self):
        DemoHelper.add_bottom_space(
            self.page
        )

        self.__NEXT_BUTTON.evaluate(
            """
            element => {
                element.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center',
                    inline: 'center'
                });
            }
            """
        )

        self.page.wait_for_timeout(300)

        DemoHelper.click(
            self.page,
            self.__NEXT_BUTTON
        )

        self.page.wait_for_url(
            "**/checkout/select-shipping"
        )

    def select_shipping_method(self):
        DemoHelper.check(
            self.page,
            self.__SHIPPING_METHOD
        )

    def continue_to_payment(self):
        DemoHelper.click(
            self.page,
            self.__NEXT_BUTTON
        )

        self.page.wait_for_url(
            "**/checkout/select-payment"
        )

    def select_cash_on_delivery(self):
        DemoHelper.check(
            self.page,
            self.__CASH_ON_DELIVERY
        )

    def select_bank_transfer(self):
        DemoHelper.check(
            self.page,
            self.__BANK_TRANSFER
        )

    def continue_from_payment(self):
        DemoHelper.click(
            self.page,
            self.__NEXT_BUTTON
        )

    def place_order(self):
        DemoHelper.click(
            self.page,
            self.__PLACE_ORDER_BUTTON
        )

        self.page.wait_for_url(
            "**/order/thank-you"
        )

    def get_thank_you_title(self):
        DemoHelper.show_result(
            self.page,
            self.__THANK_YOU_TITLE
        )

        return self.__THANK_YOU_TITLE

    def submit_address(self):
        DemoHelper.click(
            self.page,
            self.__NEXT_BUTTON
        )

    def get_address_validation_errors(self):
        visible_errors = self.page.locator(
            ".invalid-feedback:visible"
        )

        visible_errors.first.wait_for(
            state="visible"
        )

        if DemoHelper.is_enabled():
            DemoHelper.show_result(
                self.page,
                visible_errors.first
            )

        return [
            error.strip()
            for error in visible_errors.all_inner_texts()
            if error.strip()
        ]