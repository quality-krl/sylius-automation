from decimal import Decimal

from utils.demo_helper import DemoHelper
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__PRODUCT_ADDED_MESSAGE = self.page.locator(
            "[data-test-sylius-flash-message]"
        )

        self.__CART_FORM = self.page.locator(
            "#sylius_shop_cart"
        )

        self.__QUANTITY_FIELD = self.page.locator(
            "#sylius_shop_cart_items_0_quantity"
        )

        self.__EMPTY_CART_MESSAGE = self.page.locator(
            ".alert.alert-info"
        )

        self.__CHECKOUT_FORM = self.page.locator(
            'form[action$="/cart/checkout"]'
        )

        self.__CHECKOUT_BUTTON = self.__CHECKOUT_FORM.get_by_role(
            "button",
            name="Checkout",
            exact=True
        )

    def get_added_message(self):
        DemoHelper.show_result(
            self.page,
            self.__PRODUCT_ADDED_MESSAGE
        )

        return self.__PRODUCT_ADDED_MESSAGE

    def get_product_by_name(self, product_name):
        return self.__CART_FORM.get_by_role(
            "link",
            name=product_name,
            exact=True
        )

    def set_quantity(self, quantity):
        self.__wait_for_live_component_ready()

        DemoHelper.highlight(
            self.page,
            self.__QUANTITY_FIELD
        )

        self.__QUANTITY_FIELD.fill(
            str(quantity)
        )

        DemoHelper.clear_highlight(
            self.__QUANTITY_FIELD
        )

    def __get_product_row(self, product_name):
        return self.__CART_FORM.locator(
            "tbody tr"
        ).filter(
            has_text=product_name
        )

    def get_total_price(self, product_name):
        product_row = self.__get_product_row(
            product_name
        )

        total_price = product_row.locator(
            "td"
        ).nth(5)

        DemoHelper.show_result(
            self.page,
            total_price
        )

        return total_price

    def get_total_price_value(self, product_name):
        price_text = self.get_total_price(
            product_name
        ).inner_text()

        return Decimal(
            price_text.replace(
                "€",
                ""
            ).strip()
        )

    def get_current_quantity(self):
        return self.__QUANTITY_FIELD

    def remove_product(self, product_name):
        self.__wait_for_live_component_ready()

        product_row = self.__get_product_row(
            product_name
        )

        remove_button = product_row.locator(
            '[data-live-action-param="removeItem"]'
        )

        DemoHelper.click(
            self.page,
            remove_button
        )

        if DemoHelper.is_enabled():
            product_row.wait_for(
                state="detached"
            )

            if self.__EMPTY_CART_MESSAGE.is_visible():
                DemoHelper.show_result(
                    self.page,
                    self.__EMPTY_CART_MESSAGE
                )

    def get_empty_cart_message(self):
        DemoHelper.show_result(
            self.page,
            self.__EMPTY_CART_MESSAGE
        )

        return self.__EMPTY_CART_MESSAGE

    def __wait_for_live_component_ready(self):
        self.page.wait_for_function(
            """
            () => {
                const cart = document.querySelector(
                    '#sylius_shop_cart'
                );

                const liveRoot = cart?.closest(
                    '[data-controller~="live"]'
                );

                return Boolean(liveRoot?.__component);
            }
            """
        )

    def proceed_to_checkout(self):
        DemoHelper.click(
            self.page,
            self.__CHECKOUT_BUTTON
        )

        self.page.wait_for_url(
            "**/checkout/**"
        )