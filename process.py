import datetime
from collections import Counter
import re
import subprocess
import sys

user_reg = r'^\S*'
cpu_reg = r'\d*\s\s(\d*\.\d*)'
mem_reg = r'\d*\s\s\d*\.\d*\s*(\d*\.\d*)'
proc_reg = r'\/.*$'

proc = subprocess.Popen(('ps', 'aux'), stdout=subprocess.PIPE, universal_newlines=True)

out, err = proc.communicate()

out = out.split('\n')[1:]
proc_count = len(out)

result_list = []

for line in out:
    user = re.search(user_reg, line)
    mem = re.search(mem_reg, line)
    cpu = re.search(cpu_reg, line)
    proc = re.search(proc_reg, line)
    if user is not None and mem is not None and cpu is not None and proc is not None:
        result_list.append([proc.group(), user.group(), float(mem.groups()[0]), float(cpu.groups()[0])])

user_list = []
memory = 0
proc = 0
for elem in result_list:
    user_list.append(elem[1])
    memory += elem[2]
    proc += elem[3]

max_memory = max(result_list, key=lambda item: item[2])
max_memory = max_memory[0].split('/')
max_cpu = max(result_list, key=lambda item: item[3])
max_cpu = max_cpu[0].split('/')

users = ', '.join(set(user_list))
user_process = Counter(user_list).most_common()

original_stdout = sys.stdout

filename = str(datetime.datetime.now().strftime('%d-%m-%Y-%H:%M')) + '-scan.txt'

with open(filename, 'w') as f:
    sys.stdout = f
    print('Отчет о состоянии системы:')
    print(f'Пользователи системы: {users}')
    print(f'Процессов запущено: {proc_count}')
    print('Пользовательских процессов:')
    for elem in user_process:
        print(elem[0] + ': ' + str(elem[1]))
    print(f'Всего памяти используется: {round(memory, 2)}%')
    print(f'Всего CPU используется: {round(proc, 2)}%')
    print(f'Больше всего памяти использует: {(max_memory[-1])[:20]}')
    print(f'Больше всего CPU использует: {(max_cpu[-1][:20])}')
    sys.stdout = original_stdout

with open(filename, 'r') as f:
    lines = f.readlines()

for line in lines:
    print(line, end='')


