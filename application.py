import tkinter as tk
from tkinter import Button as Bt
from functools import partial
import language as lg
import timer as tm
import command as cm


# 設定クラス
class Setting:
    def __init__(self):
        self.lg = "JPN"
        self.clr0 = "#000000"
        self.bgc0 = "#FFFFFF"
        self.rwc0 = "#00FF00"
        self.row = 6
        self.ccd = {
            "white": "#FFFFFF", "black": "#000000",
            "red": "#FF0000", "green": "#00FF00", "blue": "#0000FF"
        }


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
        self.tmr = tm.Time()                # 表示時間
        # self.set_tmr = tm.Time()            # 設定用時間
        self.etr = tk.Entry(self.master, width=50)  # コマンド入力欄

        self.bt_dp = Bt(self.master, text=self.lg.viw, width=20, command=self.viw_win)  # 表示ボタン
        self.bt_ss = Bt(
            self.master, text=self.lg.stt, font=("", 15),
            width=10, height=2, command=self.ps_ss
        )   # 開始/停止ボタン
        self.bt_rs = tk.Button(
            self.master, text=self.lg.rst, font=("", 15),
            width=10, height=2, command=self.ps_rs
        )   # 初期化ボタン
        self.bt_cv = Bt(self.master, text=self.lg.ccv, width=20, command=self.ps_cv)  # 現在値変更ボタン

        # ウインドウの定義
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("430x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()                       # ウィジェット
        self.event()                         # イベント

        # サブウインドウの定義
        self.viw_mas = None  # 表示マスター
        self.viw_app = None
        self.chg_mas = None  # 変更マスター
        self.chg_app = None

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
    def viw_win(self):
        if self.viw_mas is None:
            self.viw_mas = tk.Toplevel(self.master)
            self.viw_app = ViewWin(self.viw_mas, self)
            self.viw_mas.focus_set()
        elif not self.viw_mas.winfo_exists():
            self.viw_mas = tk.Toplevel(self.master)
            self.viw_app = ViewWin(self.viw_mas, self)
            self.viw_mas.focus_set()

    # 時間変更ウインドウ表示
    def tim_win(self, typ, tim: tm.Time):
        if self.chg_mas is None:
            self.chg_mas = tk.Toplevel(self.master)
            self.chg_app = ChanTimeWin(self.chg_mas, self, typ, tim)
            self.chg_mas.focus_set()
        elif not self.chg_mas.winfo_exists():
            self.chg_mas = tk.Toplevel(self.master)
            self.chg_app = ChanTimeWin(self.chg_mas, self, typ, tim)
            self.chg_mas.focus_set()

    # 色変更ウインドウ表示
    def clr_win(self, typ, clr: str):
        if self.chg_mas is None:
            self.chg_mas = tk.Toplevel(self.master)
            self.chg_app = ChanColorWin(self.chg_mas, self, typ, clr)
            self.chg_mas.focus_set()
        elif not self.chg_mas.winfo_exists():
            self.chg_mas = tk.Toplevel(self.master)
            self.chg_app = ChanColorWin(self.chg_mas, self, typ, clr)
            self.chg_mas.focus_set()

    # 開始/停止ボタン押下
    def ps_ss(self, e=None):
        self.cnt = not self.cnt
        if self.cnt:
            self.bt_ss.configure(text=self.lg.stp)
        else:
            self.bt_ss.configure(text=self.lg.stt)

    # 初期化ボタン押下
    def ps_rs(self):
        self.set_tab.tab[self.set_tab.crt].configure(bg="SystemButtonFace")
        self.rsv_tab.tab[self.rsv_tab.crt].configure(bg="SystemButtonFace")
        self.set_tab.crt = 4
        self.rsv_tab.crt = 3
        self.tmr.set_int(0)

    # 現在値変更ボタン押下
    def ps_cv(self):
        self.tim_win("ccv", self.tmr)

    # コマンド入力(仮)
    def in_cd(self, e):
        cm.command(self, self.etr.get())

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
            if e.keysym == "return":
                pass
            if "c" in self.keys:
                if "m" in self.keys:
                    if "d" in self.keys:
                        self.etr.place(x=65, y=0)
                        self.etr.focus_set()
                        self.etr.bind("<Key-Return>", self.in_cd)
            if e.keysym == "space":
                pass

        def k_release(e):  # キーボード離した場合
            self.keys.remove(e.keysym)
            if e.keysym == "Escape":
                self.exit()  # プログラム終了

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)


# 設定表クラス
class SetTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw
        self.x = None
        self.y = None
        self.crt = 4  # 現在の設定行
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []
        self.tmr = tm.Time()  # 控え用の時間
        self.clr = self.set.clr0  # 控え用の色

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
        self.tab[4].configure(text="1", bg=self.set.rwc0)
        self.tab[5].configure(text="00:00:00.00")
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
                    if self.tab[xy]["text"] != "":  # 既に入力されていた場合
                        self.tmr.set_txt(self.tab[xy]["text"])  # クラス保存設定値を変更
                    self.mw.tim_win("set", self.tmr)  # 時間設定ウインドウ表示
            elif self.x in [2, 3]:  # 文字色列、背景色列
                if self.tab[xy]["text"] != "":  # 既に入力されている場合
                    self.clr = self.tab[xy]["text"]  # クラス保存設定値を変更
                self.mw.clr_win("set", self.clr)  # 色変更ウインドウ表示

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
        self.tab[self.crt].configure(bg="SystemButtonFace")  # 現在の行の色取消
        row = self.crt + 4  # 現在の次の行
        if row >= self.mw.set.row*4:  # 最終行の場合
            pass
        elif self.tab[row]["text"] == "":  # 現在の次が空白の場合
            pass
        elif self.tab[row+1]["text"] == tmr.out_txt():  # 次の時間と同じ場合
            self.crt += 4  # 現在行更新
            self.crt_set(tmr)  # もう一度関数実行
        self.tab[self.crt].configure(bg=self.set.rwc0)  # 現在の行に色付け
        return self.tab[self.crt+2]["text"], self.tab[self.crt+3]["text"]


# 予約表クラス
class RsvTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw
        self.x = None
        self.y = None
        self.crt = 3  # 現在の予約行
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []  # 予約表
        self.tmr = tm.Time()  # 控え用の時間

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
                if self.tab[xy]["text"] != "":
                    self.tmr.set_txt(self.tab[xy]["text"])
                self.mw.tim_win("rsv", self.tmr)  # 時間変更ウインドウ表示

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
        self.tab[self.crt].configure(bg="SystemButtonFace")  # 現在の行の色取消
        if self.crt >= self.set.row*3:  # 最終行を超えた場合
            pass
        elif self.tab[self.crt]["text"] == "":  # 現在が空白の場合
            pass
        elif self.mw.cnt is False:  # タイマーが止まっている場合
            if self.tab[self.crt+1]["text"] == "":  # 空欄の場合
                pass
            elif self.tab[self.crt+1]["text"] == tmr.out_txt():  # 現在の時間と同じ場合
                self.mw.ps_ss()    # カウント開始
                self.crt_rsv(tmr)  # もう一度関数実行
        elif self.mw.cnt is True:  # タイマーが動いている場合
            if self.tab[self.crt+2]["text"] == "":  # 空欄の場合
                pass
            elif self.tab[self.crt+2]["text"] == tmr.out_txt():  # 現在の時間と同じ場合
                self.mw.ps_ss()  # カウント停止
                if self.tab[self.crt+3]["text"] != "":  # 現在の次が空白でない場合
                    self.crt += 3  # 次の行へ
                    self.crt_rsv(tmr)  # もう一度関数実行
        self.tab[self.crt].configure(bg=self.set.rwc0)  # 現在の行に色付け


# 表示ウインドウ
class ViewWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw                        # メインウインドウ
        self.wwd = 400                      # ウインドウ幅
        self.whg = 300                      # ウインドウ高
        self.siz = self.wwd // 85           # 文字サイズ
        self.cvs = tk.Canvas(self.master, bg=self.mw.set.bgc0)  # キャンバス

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

        # 現在時刻取得
        pnm = self.mw.now.n  # 前回のミリ秒
        self.mw.now.get_now()  # 現在時刻取得

        # タイマーカウント
        if self.mw.cnt:  # カウントが有効の場合
            if pnm != self.mw.now.n:  # ミリ秒が進んでいる場合
                c = self.mw.now.n - pnm  # 前回と今回の差分
                self.mw.tmr.n += c  # 差分だけ進ませる

        # 予約を確認
        self.mw.rsv_tab.crt_rsv(self.mw.now)

        # 7セグ表示
        clr, bgc = self.mw.set_tab.crt_set(self.mw.tmr)
        self.cvs.configure(bg=bgc)  # 背景色
        self.mw.tmr.out_seg(
            self.cvs, clr, bgc, self.wwd/2, self.whg/2, self.siz
        )  # 7セグ表示

        self.master.after(2, self.re_frm)  # 0.002s後再描画

    # イベント
    def event(self):
        def win_size(e):
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.siz = self.wwd // 85

        self.bind("<Configure>", win_size)
        self.master.bind("<KeyPress-space>", self.mw.ps_ss)


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw, typ, tmr):
        super().__init__(master)
        self.pack()

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw  # メインウインドウ
        self.typ = typ  # 呼び出された種類
        self.tmr = tm.Time(tmr.n)
        self.dsp = tk.Label(master=master, text=self.tmr.out_txt(), font=("", 60, ))
        self.bt_nw = Bt(self.master, width=10, text=self.lg.now, command=self.ps_nw)
        self.bt_rs = Bt(self.master, width=10, text=self.lg.rst, command=self.ps_rs)
        self.bt_ok = Bt(self.master, width=10, text=self.lg.ook, command=self.ps_ok)
        self.bt_dl = Bt(self.master, width=10, text=self.lg.dlt, command=self.ps_dl)
        self.bt_cn = Bt(
            self.master, width=10, text=self.lg.ccl, command=self.master.destroy
        )

        # 変更ボタン
        lst = [360000, -360000, 6000, -6000, 100, -100, 1, -1]
        self.bt_ch = [None] * 8
        for i in range(8):
            if i % 2 == 0:
                self.bt_ch[i] = tk.Button(
                    self.master, text="↑", width=10,
                    repeatdelay=1000, repeatinterval=50,
                    command=partial(self.ps_ch, n=lst[i])
                )
            else:
                self.bt_ch[i] = tk.Button(
                    self.master, text="↓", width=10,
                    repeatdelay=1000, repeatinterval=50,
                    command=partial(self.ps_ch, n=lst[i])
                )

        # ボタンの無効化
        if self.typ == "ccv":
            self.bt_dl.configure(state=tk.DISABLED)

        # ウインドウの定義
        self.master.title(self.mw.lg.mwn)    # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()

    def widgets(self: tk.Tk):
        self.dsp.place(x=15, y=80)      # 時間表示
        self.bt_nw.place(x=120, y=210)  # 現在時刻ボタン
        self.bt_rs.place(x=210, y=210)  # 初期化ボタン
        self.bt_ok.place(x=120, y=250)  # 決定ボタン
        self.bt_dl.place(x=210, y=250)  # 削除ボタン
        self.bt_cn.place(x=300, y=250)  # 取消ボタン

        p = [
            [18, 60], [18, 165], [114, 60], [114, 165],
            [210, 60], [210, 165], [306, 60], [306, 165]
        ]
        for i in range(8):
            self.bt_ch[i].place(x=p[i][0], y=p[i][1])

    def ps_ch(self, n):
        self.tmr.n += n
        self.tmr.n = self.tmr.n % 36000000
        self.dsp.configure(text=self.tmr.out_txt())

    # 現在時刻押下
    def ps_nw(self):
        self.tmr.get_now()
        self.dsp.configure(text=self.tmr.out_txt())

    # 初期化押下
    def ps_rs(self):
        self.tmr.set_int(0)
        self.dsp.configure(text=self.tmr.out_txt())

    # 決定押下
    def ps_ok(self):
        if self.typ == "ccv":
            self.mw.tmr.n = self.tmr.n
        elif self.typ == "set":
            self.mw.set_tab.tmr.n = self.tmr.n
            self.mw.set_tab.update(self.tmr.out_txt())
        elif self.typ == "rsv":
            self.mw.rsv_tab.tmr.n = self.tmr.n
            self.mw.rsv_tab.update(self.tmr.out_txt())
        self.master.destroy()

    # 削除押下
    def ps_dl(self):
        if self.typ == "set":
            self.mw.set_tab.update("")
        elif self.typ == "rsv":
            self.mw.rsv_tab.update("")
        self.master.destroy()


# 色変更ウインドウ
class ChanColorWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw, typ, ccd):
        super().__init__(master)
        self.pack()

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.mw = mw
        self.typ = typ  # 呼び出された種類
        self.ccd = ccd
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
        self.dsp = tk.Label(self.master, width=10, height=6, bg=self.ccd)
        self.bt_ok = Bt(self.master, width=10, text=self.lg.ook, command=self.ps_ok)
        self.bt_dl = Bt(self.master, width=10, text=self.lg.dlt, command=self.ps_dl)
        self.bt_cn = Bt(
            self.master, width=10, text=self.lg.ccl, command=self.master.destroy
        )

        # スケール初期値
        self.sc_r.set(int(ccd[1], 16) * 16 + int(ccd[2], 16))  # 16進数文字列から
        self.sc_g.set(int(ccd[3], 16) * 16 + int(ccd[4], 16))  # 数値へ
        self.sc_b.set(int(ccd[5], 16) * 16 + int(ccd[6], 16))  # 変換

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

    # スライドバー移動
    def ch_sc(self, n):
        r = self.sc_r.get()
        g = self.sc_g.get()
        b = self.sc_b.get()
        self.ccd = f"#{r:02X}{g:02X}{b:02X}"  # 各色10進数からカラーコードへ
        self.dsp.configure(bg=self.ccd)

    # 決定押下
    def ps_ok(self):
        self.mw.set_tab.clr = self.ccd
        if self.typ == "set":
            self.mw.set_tab.update(self.ccd)
        self.master.destroy()

    # 削除押下
    def ps_dl(self):
        if self.typ == "set":
            self.mw.set_tab.update("")
        self.master.destroy()


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
