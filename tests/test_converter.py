import unittest
from moneytalks.converter import get_string_by_number


class TestNumberToStringHelper(unittest.TestCase):

    def test_integer_conversion(self):
        self.assertEqual(get_string_by_number(123), 'Сто двадцать три рубля ноль копеек')
        self.assertEqual(get_string_by_number(1001), 'Одна тысяча один рубль ноль копеек')

    def test_decimal_conversion(self):
        self.assertEqual(get_string_by_number(123.45), 'Сто двадцать три рубля сорок пять копеек')
        self.assertEqual(get_string_by_number(1001.01), 'Одна тысяча один рубль одна копейка')

    def test_custom_currency(self):
        custom_main = ('доллар', 'доллара', 'долларов')
        custom_additional = ('цент', 'цента', 'центов')
        self.assertEqual(get_string_by_number(50, custom_main, custom_additional), 'Пятьдесят долларов ноль центов')


if __name__ == '__main__':
    unittest.main()
