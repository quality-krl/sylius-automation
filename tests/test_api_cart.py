import pytest
import allure
from http import HTTPStatus

from test_data.api_data import (NON_EXISTING_VARIANT, NON_EXISTING_ITEM_ID)

@allure.feature("Cart API")
class TestCartApi:
    @allure.story("Cart item lifecycle")
    @allure.title("Create, update and delete a cart item successfully")
    def test_cart_item_crud_flow(self, api_client, cart_token, default_product_variant):
        endpoint = f"shop/orders/{cart_token}"
        get_response = api_client.get(endpoint)
        assert get_response.status_code == HTTPStatus.OK

        get_body = get_response.json()
        assert get_body["tokenValue"] == cart_token

        items_endpoint = f"shop/orders/{cart_token}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        updated_cart_response = api_client.get(endpoint)
        assert updated_cart_response.status_code == HTTPStatus.OK

        updated_cart_body = updated_cart_response.json()
        items = updated_cart_body["items"]
        assert len(items) == 1

        item = items[0]
        assert item["quantity"] == 1
        assert item["variant"] == default_product_variant

        item_endpoint = f"shop/orders/{cart_token}/items/{item['id']}"
        update_payload = {
            "quantity": 2
        }
        update_response = api_client.patch(item_endpoint, update_payload)
        assert update_response.status_code == HTTPStatus.OK

        verified_cart_response = api_client.get(endpoint)
        assert verified_cart_response.status_code == HTTPStatus.OK

        verified_cart_body = verified_cart_response.json()
        verified_items = verified_cart_body["items"]
        assert len(verified_items) == 1
        assert verified_items[0]["quantity"] == 2

        delete_response = api_client.delete(item_endpoint)
        assert delete_response.status_code == HTTPStatus.NO_CONTENT

        final_cart_response = api_client.get(endpoint)
        assert final_cart_response.status_code == HTTPStatus.OK

        final_cart_body = final_cart_response.json()
        final_items = final_cart_body["items"]
        assert len(final_items) == 0

    @allure.story("Cart validation")
    @allure.title("Reject invalid cart item quantity: {invalid_quantity}")
    @pytest.mark.parametrize("invalid_quantity",
    [
        0,
        10000
    ]
    )
    def test_add_item_with_invalid_quantity(self, api_client, cart_token, default_product_variant, invalid_quantity):
        items_endpoint = f"shop/orders/{cart_token}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": invalid_quantity
        }
        item_response = api_client.post(items_endpoint, item_payload)
        error_body = item_response.json()
        assert item_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["violations"][0]["propertyPath"] == "quantity"
        assert error_body["violations"][0]["message"] == "Quantity must be between 1 and 9999."

        cart_response = api_client.get(f"shop/orders/{cart_token}")
        assert cart_response.status_code == HTTPStatus.OK

        cart_body = cart_response.json()
        items = cart_body["items"]
        assert len(items) == 0

    @allure.story("Cart validation")
    @allure.title("Reject a non-existing product variant")
    def test_add_non_existing_variant(self, api_client, cart_token):
        items_endpoint = f"shop/orders/{cart_token}/items"
        item_payload = {
            "productVariant": NON_EXISTING_VARIANT,
            "quantity": 1
        }
        item_response = api_client.post(
            items_endpoint,
            item_payload
        )
        error_body = item_response.json()
        assert item_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["violations"][0]["message"] == ("The product variant THIS_VARIANT_DOES_NOT_EXIST does not exist.")

        cart_response = api_client.get(
            f"shop/orders/{cart_token}"
        )
        assert cart_response.status_code == HTTPStatus.OK
        cart_body = cart_response.json()
        assert len(cart_body["items"]) == 0

    @allure.story("Cart validation")
    @allure.title("Reject invalid quantity when updating a cart item")
    def test_update_item_with_invalid_quantity(self, api_client, cart_token, default_product_variant):
        cart_endpoint = f"shop/orders/{cart_token}"
        items_endpoint = f"shop/orders/{cart_token}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        cart_after_add_response = api_client.get(cart_endpoint)
        assert cart_after_add_response.status_code == HTTPStatus.OK

        cart_after_add_body = cart_after_add_response.json()
        items = cart_after_add_body["items"]
        assert len(items) == 1
        assert items[0]["quantity"] == 1

        item = items[0]
        item_endpoint = (
            f"shop/orders/{cart_token}/items/{item['id']}"
        )
        update_payload = {
            "quantity": 0
        }
        update_response = api_client.patch(
            item_endpoint,
            update_payload
        )
        error_body = update_response.json()
        assert update_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["violations"][0]["propertyPath"] == "quantity"
        assert error_body["violations"][0]["message"] == ("Quantity must be between 1 and 9999.")

        verify_response = api_client.get(cart_endpoint)
        assert verify_response.status_code == HTTPStatus.OK

        verify_body = verify_response.json()
        verify_items = verify_body["items"]
        assert len(verify_items) == 1
        assert verify_items[0]["quantity"] == 1

    @allure.story("Cart item deletion")
    @allure.title("Return 404 when deleting a non-existing cart item")
    def test_delete_non_existing_item(self, api_client, cart_token):
        item_endpoint = (f"shop/orders/{cart_token}/items/{NON_EXISTING_ITEM_ID}")
        delete_response = api_client.delete(item_endpoint)

        error_body = delete_response.json()
        assert delete_response.status_code == HTTPStatus.NOT_FOUND
        assert error_body["status"] == HTTPStatus.NOT_FOUND
        assert error_body["detail"] == "Not Found"

    @allure.story("Cart validation")
    @allure.title("Reject cart item request without a product variant")
    def test_add_item_without_product_variant(self, api_client, cart_token):
        items_endpoint = f"shop/orders/{cart_token}/items"
        item_payload = {
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        error_body = item_response.json()
        assert item_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["status"] == HTTPStatus.UNPROCESSABLE_ENTITY
        assert error_body["detail"] == ("Request does not have the following required fields specified: productVariant.")

        verify_response = api_client.get(f"shop/orders/{cart_token}")
        assert verify_response.status_code == HTTPStatus.OK

        verify_body = verify_response.json()
        assert len(verify_body["items"]) == 0