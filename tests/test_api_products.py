import pytest
import allure
from http import HTTPStatus

from test_data.api_data import PRODUCT_CODE, PRODUCT_NAME, NON_EXISTING_PRODUCT_CODE

@allure.feature("Products API")
class TestProductsApi:
    @allure.story("Product retrieval")
    @allure.title("Get products collection successfully")
    def test_get_products(self, api_client):
        response = api_client.get("shop/products")
        assert response.status_code == HTTPStatus.OK

        response_body = response.json()
        products = response_body["hydra:member"]
        assert len(products) > 0

        first_product = products[0]
        assert "name" in first_product
        assert "code" in first_product
        assert len(first_product["name"]) > 0
        assert len(first_product["code"]) > 0

        product_code = first_product["code"]
        endpoint = f"shop/products/{product_code}"
        product_response = api_client.get(endpoint)
        assert product_response.status_code == HTTPStatus.OK

        product_body = product_response.json()
        assert product_body["code"] == product_code
        assert "defaultVariantData" in product_body

        variant_data = product_body["defaultVariantData"]
        assert "price" in variant_data
        assert "inStock" in variant_data

    @allure.story("Product retrieval")
    @allure.title("Return 404 for a non-existing product")
    def test_get_non_existing_product(self, api_client):
        response = api_client.get(f"shop/products/{NON_EXISTING_PRODUCT_CODE}")
        assert response.status_code == HTTPStatus.NOT_FOUND

        error_body = response.json()
        assert error_body["status"] == HTTPStatus.NOT_FOUND
        assert error_body["detail"] == "Not Found"

    @allure.story("Product retrieval")
    @allure.title("Get a product by code successfully")
    def test_get_product_by_code(self, api_client):
        product_code = PRODUCT_CODE
        endpoint = f"shop/products/{product_code}"
        response = api_client.get(endpoint)
        assert response.status_code == HTTPStatus.OK

        product_body = response.json()
        assert product_body["code"] == product_code
        assert "name" in product_body
        assert len(product_body["name"]) > 0

    @allure.story("Pagination")
    @allure.title("Get the second page of products successfully")
    def test_get_products_with_query_params(self, api_client):
        params = {"page": 2}
        response = api_client.get("shop/products", params=params)
        response_body = response.json()

        assert response.status_code == HTTPStatus.OK
        assert response_body["hydra:view"]["@id"] == "/api/v2/shop/products?page=2"
        assert len(response_body["hydra:member"]) > 0
        assert response_body["hydra:view"]["hydra:previous"] == "/api/v2/shop/products?page=1"
        assert response_body["hydra:view"]["hydra:next"] == "/api/v2/shop/products?page=3"

    @allure.story("Filtering")
    @allure.title("Filter products by name successfully")
    def test_filter_products_by_name(self, api_client):
        params = {
            "translations.name": PRODUCT_NAME
        }
        response = api_client.get("shop/products", params=params)
        assert response.status_code == HTTPStatus.OK

        response_body = response.json()
        products = response_body["hydra:member"]
        assert len(products) > 0

        for product in products:
            assert product["name"] == PRODUCT_NAME

    @allure.story("HTTP behavior")
    @allure.title("Return JSON-LD content type for products endpoint")
    def test_products_response_content_type(self, api_client):
        response = api_client.get("shop/products")
        assert response.status_code == HTTPStatus.OK
        assert response.headers["Content-Type"].startswith("application/ld+json")

    @allure.story("HTTP behavior")
    @allure.title("Return a successful HEAD response for products endpoint")
    def test_products_head_request(self, api_client):
        response = api_client.head("shop/products")
        assert response.status_code == HTTPStatus.OK
        assert response.text == ""

    @allure.story("HTTP behavior")
    @allure.title("Return supported methods for products endpoint")
    def test_products_options_request(self, api_client):
        response = api_client.options("shop/products")
        assert response.status_code == HTTPStatus.NO_CONTENT
        assert "Access-Control-Allow-Methods" in response.headers

        allowed_methods = response.headers["Access-Control-Allow-Methods"]
        assert "GET" in allowed_methods
        assert "OPTIONS" in allowed_methods

    @allure.story("HTTP behavior")
    @allure.title("Return supported methods for products endpoint")
    def test_get_products_out_of_range_page(self, api_client):
        params = {"page": 999}
        response = api_client.get("shop/products", params=params)

        response_body = response.json()
        products = response_body["hydra:member"]
        assert response.status_code == HTTPStatus.OK
        assert len(products) == 0

    @pytest.mark.parametrize ("invalid_page",
    [
        0,
        "abc"
    ]
    )
    @allure.story("Pagination")
    @allure.title("Reject an invalid page's value: {invalid_page}")
    def test_get_products_invalid_page(self, api_client, invalid_page):
        params = {"page": invalid_page}
        response = api_client.get("shop/products", params=params)

        error_body = response.json()
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert error_body["status"] == HTTPStatus.BAD_REQUEST
        assert error_body["detail"] == "Page should not be less than 1"

    @pytest.mark.parametrize ("sort_order,reverse",
    [
        ("asc", False),
        ("desc", True)
    ]
    )
    @allure.story("Sorting")
    @allure.title("Sort products by price: {sort_order}")
    def test_sort_products_by_price(self, api_client, sort_order, reverse):
        params = {"order[price]": sort_order}
        response = api_client.get("shop/products", params=params)
        assert response.status_code == HTTPStatus.OK

        response_body = response.json()
        products = response_body["hydra:member"]
        prices = [
            product["defaultVariantData"]["price"]
            for product in products
        ]
        assert prices == sorted(prices, reverse=reverse)

    @allure.story("Pagination and sorting")
    @allure.title("Paginate products while sorting by price")
    def test_paginate_and_sort_products(self, api_client):
        params = {
            "page": 1,
            "order[price]": "desc"
        }
        response = api_client.get("shop/products", params=params)
        assert response.status_code == HTTPStatus.OK

        response_body = response.json()
        assert "page=1" in response_body["hydra:view"]["@id"]

        products = response_body["hydra:member"]
        prices = [
            product["defaultVariantData"]["price"]
            for product in products
        ]
        assert prices == sorted(prices, reverse=True)

    @allure.story("Filtering")
    @allure.title("Return an empty collection when a product's name does not exist")
    def test_filter_products_by_non_existing_name(self, api_client):
        params = {
            "translations.name": "This Product Does Not Exist"
        }
        response = api_client.get("shop/products", params=params)
        response_body = response.json()
        products = response_body["hydra:member"]
        assert response.status_code == HTTPStatus.OK
        assert len(products) == 0

    @allure.story("Sorting")
    @allure.title("Ignore invalid sorting direction and use default order")
    def test_sort_products_invalid_direction(self, api_client):
        params = {
            "order[price]": "sideways"
        }
        response = api_client.get("shop/products", params=params)
        response_body = response.json()
        products = response_body["hydra:member"]

        prices = [
            product["defaultVariantData"]["price"]
            for product in products
        ]

        default_response = api_client.get("shop/products")
        default_response_body = default_response.json()
        default_products = default_response_body["hydra:member"]
        default_prices = [
            product["defaultVariantData"]["price"]
            for product in default_products
        ]
        assert response.status_code == HTTPStatus.OK
        assert prices == default_prices