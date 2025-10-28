import application as app
import functions as fnc
import application1 as app1

"""
exe化は、以下のコマンドをターミナルで実行
pyinstaller main.py --onefile --noconsole
"""


def main():
    app.application()


if __name__ == "__main__":
    main()

