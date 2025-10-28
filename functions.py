import tkinter as tk
from functools import partial
from datetime import datetime
import os
import global_val as g


# 言語設定
lg = g.lg


# 時間クラス
class Time:
    def __init__(self, n=0):
        self.n = n  # 00:00:00.00~99:59:59.99をint型に

    # 整数型から時間を登録
    def set_int(self, n: int):
        while n < 0 or 36000000 <= n:  # 範囲内にない間繰り返し
            if n < 0:                  # 0より小さい場合
                n += 36000000          # 100時間加算
            if n >= 36000000:          # 100時間より大きい場合
                n -= 36000000          # 100時間減算
        self.n = n                     # 代入

    # テキストから時間を登録
    def set_txt(self, t: str):
        try:
            self.n = int(t[9:11])           # ms
            self.n += int(t[6:8]) * 100     # s
            self.n += int(t[3:5]) * 6000    # m
            self.n += int(t[0:2]) * 360000  # h
        except IndexError:
            print("Time.set_txt Error!", IndexError)
            return 901
        except ValueError:
            print("Time.set_txt Error!", ValueError)
            return 902

    # 現在時刻取得
    def get_now(self):
        n = datetime.now()
        self.n = n.microsecond // 10000
        self.n += n.second * 100
        self.n += n.minute * 6000
        self.n += n.hour * 360000

    # テキスト出力
    def out_txt(self):
        n = self.n
        t = str(n % 100).zfill(2)                      # ---------ms
        t = str(n // 100 % 60).zfill(2) + "." + t      # ------ss.ms
        t = str(n // 6000 % 60).zfill(2) + ":" + t     # ---mm:ss.ms
        t = str(n // 360000 % 100).zfill(2) + ":" + t  # hh:mm:ss.ms
        return t


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, tim=None):
        super().__init__(master)
        self.pack()

        # 定義
        if tim is None:
            self.tim = Time()
        else:
            self.tim = tim                   # 表示時間
        self.dsp = tk.Label(self.master)     # 表示ラベル
        self.now = tk.Button(self.master)    # 現在時刻ボタン
        self.rst = tk.Button(self.master)    # 初期化ボタン
        self.ook = tk.Button(self.master)    # 決定ボタン
        self.ccl = tk.Button(self.master)    # 取消ボタン

        # ウインドウの定義
        self.master.title(lg.mwn)            # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()
        self.event()

    # ウィジェット
    def widgets(self):
        # 設定
        self.dsp.configure(text=self.tim.out_txt(), font=("", 60))
        self.now.configure(text=lg.now, width=10)
        self.rst.configure(text=lg.rst, width=10)
        self.ook.configure(text=lg.ook, width=10)
        self.ccl.configure(text=lg.ccl, width=10)

        # 関数割り当て


        # 配置
        self.dsp.place(x=15, y=80)
        self.now.place(x=120, y=210)
        self.rst.place(x=210, y=210)
        self.ook.place(x=210, y=250)
        self.ccl.place(x=300, y=250)

    # イベント
    def event(self):
        self.dsp.bind("<ButtonPress>", self.ck_dp)
        # self.dsp.bind("<Motion>", self.ck_dp)

    # 文字クリック
    def ck_dp(self, e):
        print(e.x, e.y)
        if e.num == 1:
            if e.x < 90:
                self.tim.set_int(self.tim.n + 360000)
            elif e.x < 187:
                self.tim.set_int(self.tim.n + 6000)
            elif e.x < 282:
                self.tim.set_int(self.tim.n + 100)
            else:
                self.tim.set_int(self.tim.n + 1)
        elif e.num == 3:
            if e.x < 90:
                self.tim.set_int(self.tim.n - 360000)
            elif e.x < 187:
                self.tim.set_int(self.tim.n - 6000)
            elif e.x < 282:
                self.tim.set_int(self.tim.n - 100)
            else:
                self.tim.set_int(self.tim.n - 1)
        print(self.tim.n)
        self.dsp.configure(text=self.tim.out_txt())


# 時間変更関数
def asktime(tim=None):
    root = tk.Tk()
    app = ChanTimeWin(master=root, tim=tim)
    app.mainloop()
    return app.tim
