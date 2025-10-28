import tkinter as tk
from functools import partial as pt
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
    def __init__(self: tk.Tk, master, tim="00:00:00.00"):
        super().__init__(master)
        self.pack()

        # 定義
        self.txt = tim                       # 表示時間
        self.dsp = tk.Label(self.master)     # 表示ラベル
        self.now = tk.Button(self.master)    # 現在時刻ボタン
        self.rst = tk.Button(self.master)    # 初期化ボタン
        self.ook = tk.Button(self.master)    # 決定ボタン
        self.ccl = tk.Button(self.master)    # 取消ボタン
        self.csr = tk.Label(self.master)     # カーソル
        self.plc = 0                         # カーソル位置

        # ウインドウの定義
        self.master.title(lg.mwn)            # ウインドウタイトル
        self.master.geometry("400x240")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()
        self.event()

    # ウィジェット
    def widgets(self):
        # 設定
        self.dsp.configure(text=self.txt, font=("", 60))
        self.now.configure(text=lg.now, width=10, command=self.ps_nw)
        self.rst.configure(text=lg.rst, width=10, command=self.ps_rs)
        self.ook.configure(text=lg.ook, width=10, command=self.ps_ok)
        self.ccl.configure(text=lg.ccl, width=10, command=self.ps_cn)
        self.csr.configure(bg="black", width=1, font=("", 40))

        # 配置
        self.dsp.place(x=15, y=20)
        self.now.place(x=120, y=150)
        self.rst.place(x=210, y=150)
        self.ook.place(x=210, y=190)
        self.ccl.place(x=300, y=190)
        # self.csr.place(x=22, y=100, height=2)

    # イベント
    def event(self):
        self.master.bind("<KeyPress>", self.ps_ky)
        self.dsp.bind("<ButtonPress>", self.ck_dp)

    # 文字クリック
    def ck_dp(self, e):
        if e.num == 1:                                             # 左クリック
            if e.x < 90:                                           # hh
                k = int(self.txt[0]) * 10 + int(self.txt[1]) + 1   # インクリメント
                if k >= 100:                                       # 100時間を超えた場合
                    k = 0                                          # 0時間
                self.txt = str(k).zfill(2) + self.txt[2:]          # 文字列に戻す
            elif e.x < 187:                                        # mm
                k = int(self.txt[3]) * 10 + int(self.txt[4]) + 1   # インクリメント
                if k >= 60:                                        # 60分を超えた場合
                    k = 0                                          # 0分
                self.txt = self.txt[:3] + str(k).zfill(2) + self.txt[5:]  # 文字列化
            elif e.x < 282:                                        # ss
                k = int(self.txt[6]) * 10 + int(self.txt[7]) + 1   # インクリメント
                if k >= 60:                                        # 60秒を超えた場合
                    k = 0                                          # 0秒
                self.txt = self.txt[:6] + str(k).zfill(2) + self.txt[8:]  # 文字列化
            else:                                                  # ms
                k = int(self.txt[9]) * 10 + int(self.txt[10]) + 1  # インクリメント
                if k >= 100:                                       # 1秒を超えた場合
                    k = 0                                          # 0秒
                self.txt = self.txt[:9] + str(k).zfill(2)          # 文字列化
        elif e.num == 3:                                           # 右クリック
            if e.x < 90:                                           # hh
                k = int(self.txt[0]) * 10 + int(self.txt[1]) - 1   # デクリメント
                if k < 0:                                          # 0時間未満の場合
                    k = 99                                         # 99時間
                self.txt = str(k).zfill(2) + self.txt[2:]          # 文字列に戻す
            elif e.x < 187:                                        # mm
                k = int(self.txt[3]) * 10 + int(self.txt[4]) - 1   # デクリメント
                if k < 0:                                          # 0分未満の場合
                    k = 59                                         # 59分
                self.txt = self.txt[:3] + str(k).zfill(2) + self.txt[5:]  # 文字列化
            elif e.x < 282:                                        # ss
                k = int(self.txt[6]) * 10 + int(self.txt[7]) - 1   # デクリメント
                if k < 0:                                          # 0秒未満の場合
                    k = 59                                         # 59秒
                self.txt = self.txt[:6] + str(k).zfill(2) + self.txt[8:]  # 文字列化
            else:                                                  # ms
                k = int(self.txt[9]) * 10 + int(self.txt[10]) - 1  # デクリメント
                if k < 0:                                          # 0秒未満の場合
                    k = 99                                         # 0.99秒
                self.txt = self.txt[:9] + str(k).zfill(2)          # 文字列化
        self.dsp.configure(text=self.txt)

    # キーボード押下
    def ps_ky(self, e):
        if e.keysym == "Right":
            self.mv_cs(self.plc + 1)
        elif e.keysym == "Left":
            self.mv_cs(self.plc - 1)

    # カーソル移動
    def mv_cs(self, m):
        n = m % 8
        l = [22, 60, 118, 156, 214, 252, 310, 348]
        self.csr.place(x=l[n], y=100, height=2)
        self.plc = n

    # 現在時刻押下
    def ps_nw(self):
        t = Time()
        t.get_now()
        self.txt = t.out_txt()
        self.dsp.configure(text=self.txt)

    # 初期化押下
    def ps_rs(self):
        self.txt = "00:00:00.00"
        self.dsp.configure(text=self.txt)

    # 決定押下
    def ps_ok(self):
        self.master.quit()
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.txt = None
        self.master.quit()
        self.master.destroy()


# 時間変更関数
def asktime(tim=None):
    root = tk.Tk()
    app = ChanTimeWin(master=root, tim=tim)
    app.mainloop()
    return app.txt
