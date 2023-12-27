from datetime import datetime
from typing import Any


class CreateVacancies:

    def __init__(self, response):
        self.response = response

    def create_hh_vacancies(self) -> Any:
        hh_list = []
        for vacancies in self.response.get("items"):
            published_at = datetime.strptime(vacancies['published_at'], "%Y-%m-%dT%H:%M:%S%z")
            vacancy_info = {
                'id': vacancies['id'],
                'name': vacancies['name'],
                'solary_ot': vacancies['salary']['from'] if vacancies.get('salary') else None,
                'solary_do': vacancies['salary']['to'] if vacancies.get('salary') else None,
                'responsibility': vacancies['snippet']['responsibility'],
                'data': published_at.strftime("%d.%m.%Y"),
                'link': vacancies['alternate_url'] if vacancies.get('alternate_url') else None}
            hh_list.append(vacancy_info)
        return hh_list

    def create_sj_vacancies(self):
        sj_list = []
        for vacancy in self.response['objects']:
            published_at = datetime.fromtimestamp(vacancy.get('date_published', ''))
            super_job = {
                'id': vacancy['id'],
                'name': vacancy.get('profession', ''),
                'solary_ot': vacancy.get('payment_from', '') if vacancy.get('payment_from') else None,
                'solary_do': vacancy.get('payment_to') if vacancy.get('payment_to') else None,
                'responsibility': vacancy.get('candidat').replace('\n', '').replace('•', '')
                if vacancy.get('candidat') else None,
                'data': published_at.strftime("%d.%m.%Y"),
                'link': vacancy.get('link') if vacancy.get('link') else None}
            sj_list.append(super_job)
        return sj_list

    @staticmethod
    def top_vacancies(self, vacancy):
        top_5_vacancies = sorted(vacancy, key=lambda x: x.get('salary', {}).get('from', 0), reverse=True)[:5]
        return top_5_vacancies
