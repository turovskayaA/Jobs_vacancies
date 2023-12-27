import os
from typing import Any

import requests

from dotenv import load_dotenv
from abc import ABC, abstractmethod

load_dotenv()


class VacancyAPI(ABC):

    @abstractmethod
    def get_vacancies(self):
        raise NotImplementedError


class Vacancy:

    def __init__(self, name, sorting, salary_from, no_agreement):
        self.name = name
        self.sorting = sorting
        self.salary_from = salary_from
        self.no_agreement = no_agreement

    def __repr__(self) -> str:
        """ Вывод введенной вакансии """
        return f'{self.name}'


class HeadHunterAPI(Vacancy, VacancyAPI):

    def __init__(self, name: str, sorting: Any, payment_from: int, no_agreement: int):
        super().__init__(name, sorting, payment_from, no_agreement)
        self.basic_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self):
        params = {"text": self.name,
                  "order_by": self.sorting,
                  "salary": self.salary_from,
                  "only_with_salary": self.no_agreement,
                  "peg_page": 50}
        response = requests.get(self.basic_url, params=params).json()
        return response


class SuperJobAPI(Vacancy, VacancyAPI):

    def __init__(self, name, sorting, salary_from, no_agreement):
        super().__init__(name, sorting, salary_from, no_agreement)
        self.basic_url = "https://api.superjob.ru/2.0/vacancies"
        self.headers = {"X-Api-App-Id": os.getenv('SECRET_KEY')}

    def get_vacancies(self):
        params = {"keyword": self.name,
                  "order_field": self.sorting,
                  "payment_from": self.salary_from,
                  "no_agreement": self.no_agreement,
                  "count": 50}
        response = requests.get(self.basic_url, headers=self.headers,
                                params=params).json()
        return response
