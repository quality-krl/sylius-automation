import pytest

from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.config_reader import ConfigReader
from playwright.sync_api import expect

class TestLoginPage:
    def test_login_valid(self, page):
        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)

        username = ConfigReader.get_username()
        password = ConfigReader.get_password()

        login_page.login(username, password)

        expect(home_page.get_logout_button()).to_be_visible()

    def test_login_invalid_password(self, page):
        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)

        username = ConfigReader.get_username()
        invalid_password = ConfigReader.get_invalid_password()

        login_page.login(username, invalid_password)

        error_message = login_page.get_error_message().lower()
        assert "invalid credentials" in error_message

    @pytest.mark.parametrize("username,password",
        [
            ("wrong@example.com", "sylius"),
            ("shop@example.com", "wrongpass")
        ]
    )
    def test_login_invalid_credentials(self, page, username, password):
        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)

        login_page.login(username, password)


