import pytest
import sys
import os

# Добавляем путь к модулю (если тесты запускаются из корня)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_validator import fix_name, fix_age, fix_phone, fix_email, process_line

# ----- Тесты для fix_name -----
def test_fix_name_normal():
    assert fix_name("Иван Иванов") == "Иван Иванов"
    assert fix_name("петр петров") == "Петр Петров"
    assert fix_name("Анна") == "Анна"

def test_fix_name_merged():
    assert fix_name("ИванИванов") == "Иван Иванов"
    assert fix_name("петрпетров") == "Петр Петров"  # Должен исправить регистр и разделить
    assert fix_name("АннаСмирнова") == "Анна Смирнова"

def test_fix_name_empty():
    assert fix_name("") == ""
    assert fix_name("   ") == ""
    assert fix_name(None) == ""

def test_fix_name_extra_spaces():
    assert fix_name("  Петр  Петров  ") == "Петр Петров"

# ----- Тесты для fix_age -----
def test_fix_age_normal():
    assert fix_age("25") == "25"
    assert fix_age("0") == "0"
    assert fix_age("120") == "120"

def test_fix_age_with_garbage():
    assert fix_age("¬27") == "27"
    assert fix_age("age 35 years") == "35"
    assert fix_age("+99") == "99"

def test_fix_age_out_of_range():
    assert fix_age("150") == ""   # больше 120
    assert fix_age("-5") == ""    # отрицательное
    assert fix_age("abc") == ""

def test_fix_age_empty():
    assert fix_age("") == ""
    assert fix_age("   ") == ""

# ----- Тесты для fix_phone -----
def test_fix_phone_normal():
    assert fix_phone("+79990001111") == "+7 (999) 000-11-11"
    assert fix_phone("8 (999) 000-11-11") == "+7 (999) 000-11-11"
    assert fix_phone("9990001111") == "+7 (999) 000-11-11"   # 10 цифр

def test_fix_phone_with_spaces():
    assert fix_phone("+7 999 000 11 11") == "+7 (999) 000-11-11"
    assert fix_phone("+7999000 1 1 11") == "+7 (999) 000-11-11"

def test_fix_phone_too_short():
    assert fix_phone("123") == ""
    assert fix_phone("+7123") == ""

def test_fix_phone_too_long():
    # Обрезает последние 11 цифр (или 10, если начинается с 7/8)
    assert fix_phone("+7123456789012345") == "+7 (123) 456-78-90"
    assert fix_phone("89123456789012345") == "+7 (912) 345-67-89"

def test_fix_phone_empty():
    assert fix_phone("") == ""
    assert fix_phone(None) == ""

# ----- Тесты для fix_email -----
def test_fix_email_normal():
    assert fix_email("user@example.ru") == "user@example.ru"
    assert fix_email("User.Name@mail.com") == "user.name@mail.com"

def test_fix_email_double_at():
    assert fix_email("user@@example.ru") == "user@example.ru"

def test_fix_email_double_dot():
    assert fix_email("user@yandex..ru") == "user@yandex.ru"
    assert fix_email("user..name@example.com") == "user.name@example.com"  # точки в локальной части допустимы

def test_fix_email_invalid_chars():
    assert fix_email("user!@#name@example.ru") == "username@example.ru"
    assert fix_email("user name@example.ru") == "username@example.ru"

def test_fix_email_wrong_format():
    assert fix_email("user@example") == ""          # нет доменной зоны
    assert fix_email("user@.com") == ""             # домен начинается с точки
    assert fix_email("@example.ru") == ""           # нет имени

def test_fix_email_empty():
    assert fix_email("") == ""
    assert fix_email(None) == ""

# ----- Тесты для process_line (интеграционные) -----
def test_process_line_full_correction():
    line = "ИванИванов|¬27|+7999000 1 1 11|example@@yandex..ru"
    expected = "Иван Иванов|27|+7 (999) 000-11-11|example@yandex.ru"
    assert process_line(line) == expected

def test_process_line_partial_correction():
    line = "Анна|abc|88005553535|invalid_email"
    # age не число -> пусто, email невалидный -> пусто, телефон исправляется
    expected = "Анна||+7 (800) 555-35-35|"
    assert process_line(line) == expected

def test_process_line_all_empty():
    line = "|||"
    expected = "||||"
    # В процессе line.strip() даст "", но мы считаем, что пустые строки пропускаются в main.
    # Однако функция process_line может обработать: все поля пустые.
    # В коде коммита 4 при split('|') получим ['', '', '', ''].
    # fix_name('') -> '', fix_age('') -> '', fix_phone('') -> '', fix_email('') -> ''
    assert process_line(line) == "||||"

def test_process_line_missing_fields():
    line = "Иван|30"
    expected = "Иван|30||"
    assert process_line(line) == expected
