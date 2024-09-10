from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk

if TYPE_CHECKING:
    from application import MainWin


# コマンド入力
def command(mw: MainWin, cmd: str):
    cmd = cmd.split()
    err = 0

    # 予約設定
    if cmd[0] == "rsv":
        pass

    # 設定
    elif cmd[0] == "set":
        pass

    # 現在値変更
    elif cmd[0] == "tmr":
        err = mw.tmr.set_txt(cmd[1])
        print(mw.tmr.out_txt())

    # 表示ウインドウ表示
    elif cmd[0] == "view":
        mw.viw_win()

    # エラー処理
    if err != 0:
        print("err", err)
    else:
        print("else")
        mw.etr.delete(0, "end")
        # mw.master.attributes("-topmost", True)
        # mw.master.attributes("-topmost", False)
        mw.master.focus_set()
        mw.etr.focus_set()  # 入力欄にフォーカスを設定したい
