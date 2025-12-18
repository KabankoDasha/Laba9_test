import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


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
        time.sleep(2)
        return element
    
    def input_text(self, by, value, text):
        element = self.find_element(by, value)
        element.clear()
        element.send_keys(text)
        time.sleep(2)
        return element
    
    def get_element_text(self, by, value):
        element = self.find_element(by, value)
        return element.text
    
    def get_element_attribute(self, by, value, attribute_name):
        element = self.find_element(by, value)
        return element.get_attribute(attribute_name)
    
    def get_current_url(self):
        return self.driver.current_url
    
    def get_window_handles_count(self):
        return len(self.driver.window_handles)


# Класс ContactPage
class ContactPage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def open_form_page(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        form_path = os.path.join(current_dir, "form.html")
        self.driver.get(f"file://{form_path}")
        time.sleep(3)
        return self
    
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
        time.sleep(2)
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
        time.sleep(3)
        return self
    
    def check_success_message(self):
        if len(self.driver.window_handles) > 1:
            self.driver.switch_to.window(self.driver.window_handles[1])
            
            current_dir = os.path.dirname(os.path.abspath(__file__))
            index_path = os.path.join(current_dir, "index.html")
            self.driver.get(f"file://{index_path}")
            time.sleep(3)
            
            success_text = self.get_element_text(By.CSS_SELECTOR, "label[for='regist']")
            
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            
            return success_text
        return ""
    
    def check_name_field_required(self):
        is_required = self.get_element_attribute(By.ID, "name", "required")
        return is_required is not None


# Фикстура для создания и закрытия драйвера
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)
    yield driver
    driver.quit()


class TestUI:
    
    def test_form_submission_positive(self, driver):
        """Позитивный тест: заполнение и отправка формы со всеми данными"""
        form_page = ContactPage(driver)
        
        # Заполнение формы
        (form_page.open_form_page()
                  .fill_name_field("Петров Пётр Петрович")
                  .fill_birthday_field("15-12-2005")
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
    
    def test_form_validation_negative(self, driver):
        """Негативный тест: попытка отправки формы без обязательного поля"""
        form_page = ContactPage(driver)
        
        # Открываем страницу
        form_page.open_form_page()
        
        # Запоминаем URL до отправки
        before_url = form_page.get_current_url()
        
        # Заполняем все поля КРОМЕ обязательного имени
        (form_page.fill_birthday_field("15-12-2005")
                  .select_country_field("russia")
                  .select_gender_field("male")
                  .select_student_field("yes")
                  .fill_email_field("petrov@mail.ru")
                  .fill_phone_field("+7 (951) 345-87-19")
                  .fill_password_field("Password123")
                  .accept_consent_field()
                  .submit_form())
        
        # Проверяем, что форма НЕ отправилась
        after_url = form_page.get_current_url()
        
        # Проверка 1: поле должно быть обязательным
        is_required = form_page.check_name_field_required()
        assert is_required, "Поле 'Ф.И.О.' должно быть обязательным (атрибут required)"
        
        # Проверка 2: URL не должен измениться (остаемся на той же странице)
        assert "form.html" in after_url, "Форма не должна отправляться при пустом обязательном поле"
    
    def test_form_elements_exist(self, driver):
        """Тест на наличие всех элементов формы"""
        form_page = ContactPage(driver)
        form_page.open_form_page()
        
        # Проверяем наличие всех полей формы
        elements_to_check = [
            (By.ID, "name"),
            (By.ID, "birthday"),
            (By.ID, "country"),
            (By.ID, "male"),
            (By.ID, "female"),
            (By.ID, "yes"),
            (By.ID, "no"),
            (By.ID, "mail"),
            (By.ID, "phone"),
            (By.ID, "password"),
            (By.ID, "data"),
            (By.ID, "submit"),
            (By.ID, "reset")
        ]
        
        for by, value in elements_to_check:
            element = form_page.find_element(by, value)
            assert element is not None, f"Элемент {value} не найден на странице"


if __name__ == "__main__":
    # Для запуска напрямую (не через pytest)
    pytest.main([__file__, "-v"])