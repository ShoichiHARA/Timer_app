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
        self.now = tm.Time()                # 現在時刻
        self.clr = self.set.clr0            # 文字色
        self.bgc = self.set.bgc0            # 背景色
        self.cnt = False                    # カウントアップ
        self.lst = tk.Label(self.master, text=self.lg.ccr)  # 設定表のラベル
        self.lrv = tk.Label(self.master, text=self.lg.rss)  # 予約表のラベル
        self.set_tab = SetTab(self)         # 設定表
        self.rsv_tab = RsvTab(self)         # 予約表
        self.tmr = tm.Time()                # タイマー
        self.set_tmr = tm.Time()            # 設定用タイマー

        self.bt_dp = tk.Button(
            self.master, text=self.lg.viw, width=20, command=self.tm_win
        )  # 表示ボタン
        self.bt_ss = tk.Button(
            self.master, text=self.lg.stt, font=("", 15),
            width=10, height=2, command=self.ps_ss
        )   # 開始/停止ボタン
        self.bt_rs = tk.Button(
            self.master, text=self.lg.rst, font=("", 15),
            width=10, height=2, command=self.ps_rs
        )   # 初期化ボタン
        self.bt_cv = tk.Button(
            self.master, text=self.lg.ccv, width=20, command=self.ps_cv
        )  # 現在値変更ボタン

        # ウインドウの定義
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("430x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
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
        self.bt_dp.place(x=60, y=100)
        self.bt_ss.place(x=80, y=20)
        self.bt_rs.place(x=230, y=20)
        self.bt_cv.place(x=220, y=100)
        self.lst.place(x=10, y=150)   # 設定表タイトル
        self.set_tab.frm.place(x=10, y=170)  # 設定表
        self.lrv.place(x=250, y=150)  # 予約表タイトル
        self.rsv_tab.frm.place(x=250, y=170)  # 予約表

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
    def ch_tm_win(self, typ):
        if self.ch_mas is None:
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanTimeWin(self.ch_mas, self, typ)
        elif not self.ch_mas.winfo_exists():
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanTimeWin(self.ch_mas, self, typ)

    # 色変更ウインドウ表示
    def ch_cl_win(self, typ):
        if self.ch_mas is None:
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanColorWin(self.ch_mas, self, typ)
        elif not self.ch_mas.winfo_exists():
            self.ch_mas = tk.Toplevel(self.master)
            self.ch_app = ChanColorWin(self.ch_mas, self, typ)

    # 開始/停止ボタン押下
    def ps_ss(self):
        self.cnt = not self.cnt
        if self.cnt:
            self.bt_ss.configure(text=self.lg.stp)
        else:
            self.bt_ss.configure(text=self.lg.stt)

    # 初期化ボタン押下
    def ps_rs(self):
        self.set_tab.crt = 0
        self.tmr.set_tmr(h=0, m=0, s=0, ms=0)

    # 現在値変更ボタン押下
    def ps_cv(self):
        self.ch_tm_win("ccv")

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


# 設定表
class SetTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw
        self.x = None
        self.y = None
        self.crt = 0  # 現在の設定
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []

        # ラベルを表状に生成
        for i in range(self.set.row*4):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=7, height=1, font=("", 9))
            )  # ラベルの生成
            self.tab[i].grid(row=i//4, column=i%4, padx=1, pady=1)  # ラベルを配置
            self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定

        # 列名ラベル設定
        self.tab[0].configure(text="No.", bg="silver")
        self.tab[1].configure(text=self.lg.tim, bg="silver")
        self.tab[2].configure(text=self.lg.clr, bg="silver")
        self.tab[3].configure(text=self.lg.bgc, bg="silver")
        self.tab[4].configure(text="1")
        self.tab[5].configure(text="00:00:00.0")
        self.tab[6].configure(text=self.set.clr0, bg=self.set.clr0)
        self.tab[7].configure(text=self.set.bgc0, bg=self.set.bgc0)

    # 表クリック時動作
    def click(self, e, xy):
        # 座標
        self.x = xy % 4
        self.y = xy // 4

        # クリック有効範囲
        if self.y != 0:  # タイトル行でない
            if self.x == 1:  # 時間列
                if self.y > 1:  # 最初の時間は変更不可
                    self.mw.ch_tm_win("set")  # 時間設定ウインドウ表示
            elif self.x in [2, 3]:  # 文字色列、背景色列
                self.mw.ch_cl_win("set")

    # 表の更新
    def update(self, txt):
        # 表の文字変更
        self.tab[self.y*4+self.x].configure(text=txt)

        # セルの色付け
        if self.x in [2, 3]:
            if txt == "":
                self.tab[self.y*4+self.x].configure(bg="SystemButtonFace")
            else:
                self.tab[self.y*4+self.x].configure(bg=txt)

        # 行の番号付け
        if self.tab[self.y*4+1]["text"] == "":  # 時間列が空白の場合
            self.tab[self.y*4].configure(text="")
        elif self.tab[self.y*4+2]["text"] == "":  # 文字色列が空白の場合
            self.tab[self.y*4].configure(text="")
        elif self.tab[self.y*4+3]["text"] == "":  # 背景色が空白の場合
            self.tab[self.y*4].configure(text="")
        else:  # 行に空白がない場合
            self.tab[self.y*4].configure(text=str(self.y))

        # 座標リセット
        self.x = None
        self.y = None

    # 現在の設定
    def crt_set(self, tmr):
        for i in range(self.set.row-1):
            row = self.crt + 4  # 現在の次の行
            if self.crt+4 > len(self.tab):  # 最終行の場合
                row = 4  # 最初の行
            if self.tab[row]["text"] == "":  # 現在の次が空白の場合
                break
            if tmr.cmp_txt(self.tab[self.crt+5]["text"]) == 0:  # 次の時間と同じ場合
                self.crt += 4  # 現在行更新
                if self.crt > len(self.tab):  # 最終行を超えた場合
                    self.crt = 4
            else:
                break
        return self.tab[self.crt+2]["text"], self.tab[self.crt+3]["text"]


# 予約表
class RsvTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw
        self.x = None
        self.y = None
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []

        # ラベルを表状に生成
        for i in range(self.set.row*3):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=7, height=1, font=("", 9))
            )  # ラベルの生成
            self.tab[i].grid(row=i//3, column=i%3, padx=1, pady=1)  # ラベルを配置
            self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定

        # 列名ラベル設定
        self.tab[0].configure(text="No.", bg="silver")
        self.tab[1].configure(text=self.lg.stt, bg="silver")
        self.tab[2].configure(text=self.lg.stp, bg="silver")

    # 表クリック時動作
    def click(self, e, xy):
        # 座標
        self.x = xy % 3
        self.y = xy // 3

        # クリック有効範囲
        if self.y != 0:  # タイトル行でない場合
            if self.x != 0:  # 番号列でない場合
                self.mw.ch_tm_win("rsv")

    # 表の更新
    def update(self, txt):
        # 表の文字変更
        self.tab[self.y*3+self.x].configure(text=txt)

        # 行の番号付け
        if self.tab[self.y*3+1]["text"] != "":  # 開始列が空白でない場合
            self.tab[self.y*3].configure(text=str(self.y))
        elif self.tab[self.y*3+2]["text"] != "":  # 停止列が空白でない場合
            self.tab[self.y*3].configure(text=str(self.y))
        else:  # 行に時間がない場合
            self.tab[self.y*3].configure(text="")

        # 座標リセット
        self.x = None
        self.y = None

    # 現在の予約
    def crt_rsv(self, tmr):
        pass


# 表示ウインドウ
class TMWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw                        # メインウインドウ
        self.wwd = 400                      # ウインドウ幅
        self.whg = 300                      # ウインドウ高
        self.siz = self.wwd // 110          # 文字サイズ
        self.clr = self.mw.set.clr0         # 文字色
        self.bgc = self.mw.set.bgc0         # 背景色
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

        # 7セグ表示
        clr, bgc = self.mw.set_tab.crt_set(self.mw.tmr)
        self.mw.tmr.out_seg(
            self.cvs, clr, bgc,
            self.wwd/2, self.whg/2, self.siz
        )

        self.master.after(10, self.re_frm)  # 0.01s後再描画

    # イベント
    def event(self):
        def win_size(e):
            self.e = e  # エラー処理(仮)
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.siz = self.wwd // 110

        self.bind("<Configure>", win_size)


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw, typ):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw  # メインウインドウ
        self.typ = typ  # 呼び出された種類
        self.tmr = self.mw.set_tmr
        self.dsp = tk.Label(master=master, text=self.tmr.out_txt(), font=("", 60, ))
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
        self.bt_nw = tk.Button(
            self.master, width=10, text=self.mw.lg.now, command=self.ps_nw
        )
        self.bt_rs = tk.Button(
            self.master, width=10, text=self.mw.lg.rst, command=self.ps_rs
        )
        self.bt_ok = tk.Button(
            self.master, width=10, text=self.mw.lg.ook, command=self.ps_ok
        )
        self.bt_dl = tk.Button(
            self.master, width=10, text=self.mw.lg.dlt, command=self.ps_dl
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
        self.bt_nw.place(x=120, y=210)
        self.bt_rs.place(x=210, y=210)
        self.bt_ok.place(x=120, y=250)
        self.bt_dl.place(x=210, y=250)
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

    # 現在時刻押下
    def ps_nw(self):
        self.tmr.get_now()
        self.dsp.configure(text=self.tmr.out_txt())

    # 初期化押下
    def ps_rs(self):
        self.tmr.set_tmr(h=0, m=0, s=0, ms=0)
        self.dsp.configure(text=self.tmr.out_txt())

    # 決定押下
    def ps_ok(self):
        self.mw.set_tmr = self.tmr
        if self.typ == "ccv":
            self.mw.tmr = self.tmr
        elif self.typ == "set":
            self.mw.set_tab.update(self.tmr.out_txt())
        elif self.typ == "rsv":
            self.mw.rsv_tab.update(self.tmr.out_txt())
        self.master.destroy()

    # 削除押下
    def ps_dl(self):
        if self.typ == "set":
            self.mw.set_tab.update("")
        elif self.typ == "rsv":
            self.mw.rsv_tab.update("")
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.master.destroy()


# 色変更ウインドウ
class ChanColorWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw, typ):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw
        self.typ = typ  # 呼び出された種類
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
        self.bt_dl = tk.Button(
            self.master, width=10, text=self.mw.lg.dlt, command=self.ps_dl
        )
        self.bt_cn = tk.Button(
            self.master, width=10, text=self.mw.lg.ccl, command=self.ps_cn
        )

        # ボタンの無効化
        if self.mw.set_tab.y*4+self.mw.set_tab.x in [6, 7]:
            self.bt_dl.configure(state=tk.DISABLED)

        # ウインドウの定義
        self.master.title(self.mw.lg.ccr)
        self.master.geometry("400x300")
        self.master.resizable(False, False)
        self.widgets()

    def widgets(self):
        self.sc_r.place(x=50, y=50)
        self.sc_g.place(x=50, y=100)
        self.sc_b.place(x=50, y=150)
        self.dsp.place(x=280, y=80)
        self.bt_ok.place(x=120, y=250)
        self.bt_dl.place(x=210, y=250)
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
        if self.typ == "set":
            self.mw.set_tab.update(self.ccd)
        self.master.destroy()

    # 削除押下
    def ps_dl(self):
        if self.typ == "set":
            self.mw.set_tab.update("")
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.master.destroy()


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
