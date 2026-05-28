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

def process_line(line):
    parts = line.strip().split('|')
    while len(parts) < 4:
        parts.append('')
    
    name = fix_name(parts[0])
    return f"{name}|{parts[1]}|{parts[2]}|{parts[3]}"

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
