import re
import sys

def fix_name(name_part):
    if not name_part or name_part.strip() == '':
        return ''
    
    name_part = name_part.strip()
    
    if ' ' not in name_part:
        parts = re.findall('[А-ЯЁ][а-яё]*', name_part)
        if len(parts) >= 2:
            name_part = ' '.join(parts)
    
    words = name_part.split()
    if len(words) >= 2:
        words[0] = words[0].capitalize()
        words[1] = words[1].capitalize()
        return ' '.join(words[:2])
    elif len(words) == 1:
        return words[0].capitalize()
    return ''

def fix_age(age_part):
    """Исправляет возраст: оставляет только цифры"""
    if not age_part or age_part.strip() == '':
        return ''
    
    digits = re.findall(r'\d+', str(age_part))
    if digits:
        age = digits[0]
        if 0 <= int(age) <= 120:
            return age
    return ''

def fix_phone(phone_part):
    """Исправляет номер телефона к формату +7 (XXX) XXX-XX-XX"""
    if not phone_part or phone_part.strip() == '':
        return ''
    
    digits = re.findall(r'\d+', str(phone_part))
    phone_digits = ''.join(digits)
    
    if phone_digits.startswith('8'):
        phone_digits = '7' + phone_digits[1:]
    
    if len(phone_digits) < 10:
        return ''
    
    if len(phone_digits) > 11:
        phone_digits = phone_digits[-11:]
    
    if len(phone_digits) == 11:
        return f"+{phone_digits[0]} ({phone_digits[1:4]}) {phone_digits[4:7]}-{phone_digits[7:9]}-{phone_digits[9:11]}"
    return ''

def process_line(line):
    parts = line.strip().split('|')
    while len(parts) < 4:
        parts.append('')
    
    fixed_name = fix_name(parts[0])
    fixed_age = fix_age(parts[1])
    fixed_phone = fix_phone(parts[2])
    
    return f"{fixed_name}|{fixed_age}|{fixed_phone}|{parts[3]}"

def main():
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip():
                    corrected_line = process_line(line)
                    f.write(corrected_line + '\n')
        
        print(f"Готово! Результат сохранён в {output_file}")
    
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)

if __name__ == "__main__":
    main()
