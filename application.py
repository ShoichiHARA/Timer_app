import tkinter as tk
from tkinter import Button as Bt
from functools import partial
import functions as fc
import global_val as g


# メインウインドウクラス
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラス継承
        self.pack()               # 配置

        # 定義
        self.keys = []                      # キーボードの状態
        self.now = fc.Time()                # 現在時刻
        self.clr = g.clr0            # 文字色
        self.bgc = g.bgc0            # 背景色
        self.frm = tk.Frame(self.master, width=400, height=280)
        self.cnt = False                    # カウントアップ
        self.lst = tk.Label(self.frm, text=g.lg.ccr)  # 設定表のラベル
        self.lrv = tk.Label(self.frm, text=g.lg.rss)  # 予約表のラベル
        self.set_tab = SetTab(self)         # 設定表
        self.rsv_tab = RsvTab(self)         # 予約表
        self.tmr = fc.Time()                # 表示時間
        self.etr = tk.Entry(self.master, width=50)  # コマンド入力欄
        self.wt = Watch(self)
        self.st = Setting(self)
        self.mn = Menu(self)

        # ウインドウの定義
        self.master.title(g.lg.mwn)          # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
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
    def tim_win(self, e, typ, tim: fc.Time):
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

    # コマンド入力(仮)
    def in_cd(self, e):
        err = fc.command(None, self, self.etr.get())
        if err != 0:  # エラー
            pass

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
                        print("entry")
                        self.etr.place(x=50, y=280)
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


# メニューバークラス
class Menu:
    def __init__(self, mw):
        # 定義
        self.mw = mw
        self.bar = tk.Menu(self.mw.master)  # メニューバー

        # 設定
        self.mw.master.configure(menu=self.bar)  # メニューバー追加
        self.bar.add_command(label=g.lg.fil, command=self.hoge)       # ファイルコマンド追加
        self.bar.add_command(label=g.lg.swc, command=self.mw.wt.widgets)  # タイマーコマンド追加
        self.bar.add_command(label=g.lg.set, command=self.mw.st.widgets)  # 設定コマンド追加
        self.bar.add_command(label=g.lg.rsv, command=self.hoge)  # 予約コマンド追加
        self.bar.add_command(label=g.lg.hlp, command=self.hoge)  # ヘルプコマンド追加

    def hoge(self):
        pass


# ストップウォッチクラス
class Watch:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.wtc = None
        self.ssb = None
        self.rst = None
        self.dsp = None

    def widgets(self):
        print("Watch")
        # 定義
        self.mw.frm.destroy()  # フレーム破壊
        self.mw.frm = tk.Frame(self.mw.master, width=400, height=280)  # 新たに生成
        self.wtc = tk.Label(self.mw.frm, text=self.mw.tmr.out_txt(), font=("", 60))
        self.wtc.bind("<Button-1>", partial(self.mw.tim_win, typ="ccv", tim=self.mw.tmr))
        self.ssb = tk.Button(
            self.mw.frm, text=g.lg.stt, font=("", 15), width=15, height=3,
            command=partial(fc.command, e=None, mw=self.mw, cmd="ss")
        )  # 開始/停止ボタン
        self.rst = tk.Button(
            self.mw.frm, text=g.lg.rst, font=("", 15), width=15, height=3,
            command=partial(fc.command, e=None, mw=self.mw, cmd="rst")
        )  # 初期化ボタン
        self.dsp = tk.Button(
            self.mw.frm, text=g.lg.viw, font=("", 15), width=32, height=1,
            command=partial(fc.command, e=None, mw=self.mw, cmd="view")
        )

        # 配置
        self.wtc.place(x=15, y=20)    # 現在値
        self.ssb.place(x=20, y=120)   # 開始/停止ボタン
        self.rst.place(x=210, y=120)  # 初期化ボタン
        self.dsp.place(x=22, y=210)   # 表示ボタン
        self.mw.frm.place(x=0, y=0)


# 設定クラス
class Setting:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.add = None
        self.dlt = None
        self.tab = None
        self.tit = None
        self.scr = None
        self.row = g.row + 2
        self.txt = [""] * self.row * 4

        self.txt[0] = "0"
        self.txt[1] = "00:00:00.00"
        self.txt[2] = g.clr0
        self.txt[3] = g.bgc0

    def widgets(self):
        print("Setting")
        # 定義
        self.mw.frm.destroy()
        self.mw.frm = tk.Frame(self.mw.master, width=400, height=280)
        self.add = tk.Button(self.mw.frm, text=g.lg.rad, command=self.ps_ad)  # 行追加ボタン
        self.dlt = tk.Button(self.mw.frm, text=g.lg.rdl, command=self.ps_dl)  # 行削除ボタン
        self.scr = tk.Scrollbar(self.mw.frm, orient=tk.VERTICAL)  # スクロールバー
        self.tab = tk.Canvas(
            self.mw.frm, width=321, height=g.row*25+2,
            scrollregion=(0, 0, 321, self.row*25+2), yscrollcommand=self.scr.set
        )  # 設定表
        self.tit = tk.Canvas(
            self.mw.frm, width=321, height=25, bg="silver",
            scrollregion=(0, 0, 321, 25)
        )  # タイトル行
        self.scr.configure(command=self.tab.yview)
        self.tab.bind("<Button-1>", self.ck_tb)

        for i in range(self.row*4):
            self.tab.create_rectangle(
                i%4*80, i//4*25, i%4*80+80, i//4*25+25, fill="SystemButtonFace", tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%4*80+40, i//4*25+13, text=self.txt[i], font=("", 10), tags="t"+str(i)
            )  # 表に入る文字
            if i % 4 in [2, 3]:  # 文字色列または背景色
                if self.txt[i] != "":  # 空白でない場合
                    self.tab.itemconfig("r"+str(i), fill=self.txt[i])  # 表の背景色変更

        # タイトル行設定
        self.tit.create_text(40, 13, text="No.", font=("", 10))
        self.tit.create_text(120, 13, text=g.lg.tim, font=("", 10))
        self.tit.create_text(200, 13, text=g.lg.clr, font=("", 10))
        self.tit.create_text(280, 13, text=g.lg.bgc, font=("", 10))
        self.tit.create_rectangle(0, 0, 80, 24)
        self.tit.create_rectangle(80, 0, 160, 24)
        self.tit.create_rectangle(160, 0, 240, 24)
        self.tit.create_rectangle(240, 0, 320, 24)

        # 配置
        self.add.place(x=50, y=250)              # 行追加ボタン
        self.dlt.place(x=150, y=250)             # 行削除ボタン
        self.tab.place(x=40, y=45)               # 設定表キャンバス
        self.tit.place(x=40, y=20)               # タイトル行キャンバス
        self.scr.place(x=365, y=55, height=200)  # スクロールバー
        self.mw.frm.place(x=0, y=0)
        self.scr.set(0, g.row/self.row)
        self.mw.master.update()

    # 表クリック
    def ck_tb(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量（ピクセル）
        x = e.x // 80                   # クリック列
        y = (e.y + d) // 25             # クリック行
        print(e, x, y)
        self.change(4*y+x, "hey")

    # 設定変更
    def change(self, xy, txt):
        print(xy)
        self.txt[xy] = txt
        self.tab.itemconfig(tagOrId="t"+str(xy), text=txt)
        if xy % 4 in [2, 3]:  # 文字色列または背景色
            if self.txt[xy] != "":  # 空白の場合
                self.tab.itemconfig(tagOrId="r"+str(xy), fill="SystemButtonFace")  # 表の背景色初期化
            else:
                self.tab.itemconfig(tagOrId"r"+str(xy), fill=self.txt[xy])  # 表の背景色変更

        # 行が埋まっているか
        y = xy // 4
        if (self.txt[y+1] != "") and (self.txt[y+2] != "") and (self.txt[y+3] != ""):
            self.txt[4*y] = str(y)
            self.tab.itemconfig(tagOrId="t"+str(4*y), text=str(y))
    
    # 行追加ボタン押下
    def ps_ad(self):
        print("addition")
        self.row += 1  # 行を追加
        self.tab.configure(scrollregion=(0, 0, 321, self.row*25+2))
        for i in range(4):
            self.txt.append("")
            self.tab.create_text(
                i*80+40, i//4*25+13, text=self.txt[i], font=("", 10), tags=self.row*4+i
            )  # 表に入る文字
            self.tab.create_rectangle(
                i*80, self.row*25-25, i*80+80, self.row*25, fill="SystemButtonFace"
            )  # 表の格子

    # 行削除ボタン押下
    def ps_dl(self):
        print(self.txt)
        # y = self.scr.get()
        # print(y)


# 設定クラス
class Setting1:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.add = None
        self.dlt = None
        self.frm = None
        self.tab = []
        self.cvs = None
        self.scr = None
        self.lbl = None
        self.txt = [""] * g.row * 4
        self.crt = 4  # 現在の設定行
        self.rgy = 400  # スクロール範囲

        # 列名設定
        self.txt[0] = "No."
        self.txt[1] = g.lg.tim
        self.txt[2] = g.lg.clr
        self.txt[3] = g.lg.bgc
        self.txt[4] = "1"
        self.txt[5] = "00:00:00.00"
        self.txt[6] = g.clr0
        self.txt[7] = g.bgc0

        """
        # 表状ラベルの生成
        for i in range(g.row*4):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=9, height=1, font=("", 10), text=str(i))
            )  # ラベルの生成

        # 列名ラベル設定
        self.tab[0].configure(text="No.", bg="silver")
        self.tab[1].configure(text=g.lg.tim, bg="silver")
        self.tab[2].configure(text=g.lg.clr, bg="silver")
        self.tab[3].configure(text=g.lg.bgc, bg="silver")
        self.tab[4].configure(text="1", bg=g.rwc0)
        self.tab[5].configure(text="00:00:00.00")
        self.tab[6].configure(text=g.clr0, bg=g.clr0)
        self.tab[7].configure(text=g.bgc0, bg=g.bgc0)
        """

        # print(self.tab)

    def widgets(self):
        print("Setting1")
        # 定義
        self.mw.frm.destroy()
        self.mw.frm = tk.Frame(self.mw.master, width=400, height=280)
        self.add = tk.Button(self.mw.frm, text=g.lg.rad, command=self.ps_ad)  # 行追加ボタン
        self.dlt = tk.Button(self.mw.frm, text=g.lg.rdl)  # 行削除ボタン
        self.frm = tk.Frame(self.mw.frm, bg="black")  # 表用のフレーム
        # self.frm.propagate(False)
        # self.cvs = tk.Canvas(self.mw.frm, width=200, height=200, bg="lime", scrollregion=(0, 0, 200, 400))
        self.scr = tk.Scrollbar(
            self.mw.frm, orient=tk.VERTICAL, command=self.scroll
        )
        # self.lbl = tk.Label(self.cvs, text="hoge")
        # self.scr = tk.Scale(self.mw.frm)

        """
        # ラベルを表状に生成
        print(self.tab)
        for i in range(g.row*4):
            # self.tab[i].pack()
            self.tab[i].grid(row=i//4, column=i%4, padx=1, pady=1)  # ラベルを配置
            # self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定
        """
        self.table()

        # 設定
        self.scr.set(0, 200/self.rgy)
        # self.cvs.create_rectangle(50, 50, 100, 150, fill="red")
        # self.cvs.configure(yscrollcommand=self.scr.set)

        # 配置
        self.add.place(x=300, y=200)
        self.dlt.place(x=300, y=220)
        # self.cvs.place(x=50, y=50)
        self.frm.place(x=20, y=50)
        # self.scr.pack(side=tk.LEFT)
        self.scr.place(x=270, y=50, height=200)
        # self.lbl.place(x=50, y=50)
        self.mw.frm.place(x=0, y=0)

    def table(self):
        self.tab = []
        for i in range(g.row*4):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=9, height=1, font=("", 10), text=self.txt[i])
            )  # ラベルの生成
            self.tab[i].grid(row=i//4, column=i%4, padx=1, pady=1)  # ラベルを配置
            # self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定
            if i < 4:
                self.tab[i].configure(bg="silver")

        # 列名ラベル設定
        self.tab[6].configure(bg=g.clr0)
        self.tab[7].configure(bg=g.bgc0)

    def ps_ad(self):
        # y0 = self.scr.get()
        # print(y0)
        print(self.frm)
        print(self.frm["width"], self.frm["height"])

    def scroll(self, e, y0, y1=None):
        # print(e, y0, y1)
        # y = self.scr.get()
        # print(y)
        if e == "moveto":
            self.scr.set(y0, 200/self.rgy+float(y0))


# 設定表クラス
class SetTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.mw = mw
        self.x = None
        self.y = None
        self.crt = 4  # 現在の設定行
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []
        self.tmr = fc.Time()  # 控え用の時間
        self.clr = g.clr0  # 控え用の色

        # ラベルを表状に生成
        for i in range(g.row*4):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=7, height=1, font=("", 9))
            )  # ラベルの生成
            self.tab[i].grid(row=i//4, column=i%4, padx=1, pady=1)  # ラベルを配置
            self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定

        # 列名ラベル設定
        self.tab[0].configure(text="No.", bg="silver")
        self.tab[1].configure(text=g.lg.tim, bg="silver")
        self.tab[2].configure(text=g.lg.clr, bg="silver")
        self.tab[3].configure(text=g.lg.bgc, bg="silver")
        self.tab[4].configure(text="1", bg=g.rwc0)
        self.tab[5].configure(text="00:00:00.00")
        self.tab[6].configure(text=g.clr0, bg=g.clr0)
        self.tab[7].configure(text=g.bgc0, bg=g.bgc0)

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
                    self.mw.tim_win(None, "set", self.tmr)  # 時間設定ウインドウ表示
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
        if row >= g.row*4:  # 最終行の場合
            pass
        elif self.tab[row]["text"] == "":  # 現在の次が空白の場合
            pass
        elif self.tab[row+1]["text"] == tmr.out_txt():  # 次の時間と同じ場合
            self.crt += 4  # 現在行更新
            self.crt_set(tmr)  # もう一度関数実行
        self.tab[self.crt].configure(bg=g.rwc0)  # 現在の行に色付け
        return self.tab[self.crt+2]["text"], self.tab[self.crt+3]["text"]


# 予約表クラス
class RsvTab:
    def __init__(self: tk.Tk, mw):
        # 定義
        self.mw = mw
        self.x = None
        self.y = None
        self.crt = 3  # 現在の予約行
        self.frm = tk.Frame(self.mw.master, bg="black")  # フレーム
        self.tab = []  # 予約表
        self.tmr = fc.Time()  # 控え用の時間

        # ラベルを表状に生成
        for i in range(g.row*3):
            self.tab.append(
                tk.Label(self.frm, bd=2, width=7, height=1, font=("", 9))
            )  # ラベルの生成
            self.tab[i].grid(row=i//3, column=i%3, padx=1, pady=1)  # ラベルを配置
            self.tab[i].bind("<Button-1>", partial(self.click, xy=i))  # 関数を設定

        # 列名ラベル設定
        self.tab[0].configure(text="No.", bg="silver")
        self.tab[1].configure(text=g.lg.stt, bg="silver")
        self.tab[2].configure(text=g.lg.stp, bg="silver")

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
                self.mw.tim_win(None, "rsv", self.tmr)  # 時間変更ウインドウ表示

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
        if self.crt >= g.row*3:  # 最終行を超えた場合
            pass
        elif self.tab[self.crt]["text"] == "":  # 現在が空白の場合
            pass
        elif self.mw.cnt is False:  # タイマーが止まっている場合
            if self.tab[self.crt+1]["text"] == "":  # 空欄の場合
                pass
            elif self.tab[self.crt+1]["text"] == tmr.out_txt():  # 現在の時間と同じ場合
                # self.mw.ps_ss()    # カウント開始
                fc.command(None, self.mw, "start")  # カウント開始
                self.crt_rsv(tmr)  # もう一度関数実行
        elif self.mw.cnt is True:  # タイマーが動いている場合
            if self.tab[self.crt+2]["text"] == "":  # 空欄の場合
                pass
            elif self.tab[self.crt+2]["text"] == tmr.out_txt():  # 現在の時間と同じ場合
                # self.mw.ps_ss()  # カウント停止
                fc.command(None, self.mw, "stop")  # カウント停止
                if self.tab[self.crt+3]["text"] != "":  # 現在の次が空白でない場合
                    self.crt += 3  # 次の行へ
                    self.crt_rsv(tmr)  # もう一度関数実行
        self.tab[self.crt].configure(bg=g.rwc0)  # 現在の行に色付け


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
        self.cvs = tk.Canvas(self.master, bg=g.bgc0)  # キャンバス

        # ウインドウの定義
        self.master.title(g.lg.twn)
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
        self.mw.wt.wtc.configure(text=self.mw.tmr.out_txt())

        self.master.after(2, self.re_frm)  # 0.002s後再描画

    # イベント
    def event(self):
        def win_size(e):
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.siz = self.wwd // 85

        self.bind("<Configure>", win_size)
        self.master.bind("<KeyPress-space>", partial(fc.command, mw=self.mw, cmd="ss"))


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw, typ, tmr):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw  # メインウインドウ
        self.typ = typ  # 呼び出された種類
        self.tmr = fc.Time(tmr.n)
        self.dsp = tk.Label(master=master, text=self.tmr.out_txt(), font=("", 60, ))
        self.bt_nw = Bt(self.master, width=10, text=g.lg.now, command=self.ps_nw)
        self.bt_rs = Bt(self.master, width=10, text=g.lg.rst, command=self.ps_rs)
        self.bt_ok = Bt(self.master, width=10, text=g.lg.ook, command=self.ps_ok)
        self.bt_dl = Bt(self.master, width=10, text=g.lg.dlt, command=self.ps_dl)
        self.bt_cn = Bt(
            self.master, width=10, text=g.lg.ccl, command=self.master.destroy
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
        self.master.title(g.lg.mwn)    # ウインドウタイトル
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
        self.bt_ok = Bt(self.master, width=10, text=g.lg.ook, command=self.ps_ok)
        self.bt_dl = Bt(self.master, width=10, text=g.lg.dlt, command=self.ps_dl)
        self.bt_cn = Bt(
            self.master, width=10, text=g.lg.ccl, command=self.master.destroy
        )

        # スケール初期値
        self.sc_r.set(int(ccd[1], 16) * 16 + int(ccd[2], 16))  # 16進数文字列から
        self.sc_g.set(int(ccd[3], 16) * 16 + int(ccd[4], 16))  # 数値へ
        self.sc_b.set(int(ccd[5], 16) * 16 + int(ccd[6], 16))  # 変換

        # ボタンの無効化
        if self.mw.set_tab.y*4+self.mw.set_tab.x in [6, 7]:
            self.bt_dl.configure(state=tk.DISABLED)

        # ウインドウの定義
        self.master.title(g.lg.ccr)
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
