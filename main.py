import subprocess
import string


def check_command(command: str, text: str, mode=0):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = result.stdout
    if result.returncode == 0:
        if mode == 0:
            if text in out:
                return True
            else:
                return False
        else:
            for i in out:
                if i in string.punctuation:
                    out = out.replace(i, ' ')
            lst = out.split()
            if text in lst:
                return True
            else:
                return False
    else:
        return False


if __name__ == '__main__':
    print(check_command('cat /etc/os-release', 'VERSION="22.04.1 LTS (Jammy Jellyfish)"'))
    print(check_command('cat /etc/os-release', 'VERSION="23.02.5 LTS (Jammy Jellyfish)"'))
    print(check_command('cat /etc/os-release', 'VERSION', 1))
    print(check_command('cat /etc/os-release', 'VISION', 1))
