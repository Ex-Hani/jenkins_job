### Применение
Набор скриптов которые помогают создать готовую схему (json-файлы) из xlsx-файла.
Excel-файл необходимо предварительно заполнить.
### Установка скрипта
Скрипты работают на python версии 3.8 и выше.

Выполнить последовательно команды:
```
git clone git@github.com:huntflow/support-engineers.git
cd support-engineers/scripts/schema/vacancy_request_creator/
python3 -m venv my_env
source my_env/bin/activate
pip3 install -r ../../requirements.txt
```
## Скрипт main.py
### Описание
Скрипт создает форму заявки на вакансию (vacancy_request), форму полей вакансии (vacancy_field) 
и справочники (dictionary).
На вход подается xlsx-файл. Пример заполненного файла - `templates/vacancy_request_template.xlsx`
### Пример запуска скрипта
```
python3 main.py --input_file=templates/vacancy_request_template.xlsx --folder_name=template_name --org_name="org_name" --output_path=/path/to/schema_folder --vacancy_file_path=templates/vacancy_fields_template.xlsx --questionary_file_path=templates/questionary_fields_template.xlsx --disable_dict_value_capitalize
```
Где:
  - `--input_file` - имя xlsx-файла. Обязательный параметр.
  - `--folder_name` - название папки со схемой на выходе. Это же имя будет подставляться в названиях файлов. 
Например: значение параметра uniliver, файл с оргструктурой будет называться division_uniliver.json. 
Обязательный параметр.
  - `--output_path` - Путь, куда будет выгружена папка из параметра `--folder_name`. Необязательный параметр.
  - `--mapping_file` - Файл маппинга типов полей. По-умолчанию используется файл `common_files/fields_mapping.json`. 
Необязательный параметр.
  - `--org_name` - полное название организации. Пишется в кавычках. Используется для параметра `name` в файле 
`template.json`. Необязательный параметр.
  - `--vacancy_file_path` - путь к xlsx-файлу содержащий поля вакансии. Конечный 
json-файл (schema_vacancy_fields_*.json), который содержит поля вакансии, будет дополнен полями 
из `--vacancy_file_path`. Поля которые уже есть в файле - остаются без изменений.
  - `--questionary_file_path` - путь к корректно заполненному xlsx-файлу. На выходе будет json-файл с готовой
структурой схемы доп. полей кандидата.
  - `--disable_dict_value_capitalize` - отключить изменение значений справочника. Если параметр указан - значения
справочника не будут меняться.

## Скрипт create_vacancy_fields.py
### Описание
Скрипт создает форму полей вакансии (vacancy_field) и справочники (dictionary).
На вход подается xlsx-файл. Пример заполненного файла - `templates/vacancy_fields_template.xlsx`
### Пример запуска скрипта
```
python3 create_vacancy_fields.py --input_file=templates/vacancy_fields_template.xlsx --folder_name=template_name --org_name="org_name" --output_path=/path/to/schema_folder --disable_dict_value_capitalize
```
Где:
  - `--input_file` - имя xlsx-файла. Обязательный параметр.
  - `--folder_name` - название папки со схемой на выходе. Это же имя будет подставляться в названиях файлов. 
Например: значение параметра uniliver, файл с оргструктурой будет называться division_uniliver.json. 
Обязательный параметр.
  - `--output_path` - Путь, куда будет выгружена папка из параметра `--folder_name`. Необязательный параметр.
  - `--mapping_file` - Файл маппинга типов полей. По-умолчанию используется файл `common_files/fields_mapping.json`. 
Необязательный параметр.
  - `--org_name` - полное название организации. Пишется в кавычках. Используется для параметра `name` в файле 
`template.json`. Необязательный параметр.
  - `--disable_dict_value_capitalize` - отключить изменение значений справочника. Если параметр указан - значения
справочника не будут меняться.

## Скрипт create_questionary_fields.py
### Описание
Скрипт создает форму доп. полей кандидата (questionary) и необходимые справочники (dictionary).
На вход подается xlsx-файл. Пример заполненного файла - `templates/questionary_fields_template.xlsx`
### Пример запуска скрипта
```
python3 create_questionary_fields.py --input_file=templates/questionary_fields_template.xlsx --folder_name=template_name --org_name="org_name" --output_path=/path/to/schema_folder --disable_dict_value_capitalize
```
Где:
  - `--input_file` - имя xlsx-файла. Обязательный параметр.
  - `--folder_name` - название папки со схемой на выходе. Это же имя будет подставляться в названиях файлов. 
Например: значение параметра uniliver, файл с оргструктурой будет называться division_uniliver.json. 
Обязательный параметр.
  - `--output_path` - Путь, куда будет выгружена папка из параметра `--folder_name`. Необязательный параметр.
  - `--mapping_file` - Файл маппинга типов полей. По-умолчанию используется файл `common_files/fields_mapping.json`. 
Необязательный параметр.
  - `--org_name` - полное название организации. Пишется в кавычках. Используется для параметра `name` в файле 
`template.json`. Необязательный параметр.
  - `--disable_dict_value_capitalize` - отключить изменение значений справочника. Если параметр указан - значения
справочника не будут меняться.

## Скрипт create_dictionary.py
### Описание
Скрипт создает справочники (dictionary).
На вход подается xlsx-файл. Пример заполненного файла - `templates/dictionary_template.xlsx`
### Пример запуска скрипта
```
python3 create_dictionary.py --input_file=templates/dictionary_template.xlsx --folder_name=template_name --org_name="org_name" --output_path=/path/to/schema_folder --disable_dict_value_capitalize
```
Где:
  - `--input_file` - имя xlsx-файла. Обязательный параметр.
  - `--folder_name` - название папки со схемой на выходе. Это же имя будет подставляться в названиях файлов. 
Например: значение параметра uniliver, файл с оргструктурой будет называться division_uniliver.json. 
Обязательный параметр.
  - `--output_path` - Путь, куда будет выгружена папка из параметра `--folder_name`. Необязательный параметр.
  - `--mapping_file` - Файл маппинга типов полей. По-умолчанию используется файл `common_files/fields_mapping.json`. 
Необязательный параметр.
  - `--org_name` - полное название организации. Пишется в кавычках. Используется для параметра `name` в файле 
`template.json`. Необязательный параметр.
  - `--disable_dict_value_capitalize` - отключить изменение значений справочника. Если параметр указан - значения
справочника не будут меняться.

## Скрипт order_redefine.py
### Описание
Скрипт выстраивает значения order по порядку в указанном файле.
На вход подается json-файл полей вакансии или заявки на вакансию. Изменения записываются в тот же файл.
### Пример запуска скрипта
```
python3 order_redefine.py /path/to/schema_folder/schema_vacancy_request_bank_tochka.json
```
Где:
 - В качестве параметра, передается путь до файла.

## Скрипт sorts_dict_by_alpha.py
### Описание
Скрипт сортирует данные словаря (справочника) в алфавитном порядке.
На вход подается json-файл dictionary. Изменения записываются в тот же файл.
### Пример запуска скрипта
```
python3 sorts_dict_by_alpha.py /path/to/schema_folder/dictionary_city_simple.json
```
Где:
 - В качестве параметра, передается путь до файла.