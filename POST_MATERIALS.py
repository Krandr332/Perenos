import os
import time

import pandas as pd
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

    def get(self, table_name, **kwargs):
        info = requests.get(self.base_url + table_name, headers=self.auth_token, params=kwargs)
        return info

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

pdf_folder = 'PDF'

with open('result_file.csv', 'r', encoding='utf-8-sig') as csv_file:
    csv_reader = csv.reader(csv_file)

    next(csv_reader, None)
    number = 0

    for row in csv_reader:
        try:
            id_value = row[0]
            print(f"Обрабатывается строка с ID: {id_value}")

            title_value = row[2]

            type_value = 'WORKBOOK' if 'рабочая тетрадь' in row[1].lower() else 'SUMMARY'

            pdf_file_name = row[5]

            pdf_file_path = os.path.join(pdf_folder, pdf_file_name)

            if os.path.exists(pdf_file_path):
                data = {
                    'title': title_value,
                    'type': type_value,
                    'lessons_ids': '',
                }
                files = {
                    'file_color': (pdf_file_path, open(pdf_file_path, 'rb'), 'application/pdf'),
                }

                response = umschool_api.post(url, data=data, files=files)

                responses.append(response.json())
            else:
                print(f"Файл не найден: {pdf_file_path}")

            print(f"Строка с ID {id_value} обработана")

            time.sleep(1)
            if number%10==0:
                print("Ждем 20 секунд...")
                time.sleep(20)
                number = 0
            number+=1
        except:
            print("Ошибка")
            continue

with open('responses2.json', 'w', encoding='utf-8') as json_file:
    json.dump(responses, json_file, ensure_ascii=False, indent=2)
df = pd.DataFrame(responses)

df.to_csv('output_file.csv', index=False)

print("Сохранено в output_file.csv")

print(" сохранено в responses.json")
