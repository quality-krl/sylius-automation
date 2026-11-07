from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.__PRODUCT_ADDED_MESSAGE = self.page.locator("[data-test-sylius-flash-message]")
        self.__CART_FORM = self.page.locator("#sylius_shop_cart")
        self.__QUANTITY_FIELD = self.page.locator("#sylius_shop_cart_items_0_quantity")
        self.__EMPTY_CART_MESSAGE = self.page.locator(".alert.alert-info")

    def get_added_message(self):
        return self.__PRODUCT_ADDED_MESSAGE

    def get_product_by_name(self, product_name):
        return self.__CART_FORM.get_by_role(
            "link", name=product_name, exact=True
        )

    def set_quantity(self, quantity):
        self.__wait_for_live_component_ready()
        self.__QUANTITY_FIELD.fill(str(quantity))

    def __get_product_row(self, product_name):
        return self.__CART_FORM.locator("tbody tr").filter(has_text=product_name)

    def get_total_price(self, product_name):
        product_row = self.__get_product_row(product_name)
        return product_row.locator("td").nth(5)

    def get_current_quantity(self):
        return self.__QUANTITY_FIELD

    def remove_product(self, product_name):
        self.__wait_for_live_component_ready()
        product_row = self.__get_product_row(product_name)
        remove_button = product_row.locator('[data-live-action-param="removeItem"]')
        remove_button.click()

    def get_empty_cart_message(self):
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
