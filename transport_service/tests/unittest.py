import unittest  # Стандартная библиотека для тестирования

class TestRouterConsistency(unittest.TestCase):
    def setUp(self):
        # Подготовка перед каждым тестом
        self.base_route = "/api/v1/transport"

    def test_route_base_path(self):
        # Проверка базового пути
        self.assertEqual(self.base_route, "/api/v1/transport")

    def test_route_trailing_slash(self):
        # Проверка консистентности слеша в конце
        self.assertTrue(self.base_route.endswith("/") or len(self.base_route) > 1)

    def test_route_prefix(self):
        # Проверка начала пути
        self.assertTrue(self.base_route.startswith("/"))

    def tearDown(self):
        # Очистка после теста (если нужна)
        pass

# Запуск тестов
if __name__ == '__main__':
    unittest.main()