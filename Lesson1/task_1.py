import os
import platform
import subprocess
import time
from ipaddress import ip_address
from pprint import  pprint

result = {'Доступные узлы': "", "Недоступные узлы": ""}

DNULL = open(os.devnull, 'w')
#Проверка на ip адресс

def check_is_ipadress(value):
    try:
        ipv4 = ip_address(value)
    except ValueError:
        raise Exception('Некорректный ip адрес')
    return ipv4
#Функция, проверяющая доступность хостов

def host_ping(hosts_list, get_list=False):
    print("Запуск проверки доступности узлов..")
    for host in hosts_list:
        try:
            ipv4 = check_is_ipadress(host)
        except Exception as e:
            print(f'{host} - {e} воспринимается как имя домена')
            ipv4 = host

        param = '-n' if platform.system().lower() == 'windows' else '-c'
        response = subprocess.Popen(["ping", param, '1', '-w', '1', str(ipv4)],
                                    stdout=subprocess.PIPE)
        if response.wait() == 0:
            result["Доступные узлы"] += f"{ipv4}\n"
            res_string = f"{ipv4} - Узел доступен"
        else:
            result["Недоступные узлы"] += f"{ipv4}\n"
            res_string = f"{ipv4} - Узел недоступен"
        if not get_list:
            print(res_string)
    if get_list:
        return result
if __name__ == '__main__':

    hosts_list = ['yandex.ru', '0.0.0.1', '8.8.8.8', 'google.com', '0.0.0.2', '0.0.0.4', '0.0.0.5',
                  '0.0.0.6', '0.0.0.7', '0.0.0.8', '0.0.0.9', '192.168.8.1', '0.0.1.0']
    start = time.time()
    host_ping(hosts_list)
    end = time.time()
    print(f'total time: {int(end - start)}')
    pprint(result)