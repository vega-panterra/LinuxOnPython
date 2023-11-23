import subprocess
import yaml

from checkers import checkout_negative

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_bad_arx):
        # test1
        assert checkout_negative(f'cd {data["out"]}; 7z e bad_arx.{data["type"]} -o{data["folder1"]} -y', 'ERRORS'), 'test1 FAIL'

    def test_step2(self, make_bad_arx):
        # test2
        assert checkout_negative(f'cd {data["out"]}; 7z t bad_arx.{data["type"]}', 'ERRORS'), 'test2 FAIL'
