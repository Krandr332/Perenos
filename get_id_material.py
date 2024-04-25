import os
import time
import requests
import csv
import json
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

class API:
    def __init__(self, login: str, password: str, api_headers: dict):
        self.base_url = ''
        self.auth_token = self.auth(login, password, api_headers)
        print(f": {self.auth_token}")

    def auth(self, login, password, api_headers):
        auth_data = {
            "username": login,
            "password": password
        }
        token = requests.post(self.base_url + "auth/obtain/", headers=api_headers, data=auth_data).json()
        token = {"Authorization": "Bearer " + token['access']}
        return token

    def get(self, table_name, params=None):
        response = requests.get(self.base_url + table_name, headers=self.auth_token, params=params)
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as err:
            print(f"HTTP error occurred: {err}")
            return None

    def post(self, url, data=None, files=None):
        response = requests.post(url, headers=self.auth_token, data=data, files=files)
        return response

url = ''
session_id = ''

api_headers = {
    'accept': 'application/json',
    'X-CSRFTOKEN': '',
    'Cookie': f'',
}

umschool_api = UmschoolAPI(login="", password="", api_headers=api_headers)

responses = []

with open('result_file.csv', 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader, None)
    number = 0

    for row in csv_reader:
        id_value = row[0]
        print(f"Обрабатывается строка с ID: {id_value}")

        title_value = row[2]
        type_value = 'WORKBOOK' if 'рабочая тетрадь' in row[1].lower() else 'SUMMARY'

        params = {
            'title': title_value,
            'type': type_value,
        }

        response = umschool_api.get('materials/', params=params)

        if response:
            responses.append(response)
        else:
            print(f"Не удалось выполнить GET-запрос для строки с ID {id_value}")

        print(f"Строка с ID {id_value} обработана")


with open('responses.json', 'w', encoding='utf-8') as json_file:
    json.dump(responses, json_file, ensure_ascii=False, indent=2)

print("Сохранено в responses.json")
