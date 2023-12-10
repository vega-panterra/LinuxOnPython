import string
import random
from datetime import datetime

import pytest
import yaml

from checkers import ssh_checkout, ssh_checkout_get
from files import upload_files

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')
def make_folders():
    return ssh_checkout(f'{data["ip"]}',
                        f'{data["user"]}',
                        f'{data["password"]}',
                        f'mkdir -p {data["tst"]} {data["out"]} '
                        f'{data["folder1"]} {data["folder2"]}',
                        '')


# @pytest.fixture(autouse=True, scope='class')
@pytest.fixture(autouse=True, scope='class')
def make_files():
    list_of_files = []
    for i in range(data['count']):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout(f'{data["ip"]}',
                        f'{data["user"]}',
                        f'{data["password"]}',
                        f'cd {data["tst"]}; dd if=/dev/urandom of={filename} b'
                        f's={data["bs"]} count=1 iflag=fullblock',
                        ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope='module')
def clear_folders():
    return ssh_checkout(f'{data["ip"]}',
                        f'{data["user"]}',
                        f'{data["password"]}',
                        f'rm -rf {data["tst"]}/* {data["out"]}/* {data["folder1"]}/* {data["folder2"]}/*',
                        '')


@pytest.fixture()
def make_bad_arx():
    ssh_checkout(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["password"]}',
                 f'cd {data["tst"]}; 7z a {data["out"]}/bad_arx -t{data["type"]}',
                 'Everything is Ok')
    ssh_checkout(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["password"]}',
                 f'truncate -s 1 {data["out"]}/bad_arx.{data["type"]}',
                 '')


@pytest.fixture(autouse=True)
def stat(request):
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    name = request.node.name
    out = ssh_checkout_get(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                           f'echo "2222" | sudo -S journalctl --since "{time}"')
    with open('stat.txt', 'a', encoding='utf-8') as f, open('/proc/loadavg', 'r', encoding='utf-8') as fr:
        f.write(
            f'{name}\nвремя начала: {time}\nколичество = {data["count"]}, размер = {data["bs"]}\nзагрузка CPU: {fr.readlines()[-1]} \nOUT: \n{out} \n\n')


@pytest.fixture(autouse=True, scope='module')
def deploy():
    res = []
    upload_files(f'{data["ip"]}',
                 f'{data["user"]}',
                 f'{data["password"]}',
                 '/home/user/p7zip-full.deb',
                 '/home/user2/p7zip-full.deb')
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["password"]}',
                            'echo "2222" | sudo -S dpkg -i /home/user2/p7zip-full.deb',
                            'Настраивается пакет'))
    res.append(ssh_checkout(f'{data["ip"]}',
                            f'{data["user"]}',
                            f'{data["password"]}',
                            'echo "2222" | sudo -S dpkg -s p7zip-full',
                            'Status: install ok installed'))
    # res.append(ssh_checkout(f'{data["ip"]}',
    #                         f'{data["user"]}',
    #                         f'{data["password"]}',
    #                         'echo "2222" | sudo apt install libarchive-zip-perl',
    #                         ''))
    return all(res)
