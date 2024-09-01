import sys
import cx_Freeze

"""
exeファイル作成
ターミナルで以下のコマンドを実行
python setup.py build

参考にしたサイト
https://af-e.net/cxfreeze-how-to-use/
"""

base = None

if sys.platform == "win32":
    base = "Win32GUI"

# スクリプトの設定
exe = cx_Freeze.Executable(
    script="main.py",
    base=base
)

# オプション
options = {
    # "base": "Win32GUI",         # コンソール非表示
    # "include_files": [("image", "image")]  # ファイルの追加
}

# exeファイルの生成
cx_Freeze.setup(
    name="CountUp_Timer",
    version="1.0",
    description="converter",
    options={"build_exe": options},
    executables=[cx_Freeze.Executable("main.py", base="Win32GUI")],
)