import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog as fd
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
        self.tmr = fc.Time()                # 表示時間
        self.etr = tk.Entry(self.master, width=50)  # コマンド入力欄
        self.wt = Watch(self)     # ストップウォッチタブ
        self.st = Setting(self)   # 設定タブ
        self.sc = Schedule(self)  # 予定タブ
        self.hp = Help(self)      # ヘルプタブ
        self.fl = File(self)      # ファイルタブ
        self.mn = Menu(self)      # メニューバー
        self.mn.change(g.scn0)    # 初期タブ

        # ウインドウの定義
        self.master.title(g.lg.mwn)                          # ウインドウタイトル
        self.master.geometry("400x300")                      # ウインドウサイズ
        self.master.resizable(False, False)                  # サイズ変更禁止
        self.master.protocol("WM_DELETE_WINDOW", self.exit)  # ×ボタンクリック
        self.widgets()                                       # ウィジェット
        self.event()                                         # イベント

        # サブウインドウの定義
        self.viw_mas = None  # 表示マスター
        self.viw_app = None

        # 現在時刻取得
        self.now.get_now()
        self.reload()

    # ウィジェット
    def widgets(self: tk.Tk):
        self.dsp_cmd()  # コマンド欄
        if g.ctn:  # 前回の続き有効
            self.fl.open("backup.cut")

    # 表示ウインドウ表示
    def viw_win(self):
        if (self.viw_mas is None) or (not self.viw_mas.winfo_exists()):
            self.viw_mas = tk.Toplevel(self.master)
            self.viw_app = ViewWin(self.viw_mas, self)
            if not g.md_cmd:  # コマンド欄が無効の場合
                self.viw_mas.focus_set()

    # アプリケーション終了
    def exit(self, e=None):
        if g.ctn:
            self.fl.save("backup.cut")
        self.master.destroy()

    # コマンド欄表示
    def dsp_cmd(self):
        if g.md_cmd:
            self.etr.configure(state="normal")
            self.etr.place(x=50, y=270)
            self.etr.focus_set()
            self.etr.bind("<Key-Return>", self.in_cd)
        else:
            self.etr.delete(0, "end")
            self.etr.configure(state="disabled")
            self.etr.place_forget()

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
            # print(e.keysym)
            if e.keysym in self.keys:
                return
            self.keys.append(e.keysym)
            if e.keysym == "return":
                pass
            if "c" in self.keys:
                if "m" in self.keys:
                    if "d" in self.keys:
                        g.md_cmd = True
                        self.dsp_cmd()

        def k_release(e):  # キーボード離した場合
            self.keys.remove(e.keysym)

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)
        self.master.bind("<KeyRelease-Escape>", self.exit)

    # 再描画
    def reload(self):
        # 再描画の判断
        prv = self.now.n  # 前回の時刻
        self.now.get_now()  # 現在時刻取得
        if self.wt.cnt:  # カウントが有効の場合
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
        self.lst = ["file", "FIL", "tmr", "TMR", "set", "SET", "scd", "SCD", "help", "HLP"]

        # 設定
        self.mw.master.configure(menu=self.bar)  # メニューバー追加
        self.bar.add_command(label=g.lg.fil, command=pt(self.change, scn="FIL"))  # ファイル
        self.bar.add_command(label=g.lg.swc, command=pt(self.change, scn="TMR"))  # タイマー
        self.bar.add_command(label=g.lg.set, command=pt(self.change, scn="SET"))  # 設定
        self.bar.add_command(label=g.lg.rsv, command=pt(self.change, scn="SCD"))  # 予定
        self.bar.add_command(label=g.lg.hlp, command=pt(self.change, scn="HLP"))  # ヘルプ

    # タブ変更
    def change(self, scn):
        self.mw.fl.frm.pack_forget()
        self.mw.wt.frm.pack_forget()
        self.mw.st.frm.pack_forget()
        self.mw.sc.frm.pack_forget()
        self.mw.hp.frm.pack_forget()
        if scn in ["file", "FIL"]:
            self.mw.fl.frm.pack(expand=True, fill="both")
        elif scn in ["tmr", "TMR"]:
            self.mw.wt.frm.pack(expand=True, fill="both")
        elif scn in ["set", "SET"]:
            self.mw.st.frm.pack(expand=True, fill="both")
        elif scn in ["scd", "SCD"]:
            self.mw.sc.frm.pack(expand=True, fill="both")
        elif scn in ["help", "HLP"]:
            self.mw.hp.frm.pack(expand=True, fill="both")
        self.mw.etr.lift()


# ストップウォッチクラス
class Watch:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.cnt = False  # カウントしているか
        self.wnd = False  # 別ウインドウ表示しているか
        self.frm = tk.Frame(self.mw.master)
        self.wtc = tk.Label(self.frm, text=self.mw.tmr.out_txt(), font=("", 60))
        self.ssb = tk.Button(self.frm, text=g.lg.stt, font=("", 15), width=15, height=3)
        self.rst = tk.Button(self.frm, text=g.lg.rst, font=("", 15), width=15, height=3)
        self.dsp = tk.Button(self.frm, text=g.lg.viw, font=("", 15), width=32, height=1)

        self.widgets()

    def widgets(self):
        # 設定
        self.wtc.bind("<Button-1>", self.change)
        self.ssb.configure(command=pt(self.stt_stp, e=None, ss="ss"))
        self.rst.configure(command=pt(self.reset, e=None))
        self.dsp.configure(command=pt(self.display))
        # self.dsp.configure(command=pt(fc.command, e=None, mw=self.mw, cmd="view"))

        # 配置
        self.wtc.place(x=15, y=20)    # 現在値
        self.ssb.place(x=20, y=120)   # 開始/停止ボタン
        self.rst.place(x=210, y=120)  # 初期化ボタン
        self.dsp.place(x=22, y=210)   # 表示ボタン

    # 現在値変更
    def change(self, e, tim=None):
        if tim is None:
            tim = fc.asktime(self.mw.tmr)
        if tim is not None:
            self.mw.tmr.set_int(tim.n)

    # 初期化
    def reset(self, e):
        self.mw.st.crt = 0
        self.mw.sc.crt = 0
        self.mw.tmr.set_int(0)

    # 開始/停止
    def stt_stp(self, e, ss="ss"):
        if ss == "start":  # 開始
            self.cnt = True
        elif ss == "stop":  # 停止
            self.cnt = False
        else:  # 開始停止を切替
            self.cnt = not self.cnt
        if self.cnt:
            self.ssb.configure(text=g.lg.stp)  # 停止を表示
        else:
            self.ssb.configure(text=g.lg.stt)  # 開始を表示

    # 別ウインドウ表示/非表示
    def display(self):
        self.wnd = not self.wnd
        if self.wnd:
            self.mw.viw_win()  # 表示ウインドウ表示
            self.mw.master.tkraise(self.mw.viw_mas)  # 表示ウインドウを前面へ
            self.dsp.configure(text=g.lg.hid)  # 非表示を表示
        else:
            self.mw.viw_mas.destroy()  # 表示ウインドウ非表示
            self.dsp.configure(text=g.lg.viw)  # 表示を表示


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
        self.add.place(x=190, y=g.row*25+55)            # 行追加ボタン
        self.dlt.place(x=280, y=g.row*25+55)            # 行削除ボタン
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
        for i in range(self.row*4):   # 引数行*列だけ繰り返し
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

        if e.num == 1:  # 左クリック
            if x == 1:  # 時間変更
                if self.txt[4*y+x] != "":              # 既に入力されている場合
                    self.tim.set_txt(self.txt[4*y+x])  # 入力値
                elif g.in_zer:                         # 未記入で初期値を表示させたい場合
                    self.tim.set_int(0)                # 初期値
                tim = fc.asktime(self.tim)                # 時間変更ウインドウで時間取得
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
        if self.crt < self.row-1:  # 最終行でない場合
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
        self.tab = tk.Canvas(self.frm, width=321, height=g.row*25+1, highlightthickness=0)
        self.tit = tk.Canvas(self.frm, width=321, height=25, bg="silver", highlightthickness=0)
        self.stf = tk.Frame(self.frm)  # 設定用フレーム
        self.clk = None  # 設定時刻用ラベル
        self.scd = None  # 設定予定用ラベル
        self.val = None  # 設定値用ラベル
        self.tim = fc.Time()  # 場面保存用
        self.crt = 0  # 現在の設定行
        self.row = g.row
        self.txt = [""] * self.row * 4

        self.widgets()
        self.table(self.row)

    def widgets(self):
        # 設定
        self.tab.configure(scrollregion=(0, 0, 321, self.row+25+1), yscrollcommand=self.scr.set)
        self.scr.configure(command=self.tab.yview)
        self.tab.bind("<Button>", self.click)
        self.add.configure(command=self.setting)
        # self.add.configure(command=pt(self.table, cmd="+"))
        self.dlt.configure(command=pt(self.table, cmd="-"))

        # タイトル行設定
        self.tit.create_text(40, 13, text="No.", font=("", 11))
        self.tit.create_text(120, 13, text=g.lg.tim, font=("", 11))
        self.tit.create_text(200, 13, text=g.lg.scd, font=("", 11))
        self.tit.create_text(280, 13, text=g.lg.val, font=("", 11))
        self.tit.create_rectangle(0, 0, 80, 24)
        self.tit.create_rectangle(80, 0, 160, 24)
        self.tit.create_rectangle(160, 0, 240, 24)
        self.tit.create_rectangle(240, 0, 320, 24)

        # 配置
        self.add.place(x=190, y=g.row*25+55)                    # 行追加ボタン
        self.dlt.place(x=280, y=g.row*25+55)                    # 行削除ボタン
        self.tab.place(x=40, y=44)                      # 予定表キャンバス
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
        if self.row == g.row:                     # 行数最小の場合
            self.dlt.configure(state="disabled")  # 削除ボタン無効
        else:                                     # その他
            self.dlt.configure(state="normal")    # 削除ボタン有効

    # 予定の設定
    def setting(self, tim=None, scd="", val=None):
        # 設定用画面設定
        t1 = fc.Time(0)
        t3 = fc.Time(0)
        lst = ["", g.lg.stt, g.lg.stp, g.lg.ccv, g.lg.rst]
        self.stf.configure(width=300, height=150, bg="lime", bd=1, relief="solid")
        ook = tk.Button(self.stf, width=10, text=g.lg.ook, command=pt(self.set_bt, t=1))   # ボタン
        dlt = tk.Button(self.stf, width=10, text=g.lg.dlt, command=pt(self.set_bt, t=-1))  # ボタン
        ccl = tk.Button(self.stf, width=10, text=g.lg.ccl, command=pt(self.set_bt, t=0))   # ボタン
        tt1 = fc.Label(self.stf, width=90, height=25, text=g.lg.tim)
        tt2 = fc.Label(self.stf, width=91, height=25, text=g.lg.scd)
        tt3 = fc.Label(self.stf, width=90, height=25, text=g.lg.val)
        self.clk = fc.Label(self.stf, width=90, height=30)
        if tim is not None:
            t1.set_int(tim)
            self.clk.configure(text=t1.out_txt())
        self.scd = fc.Combobox(self.stf, width=91, height=30, row=3, lst=lst, text=scd)
        self.val = fc.Label(self.stf, width=90, height=30)
        if val is not None:
            t3.set_int(val)
            self.val.configure(text=t3.out_txt())
        self.clk.bind("<Button-1>", pt(self.set_ck, s="tim", t=t1))
        self.val.bind("<Button-1>", pt(self.set_ck, s="val", t=t3))

        # 配置
        tt1.place(x=15, y=10)
        tt2.place(x=104, y=10)
        tt3.place(x=194, y=10)
        self.clk.place(x=15, y=34)   # 時刻入力欄
        self.scd.place(x=104, y=34)  # 予定入力欄
        self.val.place(x=194, y=34)  # 値入力欄
        ook.place(x=30, y=110)  # 設定用決定ボタン
        dlt.place(x=120, y=110)  # 設定用削除ボタン
        ccl.place(x=210, y=110)  # 設定用取消ボタン
        self.stf.place(x=10, y=10)

    # 設定用クリック動作
    def set_ck(self, e, s, t):
        tim = fc.asktime(t)
        if tim is not None:
            if s == "tim":
                self.clk.configure(text=tim.out_txt())
            if s == "val":
                self.val.configure(text=tim.out_txt())

    # 設定用ボタン動作
    def set_bt(self, t):
        self.stf.place_forget()

    # 表クリック
    def click(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量（ピクセル）
        x = (e.x - 2) // 80             # クリック列
        y = (e.y + int(d)) // 25        # クリック行

        if e.num == 1:  # 左クリック
            if x == 1:  # 時間変更
                if self.txt[4*y+x] != "":              # 既に入力されている場合
                    self.tim.set_txt(self.txt[4*y+x])  # 入力値
                elif g.in_zer:                         # 未記入で初期値を表示させたい場合
                    self.tim.set_int(0)                # 初期値
                tim = fc.asktime(self.tim)                # 時間変更ウインドウで時間取得
                if tim is not None:                         # 時間が返された場合
                    self.tim.set_int(tim.n)                 # 時間を保存
                    self.change(4*y+x, self.tim.out_txt())  # 表の表示を変更
        elif e.num == 3:  # 右クリック
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
        y = xy // 4
        if (self.txt[4*y+1] != "") or (self.txt[4*y+2] != ""):
            self.txt[4*y] = str(y+1)
            self.tab.itemconfig(tagOrId="t" + str(4*y), text=str(y+1))
        else:
            self.txt[4*y] = ""
            self.tab.itemconfig(tagOrId="t" + str(4*y), text="")
        return 0

    # 現在の設定
    def current(self, tim: fc.Time):
        cmp = fc.Time()
        if self.txt[4*self.crt] != "":                               # 予定行が無効の場合
            if not self.mw.wt.cnt:                                   # カウントが無効の場合
                if self.txt[4*self.crt+1] != "":                     # 空欄でない場合
                    cmp.set_txt(self.txt[4*self.crt+1])              # 比較用に時間を登録
                    if cmp.n <= tim.n < cmp.n+10:                    # 現在時刻の方が大きい場合
                        fc.command(e=None, mw=self.mw, cmd="start")  # カウント開始
            else:
                if self.txt[4*self.crt+1] != "":                     # 空欄でない場合
                    cmp.set_txt(self.txt[4*self.crt+2])              # 比較用に時間を登録
                    if cmp.n <= tim.n < cmp.n+10:                    # 現在時刻の方が大きい場合
                        fc.command(e=None, mw=self.mw, cmd="stop")   # カウント停止
                        self.crt += 1
        if self.crt > self.row:
            self.crt = self.row


# ヘルプクラス
class Help:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)
        self.lbl = fc.Label(self.frm, width=200, height=100, text="テスト環境", bg="lime")
        self.lst = ["", g.lg.stt, g.lg.stp, g.lg.ccv, g.lg.rst]
        self.tst = fc.Combobox(self.frm, 100, 20, 3, lst=self.lst)
        self.lbl.place(x=10, y=10)
        self.tst.place(x=100, y=100)


# ファイルクラス
class File:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.nam = "None"
        self.frm = tk.Frame(self.mw.master)
        self.nwb = tk.Button(self.frm, text=g.lg.new, font=("", 15), width=15, height=3)
        self.opn = tk.Button(self.frm, text=g.lg.opn, font=("", 15), width=15, height=3)
        self.sav = tk.Button(self.frm, text=g.lg.sav, font=("", 15), width=15, height=3)
        self.sva = tk.Button(self.frm, text=g.lg.sva, font=("", 15), width=15, height=3)

        self.widgets()

    def widgets(self):
        # 設定
        self.nwb.configure(command=self.new)
        self.opn.configure(command=pt(self.open, n="", d=True))
        self.sav.configure(command=pt(self.save, n="", d=False))
        self.sva.configure(command=pt(self.save, n="", d=True))

        # 配置
        self.nwb.place(x=20, y=50)
        self.opn.place(x=210, y=50)
        self.sav.place(x=20, y=150)
        self.sva.place(x=210, y=150)

    # 開く(ファイル名, ダイアログ開くか)
    def open(self, n="", d=False):
        if d:  # ダイアログ開く
            n = fd.askopenfilename(title=g.lg.opn, filetypes=[("CUTファイル", "*.cut")])
        if os.path.exists(n):  # ファイルが存在するか
            with open(n, "r") as f:
                self.nam = n                       # 名前を記録
                st_t = []                          # 設定表格納配列
                sc_t = []                          # 予定表格納配列
                self.mw.tmr.set_txt(f.readline())  # 現在時間
                st_r = int(f.readline())           # 設定行数
                st_l = f.readline().split()        # 設定表
                sc_r = int(f.readline())           # 予定行数
                sc_l = f.readline().split()        # 予定表
                for i in range(st_r*4):            # 列*行だけ繰り返し
                    if st_l[i] == "None":          # Noneの場合
                        st_t.append("")            # 空白
                    else:                          # その他
                        st_t.append(st_l[i])       # 設定
                for i in range(sc_r*3):            # 列*行だけ繰り返し
                    if sc_l[i] == "None":          # Noneの場合
                        sc_t.append("")            # 空白
                    else:                          # その他
                        sc_t.append(sc_l[i])       # 予定
                self.mw.st.table(st_r, st_t)       # 設定表表示
                self.mw.sc.table(sc_r, sc_t)       # 予定表表示
            return 0
        else:
            print("application Line 571", "No File")
            return 940

    # 保存(ファイル名, ダイアログ開くか)
    def save(self, n="", d=False):
        # ファイル取得
        if d:  # ダイアログ開く
            n = fd.asksaveasfilename(title=g.lg.sva, filetypes=[("CUTファイル", "*.cut")])
        elif n == "":
            if self.nam == "None":
                n = fd.asksaveasfilename(title=g.lg.sva, filetypes=[("CUTファイル", "*.cut")])
            else:
                n = self.nam
        if n[-4:] != ".cut":
            n += ".cut"

        # ファイル書き込み
        if n != "":
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
                f.write(t + "\n")                      # 設定書き込み
                f.write(str(self.mw.sc.row) + "\n")    # 予定行数書き込み
                t = ""                                 # 書き込み変数
                for i in range(self.mw.sc.row*3):      # 行*列だけ繰り返し
                    if self.mw.sc.txt[i] == "":        # 空欄の場合
                        t += "None"                    # 何か文字列
                    else:                              # その他の場合
                        t += self.mw.sc.txt[i]         # 入力した文字列
                    t += " "                           # 空白挿入
                f.write(t + "\n")                      # 設定書き込み

    # 新規
    def new(self):
        self.nam = "None"
        self.mw.tmr.set_int(0)
        self.mw.st.__init__(self.mw)
        self.mw.sc.__init__(self.mw)


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
        self.master.protocol("WM_DELETE_WINDOW", self.exit)  # ×ボタンクリック
        self.widgets()  # ウィジェット
        self.event()    # イベント

    def widgets(self: tk.Tk):
        # キャンバスの設定
        self.cvs.pack(fill=tk.BOTH, expand=True)

    # ウインドウ非表示
    def exit(self):
        self.mw.wt.display()
        self.master.destroy()

    # イベント
    def event(self):
        def win_size(e):
            self.wwd = self.master.winfo_width()
            self.whg = self.master.winfo_height()
            self.siz = self.wwd // 85

        self.master.bind("<Configure>", win_size)
        self.master.bind("<KeyPress-space>", pt(fc.command, mw=self.mw, cmd="ss"))
        self.master.bind("<KeyPress-BackSpace>", pt(fc.command, mw=self.mw, cmd="rst"))
        self.master.bind("<KeyRelease-Escape>", self.exit)

    # 時間表示
    def display(self, tim: fc.Time, clr: str, bgc: str):
        self.cvs.delete("all")  # 表示リセット
        self.cvs.configure(bg=bgc)
        tim.out_seg(self.cvs, clr, bgc, self.wwd/2, self.whg/2, self.siz)  # 7セグ表示


# アプリケーション
def application():
    fc.o_gval()                 # グローバル変数読み取り
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
    fc.s_gval()                 # グローバル変数保存
