from configparser import ConfigParser

config = ConfigParser()
config.read("config/config.ini")

ui_base_url = config["URLS"]["UI_BASE_URL"]
api_base_url = config["URLS"]["API_BASE_URL"]

username = config["CREDENTIALS"]["USERNAME"]
password = config["CREDENTIALS"]["PASSWORD"]

wrong_password = config["WRONG_PASSWORD"]["WRONG_PASSWORD"]

class ConfigReader:
    @staticmethod
    def get_ui_base_url():
        return ui_base_url

    @staticmethod
    def get_api_base_url():
        return api_base_url

    @staticmethod
    def get_username():
        return username

    @staticmethod
    def get_password():
        return password

    @staticmethod
    def get_invalid_password():
        return wrong_password