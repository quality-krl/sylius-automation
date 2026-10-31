from pages.base_page import BasePage
from playwright.sync_api import expect


class ProductPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__ADD_TO_CART_BUTTON = self.page.locator("#add-to-cart-button")


    def add_to_cart(self):
        # Wait until Sylius Live Component is initialized before clicking.
        # Without this wait, automation may click before the component is ready.
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
        self.__ADD_TO_CART_BUTTON.click()