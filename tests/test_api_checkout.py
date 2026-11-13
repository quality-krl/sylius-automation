import pytest
from http import HTTPStatus


class TestCheckoutApi:
    def test_select_shipping_and_payment(self, api_client, cart_token, default_product_variant):
        order_endpoint = f"shop/orders/{cart_token}"
        items_endpoint = f"{order_endpoint}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        cart_response = api_client.get(order_endpoint)
        assert cart_response.status_code == HTTPStatus.OK

        address_payload = {
            "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            },
            "billingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            }
        }
        address_response = api_client.put(order_endpoint, address_payload)
        assert address_response.status_code == HTTPStatus.OK

        address_body = address_response.json()
        assert address_body["checkoutState"] == "addressed"
        assert address_body["shippingAddress"]["firstName"] == "John"
        assert address_body["shippingAddress"]["countryCode"] == "US"
        assert address_body["billingAddress"]["firstName"] == "John"
        assert address_body["billingAddress"]["countryCode"] == "US"

        shipment = address_body["shipments"][0]
        shipment_id = shipment["id"]
        shipping_method = shipment["method"]
        shipment_endpoint = f"shop/orders/{cart_token}/shipments/{shipment_id}"
        shipping_payload = {
            "shippingMethod": shipping_method
        }
        shipping_response = api_client.patch(shipment_endpoint, shipping_payload)
        assert shipping_response.status_code == HTTPStatus.OK

        shipping_body = shipping_response.json()
        assert shipping_body["checkoutState"] == "shipping_selected"

        payment = shipping_body["payments"][0]
        payment_id = payment["id"]
        payment_method = payment["method"]
        payment_endpoint = f"shop/orders/{cart_token}/payments/{payment_id}"
        payment_payload = {
            "paymentMethod": payment_method
        }
        payment_response = api_client.patch(payment_endpoint, payment_payload)
        assert payment_response.status_code == HTTPStatus.OK

        payment_body = payment_response.json()
        assert payment_body["checkoutState"] == "payment_selected"

    def test_invalid_shipping_method(self, api_client, cart_token, default_product_variant):
        order_endpoint = f"shop/orders/{cart_token}"
        items_endpoint = f"{order_endpoint}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        address_payload = {
            "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            },
            "billingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            }
        }
        address_response = api_client.put(order_endpoint, address_payload)
        assert address_response.status_code == HTTPStatus.OK

        address_body = address_response.json()
        shipment = address_body["shipments"][0]
        shipment_id = shipment["id"]
        shipment_endpoint = f"{order_endpoint}/shipments/{shipment_id}"
        shipping_payload = {
            "shippingMethod": "/api/v2/shop/shipping-methods/invalid_method"
        }
        shipping_response = api_client.patch(shipment_endpoint, shipping_payload)
        assert shipping_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    @pytest.mark.xfail(
        reason="Sylius returns 500 instead of a controlled 4xx response when payment is selected before shipping",
        strict=False
    )
    def test_cannot_select_payment_before_shipping(self, api_client, cart_token, default_product_variant):
        order_endpoint = f"shop/orders/{cart_token}"
        items_endpoint = f"{order_endpoint}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        address_payload = {
            "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            },
            "billingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            }
        }
        address_response = api_client.put(order_endpoint, address_payload)
        assert address_response.status_code == HTTPStatus.OK

        address_body = address_response.json()
        payment = address_body["payments"][0]
        payment_id = payment["id"]
        payment_method = payment["method"]
        payment_endpoint = f"{order_endpoint}/payments/{payment_id}"
        payment_payload = {
            "paymentMethod": payment_method
        }
        payment_response = api_client.patch(payment_endpoint, payment_payload)
        assert payment_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_invalid_payment_method(self, api_client, cart_token, default_product_variant):
        order_endpoint = f"shop/orders/{cart_token}"
        items_endpoint = f"{order_endpoint}/items"
        item_payload = {
            "productVariant": default_product_variant,
            "quantity": 1
        }
        item_response = api_client.post(items_endpoint, item_payload)
        assert item_response.status_code == HTTPStatus.CREATED

        address_payload = {
            "shippingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            },
            "billingAddress": {
                "firstName": "John",
                "lastName": "Doe",
                "countryCode": "US",
                "street": "123 Main Street",
                "city": "New York",
                "postcode": "10001"
            }
        }
        address_response = api_client.put(order_endpoint, address_payload)
        assert address_response.status_code == HTTPStatus.OK

        address_body = address_response.json()
        shipment = address_body["shipments"][0]
        shipment_id = shipment["id"]
        shipping_method = shipment["method"]

        shipment_endpoint = f"{order_endpoint}/shipments/{shipment_id}"
        shipping_payload = {
            "shippingMethod": shipping_method
        }

        shipping_response = api_client.patch(shipment_endpoint, shipping_payload)
        assert shipping_response.status_code == HTTPStatus.OK

        shipping_body = shipping_response.json()
        payment = shipping_body["payments"][0]
        payment_id = payment["id"]
        payment_endpoint = f"{order_endpoint}/payments/{payment_id}"
        payment_payload = {"paymentMethod": "/api/v2/shop/payment-methods/invalid_method"}
        payment_response = api_client.patch(payment_endpoint, payment_payload)
        assert payment_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY