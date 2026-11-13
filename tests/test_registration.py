import pytest
from faker import Faker
from playwright.sync_api import expect

from config.config_reader import ConfigReader
from pages.home_page import HomePage
from pages.register_page import RegisterPage
from pages.account_page import AccountPage

fake = Faker()

class TestRegistration:
    def test_register_valid_user(self, page):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = fake.phone_number()

        password = "Test123!"
        verify_password = password

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        account_page = AccountPage(page)
        expect(account_page.get_success_message()).to_contain_text("Thank you for registering.")

    @pytest.mark.parametrize("first_name,last_name,email,error_field,expected_message",
        [
            ("", fake.last_name(), fake.email(), "first_name", "Please enter your first name."),
            (fake.first_name(), "", fake.email(), "last_name", "Please enter your last name."),
            (fake.first_name(), fake.last_name(), "", "email", "Please enter your email.")
        ],
        ids=
            [
                "first_name_missing",
                "last_name_missing",
                "email_missing"
            ]
    )
    def test_register_required_fields(self,page, first_name, last_name, email, error_field, expected_message):
        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        phone_number = ""
        password = "Test123!"
        verify_password = password
        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)
        if error_field == "first_name":
            error_locator = register_page.get_first_name_error()
        elif error_field == "last_name":
            error_locator = register_page.get_last_name_error()
        elif error_field == "email":
            error_locator = register_page.get_email_error()
        expect(error_locator).to_contain_text(expected_message)

    @pytest.mark.parametrize("first_name,last_name,email,error_field,expected_message",
    [
        ("A", fake.last_name(), fake.email(), "first_name", "First name must be at least 2 characters long."),
        (fake.first_name(), "B", fake.email(), "last_name", "Last name must be at least 2 characters long.")
    ],
    ids=[
        "first_name_under_min_req",
        "last_name_under_min_req"
    ]
    )
    def test_register_name_min_length(self, page, first_name, last_name, email, error_field, expected_message):
        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        phone_number = ""
        password = "Test123!"
        verify_password = password
        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)
        if error_field == "first_name":
            error_locator = register_page.get_first_name_error()
        elif error_field == "last_name":
            error_locator = register_page.get_last_name_error()

        expect(error_locator).to_contain_text(expected_message)

    def test_register_password_required(self, page):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = ""

        password = ""
        verify_password = ""

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        expect(register_page.get_password_error()).to_contain_text("Please enter your password.")

    def test_register_password_min_length(self, page):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = ""
        password = "Aa1"
        verify_password = password

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        expect(register_page.get_password_error()).to_contain_text("Password must be at least 4 characters long.")

    @pytest.mark.parametrize("password,verify_password",
    [
        ("Test12!", "Test1!"),
        ("", "Test12!"),
        ("Test12!", "")
    ],
    ids = [
        "different_passwords",
        "password_empty",
        "verify_password_empty"

    ]
    )
    def test_register_password_mismatch(self, page, password, verify_password):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = ""

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        expect(register_page.get_password_error()).to_contain_text("The entered passwords don't match")

    @pytest.mark.parametrize("email",
    [
        "test",
        "test@",
        "test@.com",
        "test@@gmail.com",
        "@gmail.com"
    ],
    ids = [
        "just_text",
        "text_and_@",
        "no_domain",
        "double_@",
        "empty_address_with_full_domain"
    ]
    )
    def test_register_invalid_email_format(self, page, email):
        first_name = fake.first_name()
        last_name = fake.last_name()
        phone_number = ""
        password = "Test123!"
        verify_password = password

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        expect(register_page.get_email_error()).to_contain_text("This email is invalid.")

    def test_register_password_min_boundary_valid(self, page):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = ""
        password = "Ab1!"
        verify_password = password

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        account_page = AccountPage(page)
        expect(account_page.get_success_message()).to_contain_text("Thank you for registering.")

    def test_register_duplicate_email(self, page):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = ConfigReader.get_username()
        phone_number = ""
        password = ConfigReader.get_password()
        verify_password = password

        home_page = HomePage(page)
        home_page.open()
        home_page.open_register()

        register_page = RegisterPage(page)
        register_page.register_user(first_name, last_name, email, phone_number, password, verify_password)

        expect(register_page.get_email_error()).to_contain_text("This email is already used.")