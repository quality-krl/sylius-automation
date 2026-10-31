import pytest

from pages import home_page
from pages.home_page import HomePage
from pages.login_page import LoginPage
from config.config_reader import ConfigReader
from playwright.sync_api import expect
from test_data.login_data import INVALID_USERNAME, INVALID_PASSWORD

class TestLoginPage:
    # Positive tests
    @pytest.mark.parametrize("username",
    [
        ConfigReader.get_username(),
        f" {ConfigReader.get_username()}",
        f"{ConfigReader.get_username()} ",
        (ConfigReader.get_username().upper())
    ],
    ids=[
        "valid_username",
        "leading_space",
        "trailing_space",
        "uppercase_username"
    ]
    )
    def test_login_valid(self, page, username):
        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)

        password = ConfigReader.get_password()

        login_page.login(username, password)

        expect(home_page.get_logout_button()).to_be_visible()

    # Negative tests
    @pytest.mark.parametrize("username,password",
        [
            (INVALID_USERNAME, ConfigReader.get_password()),
            (ConfigReader.get_username(), INVALID_PASSWORD),
            (ConfigReader.get_username(), ""),
            ("", ConfigReader.get_password()),
            ("", ""),
            (ConfigReader.get_username(), f" {ConfigReader.get_password()}"),
            (ConfigReader.get_username(), f"{ConfigReader.get_password()} ")
        ],
        ids=[
            "invalid_username",
            "invalid_password",
            "empty_password",
            "empty_username",
            "empty_both",
            "leading_space_password",
            "trailing_space_password"
        ]
    )
    def test_login_invalid_credentials(self, page, username, password):
        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)
        login_page.login(username, password)

        expect(login_page.get_error_message()).to_contain_text("Invalid")

    def test_logout(self, page):
        username = ConfigReader.get_username()
        password = ConfigReader.get_password()

        home_page = HomePage(page)

        home_page.open()
        home_page.open_login()

        login_page = LoginPage(page)
        login_page.login(username, password)

        expect(home_page.get_logout_button()).to_be_visible()

        home_page.logout()

        expect(home_page.get_login_button()).to_be_visible()



