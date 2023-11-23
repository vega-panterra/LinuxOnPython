import string
import random
from datetime import datetime

import pytest
import yaml

from checkers import checkout, stdout

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture(autouse=True, scope='module')  # function, class, module
def make_folders():
    return checkout(f'mkdir -p {data["tst"]} {data["out"]} {data["folder1"]} {data["folder2"]}', '')


@pytest.fixture(autouse=True, scope='class')
def make_files():
    list_of_files = []
    for i in range(data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout(f'cd {data["tst"]}; dd if=/dev/urandom of={filename} bs={data["bs"]} count=1 iflag=fullblock', ''):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture(autouse=True, scope='module')
def clear_folders():
    return checkout(f'rm -rf {data["tst"]}/* {data["out"]}/* {data["folder1"]}/* {data["folder2"]}/*', '')


@pytest.fixture()
def make_bad_arx():
    checkout(f'cd {data["tst"]}; 7z a {data["out"]}/bad_arx -t{data["type"]}', 'Everything is Ok')
    checkout(f'truncate -s 1 {data["out"]}/bad_arx.{data["type"]}', 'Everything is Ok')
    yield 'bad_arx'
    checkout(f'rm -f {data["out"]}/bad_arx.{data["type"]}', '')


@pytest.fixture(autouse=True)
def write_stat():
    yield
    stat = stdout('cat /proc/loadavg')
    checkout(f'echo "time: {datetime.now().strftime("%H:%M:%S.%f")} | count: {data["count"]} | size: {data["bs"]} | load: {stat}" >> stat.txt', '')
