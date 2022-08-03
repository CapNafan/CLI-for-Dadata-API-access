# -*- coding: utf-8 -*-
from typing import List, Dict
from dadata import Dadata
from user_settings import UserSettings


class Client:
    def __init__(self, parser_arguments):
        self.language = parser_arguments.language
        self.base_url = parser_arguments.base_url
        self.key = parser_arguments.key
        self.secret = parser_arguments.secret
        self.suggestions = None
        self.info = None

    def get_suggestions(self,
                        address: str,
                        api_key: str,
                        secret_key: str,
                        language: str = 'ru') -> List[Dict] or bool:

        with Dadata(api_key, secret_key) as dadata:
            self.suggestions = dadata.suggest(name="address", query=address, language=language)

            if self.suggestions:
                for index, suggestion in enumerate(self.suggestions):
                    print(index + 1, ') ', suggestion['value'], sep='')
                return self.suggestions
            else:
                print("No suggestions found")
                return self.suggestions

    def get_coordinates(self,
                        address: str,
                        api_key: str,
                        secret_key: str) -> tuple:

        with Dadata(api_key, secret_key) as dadata:
            self.info = dadata.clean(name='address', source=f'{address}')
            return self.info['source'], self.info['geo_lat'], self.info['geo_lon']

    def check_settings(self, settings: UserSettings) -> None:

        settings.change_base_url("https://cleaner.dadata.ru/api/v1/")  # default base url

        if self.language:
            if settings.validate_language(self.language):
                settings.change_suggestion_language(self.language)
            else:
                print(f"Language {self.language} not supported. Default language is ru")
        else:
            if not settings.get_user_settings()[0]:        # if there is no language settings in DB:
                settings.change_suggestion_language('ru')  # set default suggestions language

        if self.base_url and settings.validate_base_url(self.base_url):
            settings.change_base_url(self.base_url)
        else:
            if not settings.get_user_settings()[1]:          # if there is no base url settings in DB:
                settings.change_base_url("https://cleaner.dadata.ru/api/v1/")  # set default base url

        if self.key:
            if settings.validate_api_key(self.key):
                settings.change_api_key(self.key)
            else:
                raise ValueError

        if self.secret:
            if settings.validate_secret(self.secret):
                settings.change_secret_key(self.secret)
            else:
                raise ValueError
