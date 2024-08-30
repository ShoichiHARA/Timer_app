import tkinter as tk
# from tkinter import ttk
from functools import partial
import language as lg
import timer as tm


# 設定クラス
class Setting:
    def __init__(self):
        self.lg = "JPN"
        self.clr0 = "#000000"
        self.bgc0 = "#FFFFFF"
        self.row = 6


# メインウインドウクラス
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラス継承
        self.pack()               # 配置

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.keys = []                      # キーボードの状態
        self.now = tm.Time()
        self.siz = 10                       # 大きさ
        self.clr = self.set.clr0            # 文字色
        self.bgc = self.set.bgc0            # 背景色
        self.cnt = False                    # カウントアップ
        self.ftb = tk.Frame(self.master, bg="black")    # 表用のフレーム
        self.set_tab = []                       # 表
        self.set_tab_num = self.set.row * 4     # 表行列数
        self.set_tab_txt = [""] * self.set_tab_num  # 表の文字列
        self.set_tab_xy = 0                     # 表選択座標
        self.rsv_tab = []
        self.rsv_tab_num = self.set.row * 3
        self.rsv_tab_txt = [""] * self.rsv_tab_num  # 予約表の文字列
        self.rsv_tab_xy = 0                     # 予約表選択座標
        self.pxy = 0  # 選択座標
        self.tmr = tm.Time()                # タイマー
        self.set_tmr = tm.Time()            # 設定用タイマー

        self.bt0 = tk.Button(self.master, text="Button", command=self.tm_win)  # ボタン1
        self.bt1 = tk.Button(self.master, text=self.lg.stt, command=self.bt1_ps)   # ボタン2
        self.bt2 = tk.Button(self.master, text=self.lg.rst, command=self.bt2_ps)   # ボタン3
        self.bt3 = tk.Button(self.master, text="Button")

        # ウインドウの定義
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.set_table()                     # 表作成
        self.widgets()                       # ウィジェット
        self.event()                         # イベント

        # サブウインドウの定義
        self.tm_mas = None  # タイマー表示マスター
        self.tm_app = None
        self.ch_mas = None  # タイマー文字変更マスター
        self.ch_app = None

        # 現在時刻取得
        self.now.get_now()

    # ウィジェット
    def widgets(self: tk.Tk):
        self.bt0.pack()
        self.bt1.pack()
        self.bt2.pack()
        self.bt3.pack()
        self.ftb.pack()

    # 設定表の生成
    def set_table(self: tk.Tk):
        # 表の選択
        def clk_tab(e, xy):
            self.set_tab_xy = xy
            x = xy % 4
            y = xy // 4
            # print("x=" + str(x) + ", y=" + str(y))
            if y != 0:
                if x == 1:  # 時間列
                    self.ch_tm_win()
                elif x in [2, 3]:  # 文字色列、背景色列
                    self.ch_cl_win()

        # 行の番号付け
        def row_num():
            for i in range(1, len(self.set_tab)/4):
                if self.set_tab[i*4+1]["text"] == "":  # 時間列が空白の場合
                    pass
                elif self.set_tab[i*4+2]["text"] == "":  # 文字色列が空白の場合
                    pass
                elif self.set_tab[i*4+3]["text"] == "":  # 背景色列が空白の場合
                    pass
                else:  # 列に空白がない場合
                    self.set_tab[i*4].configure(text=str(i))

        self.set_tab_txt[0] = "No."
        self.set_tab_txt[1] = self.lg.tim  # 列名：時間
        self.set_tab_txt[2] = self.lg.clr  # 列名：文字色
        self.set_tab_txt[3] = self.lg.bgc  # 列名：背景色
        self.set_tab_txt[5] = self.set_tmr.out_txt()  # タイマー初期値
        self.set_tab_txt[6] = self.set.clr0           # 文字色初期値
        self.set_tab_txt[7] = self.set.bgc0           # 背景色初期値

        # 一行目
        for i in range(4):
            self.set_tab.append(
                tk.Label(
                    self.ftb, bd=2, width=7, height=1, bg="silver",
                    text=self.set_tab_txt[i], font=("", 9)
                )
            )

        # 二行目以降
        for i in range(4, self.set_tab_num):
            self.set_tab.append(tk.Label(self.ftb, bd=2, width=7, height=1, font=("", 9)))
        self.upd_tab1()  # 表を更新して表示

        # 表の配置
        for i in range(self.set_tab_num):
            self.set_tab[i].grid(row=i//4, column=i%4, padx=1, pady=1)
            self.set_tab[i].bind("<Button-1>", partial(clk_tab, xy=i))

    # 表の更新
    def upd_tab1(self, txt=None):
        # 変更セルの座標
        x = self.pxy % 4
        y = self.pxy // 4

        # 表の文字変更
        if txt is not None:
            # 表の文字変更
            self.set_tab[self.pxy].configure(text=txt)
            print(self.set_tab[self.pxy]["text"])

            # セルの色付け
            if x in [2, 3]:
                if txt != "":
                    self.set_tab[self.pxy].configure(bg=txt)

        # 行の番号付け
        if self.set_tab[y*4+1]["text"] == "":  # 時間列が空白の場合
            pass
        elif self.set_tab[y*4+2]["text"] == "":  # 文字色列が空白の場合
            pass
        elif self.set_tab[y*4+3]["text"] == "":  # 背景色列が空白の場合
            pass
        else:  # 列に空白がない場合
            self.set_tab[y*4].configure(text=str(y))

    # 表の更新
    def upd_tab(self):
        # 番号付け
        for i in range(1, self.set_tab_num//4):
            if self.set_tab_txt[i*4+1] == "":
                pass
            elif self.set_tab_txt[i*4+2] == "":
                pass
            elif self.set_tab_txt[i*4+3] == "":
                pass
            else:
                print(i)
                self.set_tab_txt[i*4] = str(i)

        # 表の表示
        for i in range(4, self.set_tab_num):
            self.set_tab[i].configure(text=self.set_tab_txt[i])  # テキスト変更
            if i%4 in [2, 3]:  # 色の行
                if self.set_tab_txt[i] != "":  # 空白でない場合
                    self.set_tab[i].configure(bg=self.set_tab_txt[i])  # ラベル色変更
        print(self.set_tab[1]["text"])

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

    # 時間変更ウインドウ表示
    def ch_tm_win(self):
        if self.ch_mas is None:
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanTimeWin(self.ch_mas, self)
        elif not self.ch_mas.winfo_exists():
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanTimeWin(self.ch_mas, self)

    # 色変更ウインドウ表示
    def ch_cl_win(self):
        if self.ch_mas is None:
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanColorWin(self.ch_mas, self)
        elif not self.ch_mas.winfo_exists():
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanColorWin(self.ch_mas, self)

    def bt1_ps(self):
        self.cnt = not self.cnt
        if self.cnt:
            self.bt1.configure(text=self.lg.stp)
        else:
            self.bt1.configure(text=self.lg.stt)

    def bt2_ps(self):
        self.tmr.set_tmr(h=0, m=0, s=0, ms=0)

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
                self.now.get_now()
                print(self.now.out_txt())

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
        self.mw = mw                        # メインウインドウ
        self.wwd = 400                      # ウインドウ幅
        self.whg = 300                      # ウインドウ高
        self.cvs = tk.Canvas(self.master, bg=self.mw.bgc)  # キャンバス

        # ウインドウの定義
        self.master.title(self.mw.lg.twn)
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
        if self.mw.cnt:  # カウントが有効の場合
            pnm = self.mw.now.ms  # 前回のミリ秒
            self.mw.now.get_now()         # 現在時刻取得
            if pnm != self.mw.now.ms:  # ミリ秒が進んでいる場合
                self.mw.tmr.cnt_tmr()      # 時間カウント
        self.mw.tmr.out_seg(self.cvs, self.mw.clr, self.mw.bgc, self.wwd/2, self.whg/2, self.mw.siz)

        # self.seg.place(self.wwd/2, self.whg/2, self.mw.siz)

        self.master.after(10, self.re_frm)  # 0.01s後再描画

    # イベント
    def event(self):
        def win_size(e):
            self.e = e  # エラー処理(仮)
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.mw.siz = self.wwd // 110

        self.bind("<Configure>", win_size)


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw  # メインウインドウ
        self.tmr = tm.Time()
        self.dsp = tk.Label(master=master, text="00:00:00.0", font=("", 60, ))
        self.bt_ch = [None] * 14
        self.bt_ch[0] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("a"))
        self.bt_ch[1] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("b"))
        self.bt_ch[2] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("c"))
        self.bt_ch[3] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("d"))
        self.bt_ch[4] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("e"))
        self.bt_ch[5] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("f"))
        self.bt_ch[6] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("g"))
        self.bt_ch[7] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("h"))
        self.bt_ch[8] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("i"))
        self.bt_ch[9] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("j"))
        self.bt_ch[10] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("k"))
        self.bt_ch[11] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("l"))
        self.bt_ch[12] = tk.Button(self.master, text=" ↑ ", command=lambda: self.ps_ch("m"))
        self.bt_ch[13] = tk.Button(self.master, text=" ↓ ", command=lambda: self.ps_ch("n"))
        self.bt_ok = tk.Button(
            self.master, width=10, text=self.mw.lg.ook, command=self.ps_ok
        )
        self.bt_cn = tk.Button(
            self.master, width=10, text=self.mw.lg.ccl, command=self.ps_cn
        )

        # ウインドウの定義
        self.master.title(self.mw.lg.mwn)    # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()

    def widgets(self: tk.Tk):
        self.dsp.place(x=40, y=80)
        self.bt_ok.place(x=200, y=250)
        self.bt_cn.place(x=300, y=250)

        p = [
            [48, 60], [48, 165], [88, 60], [88, 165],
            [144, 60], [144, 165], [184, 60], [184, 165],
            [240, 60], [240, 165], [280, 60], [280, 165],
            [336, 60], [336, 165]
        ]
        for i in range(14):
            self.bt_ch[i].place(x=p[i][0], y=p[i][1])

    def ps_ch(self, e):
        if e == "a":  # 時間十の位を増加
            self.tmr.h += 10
        elif e == "b":  # 時間十の位を減少
            self.tmr.h -= 10
        elif e == "c":  # 時間一の位を増加
            self.tmr.h += 1
        elif e == "d":  # 時間一の位を減少
            self.tmr.h -= 1
        elif e == "e":  # 分十の位を増加
            self.tmr.m += 10
        elif e == "f":  # 分十の位を減少
            self.tmr.m -= 10
        elif e == "g":  # 分一の位を増加
            self.tmr.m += 1
        elif e == "h":  # 分一の位を減少
            self.tmr.m -= 1
        elif e == "i":  # 秒十の位を増加
            self.tmr.s += 10
        elif e == "j":  # 秒十の位を減少
            self.tmr.s -= 10
        elif e == "k":  # 秒一の位を増加
            self.tmr.s += 1
        elif e == "l":  # 秒一の位を減少
            self.tmr.s -= 1
        elif e == "m":  # ミリ秒を増加
            self.tmr.ms += 1
        elif e == "n":  # ミリ秒を減少
            self.tmr.ms -= 1
        self.tmr.chk_tmr()
        self.dsp.configure(text=self.tmr.out_txt())

    # 決定押下
    def ps_ok(self):
        self.mw.set_tmr = self.tmr
        self.mw.set_tab_txt[self.mw.set_tab_xy] = self.tmr.out_txt()
        self.mw.upd_tab1(self.tmr.out_txt())
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.master.destroy()


# 色変更ウインドウ
class ChanColorWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw
        self.clr = [0, 0, 0]  # r, g, b
        self.ccd = "black"
        self.sc_r = tk.Scale(
            self.master, from_=0, to=255, length=200,
            orient="horizontal", command=self.ch_sc
        )
        self.sc_g = tk.Scale(
            self.master, from_=0, to=255, length=200,
            orient="horizontal", command=self.ch_sc
        )
        self.sc_b = tk.Scale(
            self.master, from_=0, to=255, length=200,
            orient="horizontal", command=self.ch_sc
        )
        self.dsp = tk.Label(
            self.master, width=10, height=6, bg=self.ccd
        )
        self.bt_ok = tk.Button(
            self.master, width=10, text=self.mw.lg.ook, command=self.ps_ok
        )
        self.bt_cn = tk.Button(
            self.master, width=10, text=self.mw.lg.ccl, command=self.ps_cn
        )

        # ウインドウの定義
        self.master.title(self.mw.lg.mwn)
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        self.widgets()

    def widgets(self):
        self.sc_r.place(x=50, y=50)
        self.sc_g.place(x=50, y=100)
        self.sc_b.place(x=50, y=150)
        self.dsp.place(x=280, y=80)
        self.bt_ok.place(x=200, y=250)
        self.bt_cn.place(x=300, y=250)

    # カラーコード変換
    def c_code(self, r=None, g=None, b=None):
        if r is not None:
            self.clr[0] = r
        if g is not None:
            self.clr[1] = g
        if b is not None:
            self.clr[2] = b
        self.ccd = f"#{self.clr[0]:02X}{self.clr[1]:02X}{self.clr[2]:02X}"

    # スライドバー移動
    def ch_sc(self, n):
        self.clr[0] = self.sc_r.get()
        self.clr[1] = self.sc_g.get()
        self.clr[2] = self.sc_b.get()
        self.c_code()
        self.dsp.configure(bg=self.ccd)

    # 決定押下
    def ps_ok(self):
        self.mw.set_tab_txt[self.mw.set_tab_xy] = self.ccd
        self.mw.upd_tab()
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.master.destroy()


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
