import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys


# Базовый класс BasePage по паттерну Page Object
class BasePage:
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
    
    def find_element(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def click_element(self, by, value):
        element = self.find_element(by, value)
        element.click()
        time.sleep(1)
        return element
    
    def input_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        time.sleep(0.5)
        return element
    
    def get_element_text(self, by, value):
        element = self.find_element(by, value)
        return element.text
    
    def get_element_attribute(self, by, value, attribute_name):
        element = self.find_element(by, value)
        return element.get_attribute(attribute_name)


# Класс ContactPage
class ContactPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_form_page(self):
        # Получаем абсолютный путь к корню проекта в GitHub Actions
        base_path = os.getcwd()  # Текущая рабочая директория
        # Пытаемся найти файл form.html
        possible_paths = [
            os.path.join(base_path, "form.html"),          # В корне проекта
            os.path.join(base_path, "tests", "form.html"), # В папке tests
            os.path.join(os.path.dirname(__file__), "form.html") # Рядом с test_ui.py
        ]
        
        for form_path in possible_paths:
            if os.path.exists(form_path):
                self.driver.get(f"file://{form_path}")
                time.sleep(2)
                return self
        
        # Если файл не найден - явно падаем с понятной ошибкой
        raise FileNotFoundError(f"Не удалось найти form.html. Проверенные пути: {possible_paths}")
    
    def fill_name_field(self, name):
        self.input_text(By.ID, "name", name)
        return self
    
    def fill_birthday_field(self, date):
        self.input_text(By.ID, "birthday", date)
        return self
    
    def select_country_field(self, country_value):
        element = self.find_element(By.ID, "country")
        select = Select(element)
        select.select_by_value(country_value)
        time.sleep(0.5)
        return self
    
    def select_gender_field(self, gender):
        if gender == "male":
            self.click_element(By.ID, "male")
        elif gender == "female":
            self.click_element(By.ID, "female")
        return self
    
    def select_student_field(self, is_student):
        if is_student == "yes":
            self.click_element(By.ID, "yes")
        elif is_student == "no":
            self.click_element(By.ID, "no")
        return self
    
    def fill_email_field(self, email):
        self.input_text(By.ID, "mail", email)
        return self
    
    def fill_phone_field(self, phone):
        self.input_text(By.ID, "phone", phone)
        return self
    
    def fill_password_field(self, password):
        self.input_text(By.ID, "password", password)
        return self
    
    def accept_consent_field(self):
        self.click_element(By.ID, "data")
        return self
    
    def submit_form(self):
        self.click_element(By.ID, "submit")
        time.sleep(2)
        return self
    
    def check_success_message(self):
        # Ждем и проверяем, появилась ли новая вкладка
        import time
        time.sleep(3)  # Даем время на открытие новой вкладки
        print(f"Количество вкладок после отправки формы: {len(self.driver.window_handles)}")
        
        if len(self.driver.window_handles) > 1:
            print("Новая вкладка обнаружена, переключаемся...")
            self.driver.switch_to.window(self.driver.window_handles[1])
            print(f"Текущий URL: {self.driver.current_url}")
            
            # Пробуем получить title страницы
            print(f"Заголовок страницы: {self.driver.title}")
            
            # Пробуем получить весь HTML для анализа
            print(f"Первые 500 символов HTML: {self.driver.page_source[:500]}")
            
            # Теперь пытаемся найти элемент
            try:
                success_text = self.get_element_text(By.CSS_SELECTOR, "label[for='regist']")
                print(f"Найден текст: {success_text}")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return success_text
            except Exception as e:
                print(f"Не удалось найти элемент: {e}")
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                return ""
        else:
            print("Новая вкладка НЕ открылась. Остаемся на текущей странице.")
            print(f"Текущий URL: {self.driver.current_url}")
            return ""


# Фикстура для драйвера
@pytest.fixture
def driver():
    # Настройка для headless режима (без GUI)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20)
    yield driver
    driver.quit()


# Тесты
def test_form_submission_positive(driver):
    """Позитивный тест: заполнение и отправка формы со всеми данными"""
    form_page = ContactPage(driver)
    
    # Заполнение формы
    (form_page.open_form_page()
              .fill_name_field("Петров Пётр Петрович")
              .fill_birthday_field("2005-12-15")  # Формат YYYY-MM-DD
              .select_country_field("russia")
              .select_gender_field("male")
              .select_student_field("yes")
              .fill_email_field("petrov@mail.ru")
              .fill_phone_field("+7 (951) 345-87-19")
              .fill_password_field("Password123")
              .accept_consent_field()
              .submit_form())
    
    # Проверка результата
    success_text = form_page.check_success_message()
    assert "Вы зарегистрированы" in success_text, f"Ожидалось 'Вы зарегистрированы', получено: {success_text}"


def test_form_elements_exist(driver):
    """Тест на наличие всех элементов формы"""
    form_page = ContactPage(driver)
    form_page.open_form_page()
    
    # Проверяем наличие всех полей формы
    elements_to_check = [
        (By.ID, "name"),
        (By.ID, "birthday"),
        (By.ID, "country"),
        (By.ID, "mail"),
        (By.ID, "phone"),
        (By.ID, "password"),
        (By.ID, "data"),
        (By.ID, "submit"),
    ]
    
    for by, value in elements_to_check:
        element = form_page.find_element(by, value)
        assert element is not None, f"Элемент {value} не найден"


def test_form_validation(driver):
    """Тест на валидацию формы"""
    form_page = ContactPage(driver)
    form_page.open_form_page()
    
    # Пробуем отправить пустую форму
    form_page.submit_form()
    
    # Проверяем, что остались на той же странице
    assert "form.html" in driver.current_url, "Форма не должна отправляться без данных"


if __name__ == "__main__":
    # Для локального запуска
    pytest.main([__file__, "-v"])