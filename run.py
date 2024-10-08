import subprocess
import sys
from parser1 import parser1 
from parser2 import parser2
# Список необходимых библиотек
required_packages = [
    'selenium',
    'python-docx'
]

# Функция для установки пакетов
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Установка всех необходимых пакетов
for package in required_packages:
    install(package)

print("Все библиотеки установлены. Теперь запускаем основной код...")

# Получить параметры командной строки
if len(sys.argv) != 4:
    print("Использование: python run.py <param1> <param2> <param3>")
    sys.exit(1)

param1 = sys.argv[1]  # string_to_put_in_search
param2 = sys.argv[2]  # date_from
param3 = sys.argv[3]  # date_up

# Вызов функции parser1 с параметрами
# parser1(param1, param2, param3)
parser1(param1,param2,param3)
parser2(param1,param2,param3)