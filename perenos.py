import csv
import json

# Чтение CSV-файла с указанием кодировки
csv_file_path = 'result_file.csv'
responses1_file_path = 'responses2.json'
responses2_file_path = 'responses.json'
output_file_path = 'output_result2.csv'

with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    rows = list(csv_reader)

with open(responses1_file_path, 'r', encoding='utf-8') as responses1_file:
    responses1_data = json.load(responses1_file)

with open(responses2_file_path, 'r', encoding='utf-8') as responses2_file:
    responses2_data = json.load(responses2_file)

def find_id_by_file_color(file_color):
    for item in responses1_data:
        if item.get('file_color') == file_color:
            title = item.get('title')
            if title:
                for result in responses2_data:
                    for response_item in result.get('results', []):
                        if response_item.get('title') == title:
                            return response_item.get('id')
    return None

for row in rows:
    # Получение значения из третьего столбца
    value_from_csv = row[2]

    # Поиск file_color в responses1.json
    file_color = None
    for item in responses1_data:
        if item.get('title') == value_from_csv:
            file_color = item.get('file_color')
            break

    # Если найден file_color, то поиск соответствующего id в responses2.json
    if file_color:
        corresponding_id = find_id_by_file_color(file_color)
        row.append(corresponding_id)
    else:
        row.append(None)

with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
    csv_writer = csv.writer(output_file)
    csv_writer.writerows(rows)
