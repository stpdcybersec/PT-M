import unittest
import sys
import os
import datetime
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QDate, Qt
from CarPass import CarPass
from CarPassBase import CarPassBase
from main import (
    ProductManager,
    ProductTableModel,
    ProductFormManager,
    ProductFileHandler,
    ProductWindow
)

app = QApplication(sys.argv)

class TestCarPass(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.sample_car_pass = CarPass(datetime.datetime(2023, 1, 2), "А123БВ78", 7.5)
    
    def test_car_pass_as_string(self):
        """Тестирование строкового представления записи"""
        self.assertEqual(str(self.sample_car_pass), "2023-01-02,А123БВ78,7.5")

class TestProductManager(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.manager = ProductManager()
        self.sample_car_pass = CarPass(datetime.datetime.now(), "А123БВ78", 7.5)

    def test_add_product(self):
        """Тестирование добавления записи"""
        self.manager.add_product(self.sample_car_pass)
        self.assertEqual(len(self.manager.car_passes), 1)
        self.assertIsInstance(self.manager.car_passes[0], CarPass)

    def test_delete_product(self):
        """Тестирование удаления записи"""
        self.manager.add_product(self.sample_car_pass)
        self.manager.delete_product(0)
        self.assertEqual(len(self.manager.car_passes), 0)

    def test_clear_products(self):
        """Тестирование очистки списка записей"""
        self.manager.add_product(self.sample_car_pass)
        self.manager.clear_products()
        self.assertEqual(len(self.manager.car_passes), 0)

    def test_get_products(self):
        """Тестирование получения копии списка записей"""
        self.manager.add_product(self.sample_car_pass)
        car_passes = self.manager.get_products()
        self.assertEqual(len(car_passes), 1)
        self.assertEqual(car_passes[0].car_number, "А123БВ78")

class TestProductTableModel(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.manager = ProductManager()
        self.model = ProductTableModel(self.manager)
        self.sample_car_pass = CarPass(datetime.datetime.now(), "А123БВ78", 7.5)

    def test_row_count(self):
        """Тестирование количества строк"""
        self.assertEqual(self.model.rowCount(), 0)
        self.manager.add_product(self.sample_car_pass)
        self.assertEqual(self.model.rowCount(), 1)

    def test_column_count(self):
        """Тестирование количества столбцов"""
        self.assertEqual(self.model.columnCount(), 3)

    def test_data_display(self):
        """Тестирование отображения данных"""
        self.manager.add_product(self.sample_car_pass)
        index = self.model.index(0, 1)
        self.assertEqual(self.model.data(index), "А123БВ78")
        
        index = self.model.index(0, 2)
        self.assertEqual(self.model.data(index), "7.5")
        
        index = self.model.index(0, 0)
        self.assertEqual(self.model.data(index), datetime.datetime.now().date().strftime("%Y-%m-%d"))

    def test_header_data(self):
        """Тестирование заголовков таблицы"""
        self.assertEqual(self.model.headerData(0, Qt.Orientation.Horizontal), "Дата проезда")
        self.assertEqual(self.model.headerData(1, Qt.Orientation.Horizontal), "Номер автомобиля")
        self.assertEqual(self.model.headerData(2, Qt.Orientation.Horizontal), "Расход топлива")

class TestProductFormManager(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.mock_layout = MagicMock()
        self.form_manager = ProductFormManager(self.mock_layout)

    @patch('PyQt6.QtWidgets.QLineEdit', autospec=True)
    @patch('PyQt6.QtWidgets.QDoubleSpinBox', autospec=True)
    def test_get_form_values(self, mock_spin, mock_line):
        """Тестирование получения значений формы"""
        mock_line.text.return_value = "А123БВ78"
        mock_spin.value.return_value = 7.5
        self.form_manager.car_number_edit = mock_line
        self.form_manager.fuel_consumption_edit = mock_spin
        car_number, fuel = self.form_manager.get_form_values()
        self.assertEqual(car_number, "А123БВ78")
        self.assertEqual(fuel, 7.5)

class TestProductFileHandler(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.temp_file = "temp_test_file.txt"
        self.sample_car_pass = CarPass(datetime.datetime(2023, 1, 2), "А123БВ78", 7.5)
        self.logger = MagicMock()

    def tearDown(self):
        """Очистка после тестов"""
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load_products(self):
        """Тестирование сохранения и загрузки записей"""
        products = [self.sample_car_pass]
        file_handler = ProductFileHandler(self.logger)
        file_handler.save_products(products, self.temp_file)
        
        loaded_products = file_handler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 1)
        self.assertIsInstance(loaded_products[0], CarPass)
        self.assertEqual(loaded_products[0].car_number, "А123БВ78")
        self.assertEqual(loaded_products[0].fuel_consumption, 7.5)

    def test_load_invalid_format(self):
        """Тестирование загрузки некорректного формата"""
        file_handler = ProductFileHandler(self.logger)
        with open(self.temp_file, 'w', encoding='utf-8') as file:
            file.write("2023-01-02,InvalidNumber,7.5\n")
        loaded_products = file_handler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 0)
        self.logger.log_message.assert_called_once()

    def test_load_invalid_letter(self):
        """Тестирование загрузки номера с недопустимой буквой"""
        file_handler = ProductFileHandler(self.logger)
        with open(self.temp_file, 'w', encoding='utf-8') as file:
            file.write("2023-01-02,И123БВ78,7.5\n")  # Буква И недопустима
        loaded_products = file_handler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 0)
        self.logger.log_message.assert_called_once_with(
            "ОШИБКА", 
            unittest.mock.ANY
        )

    def test_load_invalid_letter_in_second_part(self):
        """Тестирование загрузки номера с недопустимой буквой во второй части"""
        file_handler = ProductFileHandler(self.logger)
        with open(self.temp_file, 'w', encoding='utf-8') as file:
            file.write("2023-01-02,А123ГД78,7.5\n")  # Буквы Г и Д недопустимы
        loaded_products = file_handler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 0)
        self.logger.log_message.assert_called_once_with(
            "ОШИБКА", 
            unittest.mock.ANY
        )

    def test_load_future_date(self):
        """Тестирование загрузки записи с датой позднее текущей"""
        file_handler = ProductFileHandler(self.logger)
        future_date = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        with open(self.temp_file, 'w', encoding='utf-8') as file:
            file.write(f"{future_date},А123БВ78,7.5\n")
        loaded_products = file_handler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 0)
        self.logger.log_message.assert_called_once_with(
            "ОШИБКА", 
            unittest.mock.ANY
        )

class TestProductWindow(unittest.TestCase):
    def setUp(self):
        """Подготовка тестового окружения"""
        self.window = ProductWindow()

    def test_initial_state(self):
        """Тестирование начального состояния окна"""
        self.assertEqual(self.window.windowTitle(), "Реестр проездов автомобилей")
        self.assertEqual(len(self.window.product_manager.car_passes), 0)
        
    def test_add_product(self):
        """Тестирование добавления записи"""
        self.window.form_manager.car_number_edit.setText("А123БВ78")
        self.window.form_manager.fuel_consumption_edit.setValue(7.5)
        self.window.date_edit.setDate(QDate.currentDate())
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 1)
        self.assertEqual(self.window.product_manager.car_passes[0].car_number, "А123БВ78")

    @patch.object(QMessageBox, 'warning')
    def test_add_product_invalid_number(self, mock_warning):
        """Тестирование добавления записи с некорректным номером"""
        self.window.form_manager.car_number_edit.setText("Invalid")
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 0)
        mock_warning.assert_called_once()

    @patch.object(QMessageBox, 'warning')
    def test_add_product_invalid_letter(self, mock_warning):
        """Тестирование добавления записи с недопустимой буквой"""
        self.window.form_manager.car_number_edit.setText("И123БВ78")
        self.window.form_manager.fuel_consumption_edit.setValue(7.5)
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 0)
        mock_warning.assert_called_once_with(
            self.window, 
            "Предупреждение", 
            "Неверный формат номера автомобиля! Используйте формат, например, А123БВ78, с буквами А, В, Е, К, М, Н, О, Р, С, Т, У, Х"
        )

    @patch.object(QMessageBox, 'warning')
    def test_add_product_invalid_letter_in_second_part(self, mock_warning):
        """Тестирование добавления записи с недопустимой буквой во второй части"""
        self.window.form_manager.car_number_edit.setText("А123ГД78")
        self.window.form_manager.fuel_consumption_edit.setValue(7.5)
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 0)
        mock_warning.assert_called_once_with(
            self.window, 
            "Предупреждение", 
            "Неверный формат номера автомобиля! Используйте формат, например, А123БВ78, с буквами А, В, Е, К, М, Н, О, Р, С, Т, У, Х"
        )

    @patch.object(QMessageBox, 'warning')
    def test_add_product_future_date(self, mock_warning):
        """Тестирование добавления записи с датой позднее текущей"""
        self.window.form_manager.car_number_edit.setText("А123БВ78")
        self.window.form_manager.fuel_consumption_edit.setValue(7.5)
        future_date = QDate.currentDate().addDays(1)
        self.window.date_edit.setDate(future_date)
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 0)
        mock_warning.assert_called_once_with(
            self.window, 
            "Предупреждение", 
            "Дата проезда не может быть позднее текущей даты!"
        )

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Yes)
    def test_delete_product(self, mock_question):
        """Тестирование удаления записи"""
        test_product = CarPass(datetime.datetime.now(), "А123БВ78", 7.5)
        self.window.product_manager.add_product(test_product)
        self.window.table_view = MagicMock()
        self.window.table_view.currentIndex.return_value.isValid.return_value = True
        self.window.table_view.currentIndex.return_value.row.return_value = 0
        self.window.delete_product()
        self.assertEqual(len(self.window.product_manager.car_passes), 0)

    @patch.object(ProductFileHandler, 'save_products')
    @patch('PyQt6.QtWidgets.QFileDialog.getSaveFileName', return_value=("test.txt", None))
    def test_save_products(self, mock_dialog, mock_save):
        """Тестирование сохранения записей"""
        self.window.save_products()
        mock_save.assert_called_once()

    @patch.object(ProductFileHandler, 'load_products')
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=("test.txt", None))
    @patch.object(QMessageBox, 'information')
    def test_load_products_success(self, mock_info, mock_dialog, mock_load):
        """Тестирование успешной загрузки записей"""
        test_product = CarPass(datetime.datetime.now(), "А123БВ78", 7.5)
        mock_load.return_value = [test_product]
        self.window.load_products()
        self.assertEqual(len(self.window.product_manager.car_passes), 1)
        mock_info.assert_called_once()

    @patch.object(ProductFileHandler, 'load_products', side_effect=Exception("Тестовая ошибка"))
    @patch('PyQt6.QtWidgets.QFileDialog.getOpenFileName', return_value=("test.txt", None))
    @patch.object(QMessageBox, 'critical')
    def test_load_products_failure(self, mock_critical, mock_dialog, mock_load):
        """Тестирование неуспешной загрузки записей"""
        self.window.load_products()
        mock_critical.assert_called_once()

if __name__ == '__main__':
    unittest.main()