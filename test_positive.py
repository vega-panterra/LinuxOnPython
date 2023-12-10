import yaml

from checkers import ssh_checkout, ssh_checkout_get

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_files):
        # test1
        result1 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["tst"]}; 7z a {data["out"]}/arx2 -t{data["type"]}',
                               f'{data["valid"]}')
        result2 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["out"]}; ls', f'arx2.{data["type"]}')
        assert result1 and result2, 'test1 FAIL'

    def test_step2(self, make_files):
        # test2
        result1 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["out"]}; 7z l arx2.{data["type"]}', make_files[0])
        result2 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["out"]}; 7z l arx2.{data["type"]}', make_files[1])
        assert result1 and result2, 'test2 FAIL'

    def test_step3(self, make_files):
        # test3
        result1 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["out"]}; 7z e arx2.{data["type"]} -o{data["folder1"]} -y',
                               f'{data["valid"]}')
        result2 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["folder1"]}; ls', make_files[0])
        assert result1 and result2, 'test3 FAIL'

    def test_step4(self, make_files):
        # test4
        result1 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["out"]}; 7z x arx2.{data["type"]} -o{data["folder2"]} -y',
                               f'{data["valid"]}')
        result2 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["folder2"]}; ls', make_files[0])
        result3 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'cd {data["folder2"]}; ls', make_files[1])
        assert result1 and result2 and result3, 'test4 FAIL'

    def test_step5(self):
        # test5
        assert ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                            f'cd {data["out"]}; 7z t arx2.{data["type"]}',
                            f'{data["valid"]}'), 'test5 FAIL'

    def test_step6(self):
        # test6
        assert ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                            f'cd {data["tst"]}; 7z u {data["out"]}/arx2.{data["type"]}',
                            f'{data["valid"]}'), 'test6 FAIL'

    def test_step7(self):
        # test7
        result1 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'7z h {data["out"]}/arx2.{data["type"]}',
                               f'{data["valid"]}')
        hash_crc32 = ssh_checkout_get(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                                      f'crc32 {data["out"]}/arx2.{data["type"]}').upper()
        result3 = ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                               f'7z h {data["out"]}/arx2.{data["type"]}', hash_crc32)
        assert result1 and result3, 'test7 FAIL'

    def test_step8(self):
        # test8
        assert ssh_checkout(f'{data["ip"]}', f'{data["user"]}', f'{data["password"]}',
                            f'cd /home/user/out; 7z d arx2.{data["type"]}',
                            f'{data["valid"]}'), 'test8 FAIL'
