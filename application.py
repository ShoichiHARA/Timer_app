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
        self.siz = 1                        # 大きさ
        self.bt0 = tk.Button(self.master, text="Button", command=self.tm_win)  # ボタン1

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
        self.cvs = tk.Canvas(self.master, bg="white")  # キャンバス
        self.seg = SevenSeg(cvs=self.cvs)

        # ウインドウの定義
        self.master.title(self.lg.twn)
        self.master.geometry("400x300")
        self.widgets()  # ウィジェット

        self.re_frm()

    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs.pack(fill=tk.BOTH, expand=True)
        self.seg.place(200, 150, 10)

    # 画面更新
    def re_frm(self):
        self.mw.get_now()
        self.cvs.delete("all")

        self.seg.set_num(self.mw.now["msc"])
        self.seg.place(200, 150, 10)

        # print(datetime.datetime.now())

        self.master.after(10, self.re_frm)  # 0.01s後再描画


# 7セグクラス
class SevenSeg:
    def __init__(self, tag="", cvs=None, num=0, clr="black"):
        # 定義
        self.num = None  # 数値
        self.clr = None  # 色
        self.tag = tag   # タグ
        self.cvs = cvs   # キャンバス
        self.seg = [None] * 7
        self.cls = [None] * 7
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
        self.set_num(num)  # 数値
        self.set_clr(clr)  # 色
        self.set_bit()     # セグの設定

    # 数値の設定
    def set_num(self, num):
        self.num = num % 10  # 一の位
        self.set_bit()

    # 色の設定
    def set_clr(self, clr):
        self.clr = clr
        self.set_bit()

    def set_bit(self):
        for i in range(7):
            if self.bit[self.num][i] == 0:
                self.cls[i] = "white"
            else:
                self.cls[i] = self.clr

    # 配置
    def place(self, x, y, s):
        a = 3
        b = 5
        self.seg[0] = self.cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-3)*s+y, a*s+x, (-b-3)*s+y,
            (a+1)*s+x, (-b-2)*s+y, a*s+x, (-b-1)*s+y, -a*s+x, (-b-1)*s+y,
            fill=self.cls[0]
        )
        self.seg[1] = self.cvs.create_polygon(
            (a+1)*s+x, (-b-2)*s+y, (a+2)*s+x, (-b-1)*s+y, (a+2)*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, -s+y, a*s+x, (-b-1)*s+y,
            fill=self.cls[1]
        )
        self.seg[2] = self.cvs.create_polygon(
            (a+1)*s+x, y, (a+2)*s+x, s+y, (a+2)*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+1)*s+y, a*s+x, s+y,
            fill=self.cls[2]
        )
        self.seg[3] = self.cvs.create_polygon(
            (-a-1)*s+x, (b+2)*s+y, -a*s+x, (b+1)*s+y, a*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+3)*s+y, -a*s+x, (b+3)*s+y,
            fill=self.cls[3]
        )
        self.seg[4] = self.cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, s+y, -a*s+x, (b+1)*s+y,
            (-a-1)*s+x, (b+2)*s+y, (-a-2)*s+x, (b+1)*s+y, (-a-2)*s+x, s+y,
            fill=self.cls[4]
        )
        self.seg[5] = self.cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-1)*s+y, -a*s+x, -s+y,
            (-a-1)*s+x, y, (-a-2)*s+x, -s+y, (-a-2)*s+x, (-b-1)*s+y,
            fill=self.cls[5]
        )
        self.seg[6] = self.cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, -s+y, a*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, s+y, -a*s+x, s+y,
            fill=self.cls[6]
        )


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
