import json
import os
from abc import ABC, abstractmethod

from src.api.setting import JSON_PATH


class Save(ABC):

    @abstractmethod
    def save_vacancy(self):
        """
        Добавление вакансий в файл
        """
        raise NotImplementedError

    def delete_vacancy(self, query):
        """
        Удаление данных из файла
        """
        raise NotImplementedError

    def add_vacancy(self):
        """
        Добавление вакансий в существующий файл
        """
        raise NotImplementedError


class JSONSaver(Save):

    def __init__(self, list_):
        self.lict_ = list_

    def save_vacancy(self):
        with open(JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(self.lict_, file)

    def delete_vacancy(self, query):
        initial_data = json.load(open(JSON_PATH, encoding='utf-8'))
        new_list = [vacancy for vacancy in initial_data if vacancy.get('id') != query]
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(new_list, file, ensure_ascii=False, indent=2)

    def add_vacancy(self):
        initial_data = json.load(open(JSON_PATH, encoding='utf-8'))
        new_list = initial_data + self.lict_
        with open(JSON_PATH, 'w', encoding='utf-8') as file:
            json.dump(new_list, file, ensure_ascii=False, indent=2)









