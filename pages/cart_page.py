from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__PRODUCT_ADDED_MESSAGE = self.page.locator("[data-test-sylius-flash-message]")
        self.__PRODUCT_NAME = self.page.get_by_role("link", name="Radiant Reflection Cap")
        self.__CART_FORM = self.page.locator("#sylius_shop_cart")

    def get_added_message(self):
        return self.__PRODUCT_ADDED_MESSAGE

    def get_product_by_name(self, product_name):
        return self.__CART_FORM.get_by_role(
            "link", name=product_name, exact=True
        )
