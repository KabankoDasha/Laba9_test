import math

class Calculator:
    
    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def subtract(a, b):
        return a - b

    @staticmethod
    def multiply(a, b):
        return a * b

    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return a / b

    @staticmethod
    def power(a, exponent=2):
        return a ** exponent

    @staticmethod
    def square_root(a):
        if a < 0:
            raise ValueError("Корень из отрицательного числа невозможен")
        return math.sqrt(a)

    @staticmethod
    def is_prime_number(n):
        if n < 2:
            raise ValueError("Простые числа начинаются с 2")
        
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(n ** 0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def change_sign(a):
        return -a

    @staticmethod
    def factorial(n):
        if n < 0:
            raise ValueError("Факториал отрицательного числа не определен")
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result

    @staticmethod
    def percentage(value, percent):
        return (value * percent) / 100

    @staticmethod
    def evaluate_expression(expression):
        """
        Вычисление математического выражения в виде строки
        Args:
            expression (str): математическое выражение, например "2 + 3 * 4"
        Returns:
            float или int: результат вычисления
        Raises:
            ValueError: если выражение некорректно или содержит деление на ноль
        """
        expression = expression.strip()
        if not expression:
            raise ValueError("Пустое выражение")

        if '/0' in expression:
            raise ValueError("Деление на ноль")
        
        import re
        valid_chars = r'^[0-9+\-*/().\s]+$'
        if not re.match(valid_chars, expression):
            raise ValueError("Некорректные символы в выражении")
        
        temp_expr = expression.replace('**', '  ')  
        if re.search(r'[+\-*/]\s*[+\-*/]', temp_expr):
            raise ValueError("Некорректное математическое выражение")

        try:
            result = eval(expression)
            
            if isinstance(result, (int, float)):
                if not abs(result) < float('inf'):  
                    raise ValueError("Деление на ноль")
            return result
        except ZeroDivisionError:
            raise ValueError("Деление на ноль")
        except SyntaxError:
            raise ValueError("Некорректное математическое выражение")
        except Exception as e:
            raise ValueError(f"Некорректное математическое выражение: {str(e)}")