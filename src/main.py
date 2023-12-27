import json
from pprint import pprint

from src.api.class_api import HeadHunterAPI, SuperJobAPI
from src.api.setting import JSON_PATH
from src.saver.config import CreateVacancies
from src.saver.saver_json import JSONSaver


def user_interaction() -> None:
    """ Функция для взаимодействия с пользователем """
    while True:
        platforms = input("""Выберете цифру для поиска:
        1 - HeadHunter
        2 - SuperJob
        """)
        vakancy_name = input("""Укажите профессию
        """)
        payment_from = int(input("""Укажите минимальную желаемую сумму зарплаты
        """))
        no_agreement = int(input("""Нужно ли выводить вакансии без указания заработной платы (По договоренности)?
        1 - Нет
        2 - Да
        """))
        sorting = input("""Укажите сортировку: Дата/Зарплата
        """).lower()

        if platforms == '1':
            if sorting == "дата":
                sorting = 'publication_time'
            else:
                sorting = 'salary_desc'
            activation_class = HeadHunterAPI(vakancy_name, sorting, payment_from, no_agreement)
            sending_request = activation_class.get_vacancies()
            creation_of_vacancies = CreateVacancies(sending_request)
            vacancy_data = creation_of_vacancies.create_hh_vacancies()
        else:
            if sorting == "дата":
                sorting = 'date'
            else:
                sorting = 'payment'
            activation_class = SuperJobAPI(vakancy_name, sorting, payment_from, no_agreement)
            sending_request = activation_class.get_vacancies()
            creation_of_vacancies = CreateVacancies(sending_request)
            vacancy_data = creation_of_vacancies.create_sj_vacancies()

        activating_class_for_record = JSONSaver(vacancy_data)

        data_status = input("""Выберите действие:
        1. Создать новый файл
        2. Дополнить прежний (при условии уже выполненого ранее 1 пункта)
        """)
        if data_status == '1':
            activating_class_for_record.save_vacancy()
            print("Файл создан успешно")
        else:
            activating_class_for_record.add_vacancy()
            print("Файл дополнен успешно")
        while True:
            choice_to_delete = input('''Хотите удалить какую-либо вакансию из файла? Да/Нет
            ''').lower()
            if choice_to_delete == "да":
                vacancy_for_removal = input("""Введите id вакансии для удаления
                """)
                activating_class_for_record.delete_vacancy(vacancy_for_removal)
                print("Успешно удалено")
            else:
                break
        continuation_of_the_cycle = input("""Хотите повторно сформировать список подходящих вакансий? Да/Нет
        """).lower()
        if continuation_of_the_cycle == "нет":
            break
    selecting_console_output = input("""Вывести топ-5 вакансии по заработной плате в консоль? Да/Нет
    """).lower()
    if selecting_console_output == "да":
        with open(JSON_PATH, 'r', encoding='utf-8') as file:
            data = json.load(file)
            pprint(CreateVacancies(data).top_vacancies(data, data))


if __name__ == "__main__":
    user_interaction()