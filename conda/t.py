from subprocess import call, TimeoutExpired


def main():
    try:
        call(['python', 'count.py'], timeout=5)
    except TimeoutExpired:
        pass


if __name__ == '__main__':
    main()
