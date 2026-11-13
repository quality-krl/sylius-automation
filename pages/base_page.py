from config.config_reader import ConfigReader


class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = ConfigReader.get_ui_base_url()

    def open(self):
        self.page.goto(self.base_url)