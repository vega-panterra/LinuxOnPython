import subprocess


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


def test_step1():
    # test1
    assert checkout('cd home/user/tst; 7z a ../out/arx2', 'Everything is Ok'), 'test1 FAIL'

