from utils.demo_helper import DemoHelper

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__FIRST_NAME_FIELD = self.page.locator("#sylius_shop_customer_registration_firstName")
        self.__LAST_NAME_FIELD = self.page.locator("#sylius_shop_customer_registration_lastName")
        self.__EMAIL_FIELD = self.page.locator("#sylius_shop_customer_registration_email")
        self.__PHONE_FIELD = self.page.locator("#sylius_shop_customer_registration_phoneNumber")
        self.__PASSWORD_FIELD = self.page.locator("#sylius_shop_customer_registration_user_plainPassword_first")
        self.__VERIFY_PASSWORD_FIELD = self.page.locator("#sylius_shop_customer_registration_user_plainPassword_second")
        self.__REGISTER_BUTTON = self.page.locator("#register-button")

        self.__FIRST_NAME_ERROR = self.page.locator("#sylius_shop_customer_registration_firstName + .invalid-feedback")
        self.__LAST_NAME_ERROR = self.page.locator("#sylius_shop_customer_registration_lastName + .invalid-feedback")
        self.__EMAIL_ERROR = self.page.locator("#sylius_shop_customer_registration_email + .invalid-feedback")
        self.__PASSWORD_ERROR = self.page.locator("#sylius_shop_customer_registration_user_plainPassword_first + .invalid-feedback")

    def register_user(self, first_name, last_name, email, phone_number, password, verify_password):
        self.__wait_for_live_component_ready()

        self.__fill_live_field(self.__FIRST_NAME_FIELD, first_name)
        self.__fill_live_field(self.__LAST_NAME_FIELD, last_name)
        self.__fill_live_field(self.__EMAIL_FIELD, email)
        self.__fill_live_field(self.__PHONE_FIELD, phone_number)
        self.__fill_live_field(self.__PASSWORD_FIELD, password)
        self.__fill_live_field(self.__VERIFY_PASSWORD_FIELD, verify_password)

        DemoHelper.click(
            self.page,
            self.__REGISTER_BUTTON
        )

    def __wait_for_live_component_ready(self):
        self.page.wait_for_function(
            """
            () => {
                const field = document.querySelector(
                    '#sylius_shop_customer_registration_firstName'
                );

                const liveRoot = field?.closest(
                    '[data-controller~="live"]'
                );

                return Boolean(liveRoot?.__component);
            }
            """
        )

    def __wait_for_live_component_update(self):
        try:
            self.page.wait_for_function(
                """
                () => document.querySelectorAll(
                    '[data-controller~="live"][busy], [data-live-is-loading]'
                ).length > 0
                """,
                timeout=1000
            )

        except PlaywrightTimeoutError:
            pass

        self.page.wait_for_function(
            """
            () => document.readyState === "complete" &&
                  document.querySelectorAll(
                      '[data-controller~="live"][busy], [data-live-is-loading]'
                  ).length === 0
            """,
            timeout=5000
        )

    def __fill_live_field(self, field, value):
        if value == "":
            return

        DemoHelper.highlight(
            self.page,
            field
        )

        field.fill(value)
        field.blur()

        self.__wait_for_live_component_update()

        DemoHelper.clear_highlight(
            field
        )

    def get_first_name_error(self):
        DemoHelper.show_result(
            self.page,
            self.__FIRST_NAME_ERROR
        )
        return self.__FIRST_NAME_ERROR

    def get_last_name_error(self):
        DemoHelper.show_result(
            self.page,
            self.__LAST_NAME_ERROR
        )
        return self.__LAST_NAME_ERROR

    def get_email_error(self):
        DemoHelper.show_result(
            self.page,
            self.__EMAIL_ERROR
        )
        return self.__EMAIL_ERROR

    def get_password_error(self):
        DemoHelper.show_result(
            self.page,
            self.__PASSWORD_ERROR
        )
        return self.__PASSWORD_ERROR