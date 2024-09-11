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

    # 色設定
    elif cmd[0] == "set":
        for i in range(len(mw.set_tab)/4):
            if mw.set_tab.tab[i]["text"] == "":  # 行が未完成の場合
                for j in range(1, 3):  # 時間、文字色、背景色の順に登録
                    mw.set_tab.x = j
                    mw.set_tab.y = i
                    mw.set_tab.tab[4*i+j].update(cmd[j])  # 入力データが有効か判断する必要あり
                break
        mw.set_tab.update()

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
