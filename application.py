import tkinter as tk
from tkinter import ttk
import datetime
import language as lg


# 設定クラス
class Setting:
    def __init__(self):
        self.lg = "JPN"


# メインウインドウクラス
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラス継承
        self.pack()               # 配置

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.keys = []                      # キーボードの状態
        self.now = {
            "y": 0, "m": 0, "d": 0,
            "h": 0, "min": 0, "sec": 0, "msc": 0
        }                    # 現在時刻
        self.siz = 10                       # 大きさ
        self.clr = "black"                  # 文字色
        self.bgc = "white"                  # 背景色
        self.cnt = False                    # カウントアップ
        self.tmr = Time(clr=self.clr, bgc=self.bgc)  # タイマー

        self.bt0 = tk.Button(self.master, text="Button", command=self.tm_win)  # ボタン1
        self.bt1 = tk.Button(self.master, text=self.lg.stt, command=self.bt1_ps)   # ボタン2
        self.bt2 = tk.Button(self.master, text=self.lg.rst, command=self.bt2_ps)   # ボタン3

        # ウインドウの定義
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()                       # ウィジェット
        self.event()                         # イベント

        # サブウインドウの定義
        self.tm_mas = None
        self.tm_app = None

        # 現在時刻取得
        self.get_now()

    # ウィジェット
    def widgets(self: tk.Tk):
        self.bt0.pack()
        self.bt1.pack()
        self.bt2.pack()

    # 終了
    def exit(self):
        self.master.destroy()

    # 表示ウインドウ表示
    def tm_win(self):
        if self.tm_mas is None:
            self.tm_mas = tk.Toplevel(self.master)
            self.tm_app = TMWin(self.tm_mas, self)
        elif not self.tm_mas.winfo_exists():
            self.tm_mas = tk.Toplevel(self.master)
            self.tm_app = TMWin(self.tm_mas, self)

    def bt1_ps(self):
        self.cnt = not self.cnt
        if self.cnt:
            self.bt1.configure(text=self.lg.stp)
        else:
            self.bt1.configure(text=self.lg.stt)

    def bt2_ps(self):
        self.tmr.rst_tim()

    # 現在時刻取得
    def get_now(self):
        now = datetime.datetime.now()
        self.now["y"] = now.year
        self.now["m"] = now.month
        self.now["d"] = now.day
        self.now["h"] = now.hour
        self.now["min"] = now.minute
        self.now["sec"] = now.second
        self.now["msc"] = now.microsecond // 100000

    # 現在時刻カウント
    def cnt_now(self):
        self.now["msc"] += 1                               # +1 -> 100ms
        if self.now["msc"] >= 10:                          # 1000ms超えた場合
            self.now["sec"] += self.now["msc"] // 10       # 繰り上げ
            self.now["msc"] -= self.now["msc"] // 10 * 10  # 繰り上げ分減算
            if self.now["sec"] >= 60:                          # 60秒超えた場合
                self.now["min"] += self.now["sec"] // 60       # 繰り上げ
                self.now["sec"] -= self.now["sec"] // 60 * 60  # 繰り上げ分減算
                if self.now["min"] >= 60:                          # 60分超えた場合
                    self.now["h"] += self.now["min"] // 60         # 繰り上げ
                    self.now["min"] -= self.now["min"] // 60 * 60  # 繰り上げ分減算
        if self.now["min"] == 0:
            if self.now["sec"] == 0:
                if self.now["msc"] == 0:
                    self.get_now()

    # イベント
    def event(self):
        def m_press(e):  # マウスボタン押した場合
            if e.num == 1:  # 左
                pass
            if e.num == 3:  # 右
                pass

        def m_release(e):  # マウスボタン離した場合
            if e.num == 1:  # 左
                pass
            if e.num == 3:  # 右
                pass

        def k_press(e):  # キーボード押した場合
            if e.keysym in self.keys:
                return
            self.keys.append(e.keysym)
            if e.keysym == "space":
                self.now = datetime.datetime.now()
                print(self.now)
                print(self.now.microsecond // 100000)

        def k_release(e):  # キーボード離した場合
            self.keys.remove(e.keysym)
            if e.keysym == "Escape":
                self.exit()  # プログラム終了

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)


# 表示ウインドウ
class TMWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw                        # メインウインドウ
        self.wwd = 400                      # ウインドウ幅
        self.whg = 300                      # ウインドウ高
        self.cvs = tk.Canvas(self.master, bg=self.mw.bgc)  # キャンバス

        # ウインドウの定義
        self.master.title(self.lg.twn)
        self.master.geometry("400x300")
        self.widgets()  # ウィジェット
        self.event()    # イベント

        self.re_frm()

    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs.pack(fill=tk.BOTH, expand=True)

    # 画面更新
    def re_frm(self):
        self.cvs.delete("all")    # 表示リセット
        if self.mw.cnt:
            pnm = self.mw.now["msc"]  # 前回のミリ秒
            self.mw.get_now()         # 現在時刻取得
            if pnm != self.mw.now["msc"]:  # ミリ秒が進んでいる場合
                self.mw.tmr.cnt_tim()         # 時間カウント
        self.mw.tmr.display(self.cvs, self.mw.clr, self.mw.bgc, self.wwd/2, self.whg/2, self.mw.siz)

        # self.seg.set_num(self.mw.now["msc"])
        # self.seg.place(self.wwd/2, self.whg/2, self.mw.siz)

        # print(datetime.datetime.now())

        self.master.after(10, self.re_frm)  # 0.01s後再描画

    # イベント
    def event(self):
        def win_size(e):
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.mw.siz = self.wwd // 110

        self.bind("<Configure>", win_size)


# 時間クラス
class Time:
    def __init__(self, clr="black", bgc="white"):
        self.clr = clr
        self.h = [
            SevenSeg(clr=clr, bgc=bgc),
            SevenSeg(clr=clr, bgc=bgc)
        ]                        # 時間　一の位, 十の位
        self.m = [
            SevenSeg(clr=clr, bgc=bgc),
            SevenSeg(clr=clr, bgc=bgc)
        ]                        # 分　　一の位, 十の位
        self.s = [
            SevenSeg(clr=clr, bgc=bgc),
            SevenSeg(clr=clr, bgc=bgc)
        ]                        # 秒　　一の位, 十の位
        self.ms = SevenSeg(clr=clr, bgc=bgc)  # 秒　　1/10の位

    # 7セグに時間を登録
    def set_tim(self, h=None, m=None, s=None, ms=None):
        if h is not None:
            self.h[0].set_num(h % 10)   # 時間　一の位
            self.h[1].set_num(h // 10)  # 時間　十の位
        if m is not None:
            self.m[0].set_num(m % 10)   # 分　一の位
            self.m[1].set_num(m // 10)  # 分　十の位
        if s is not None:
            self.s[0].set_num(s % 10)   # 秒　一の位
            self.s[1].set_num(s // 10)  # 秒　十の位
        if ms is not None:
            self.ms.set_num(ms)         # 秒　1/10の位

    # 7セグの色を登録
    def set_clr(self, clr, bgc):
        self.clr = clr
        self.h[0].set_clr(clr, bgc)  # 時間　一の位
        self.h[1].set_clr(clr, bgc)  # 時間　十の位
        self.m[0].set_clr(clr, bgc)  # 分　一の位
        self.m[1].set_clr(clr, bgc)  # 分　十の位
        self.s[0].set_clr(clr, bgc)  # 秒　一の位
        self.s[1].set_clr(clr, bgc)  # 秒　十の位
        self.ms.set_clr(clr, bgc)    # 秒　1/10の位

    # カウント
    def cnt_tim(self):
        self.ms.set_num(self.ms.num+1)
        if self.ms.num == 0:  # 1/10秒桁を繰り上げ
            self.s[0].set_num(self.s[0].num+1)
            if self.s[0].num == 0:  # 1秒桁を繰り上げ
                self.s[1].set_num(self.s[1].num+1)
                if self.s[1].num == 6:  # 10秒桁を繰り上げ
                    self.m[0].set_num(self.m[0].num+1)
                    self.s[1].set_num(0)
                    if self.m[0].num == 0:  # 1分桁を繰り上げ
                        self.m[1].set_num(self.m[1].num+1)
                        if self.m[1].num == 6:  # 10分桁を繰り上げ
                            self.h[0].set_num(self.h[0].num+1)
                            self.m[1].set_num(0)
                            if self.h[0].num == 0:  # 1時間桁を繰り上げ
                                self.h[1].set_num(self.h[1].num+1)

    # リセット
    def rst_tim(self):
        self.h[0].set_num(0)  # 時間　一の位
        self.h[1].set_num(0)  # 時間　十の位
        self.m[0].set_num(0)  # 分　一の位
        self.m[1].set_num(0)  # 分　十の位
        self.s[0].set_num(0)  # 秒　一の位
        self.s[1].set_num(0)  # 秒　十の位
        self.ms.set_num(0)    # 秒　1/10の位

    # ディスプレイ表示
    def display(self, cvs, c, b, x, y, s):
        # 色の設定
        self.set_clr(c, b)

        # セグとコロンの配置
        self.h[1].place(cvs, -45*s+x, y, s)
        self.h[0].place(cvs, -33*s+x, y, s)
        cvs.create_rectangle(
            -25*s+x, -4*s+y, -23*s+x, -2*s+y,
            fill=self.clr, width=0
        )
        cvs.create_rectangle(
            -25*s+x, 2*s+y, -23*s+x, 4*s+y,
            fill=self.clr, width=0
        )
        self.m[1].place(cvs, -15*s+x, y, s)
        self.m[0].place(cvs, -3*s+x, y, s)
        cvs.create_rectangle(
            5*s+x, -4*s+y, 7*s+x, -2*s+y,
            fill=self.clr, width=0
        )
        cvs.create_rectangle(
            5*s+x, 2*s+y, 7*s+x, 4*s+y,
            fill=self.clr, width=0
        )
        self.s[1].place(cvs, 15*s+x, y, s)
        self.s[0].place(cvs, 27*s+x, y, s)
        cvs.create_rectangle(
            35*s+x, 6*s+y, 37*s+x, 8*s+y,
            fill=self.clr, width=0
        )
        self.ms.place(cvs, 45*s+x, y, s)


# 7セグクラス
class SevenSeg:
    def __init__(self, num=0, clr="black", bgc="white"):
        # 定義
        self.num = None  # 数値
        self.clr = None  # 文字色
        self.bgc = None  # 背景色
        self.seg = [None] * 7  # セグデータ
        self.cls = [None] * 7  # セグの色データ
        self.bit = [
            [1, 1, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0, 0, 1],
            [0, 1, 1, 0, 0, 1, 1],
            [1, 0, 1, 1, 0, 1, 1],
            [1, 0, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 0, 1, 1]
        ]

        # 初期設定
        self.set_num(num)       # 数値
        self.set_clr(clr, bgc)  # 色
        self.set_bit()          # セグの設定

    # 数値の設定
    def set_num(self, num):
        self.num = num % 10  # 一の位
        self.set_bit()

    # 色の設定
    def set_clr(self, clr, bgc):
        self.clr = clr  # 文字色
        self.bgc = bgc  # 背景色
        self.set_bit()  # セグの設定

    def set_bit(self):
        for i in range(7):
            if self.bit[self.num][i] == 0:
                self.cls[i] = self.bgc
            else:
                self.cls[i] = self.clr

    # 配置
    def place(self, cvs,  x, y, s):
        self.set_bit()
        a = 3
        b = 5
        self.seg[0] = cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-3)*s+y, a*s+x, (-b-3)*s+y,
            (a+1)*s+x, (-b-2)*s+y, a*s+x, (-b-1)*s+y, -a*s+x, (-b-1)*s+y,
            fill=self.cls[0], outline=self.bgc, width=s/5
        )
        self.seg[1] = cvs.create_polygon(
            (a+1)*s+x, (-b-2)*s+y, (a+2)*s+x, (-b-1)*s+y, (a+2)*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, -s+y, a*s+x, (-b-1)*s+y,
            fill=self.cls[1], outline=self.bgc, width=s/5
        )
        self.seg[2] = cvs.create_polygon(
            (a+1)*s+x, y, (a+2)*s+x, s+y, (a+2)*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+1)*s+y, a*s+x, s+y,
            fill=self.cls[2], outline=self.bgc, width=s/5
        )
        self.seg[3] = cvs.create_polygon(
            (-a-1)*s+x, (b+2)*s+y, -a*s+x, (b+1)*s+y, a*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+3)*s+y, -a*s+x, (b+3)*s+y,
            fill=self.cls[3], outline=self.bgc, width=s/5
        )
        self.seg[4] = cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, s+y, -a*s+x, (b+1)*s+y,
            (-a-1)*s+x, (b+2)*s+y, (-a-2)*s+x, (b+1)*s+y, (-a-2)*s+x, s+y,
            fill=self.cls[4], outline=self.bgc, width=s/5
        )
        self.seg[5] = cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-1)*s+y, -a*s+x, -s+y,
            (-a-1)*s+x, y, (-a-2)*s+x, -s+y, (-a-2)*s+x, (-b-1)*s+y,
            fill=self.cls[5], outline=self.bgc, width=s/5
        )
        self.seg[6] = cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, -s+y, a*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, s+y, -a*s+x, s+y,
            fill=self.cls[6], outline=self.bgc, width=s/5
        )


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
