import sys
import re
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QDoubleSpinBox,
                             QLabel, QMessageBox, QFileDialog)
from PyQt6.QtCore import QDate, Qt, QAbstractTableModel, QModelIndex
from CarPass import CarPass
from CarPassBase import CarPassBase
import datetime
import os.path

class Logger:
    """Класс для управления логированием ошибок"""
    
    def __init__(self):
        """Инициализация папки для логов"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
    def log_message(self, level: str, message: str, filename = f"{datetime.datetime.now().strftime('%d-%m-%Y')}.log") -> None:
        """
        Запись сообщения в лог-файл
        
        Args:
            level (str): Уровень лога (ОШИБКА, ПРЕДУПРЕЖДЕНИЕ...)
            message (str): Сообщение для записи
            filename (str): Имя лог-файла (по умолчанию текущая дата)
        """
        if not os.path.exists(f"logs/{filename}"):
            with open(f"logs/{filename}", "w", encoding='utf-8') as file:
                file.write(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {level} {message}\n")
        else:
            with open(f"logs/{filename}", "a", encoding='utf-8') as file:
                file.write(f"{datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')} {level} {message}\n")

class ProductManager:
    """Класс для управления коллекцией записей о проездах"""
    
    def __init__(self):
        """Инициализация пустого списка записей"""
        self.car_passes = []
    
    def add_product(self, product: CarPassBase) -> None:
        """
        Добавление записи о проезде
        
        Args:
            product (CarPassBase): Запись о проезде
        """
        self.car_passes.append(product)
    
    def delete_product(self, index: int) -> None:
        """
        Удаление записи о проезде по индексу
        
        Args:
            index (int): Индекс записи
        """
        if 0 <= index < len(self.car_passes):
            del self.car_passes[index]
    
    def clear_products(self) -> None:
        """Удаление всех записей о проездах"""
        self.car_passes = []
    
    def get_products(self) -> list[CarPassBase]:
        """Получение копии списка записей"""
        return self.car_passes.copy()

class ProductTableModel(QAbstractTableModel):
    """Модель Qt для отображения записей о проездах в таблице"""
    
    def __init__(self, product_manager: ProductManager, parent=None):
        """
        Инициализация модели таблицы
        
        Args:
            product_manager (ProductManager): Менеджер записей
            parent: Родительский объект Qt
        """
        super().__init__(parent)
        self.product_manager = product_manager
        self.headers = ["Дата проезда", "Номер автомобиля", "Расход топлива"]
    
    def columnCount(self, parent=None) -> int:
        """Получение количества столбцов"""
        return len(self.headers)
    
    def rowCount(self, parent=None) -> int:
        """Получение количества строк"""
        return len(self.product_manager.get_products())
    
    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> str|None:
        """
        Получение данных для отображения в таблице
        
        Args:
            index (QModelIndex): Индекс ячейки
            role (Qt.ItemDataRole): Роль данных Qt
        
        Returns:
            str|None: Данные ячейки или None
        """
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        product = self.product_manager.get_products()[index.row()]
        
        if index.column() == 0:
            return product.pass_date.date().strftime("%Y-%m-%d")
        elif index.column() == 1:
            return product.car_number
        elif index.column() == 2:
            return str(product.fuel_consumption)
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> str|None:
        """
        Получение заголовков таблицы
        
        Args:
            section (int): Номер секции
            orientation (Qt.Orientation): Ориентация таблицы (вертикальная/горизонтальная)
        
        Returns:
            str|None: Заголовок или None
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None

class ProductFormManager:
    """Класс для управления полями формы ввода данных о проезде"""
    
    def __init__(self, form_layout: QHBoxLayout):
        """
        Инициализация менеджера формы
        
        Args:
            form_layout (QHBoxLayout): Макет для полей формы
        """
        self.form_layout = form_layout
        self.car_number_edit = QLineEdit()
        self.fuel_consumption_edit = QDoubleSpinBox()
        self.init_form_fields()
    
    def init_form_fields(self) -> None:
        """Инициализация полей формы для записи о проезде"""
        # Поле для номера автомобиля
        car_number_layout = QVBoxLayout()
        car_number_layout.addWidget(QLabel("Номер автомобиля"))
        self.car_number_edit.setPlaceholderText("Например, А123КВ78")
        car_number_layout.addWidget(self.car_number_edit)
        self.form_layout.addLayout(car_number_layout)
        
        # Поле для расхода топлива
        fuel_layout = QVBoxLayout()
        fuel_layout.addWidget(QLabel("Расход топлива (л/100км)"))
        self.fuel_consumption_edit.setMinimum(0.1)
        self.fuel_consumption_edit.setMaximum(50.0)
        self.fuel_consumption_edit.setSingleStep(0.1)
        fuel_layout.addWidget(self.fuel_consumption_edit)
        self.form_layout.addLayout(fuel_layout)
    
    def get_form_values(self) -> tuple[str, float]:
        """
        Получение значений из полей формы
        
        Returns:
            tuple[str, float]: Номер автомобиля и расход топлива
        """
        return self.car_number_edit.text().strip(), self.fuel_consumption_edit.value()

class ProductFileHandler:
    """Класс для обработки сохранения и загрузки записей о проездах"""
    
    def __init__(self, logger: Logger):
        self.logger = logger
    
    def save_products(self, products: list[CarPassBase], filename: str) -> None:
        """
        Сохранение записей о проездах в файл
        
        Args:
            products (list[CarPassBase]): Список записей
            filename (str): Путь к файлу
        """
        with open(filename, 'w', encoding='utf-8') as file:
            for product in products:
                file.write(str(product) + "\n")
    
    def load_products(self, filename: str) -> list[CarPassBase]:
        """
        Загрузка записей о проездах из файла
        
        Args:
            filename (str): Путь к файлу
            
        Returns:
            list[CarPassBase]: Список записей
        """
        products = []
        car_number_pattern = re.compile(r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$')
        current_date = datetime.datetime.now()
        
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    date_str, car_number, fuel_str = line.split(',')
                    # Валидация даты
                    pass_date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                    if pass_date > current_date:
                        raise ValueError(f"Дата проезда позднее текущей: {date_str}")
                    # Валидация номера автомобиля
                    if not car_number_pattern.match(car_number):
                        raise ValueError(f"Неверный формат номера автомобиля: {car_number}. Допустимы только буквы: А, В, Е, К, М, Н, О, Р, С, Т, У, Х")
                    # Валидация расхода топлива
                    fuel_consumption = float(fuel_str)
                    if fuel_consumption <= 0:
                        raise ValueError(f"Неверный расход топлива: {fuel_consumption}")
                    products.append(CarPass(pass_date, car_number, fuel_consumption))
                except Exception as e:
                    self.logger.log_message("ОШИБКА", f"Не удалось разобрать строку {line_number}: {line}. Ошибка: {str(e)}")
        return products

class ProductWindow(QMainWindow):
    """Главное окно приложения для управления записями о проездах"""
    
    def __init__(self):
        """Инициализация главного окна"""
        super().__init__()
        self.setWindowTitle("Реестр проездов автомобилей")
        self.setGeometry(100, 100, 800, 600)
        
        # Инициализация компонентов
        self.product_manager = ProductManager()
        self.logger = Logger()
        self.file_handler = ProductFileHandler(self.logger)
        
        # Создание интерфейса
        self.init_ui()
    
    def init_ui(self) -> None:
        """Инициализация пользовательского интерфейса"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Создание таблицы
        self.table_view = QTableView()
        self.table_model = ProductTableModel(self.product_manager)
        self.table_view.setModel(self.table_model)
        layout.addWidget(self.table_view)
        
        # Создание формы
        form_layout = QHBoxLayout()
        
        # Поле для даты
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Дата проезда"))
        self.date_edit = QDateEdit(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        form_layout.addLayout(date_layout)
        
        # Инициализация менеджера формы
        self.form_manager = ProductFormManager(form_layout)
        
        # Кнопка добавления записи
        self.add_button = QPushButton("Добавить запись")
        self.add_button.clicked.connect(self.add_product)
        form_layout.addWidget(self.add_button)
        
        layout.addLayout(form_layout)
        
        # Макет для кнопок управления
        button_layout = QHBoxLayout()
        
        # Кнопка загрузки
        self.load_button = QPushButton("Загрузить данные")
        self.load_button.clicked.connect(self.load_products)
        button_layout.addWidget(self.load_button)
        
        # Кнопка сохранения
        self.save_button = QPushButton("Сохранить данные")
        self.save_button.clicked.connect(self.save_products)
        button_layout.addWidget(self.save_button)
        
        # Кнопка удаления
        self.delete_button = QPushButton("Удалить выбранное")
        self.delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
    
    def add_product(self) -> None:
        """Добавление новой записи о проезде на основе данных формы"""
        car_number, fuel_consumption = self.form_manager.get_form_values()
        
        # Валидация номера автомобиля
        car_number_pattern = re.compile(r'^[АВЕКМНОРСТУХ]\d{3}[АВЕКМНОРСТУХ]{2}\d{2,3}$')
        if not car_number:
            QMessageBox.warning(self, "Предупреждение", "Номер автомобиля не может быть пустым!")
            self.logger.log_message("ПРЕДУПРЕЖДЕНИЕ", "Попытка добавить запись с пустым номером автомобиля")
            return
        if not car_number_pattern.match(car_number):
            QMessageBox.warning(self, "Предупреждение", "Неверный формат номера автомобиля! Используйте формат, например, А123КВ78, с буквами А, В, Е, К, М, Н, О, Р, С, Т, У, Х")
            self.logger.log_message("ПРЕДУПРЕЖДЕНИЕ", f"Неверный формат номера автомобиля: {car_number}. Допустимы только буквы: А, В, Е, К, М, Н, О, Р, С, Т, У, Х.")
            return
        
        # Валидация расхода топлива
        if fuel_consumption <= 0:
            QMessageBox.warning(self, "Предупреждение", "Расход топлива должен быть положительным!")
            self.logger.log_message("ПРЕДУПРЕЖДЕНИЕ", f"Неверный расход топлива: {fuel_consumption}")
            return
        
        # Валидация даты
        pass_date = datetime.datetime.combine(
            self.date_edit.date().toPyDate(),
            datetime.datetime.min.time()
        )
        if pass_date > datetime.datetime.now():
            QMessageBox.warning(self, "Предупреждение", "Дата проезда не может быть позднее текущей даты!")
            self.logger.log_message("ПРЕДУПРЕЖДЕНИЕ", f"Дата проезда позднее текущей: {pass_date.strftime('%Y-%m-%d')}")
            return
        
        product = CarPass(pass_date, car_number, fuel_consumption)
        self.product_manager.add_product(product)
        self.table_model.layoutChanged.emit()
    
    def delete_product(self) -> None:
        """Удаление выбранной записи о проезде"""
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            QMessageBox.warning(self, "Предупреждение", "Выберите запись для удаления!")
            self.logger.log_message("ПРЕДУПРЕЖДЕНИЕ", "Попытка удаления записи без выбора")
            return
        
        reply = QMessageBox.question(
            self, "Подтверждение удаления", 
            "Вы уверены, что хотите удалить эту запись?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.product_manager.delete_product(selected.row())
            self.table_model.layoutChanged.emit()
    
    def save_products(self) -> None:
        """Сохранение записей о проездах в файл"""
        filename, _ = QFileDialog.getSaveFileName(
            None, "Сохранить файл", ".", "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if filename:
            self.file_handler.save_products(
                self.product_manager.get_products(),
                filename
            )
    
    def load_products(self) -> None:
        """Загрузка записей о проездах из файла"""
        filename, _ = QFileDialog.getOpenFileName(
            None, "Открыть файл", ".", "Текстовые файлы (*.txt);;Все файлы (*)"
        )
        if filename:
            try:
                products = self.file_handler.load_products(filename)
                self.product_manager.clear_products()
                for product in products:
                    self.product_manager.add_product(product)
                self.table_model.layoutChanged.emit()
                QMessageBox.information(self, "Успех", "Данные успешно загружены!")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {str(e)}")
                self.logger.log_message("ОШИБКА", f"Не удалось загрузить файл: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec())
