import unittest
from main import get_city, translate_city


class TestFunc(unittest.TestCase):
    """Тестик чисто добавить.

     в actions, чтобы были"""

    def test_get_city(self):
        result_bool, result = get_city("Moscow")
        self.assertEqual(result_bool, True)
if __name__ == '__main__':

	unittest.main()
