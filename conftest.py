import pytest
import allure
import os

from http import HTTPStatus
from config.config_reader import ConfigReader
from utils.api_client import ApiClient
from test_data.api_data import PRODUCT_CODE
from pages.product_page import ProductPage

@pytest.fixture(scope="session")
def api_client():
    base_url = ConfigReader.get_api_base_url()
    return ApiClient(base_url)

@pytest.fixture
def cart_token(api_client):
    payload = {
        "channelCode": "WEB",
        "localeCode": "en_US",
    }
    response = api_client.post("shop/orders", payload)
    assert response.status_code == HTTPStatus.CREATED

    response_body = response.json()
    return response_body["tokenValue"]

@pytest.fixture(scope="session")
def default_product_variant(api_client):
    response = api_client.get(f"shop/products/{PRODUCT_CODE}")
    assert response.status_code == HTTPStatus.OK

    response_body = response.json()
    return response_body["defaultVariant"]

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")

        if page and not page.is_closed():
            try:
                allure.attach(
                    page.screenshot(),
                    name="failure-screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception:
                pass

            try:
                allure.attach(
                    page.url,
                    name="failure-url",
                    attachment_type=allure.attachment_type.TEXT
                )
            except Exception:
                pass

            try:
                allure.attach(
                    page.content(),
                    name="failure-page-source",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception:
                pass

@pytest.fixture
def product_page(page):
    return ProductPage(page)

@pytest.fixture
def radiant_product_page(product_page):
    response = product_page.open_product("radiant-reflection-cap")
    if response is None or response.status >= 500:
        pytest.skip("External Sylius product page is unavailable")
    return product_page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    context_args = {
        **browser_context_args
    }

    if os.getenv("DEMO_MODE") == "1":
        context_args["viewport"] = {
            "width": 1280,
            "height": 720
        }

        context_args["record_video_size"] = {
            "width": 1280,
            "height": 720
        }

    return context_args