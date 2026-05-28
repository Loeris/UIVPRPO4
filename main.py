import re
import sys

def fix_name(name_part):
    """Исправляет имя и фамилию: разделяет пробелом, если слитно, и делает заглавными"""
    if not name_part or name_part.strip() == '':
        return ''
    
    name_part = name_part.strip()
    
    # Если имя и фамилия слитно (например, ИванИванов или петрпетров)
    if ' ' not in name_part and len(name_part) > 1:
        # Пытаемся разделить по заглавным буквам
        parts = re.findall('[А-ЯЁ][а-яё]*', name_part)
        
        # Если не нашли заглавные (всё в нижнем регистре), ищем переход от буквы к букве
        if len(parts) < 2:
            # Для русских имён: ищем возможную границу (обычно имя короче фамилии)
            # Пробуем разные варианты разделения
            best_parts = None
            best_score = 0
            
            # Пробуем разделить на разных позициях (от 2 до len-2)
            for split_pos in range(2, len(name_part) - 1):
                first = name_part[:split_pos]
                second = name_part[split_pos:]
                
                # Проверяем, что обе части выглядят как слова (только буквы)
                if first.isalpha() and second.isalpha():
                    # Оцениваем: имя обычно 4-6 букв, фамилия 5-10
                    score = 0
                    if 3 <= len(first) <= 7:
                        score += 1
                    if 4 <= len(second) <= 12:
                        score += 1
                    # Предпочитаем равномерное разделение
                    score += 1 / (abs(len(first) - len(second)) + 1)
                    
                    if score > best_score:
                        best_score = score
                        best_parts = [first, second]
            
            if best_parts:
                parts = best_parts
            else:
                # Если не нашли хорошего разделения, делим пополам
                mid = len(name_part) // 2
                parts = [name_part[:mid], name_part[mid:]]
        
        if len(parts) >= 2:
            name_part = ' '.join(parts[:2])
    
    # Приводим к формату с заглавными буквами
    words = name_part.split()
    if len(words) >= 2:
        # Делаем первую букву заглавной, остальные строчными
        words[0] = words[0][0].upper() + words[0][1:].lower() if words[0] else ''
        words[1] = words[1][0].upper() + words[1][1:].lower() if words[1] else ''
        return ' '.join(words[:2])
    elif len(words) == 1:
        return words[0][0].upper() + words[0][1:].lower() if words[0] else ''
    return ''

def fix_age(age_part):
    """Исправляет возраст: оставляет только цифры и проверяет диапазон"""
    if not age_part or age_part.strip() == '':
        return ''
    
    # Извлекаем все цифры
    digits = re.findall(r'\d+', str(age_part))
    if digits:
        age = digits[0]
        # Проверяем диапазон 0-120
        if 0 <= int(age) <= 120:
            return age
    return ''

def fix_phone(phone_part):
    """Исправляет номер телефона к формату +7 (XXX) XXX-XX-XX"""
    if not phone_part or phone_part.strip() == '':
        return ''
    
    # Извлекаем все цифры
    digits = re.findall(r'\d+', str(phone_part))
    phone_digits = ''.join(digits)
    
    if not phone_digits:
        return ''
    
    # Если номер начинается с 8, заменяем на 7
    if phone_digits.startswith('8'):
        phone_digits = '7' + phone_digits[1:]
    
    # Если номер не начинается с 7 и 10-значный, добавляем 7
    if not phone_digits.startswith('7') and len(phone_digits) == 10:
        phone_digits = '7' + phone_digits
    
    # Если номер не начинается с 7 и не 10-значный, пробуем взять последние 10 цифр
    if not phone_digits.startswith('7') and len(phone_digits) > 10:
        phone_digits = '7' + phone_digits[-10:]
    
    # Проверяем минимальную длину
    if len(phone_digits) < 10:
        return ''
    
    # Если цифр больше 11, берем последние 11
    if len(phone_digits) > 11:
        # Проверяем, есть ли код страны в начале
        if phone_digits[0] == '7':
            phone_digits = phone_digits[:11]
        else:
            phone_digits = '7' + phone_digits[-10:]
    
    # Форматируем 11-значный номер
    if len(phone_digits) == 11 and phone_digits[0] == '7':
        return f"+{phone_digits[0]} ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"
    elif len(phone_digits) == 10:
        return f"+7 ({phone_digits[0:3]}) {phone_digits[3:6]}-{phone_digits[6:8]}-{phone_digits[8:10]}"
    
    return ''

def fix_email(email_part):
    """Исправляет email: убирает лишние символы, исправляет точки"""
    if not email_part or email_part.strip() == '':
        return ''
    
    email = email_part.strip().lower()
    
    # Исправляем @@ на @
    email = email.replace('@@', '@')
    
    # Исправляем двойные точки (но не в домене)
    parts = email.split('@')
    if len(parts) == 2:
        local = parts[0]
        domain = parts[1]
        # Убираем двойные точки в локальной части и домене
        while '..' in local:
            local = local.replace('..', '.')
        while '..' in domain:
            domain = domain.replace('..', '.')
        email = f"{local}@{domain}"
    
    # Удаляем недопустимые символы, но сохраняем @ и точку
    clean_chars = []
    for char in email:
        if char.isalnum() or char in '@._-':
            clean_chars.append(char)
    email = ''.join(clean_chars)
    
    # Проверяем базовый формат email
    match = re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*@[a-zA-Z0-9][a-zA-Z0-9.-]*\.[a-zA-Z]{2,}$', email)
    if match:
        return email
    
    return ''

def process_line(line):
    """Обрабатывает одну строку и возвращает исправленную"""
    line = line.strip()
    if not line:
        return "||||"  # Возвращаем 4 пустых поля для пустой строки
    
    parts = line.split('|')
    
    # Дополняем до 4 полей
    while len(parts) < 4:
        parts.append('')
    
    fixed_name = fix_name(parts[0])
    fixed_age = fix_age(parts[1])
    fixed_phone = fix_phone(parts[2])
    fixed_email = fix_email(parts[3] if len(parts) > 3 else '')
    
    return f"{fixed_name}|{fixed_age}|{fixed_phone}|{fixed_email}"

def main():
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                corrected_line = process_line(line)
                f.write(corrected_line + '\n')
        
        print(f"Готово! Результат сохранён в {output_file}")
    
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)

if __name__ == "__main__":
    main()
