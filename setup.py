import sys
import cx_Freeze

"""
exeファイル作成
ターミナルで以下のコマンドを実行
python setup.py build

参考にしたサイト
https://af-e.net/cxfreeze-how-to-use/
https://af-e.net/cxfreeze-console-hidden/
https://af-e.net/cxfreeze-lightweight/#index_id12
"""

base = None

if sys.platform == "win32":
    base = "Win32GUI"         # コンソール非表示

# スクリプトの設定
exe = cx_Freeze.Executable(
    script="main.py",
    base=base
)

# オプション
options = {
    "optimize": 2,  # 最適化
    "include_files": [],  # ファイルの追加
    "packages":  ["tkinter", ],  # 取り込みたいパッケージ
    "zip_include_packages": []
}

# exeファイルの生成
cx_Freeze.setup(
    name="CountUp_Timer",
    version="1.0",
    description="Count Up Timer",
    options={"build_exe": options},
    executables=[exe],
)