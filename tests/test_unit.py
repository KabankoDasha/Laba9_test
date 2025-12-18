import unittest
import math
import sys
import pytest
from calculator import Calculator


# Тесты для всех методов класса Calculator
class TestCalculator:
    
    def test_add_positive_numbers(self):
        assert Calculator.add(5, 3) == 8
        assert Calculator.add(0, 0) == 0
        assert Calculator.add(100, 200) == 300
    
    def test_add_negative_numbers(self):
        assert Calculator.add(-5, -3) == -8
        assert Calculator.add(-10, 5) == -5
        assert Calculator.add(10, -5) == 5
    
    def test_add_decimal_numbers(self):
        assert Calculator.add(2.5, 3.1) == pytest.approx(5.6, 0.00001)
        assert Calculator.add(0.1, 0.2) == pytest.approx(0.3, 0.00001)
    
    def test_divide_normal_cases(self):
        assert Calculator.divide(10, 2) == 5
        assert Calculator.divide(1, 2) == 0.5
        assert Calculator.divide(0, 5) == 0
        assert Calculator.divide(9, 3) == 3
    
    def test_divide_negative_numbers(self):
        assert Calculator.divide(-10, 2) == -5
        assert Calculator.divide(10, -2) == -5
        assert Calculator.divide(-10, -2) == 5
    
    def test_divide_decimal_numbers(self):
        assert Calculator.divide(5.5, 2) == pytest.approx(2.75, 0.00001)
        assert Calculator.divide(1, 3) == pytest.approx(1/3, 0.00001)
    
    def test_divide_by_zero_exception(self):
        with pytest.raises(ValueError) as exc_info:
            Calculator.divide(10, 0)
        assert "Деление на ноль невозможно" in str(exc_info.value)
    
    def test_is_prime_number_true_cases(self):
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 97]
        
        for prime in primes:
            assert Calculator.is_prime_number(prime) == True
    
    def test_is_prime_number_false_cases(self):
        composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 100]
        
        for composite in composites:
            assert Calculator.is_prime_number(composite) == False
    
    def test_is_prime_number_edge_cases_exceptions(self):
        with pytest.raises(ValueError) as exc_info:
            Calculator.is_prime_number(1)
        assert "Простые числа начинаются с 2" in str(exc_info.value)
    
    def test_multiply(self):
        assert Calculator.multiply(4, 5) == 20
        assert Calculator.multiply(0, 100) == 0
        assert Calculator.multiply(-3, 4) == -12
        assert Calculator.multiply(-3, -4) == 12
        assert Calculator.multiply(2.5, 4) == 10.0
    
    def test_subtract(self):
        assert Calculator.subtract(10, 3) == 7
        assert Calculator.subtract(0, 5) == -5
        assert Calculator.subtract(-5, -3) == -2
        assert Calculator.subtract(5, 5) == 0
    
    def test_power(self):
        assert Calculator.power(3) == 9
        assert Calculator.power(2, 3) == 8
        assert Calculator.power(5, 0) == 1
        assert Calculator.power(-2, 2) == 4
        assert Calculator.power(4, 0.5) == 2
        assert Calculator.power(2, -1) == 0.5
    
    def test_square_root(self):
        assert Calculator.square_root(9) == 3
        assert Calculator.square_root(0) == 0
        assert Calculator.square_root(4) == 2
        assert Calculator.square_root(2) == pytest.approx(math.sqrt(2), 0.00001)
    
    def test_square_root_negative(self):
        with pytest.raises(ValueError) as exc_info:
            Calculator.square_root(-4)
        assert "Корень из отрицательного числа невозможен" in str(exc_info.value)
    
    def test_factorial(self):
        assert Calculator.factorial(0) == 1
        assert Calculator.factorial(1) == 1
        assert Calculator.factorial(5) == 120
        assert Calculator.factorial(7) == 5040
    
    def test_factorial_negative(self):
        with pytest.raises(ValueError) as exc_info:
            Calculator.factorial(-5)
        assert "Факториал отрицательного числа не определен" in str(exc_info.value)