import sys

def main():
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in lines:
                f.write(line)
        
        print(f"Файл обработан. Результат в {output_file}")
    
    except FileNotFoundError:
        print(f"Ошибка: файл {input_file} не найден")
        sys.exit(1)

if __name__ == "__main__":
    main()
