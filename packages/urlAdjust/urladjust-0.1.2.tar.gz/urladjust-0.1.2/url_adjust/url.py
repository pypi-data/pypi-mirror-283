from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import re

class Url:
    def __init__(self, url_str):
        parsed_url = urlparse(url_str)

        self.scheme = parsed_url.scheme
        self.netloc = parsed_url.netloc
        self.path = parsed_url.path
        self.params = parsed_url.params
        # will need to use ``urllib.parse.urlencode(self.query_params, doseq=True)``
        # to get new query string when reconstructing the url
        self.query_params = parse_qs(parsed_url.query)
        self.fragment = parsed_url.fragment

    def __str__(self):
        new_query_string = urlencode(self.query_params, doseq=True)
        new_url_str = urlunparse((self.scheme, self.netloc, self.path, self.params, new_query_string, self.fragment))
        return new_url_str

    def add_or_update_query_param(self, key, value):
        self.query_params[key] = value

    def update_all_query_params_matching(self, regex_key: str, higher_order_func: callable) -> None:
        for k, v in self.query_params.items():
            if re.fullmatch(regex_key, k):
                self.query_params[k] = higher_order_func(k, v)

    def remove_query_param(self, key: str) -> None:
        self.query_params.pop(key, None)

    def remove_all_query_params(self) -> None:
        self.query_params.clear()

    def remove_all_query_params_except(self, keys: list[str]) -> None:
        self.query_params = {k: v for k, v in self.query_params.items() if k in keys}

    def remove_all_query_params_matching(self, regex_key: str) -> None:
        self.query_params = {k: v for k, v in self.query_params.items() if not re.fullmatch(regex_key, k)}

    def remove_all_query_params_not_matching(self, regex_key: str) -> None:
        self.query_params = {k: v for k, v in self.query_params.items() if re.fullmatch(regex_key, k)}

    def get_query_param(self, key: str) -> str:
        return self.query_params[key][0]

    def get_all_query_params(self) -> dict[str, str]:
        result = {}
        for k, v in self.query_params.items():
            result[k] = v[0]
        return result