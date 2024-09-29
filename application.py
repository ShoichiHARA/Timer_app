import tkinter as tk
from tkinter import colorchooser
from functools import partial as pt
import _tkinter
import os
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
        self.sc = Schedule(self)
        self.fl = File(self)
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

        # 現在時刻取得
        self.now.get_now()
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
                        self.etr.place(x=50, y=270)
                        self.etr.focus_set()
                        self.etr.bind("<Key-Return>", self.in_cd)

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
        prv = self.now.n  # 前回の時刻
        self.now.get_now()  # 現在時刻取得
        if self.cnt:  # カウントが有効の場合
            if prv != self.now.n:  # 時刻が進んでいる場合
                self.tmr.set_int(self.tmr.n + self.now.n - prv)  # 前回と今回の差分だけ進ませる

        # 時間表示
        self.wt.wtc.configure(text=self.tmr.out_txt())
        if (self.viw_mas is not None) and (self.viw_mas.winfo_exists()):
            clr, bgc = self.st.current(self.tmr)
            self.viw_app.display(self.tmr, clr, bgc)

        # 予定の確認
        self.sc.current(self.now)

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
        self.bar.add_command(
            label=g.lg.rsv, command=pt(fc.command, e=None, mw=mw, cmd="scn scd")
        )  # 予約コマンド追加
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
        self.add = tk.Button(self.frm, width=10, text=g.lg.rad)  # 行追加ボタン
        self.dlt = tk.Button(self.frm, width=10, text=g.lg.rdl)  # 行削除ボタン

        self.scr = tk.Scrollbar(self.frm, orient=tk.VERTICAL)              # スクロールバー
        self.tab = tk.Canvas(self.frm, width=321, height=g.row*25+1, highlightthickness=0)
        self.tit = tk.Canvas(self.frm, width=321, height=25, bg="silver", highlightthickness=0)
        self.tim = fc.Time()  # 場面保存用
        self.clr = g.clr0     # 場面保存用
        self.crt = 0  # 現在の設定行
        self.row = g.row
        self.txt = [""] * self.row * 4

        self.txt[0] = "0"
        self.txt[1] = "00:00:00.00"
        self.txt[2] = g.clr0
        self.txt[3] = g.bgc0

        self.widgets()
        self.table(self.row)

    def widgets(self):
        # 設定
        self.tab.configure(scrollregion=(0, 0, 321, self.row*25+1), yscrollcommand=self.scr.set)
        self.scr.configure(command=self.tab.yview)
        self.tab.bind("<Button>", self.click)
        self.add.configure(command=pt(self.table, cmd="+"))
        self.dlt.configure(command=pt(self.table, cmd="-"))

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
        self.add.place(x=190, y=g.row*25+55)                     # 行追加ボタン
        self.dlt.place(x=280, y=g.row*25+55)                    # 行削除ボタン
        self.tab.place(x=40, y=44)                      # 設定表キャンバス44
        self.tit.place(x=40, y=20)                      # タイトル行キャンバス
        self.scr.place(x=360, y=44, height=g.row*25+1)  # スクロールバー

    # 表生成
    def table(self, cmd, txt=None):
        if cmd == "+":           # 行追加コマンド
            self.row += 1        # 1行追加
        elif cmd == "-":         # 行削除コマンド
            self.row -= 1        # 1行削除
        else:                    # 行数入力
            self.row = int(cmd)  # 行数設定
        if txt is None:                 # 引数が指定されていない場合
            txt = self.txt              # 自身を保存
        self.txt = [""] * self.row * 4  # 配列初期化
        self.tab.configure(scrollregion=(0, 0, 241, self.row*25+1))  # 可動域変更
        for i in range(self.row*4):      # 引数行*列だけ繰り返し
            if i < len(txt):          # 文字配列がある場合
                self.txt[i] = txt[i]  # 文字入力
            self.tab.create_rectangle(
                i%4*80, i//4*25, i%4*80+80, i//4*25+25, fill="SystemButtonFace",
                tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%4*80+40, i//4*25+13, text=self.txt[i], font=("", 11), tags="t"+str(i)
            )  # 表に入る文字
            if i%4 in [2, 3]:  # 文字色列または背景色
                if self.txt[i] != "":  # 空白でない場合
                    self.tab.itemconfig("r"+str(i), fill=self.txt[i])  # 表の背景色変更
        if self.row == g.row:                     # 行数最小の場合
            self.dlt.configure(state="disabled")  # 削除ボタン無効
        else:                                     # その他
            self.dlt.configure(state="normal")    # 削除ボタン有効

    # 表クリック
    def click(self, e):
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
        # エラー判定
        err = 0
        if xy % 4 == 1:  # 時間列
            if txt != "":
                err = self.tim.set_txt(txt)
                txt = self.tim.out_txt()
        elif xy % 4 in [2, 3]:  # 文字色列または背景色列
            if txt == "":  # 空白の場合
                self.tab.itemconfig(tagOrId="r"+str(xy), fill="SystemButtonFace")  # 背景色初期化
            else:
                try:
                    self.tab.itemconfig(tagOrId="r"+str(xy), fill=txt)  # 表の背景色変更
                except _tkinter.TclError:
                    print("application Line 282", _tkinter.TclError)
                    err = 920
        if err != 0:
            return err

        # 文字列変更
        self.txt[xy] = txt
        self.tab.itemconfig(tagOrId="t"+str(xy), text=txt)

        # 行が埋まっているか
        y = xy // 4
        if (self.txt[4*y+1] != "") and (self.txt[4*y+2] != "") and (self.txt[4*y+3] != ""):
            self.txt[4*y] = str(y)
            self.tab.itemconfig(tagOrId="t"+str(4*y), text=str(y))
        else:
            self.txt[4*y] = ""
            self.tab.itemconfig(tagOrId="t"+str(4*y), text="")
        return 0

    # 現在の設定
    def current(self, tim: fc.Time):
        cmp = fc.Time()
        if self.crt < self.row:  # 最終行でない場合
            if self.txt[4*self.crt+4] != "":  # 設定行が有効の場合
                cmp.set_txt(self.txt[4*self.crt+5])
                if tim.n >= cmp.n:  # 現在時間の方が大きい場合
                    self.crt += 1
        return self.txt[4*self.crt+2], self.txt[4*self.crt+3]


# 予定クラス
class Schedule:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 設定場面
        self.add = tk.Button(self.frm, width=10, text=g.lg.rad)  # 行追加ボタン
        self.dlt = tk.Button(self.frm, width=10, text=g.lg.rdl)  # 行削除ボタン
        self.scr = tk.Scrollbar(self.frm, orient=tk.VERTICAL)              # スクロールバー
        self.tab = tk.Canvas(self.frm, width=241, height=g.row*25+1, highlightthickness=0)
        self.tit = tk.Canvas(self.frm, width=241, height=25, bg="silver", highlightthickness=0)
        self.tim = fc.Time()  # 場面保存用
        self.crt = 0  # 現在の設定行
        self.row = g.row
        self.txt = [""] * self.row * 3

        self.widgets()
        self.table(self.row)

    def widgets(self):
        # 設定
        self.tab.configure(yscrollcommand=self.scr.set)
        self.scr.configure(command=self.tab.yview)
        self.tab.bind("<Button>", self.click)
        self.add.configure(command=pt(self.table, cmd="+"))
        self.dlt.configure(command=pt(self.table, cmd="-"))

        # タイトル行設定
        self.tit.create_text(40, 13, text="No.", font=("", 11))
        self.tit.create_text(120, 13, text=g.lg.stt, font=("", 11))
        self.tit.create_text(200, 13, text=g.lg.stp, font=("", 11))
        self.tit.create_rectangle(0, 0, 80, 24)
        self.tit.create_rectangle(80, 0, 160, 24)
        self.tit.create_rectangle(160, 0, 240, 24)

        # 配置
        self.add.place(x=150, y=g.row*25+55)                     # 行追加ボタン
        self.dlt.place(x=240, y=g.row*25+55)                    # 行削除ボタン
        self.tab.place(x=80, y=44)                      # 予定表キャンバス
        self.tit.place(x=80, y=20)                      # タイトル行キャンバス
        self.scr.place(x=320, y=44, height=g.row*25+1)  # スクロールバー

    # 表生成
    def table(self, cmd, txt=None):
        if cmd == "+":           # 行追加コマンド
            self.row += 1        # 1行追加
        elif cmd == "-":         # 行削除コマンド
            self.row -= 1        # 1行削除
        else:                    # 行数入力
            self.row = int(cmd)  # 行数設定
        if txt is None:                 # 引数が指定されていない場合
            txt = self.txt              # 自身を保存
        self.txt = [""] * self.row * 3  # 配列初期化
        self.tab.configure(scrollregion=(0, 0, 241, self.row*25+1))  # 可動域変更
        for i in range(self.row*3):      # 引数行*列だけ繰り返し
            if i < len(txt):          # 文字配列がある場合
                self.txt[i] = txt[i]  # 文字入力
            self.tab.create_rectangle(
                i%3*80, i//3*25, i%3*80+80, i//3*25+25, fill="SystemButtonFace",
                tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%3*80+40, i//3*25+13, text=self.txt[i], font=("", 11), tags="t"+str(i)
            )  # 表に入る文字
        if self.row == g.row:                     # 行数最小の場合
            self.dlt.configure(state="disabled")  # 削除ボタン無効
        else:                                     # その他
            self.dlt.configure(state="normal")    # 削除ボタン有効

    # 表クリック
    def click(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量（ピクセル）
        x = (e.x - 2) // 80             # クリック列
        y = (e.y + int(d)) // 25        # クリック行

        if e.num == 1:  # 左クリック
            if x in [1, 2]:  # 時間変更
                if self.txt[3*y+x] != "":              # 既に入力されている場合
                    self.tim.set_txt(self.txt[3*y+x])  # 入力値
                elif g.in_zer:                         # 未記入で初期値を表示させたい場合
                    self.tim.set_int(0)                # 初期値
                tim = asktime(self.tim)                # 時間変更ウインドウで時間取得
                if tim is not None:                         # 時間が返された場合
                    self.tim.set_int(tim.n)                 # 時間を保存
                    self.change(3*y+x, self.tim.out_txt())  # 表の表示を変更
        elif e.num == 3:  # 右クリック
            if y != 0:
                self.change(4*y+x, "")  # 空白を入力

    # 設定変更
    def change(self, xy, txt):
        # エラー判定
        err = 0
        if txt != "":
            err = self.tim.set_txt(txt)
            txt = self.tim.out_txt()
        if err != 0:
            return err

        # 文字列変更
        self.txt[xy] = txt
        self.tab.itemconfig(tagOrId="t" + str(xy), text=txt)

        # 行が埋まっているか
        y = xy // 3
        if (self.txt[3*y+1] != "") or (self.txt[3*y+2] != ""):
            self.txt[3*y] = str(y+1)
            self.tab.itemconfig(tagOrId="t" + str(3*y), text=str(y+1))
        else:
            self.txt[3*y] = ""
            self.tab.itemconfig(tagOrId="t" + str(3*y), text="")
        return 0

    # 現在の設定
    def current(self, tim: fc.Time):
        cmp = fc.Time()
        if self.txt[3*self.crt] != "":                               # 予定行が無効の場合
            if not self.mw.cnt:                                      # カウントが無効の場合
                if self.txt[3*self.crt+1] != "":                     # 空欄でない場合
                    cmp.set_txt(self.txt[3*self.crt+1])              # 比較用に時間を登録
                    if cmp.n <= tim.n < cmp.n+10:                    # 現在時刻の方が大きい場合
                        fc.command(e=None, mw=self.mw, cmd="start")  # カウント開始
            else:
                if self.txt[3*self.crt+1] != "":                     # 空欄でない場合
                    cmp.set_txt(self.txt[3*self.crt+2])              # 比較用に時間を登録
                    if cmp.n <= tim.n < cmp.n+10:                    # 現在時刻の方が大きい場合
                        fc.command(e=None, mw=self.mw, cmd="stop")   # カウント停止
                        self.crt += 1
        if self.crt > self.row:
            self.crt = self.row


# ファイルクラス
class File:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)
        self.opn = None
        self.sav = None
        self.gvl = "global_val.cut"

    # 開く
    def open(self, n):
        if os.path.exists(n):  # ファイルが存在するか
            with open(n, "r") as f:
                self.mw.tmr.set_txt(f.readline())
                set = f.readline().split()
                for i in range(3):
                    a = f.readline()
                    print(a)
            return 0
        else:
            print("application Line 488", "No File")
            return 940

    # 保存
    def save(self, n):
        with open(n, "w") as f:
            f.write(self.mw.tmr.out_txt() + "\n")  # 現在時間書き込み
            f.write(str(self.mw.st.row) + "\n")    # 設定行数書き込み
            t = ""                                 # 書き込み変数
            for i in range(self.mw.st.row*4):      # 行*列だけ繰り返し
                if self.mw.st.txt[i] == "":        # 空欄の場合
                    t += "None"                    # 何か文字列
                else:                              # その他の場合
                    t += self.mw.st.txt[i]         # 入力した文字列
                t += " "                           # 空白挿入
            f.write(t + "END\n")                   # 設定書き込み
            f.write(str(self.mw.sc.row) + "\n")    # 予定行数書き込み
            t = ""                                 # 書き込み変数
            for i in range(self.mw.sc.row*3):      # 行*列だけ繰り返し
                if self.mw.sc.txt[i] == "":        # 空欄の場合
                    t += "None"                    # 何か文字列
                else:                              # その他の場合
                    t += self.mw.sc.txt[i]         # 入力した文字列
                t += " "                           # 空白挿入
            f.write(t + "END\n")                   # 設定書き込み

    # 現在の状態を保存
    def save1(self, n):
        with open(n, "w") as f:
            f.write(self.mw.tmr.out_txt() + "\n")  # タイマー時間
            t = ""
            for i in range(self.mw.st.row*4):  # 色設定
                if self.mw.st.txt[i] == "":    # 空欄の場合
                    t += "None"                # 文字列生成
                else:                          # 文字がある場合
                    t += self.mw.st.txt[i]     # そのまま
                if i % 4 == 3:                 # 最終列の場合
                    t += "\n"                  # 改行
                    f.write(t)                 # ファイル書き込み
                    t = ""                     # 書き込み文字初期化
                else:                          # 後ろに列がある場合
                    t += " "                   # スペース
            f.write("end\n")                   # 色設定終了
            for i in range(self.mw.sc.row*3):  # 予定
                if self.mw.sc.txt[i] == "":    # 空欄の場合
                    t += "None"                # 文字列生成
                else:                          # 文字がある場合
                    t += self.mw.sc.txt[i]     # そのまま
                if i % 3 == 2:                 # 最終列の場合
                    t += "\n"                  # 改行
                    f.write(t)                 # ファイル書き込み
                    t = ""                     # 書き込み文字初期化
                else:                          # 後ろに列がある場合
                    t += " "                   # スペース
            f.write("end\n")                   # 予定終了


# 表示ウインドウ
class ViewWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw                                  # メインウインドウ
        self.wwd = 400                                # ウインドウ幅
        self.whg = 300                                # ウインドウ高
        self.siz = self.wwd // 85                     # 文字サイズ
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
    fc.o_gval()                 # グローバル変数読み取り
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
    fc.s_gval()                 # グローバル変数保存
