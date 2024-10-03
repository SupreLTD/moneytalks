from collections import namedtuple
from decimal import Decimal

CurrencyInfo = namedtuple('CurrencyInfo', 'main additional')


class NumberToStringHelper:
    UNITS = ['', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять', 'десять',
             'одинадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать',
             'семнадцать', 'восемнадцать', 'девятнадцать']

    DOZENS = ['', 'десять', 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят',
              'девяносто']

    HUNDREDS = ['', 'сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот']

    VALUE_TUPLES = [
        ('', '', ''),
        ('тысяча', 'тысячи', 'тысяч'),
        ('миллион', 'миллиона', 'миллионов'),
        ('миллиард', 'миллиарда', 'миллиардов'),
        ('триллион', 'триллиона', 'триллионов'),
        ('квадриллион', 'квадриллиона', 'квадриллионов'),
    ]

    def __init__(self, number, currency_main=None, currency_additional=None):
        self.decimal_number = Decimal(number)
        self.main_number = int(self.decimal_number)
        self.additional_number = int(round(self.decimal_number % 1 * 100))

        self.currency_info = CurrencyInfo(
            currency_main or ('рубль', 'рубля', 'рублей'),
            currency_additional or ('копейка', 'копейки', 'копеек')
        )

    def get_string(self):
        base = ' '.join(
            reversed([self._get_string_item(num, i) for i, num in enumerate(self._item_generator())])) or 'ноль'
        additional = 'ноль' if self.additional_number == 0 else self._get_number_string(self.additional_number,
                                                                                        is_thousands=True)

        return f'{base} {self._get_main_currency()} {additional} {self._get_additional_currency()}'.capitalize()

    def _item_generator(self):
        number = self.main_number
        while number:
            yield number % 1000
            number //= 1000

    def _get_string_item(self, number, index):
        str_number = self._get_number_string(number, index == 1)
        str_end = self._get_ends(number, self.VALUE_TUPLES[index])
        return f'{str_number} {str_end}'.strip()

    def _get_main_currency(self):
        return self._get_ends(self.main_number, self.currency_info.main)

    def _get_additional_currency(self):
        return self._get_ends(self.additional_number, self.currency_info.additional)

    @staticmethod
    def _get_ends(number, value_tuple):
        number %= 100
        if number > 19:
            number %= 10

        if number == 1:
            return value_tuple[0]
        elif 2 <= number <= 4:
            return value_tuple[1]
        else:
            return value_tuple[2]

    @classmethod
    def _get_number_string(cls, number, is_thousands=False):
        number = f'{number:03}'
        units = cls.UNITS if not is_thousands else cls._get_thousand_units()

        return ' '.join(filter(None, [cls.HUNDREDS[int(number[0])],
                                      cls.DOZENS[int(number[1]) if number[1] != '1' else 0],
                                      units[int(number[1:])] if number[1] == '1' else units[int(number[2])]]))

    @staticmethod
    def _get_thousand_units():
        units = NumberToStringHelper.UNITS[:]
        units[1], units[2] = 'одна', 'две'
        return units


def get_string_by_number(number, currency_main=None, currency_additional=None):
    return NumberToStringHelper(number, currency_main, currency_additional).get_string()
