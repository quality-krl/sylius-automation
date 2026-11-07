import pytest
import allure

from http import HTTPStatus
from config.config_reader import ConfigReader
from utils.api_client import ApiClient
from test_data.api_data import PRODUCT_CODE

@pytest.fixture(scope="session")
def api_client():
    base_url = ConfigReader.get_api_base_url()
    return ApiClient(base_url)

@pytest.fixture
def cart_token(api_client):
    payload = {
        "channelCode": "WEB",
        "localeCode": "en_US"
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
        if page:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG
            )
            allure.attach(
                page.url,
                name="failure_url",
                attachment_type=allure.attachment_type.TEXT
            )
            allure.attach(
                page.content(),
                name="failure_page_source",
                attachment_type=allure.attachment_type.HTML
            )