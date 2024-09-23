import tkinter as tk
from tkinter import colorchooser
from functools import partial as pt
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
        self.cnt = False                    # カウントアップ
        self.scn = "Tmr"
        self.tmr = fc.Time()                # 表示時間
        self.etr = tk.Entry(self.master, width=50)  # コマンド入力欄
        self.wt = Watch(self)
        self.st = Setting(self)
        self.mn = Menu(self)

        # ウインドウの定義
        self.master.title(g.lg.mwn)          # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        # self.widgets()                       # ウィジェット
        self.event()                         # イベント

        # サブウインドウの定義
        self.viw_mas = None  # 表示マスター
        self.viw_app = None

        # 初期場面
        fc.command(None, self, "scn " + g.scn0)
        fc.command(None, self, "view")  # テスト用

        # 現在時刻取得
        self.reload()

    # ウィジェット
    def widgets(self: tk.Tk):
        pass

    # 表示ウインドウ表示
    def viw_win(self):
        if (self.viw_mas is None) or (not self.viw_mas.winfo_exists()):
            self.viw_mas = tk.Toplevel(self.master)
            self.viw_app = ViewWin(self.viw_mas, self)
            if self.etr.place_info().get("in") is None:  # コマンド欄が無効の場合
                self.viw_mas.focus_set()

    # コマンド入力(仮)
    def in_cd(self, e):
        err = fc.command(e, self, self.etr.get())
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
                        self.etr.place(x=50, y=280)
                        self.etr.focus_set()
                        self.etr.bind("<Key-Return>", self.in_cd)
            if e.keysym == "space":
                print("hey", self.st.crt)

        def k_release(e):  # キーボード離した場合
            self.keys.remove(e.keysym)
            if e.keysym == "Escape":
                self.master.destroy()  # プログラム終了

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)

    # 再描画
    def reload(self):
        # 再描画の判断
        if self.cnt:  # カウントが有効の場合
            prv = self.now.n  # 前回の時刻
            self.now.get_now()  # 現在時刻取得
            if prv != self.now.n:  # 時刻が進んでいる場合
                self.tmr.set_int(self.tmr.n + self.now.n - prv)  # 前回と今回の差分だけ進ませる

        # 時間表示
        self.wt.wtc.configure(text=self.tmr.out_txt())
        if self.viw_mas is not None and self.viw_mas.winfo_exists():
            clr, bgc = self.st.current(self.tmr)
            self.viw_app.display(self.tmr, clr, bgc)

        self.master.after(2, self.reload)  # 0.002s後再描画
        return


# メニューバークラス
class Menu:
    def __init__(self, mw):
        # 定義
        self.mw = mw
        self.bar = tk.Menu(self.mw.master)  # メニューバー

        # 設定
        self.mw.master.configure(menu=self.bar)  # メニューバー追加
        self.bar.add_command(label=g.lg.fil, command=self.hoge)       # ファイルコマンド追加
        self.bar.add_command(
            label=g.lg.swc, command=pt(fc.command, e=None, mw=mw, cmd="scn tmr")
        )  # タイマーコマンド追加
        self.bar.add_command(
            label=g.lg.set, command=pt(fc.command, e=None, mw=mw, cmd="scn set")
        )  # 設定コマンド追加
        self.bar.add_command(label=g.lg.rsv, command=self.hoge)  # 予約コマンド追加
        self.bar.add_command(label=g.lg.hlp, command=self.hoge)  # ヘルプコマンド追加

    def hoge(self):
        pass


# ストップウォッチクラス
class Watch:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)
        self.wtc = tk.Label(self.frm, text=self.mw.tmr.out_txt(), font=("", 60))
        self.ssb = tk.Button(self.frm, text=g.lg.stt, font=("", 15), width=15, height=3)
        self.rst = tk.Button(self.frm, text=g.lg.rst, font=("", 15), width=15, height=3)
        self.dsp = tk.Button(self.frm, text=g.lg.viw, font=("", 15), width=32, height=1)

        self.widgets()

    def widgets(self):
        print("Watch")
        # 設定
        self.wtc.bind("<Button-1>", self.chg_tim)
        self.ssb.configure(command=pt(fc.command, e=None, mw=self.mw, cmd="ss"))
        self.rst.configure(command=pt(fc.command, e=None, mw=self.mw, cmd="rst"))
        self.dsp.configure(command=pt(fc.command, e=None, mw=self.mw, cmd="view"))

        # 配置
        self.wtc.place(x=15, y=20)    # 現在値
        self.ssb.place(x=20, y=120)   # 開始/停止ボタン
        self.rst.place(x=210, y=120)  # 初期化ボタン
        self.dsp.place(x=22, y=210)   # 表示ボタン

    def chg_tim(self, e):
        tim = asktime(self.mw.tmr)
        if tim is not None:
            self.mw.tmr.set_int(tim.n)


# 設定クラス
class Setting:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 設定場面
        self.add = tk.Button(self.frm, text=g.lg.rad, command=self.ps_ad)  # 行追加ボタン
        self.dlt = tk.Button(self.frm, text=g.lg.rdl, command=self.ps_dl)  # 行削除ボタン
        self.scr = tk.Scrollbar(self.frm, orient=tk.VERTICAL)              # スクロールバー
        self.tab = tk.Canvas(self.frm, width=321, height=g.row*25+1, highlightthickness=0)
        self.tit = tk.Canvas(self.frm, width=321, height=25, bg="silver", highlightthickness=0)
        self.tim = fc.Time()  # 場面保存用
        self.clr = g.clr0     # 場面保存用
        self.crt = 0  # 現在の設定行
        self.row = g.row + 2
        self.txt = [""] * self.row * 4

        self.txt[0] = "0"
        self.txt[1] = "00:00:00.00"
        self.txt[2] = g.clr0
        self.txt[3] = g.bgc0

        # テスト用
        self.txt[4] = "1"
        self.txt[5] = "00:00:00.01"
        self.txt[6] = "#0000FF"
        self.txt[7] = "#FFFFFF"
        self.txt[8] = "2"
        self.txt[9] = "00:00:10.00"
        self.txt[10] = "#FF0000"
        self.txt[11] = "#FFFFFF"

        self.widgets()

    def widgets(self):
        print("Setting")
        # 設定
        self.tab.configure(scrollregion=(0, 0, 321, self.row*25+1), yscrollcommand=self.scr.set)
        self.scr.configure(command=self.tab.yview)
        self.tab.bind("<Button>", self.ck_tb)

        for i in range(self.row*4):
            self.tab.create_rectangle(
                i%4*80, i//4*25, i%4*80+80, i//4*25+25, fill="SystemButtonFace", tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%4*80+40, i//4*25+13, text=self.txt[i], font=("", 11), tags="t"+str(i)
            )  # 表に入る文字
            if i % 4 in [2, 3]:  # 文字色列または背景色
                if self.txt[i] != "":  # 空白でない場合
                    self.tab.itemconfig("r"+str(i), fill=self.txt[i])  # 表の背景色変更

        # タイトル行設定
        self.tit.create_text(40, 13, text="No.", font=("", 11))
        self.tit.create_text(120, 13, text=g.lg.tim, font=("", 11))
        self.tit.create_text(200, 13, text=g.lg.clr, font=("", 11))
        self.tit.create_text(280, 13, text=g.lg.bgc, font=("", 11))
        self.tit.create_rectangle(0, 0, 80, 24)
        self.tit.create_rectangle(80, 0, 160, 24)
        self.tit.create_rectangle(160, 0, 240, 24)
        self.tit.create_rectangle(240, 0, 320, 24)

        # 配置
        self.add.place(x=50, y=250)                     # 行追加ボタン
        self.dlt.place(x=150, y=250)                    # 行削除ボタン
        self.tab.place(x=40, y=44)                      # 設定表キャンバス44
        self.tit.place(x=40, y=20)                      # タイトル行キャンバス
        self.scr.place(x=360, y=44, height=g.row*25+1)  # スクロールバー

    # 表クリック
    def ck_tb(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量（ピクセル）
        x = (e.x - 2) // 80             # クリック列
        y = (e.y + int(d)) // 25        # クリック行
        # print(e, x, y)

        if e.num == 1:  # 左クリック
            if x == 1:  # 時間変更
                if self.txt[4*y+x] != "":              # 既に入力されている場合
                    self.tim.set_txt(self.txt[4*y+x])  # 入力値
                elif g.in_zer:                         # 未記入で初期値を表示させたい場合
                    self.tim.set_int(0)                # 初期値
                tim = asktime(self.tim)                # 時間変更ウインドウで時間取得
                if tim is not None:                         # 時間が返された場合
                    self.tim.set_int(tim.n)                 # 時間を保存
                    self.change(4*y+x, self.tim.out_txt())  # 表の表示を変更
            elif x in [2, 3]:                   # 文字色、背景色変更
                if self.txt[4*y+x] != "":       # 既に入力されている場合
                    self.clr = self.txt[4*y+x]  # 入力値
                elif g.in_zer:                  # 未記入で初期値を表示させたい場合
                    self.clr = "#000000"        # 初期値
                clr = colorchooser.askcolor(self.clr, title=g.lg.ccr)
                self.clr = clr[1]
                self.change(4*y+x, self.clr)
        elif e.num == 3:  # 右クリック
            if y != 0:
                self.change(4*y+x, "")  # 空白を入力

    # 設定変更
    def change(self, xy, txt):
        self.txt[xy] = txt
        self.tab.itemconfig(tagOrId="t"+str(xy), text=txt)
        if xy % 4 in [2, 3]:  # 文字色列または背景色
            if self.txt[xy] == "":  # 空白の場合
                self.tab.itemconfig(tagOrId="r"+str(xy), fill="SystemButtonFace")  # 背景色初期化
            else:
                self.tab.itemconfig(tagOrId="r"+str(xy), fill=self.txt[xy])  # 表の背景色変更

        # 行が埋まっているか
        y = xy // 4
        if (self.txt[4*y+1] != "") and (self.txt[4*y+2] != "") and (self.txt[4*y+3] != ""):
            self.txt[4*y] = str(y)
            self.tab.itemconfig(tagOrId="t"+str(4*y), text=str(y))
        else:
            self.txt[4*y] = ""
            self.tab.itemconfig(tagOrId="t"+str(4*y), text="")

    # 現在の設定
    def current(self, tim: fc.Time):
        cmp = fc.Time()
        for i in range(self.crt, self.row):
            if self.txt[4*i] != "":  # 設定行が有効の場合
                cmp.set_txt(self.txt[4*i+1])
                if tim.n >= cmp.n:  # 現在時間の方が大きい場合
                    self.crt += 1
        self.crt -= 1
        return self.txt[4*self.crt+2], self.txt[4*self.crt+3]
    
    # 行追加ボタン押下
    def ps_ad(self):
        self.row += 1  # 行を追加
        self.tab.configure(scrollregion=(0, 0, 321, self.row*25+1))
        for i in range(self.row*4-4, self.row*4):
            self.txt.append("")
            self.tab.create_rectangle(
                i%4*80, i//4*25, i%4*80+80, i//4*25+25,
                fill="SystemButtonFace", tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%4*80+40, i//4*25+13, text=self.txt[i], font=("", 11), tags="t"+str(i)
            )  # 表に入る文字

    # 行削除ボタン押下
    def ps_dl(self):
        if self.row > g.row:
            self.row -= 1  # 行を減少
            del self.txt[-4: -1]
            self.tab.configure(scrollregion=(0, 0, 321, self.row*25+1))
            for i in range(self.row*4, self.row*4+4):
                self.tab.delete("r"+str(i))
                self.tab.delete("t"+str(i))


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
            self.tab[i].bind("<Button-1>", pt(self.click, xy=i))  # 関数を設定

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

    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs.pack(fill=tk.BOTH, expand=True)

    # イベント
    def event(self):
        def win_size(e):
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.siz = self.wwd // 85

        self.bind("<Configure>", win_size)
        self.master.bind("<KeyPress-space>", pt(fc.command, mw=self.mw, cmd="ss"))

    # 時間表示
    def display(self, tim: fc.Time, clr: str, bgc: str):
        self.cvs.delete("all")  # 表示リセット
        self.cvs.configure(bg=bgc)
        tim.out_seg(self.cvs, clr, bgc, self.wwd/2, self.whg/2, self.siz)  # 7セグ表示


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, tim=None):
        super().__init__(master)
        self.pack()

        # 定義
        if tim is None:
            self.tim = fc.Time()
        else:
            self.tim = fc.Time(tim.n)
        self.dsp = tk.Label(master=self.master, text=self.tim.out_txt(), font=("", 60, ))
        self.now = tk.Button(self.master, width=10, text=g.lg.now, command=self.ps_nw)
        self.rst = tk.Button(self.master, width=10, text=g.lg.rst, command=self.ps_rs)
        self.ook = tk.Button(self.master, width=10, text=g.lg.ook, command=self.ps_ok)
        self.ccl = tk.Button(self.master, width=10, text=g.lg.ccl, command=self.ps_cn)
        self.chg = []  # 変更ボタン

        # ウインドウの定義
        self.master.title(g.lg.mwn)    # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.master.protocol("WM_DELETE_WINDOW", self.ps_cn)  # ×ボタンクリック
        self.widgets()

    def widgets(self: tk.Tk):
        self.dsp.place(x=15, y=80)    # 時間表示
        self.now.place(x=120, y=210)  # 現在時刻ボタン
        self.rst.place(x=210, y=210)  # 初期化ボタン
        self.ook.place(x=210, y=250)  # 決定ボタン
        self.ccl.place(x=300, y=250)  # 取消ボタン

        d = [360000, -360000, 6000, -6000, 100, -100, 1, -1]
        p = [
            [18, 60], [18, 165], [114, 60], [114, 165],
            [210, 60], [210, 165], [306, 60], [306, 165]
        ]
        for i in range(8):
            self.chg.append(tk.Button(self.master))  # 変更ボタン追加
            self.chg[i].configure(
                width=10, repeatdelay=1000, repeatinterval=50,
                command=pt(self.ps_ch, n=d[i])
            )  # 変更ボタン共通設定
            if i % 2 == 0:
                self.chg[i].configure(text="↑")
            else:
                self.chg[i].configure(text="↓")
            self.chg[i].place(x=p[i][0], y=p[i][1])

    # 時間変更ボタン押下
    def ps_ch(self, n):
        self.tim.n += n
        self.tim.n = self.tim.n % 36000000
        self.dsp.configure(text=self.tim.out_txt())

    # 現在時刻押下
    def ps_nw(self):
        self.tim.get_now()
        self.dsp.configure(text=self.tim.out_txt())

    # 初期化押下
    def ps_rs(self):
        self.tim.set_int(0)
        self.dsp.configure(text=self.tim.out_txt())

    # 決定押下
    def ps_ok(self):
        self.master.quit()
        self.master.destroy()

    # 取消押下
    def ps_cn(self):
        self.tim = None
        self.master.quit()
        self.master.destroy()


# 時間変更関数
def asktime(tim=None):
    root = tk.Tk()
    app = ChanTimeWin(master=root, tim=tim)
    app.mainloop()
    return app.tim


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
