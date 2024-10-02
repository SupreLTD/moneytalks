from collections import namedtuple
from decimal import Decimal

CurrencyInfo = namedtuple('CurrencyInfo', 'main additional')


class NumberToStringHelper:
    """
    Переводит число в строку
    """
    UNITS = [
        '',
        'один',
        'два',
        'три',
        'четыре',
        'пять',
        'шесть',
        'семь',
        'восемь',
        'девять',
        'десять',
        'одинадцать',
        'двенадцать',
        'тринадцать',
        'четырнадцать',
        'пятнадцать',
        'шестнадцать',
        'семнадцать',
        'восемнадцать',
        'девятнадцать',
    ]
    DOZENS = [
        '',
        'десять',
        'двадцать',
        'тридцать',
        'сорок',
        'пятьдесят',
        'шестьдесят',
        'семьдесят',
        'восемьдесят',
        'девяносто',
    ]
    HUNDREDS = [
        '',
        'сто',
        'двести',
        'триста',
        'четыреста',
        'пятьсот',
        'шестьсот',
        'семьсот',
        'восемьсот',
        'девятьсот',
    ]

    def __init__(self, number, currency_main=None, currency_additional=None):
        self.number = number
        self.currency_main = currency_main
        self.currency_additional = currency_additional

        self.decimal_number = Decimal(number)
        self.main_number = int(self.decimal_number)
        self.additional_number = self._get_additional_number()
        self.currency_info = CurrencyInfo(
            currency_main or ('рубль', 'рубля', 'рублей'),
            currency_additional or ('копейка', 'копейки', 'копеек')
        )

    def _get_additional_number(self):
        return int(round(self.decimal_number - self.main_number, 2) * 100)

    def get_string(self):
        string_list_items = [
            self._get_string_item(number, digit_item_number)
            for digit_item_number, number in enumerate(self._item_generator())
        ]

        base = ' '.join(reversed(string_list_items)) or 'ноль'

        # Если копейки равны нулю, выводим «ноль копеек»
        if self.additional_number == 0:
            additional = 'ноль'
        else:
            additional = self._get_number_string(self.additional_number,
                                                 is_thousands=True)

        pattern = '{base} {currency_base} {additional} {currency_additional}'

        string = pattern.format(
            base=base,
            currency_base=self._get_main_currency(),
            additional=additional,
            currency_additional=self._get_additional_currency()
        )
        return string.capitalize()

    def _item_generator(self):
        number = self.main_number
        while number != 0:
            yield number % 1000
            number = number // 1000

    @property
    def value_tuples(self):
        return (
            ('', '', ''),
            ('тысяча', 'тысячи', 'тысяч'),
            ('миллион', 'миллиона', 'миллионов'),
            ('миллиард', 'миллиарда', 'миллиардов'),
            ('триллион', 'триллиона', 'триллионов'),
            ('квадриллион', 'квадриллиона', 'квадриллионов'),
        )

    def _get_string_item(self, number, digit_item_number):
        is_thousands = digit_item_number == 1
        str_number = self._get_number_string(number, is_thousands)
        str_end = self._get_ends(number, self.value_tuples[digit_item_number])

        str_item = ' '.join([str_number, str_end]) if str_end else str_number

        return str_item

    def _get_main_currency(self):
        return self._get_ends(
            self.main_number,
            self.currency_info.main,
        )

    def _get_additional_currency(self):
        return self._get_ends(
            self.additional_number,
            self.currency_info.additional,
        )

    @staticmethod
    def _get_ends(number, value_tuple=None):
        number = int(number)

        value_tuple = value_tuple or ('тысяча', 'тысячи', 'тысяч')

        number = number % 10 if number % 100 > 20 else number % 20

        if number == 1:
            return value_tuple[0]

        if 2 <= number <= 4:
            return value_tuple[1]

        return value_tuple[2]

    @classmethod
    def _get_number_string(cls, number, is_thousands=False, is_decimals=False):
        number = '{:0>3}'.format(number)

        changed_units = cls.UNITS[:]
        if is_thousands:
            changed_units[1] = 'одна'
            changed_units[2] = 'две'

        hundreds = cls.HUNDREDS[int(number[0])]

        dozens = (
            cls.DOZENS[int(number[1])]
            if int(number[1]) != 1
            else changed_units[int(number[1:])]
        )

        units = ''

        if int(number[1]) != 1:
            units = changed_units[int(number[2])]

        list_items = filter(None, [
            hundreds,
            dozens,
            units
        ])
        return ' '.join(list_items)

    @staticmethod
    def _get_additional_ends(additional_number):
        if additional_number % 10 == 1 and additional_number % 100 != 11:
            return 'копейка'
        elif 2 <= additional_number % 10 <= 4 and not 12 <= additional_number % 100 <= 14:
            return 'копейки'
        else:
            return 'копеек'


def get_string_by_number(number, currency_main=None, currency_additional=None):
    string = NumberToStringHelper(
        number=number,
        currency_main=currency_main,
        currency_additional=currency_additional,
    ).get_string()

    return string
