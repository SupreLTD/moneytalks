# MoneyTalks

Переработанный пакет https://pypi.org/project/number_to_string/

Теперь он приводит к строке копейки и рубли в правильном падеже.

`MoneyTalks` — это библиотека для конвертации чисел в строковое представление на русском языке с поддержкой различных валют.

## Установка

Установить пакет можно через pip:

```bash
pip install moneytalks
```

## Использование

Пример простого использования:
```python
from moneytalks import get_string_by_number

result = get_string_by_number(1234.56)
print(result)  # "Одна тысяча двести тридцать четыре рубля пятьдесят шесть копеек"
```
Вы также можете задать собственные валюты:
```python
from moneytalks import get_string_by_number

custom_main = ('доллар', 'доллара', 'долларов')
custom_additional = ('цент', 'цента', 'центов')

result = get_string_by_number(123.45, custom_main, custom_additional)
print(result)  # "Сто двадцать три доллара сорок пять центов"
```
## Тестирование

Запуск тестов:
```bash
python -m unittest discover
```