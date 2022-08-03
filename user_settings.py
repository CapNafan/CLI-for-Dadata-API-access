# -*- coding: utf-8 -*-
import sqlite3
import validators


SUPPORTED_LOCALES = ['en', 'ru']


class UserSettings:
    def __init__(self):
        self._db = sqlite3.connect('user_settings.db')
        self._cursor = self._db.cursor()
        self.language = None
        self.base_url = None
        self.key = None
        self.secret = None

    def _alter_db(self, column: str, value: str) -> None:
        self.column = column
        self.value = value
        if self.get_user_settings():
            self._cursor.execute(f"UPDATE settings SET {self.column} = ?", (self.value, ))
        else:
            self._cursor.execute(f"INSERT INTO settings ({self.column}) VALUES ('{self.value}')")
        self._db.commit()

    def _validate_key(self, key: str) -> bool:
        self.key = key
        return len(self.key) == 40 and self.key.isalnum()

    def create_table(self):
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS settings (
                        language TEXT,
                        base_url TEXT,
                        API_key TEXT,
                        secret_key TEXT)""")
        self._db.commit()

    @staticmethod
    def validate_language(language: str) -> bool:
        return language in SUPPORTED_LOCALES

    def validate_base_url(self, url: str) -> bool:
        self.base_url = url
        return bool(validators.url(self.base_url))

    def validate_api_key(self, api_key: str) -> bool:
        return self._validate_key(api_key)

    def validate_secret(self, secret: str) -> bool:
        return self._validate_key(secret)

    def change_suggestion_language(self, language: str) -> None:
        self.language = language
        self._alter_db('language', self.language)

    def change_base_url(self, base_url) -> None:
        self.base_url = base_url
        self._alter_db('base_url', self.base_url)

    def change_api_key(self, api_key: str) -> None:
        self.key = api_key
        self._alter_db('API_key', self.key)

    def change_secret_key(self, secret: str) -> None:
        self.secret = secret
        self._alter_db('secret_key', self.secret)

    def get_user_settings(self) -> tuple:
        self._cursor.execute("SELECT * FROM settings")
        return self._cursor.fetchone()
