import requests

class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.timeout = 10
        self.headers = {
            "Accept": "application/ld+json",
            "Content-Type": "application/ld+json"
        }

    def get(self, endpoint, params=None):
        get_response = requests.get(self.__build_url(endpoint), params=params, timeout=self.timeout)
        return get_response

    def post(self, endpoint, payload):
        post_response = requests.post(self.__build_url(endpoint), json=payload, headers=self.headers, timeout=self.timeout)
        return post_response

    def delete(self, endpoint):
        delete_response = requests.delete(self.__build_url(endpoint), headers=self.headers, timeout=self.timeout)
        return delete_response

    def put(self, endpoint, payload):
        put_response = requests.put(self.__build_url(endpoint), json=payload, headers=self.headers, timeout=self.timeout)
        return put_response

    def head(self, endpoint):
        head_response = requests.head(self.__build_url(endpoint), timeout=self.timeout)
        return head_response

    def options(self, endpoint):
        options_response = requests.options(self.__build_url(endpoint), timeout=self.timeout)
        return options_response

    def __build_url(self, endpoint):
        return f"{self.base_url}/{endpoint}"

    def patch(self, endpoint, payload):
        patch_headers = {
            "Accept": "application/ld+json",
            "Content-Type": "application/merge-patch+json"
        }
        patch_response = requests.patch(self.__build_url(endpoint), json=payload, headers=patch_headers, timeout=self.timeout)
        return patch_response