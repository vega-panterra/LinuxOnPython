import subprocess
import zlib

tst = '/home/user/tst'
out = '/home/user/out'
folder1 = '/home/user/folder1'
folder2 = '/home/user/folder2'


def stdout(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    return result.stdout


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    result1 = checkout(f'cd {tst}; 7z a {out}/arx2', 'Everything is Ok')
    result2 = checkout(f'cd {out}; ls', 'arx2.7z')
    assert result1 and result2, 'test1 FAIL'


def test_step2():
    # test2
    result1 = checkout(f'cd {out}; 7z l arx2.7z', 'file1.txt')
    result2 = checkout(f'cd {out}; 7z l arx2.7z', 'new_file.txt')
    assert result1 and result2, 'test2 FAIL'


def test_step3():
    # test3
    result1 = checkout(f'cd {out}; 7z e arx2.7z -o{folder1} -y', 'Everything is Ok')
    result2 = checkout(f'cd {folder1}; ls', 'file1.txt')
    result3 = checkout(f'cd {folder1}; ls', 'new_file.txt')
    assert result1 and result2 and result3, 'test3 FAIL'


def test_step4():
    # test4
    result1 = checkout(f'cd {out}; 7z x arx2.7z -o{folder2} -y', 'Everything is Ok')
    result2 = checkout(f'cd {folder2}; ls', 'file1.txt')
    result3 = checkout(f'cd {folder2}; ls', 'new_file.txt')
    assert result1 and result2 and result3, 'test4 FAIL'


def test_step5():
    # test5
    assert checkout(f'cd {out}; 7z t arx2.7z', 'Everything is Ok'), 'test5 FAIL'


def test_step6():
    # test6
    assert checkout(f'cd {tst}; 7z u {out}/arx2.7z', 'Everything is Ok'), 'test6 FAIL'


def test_step7():
    # test7
    result1 = checkout(f'7z h {out}/arx2.7z', 'Everything is Ok')
    result2 = stdout(f'crc32 {out}/arx2.7z').upper()
    result3 = checkout(f'7z h {out}/arx2.7z', result2)
    assert result1 and result3, 'test7 FAIL'


def test_step8():
    # test8
    assert checkout('cd /home/user/out; 7z d arx2.7z', 'Everything is Ok'), 'test8 FAIL'
