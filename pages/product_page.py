from utils.demo_helper import DemoHelper

from pages.base_page import BasePage

class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__ADD_TO_CART_BUTTON = self.page.locator("#add-to-cart-button")

    def open_product(self, product_slug):
        return self.page.goto(f"{self.base_url}products/{product_slug}")

    def add_to_cart(self):
        self.page.wait_for_function(
            """
            () => {
                const form = document.querySelector(
                    'form[name="sylius_shop_add_to_cart"]'
                );

                const liveComponent = form?.closest(
                    '[data-controller~="live"]'
                );

                return Boolean(liveComponent?.__component);
            }
            """
        )

        DemoHelper.click(
            self.page,
            self.__ADD_TO_CART_BUTTON
        )
        self.page.wait_for_url("**/cart/")