import csv
import os
import requests
from urllib.parse import urlparse, unquote

csv_file_path = 'materia_zamena_adresa.csv'

pdf_directory = 'PDF'

if not os.path.exists(pdf_directory):
    os.makedirs(pdf_directory)

downloaded_files_count = 0

def download_and_move_pdf(url, pdf_directory):
    global downloaded_files_count
    try:
        decoded_url = unquote(url)
        response = requests.get(decoded_url)
        response.raise_for_status()

        file_name = os.path.basename(urlparse(decoded_url).path)

        if file_name.lower().endswith('.pdf'):
            pdf_path = os.path.join(pdf_directory, file_name)
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            downloaded_files_count += 1
            print(f"Файл {file_name} успешно скачан и перемещен в директорию PDF.{downloaded_files_count}")
        else:
            print(f"Внимание: Файл {file_name} не является PDF и не будет скачан.")
    except Exception as e:
        print(f"Ошибка при обработке URL: {e}")

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        # Второй столбец (индекс 1) содержит ссылки на PDF
        pdf_url = row[2]
        download_and_move_pdf(pdf_url, pdf_directory)

print(f"Всего скачано {downloaded_files_count} файлов.")
