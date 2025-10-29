import tkinter as tk
from tkinter import colorchooser as cc
from tkinter import filedialog as fd
from functools import partial as pt
import functions as fc
import global_val as g


# 言語設定
lg = g.lg


# メインウインドウクラス
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラス継承
        self.pack()               # 配置

        # 定義
        self.now = fc.Time()       # 現在時刻
        self.tmr = fc.Time()       # 表示時間
        self.pnw = self.now.n      # 前回の現在時刻

        self.swc = Watch(self)     # ストップウォッタブ
        self.stg = Setting(self)   # 設定タブ
        self.scd = Schedule(self)  # 予定タブ
        self.hlp = Help(self)      # ヘルプタブ
        self.fil = File(self)      # ファイルタブ
        self.men = MenuBar(self)   # メニューバー
        self.men.change(g.scn0)    # 最初に開くタブ

        # ウインドウの定義
        self.master.title(lg.mwn)  # ウインドウタイトル
        self.master.geometry("400x300")  # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止

        # サブウインドウの定義
        self.viw_mas = None
        self.viw_app = None

        # 現在時刻取得
        self.now.get_now()     # 現在時刻取得
        self.pnw = self.now.n  # 前回の現在時刻
        self.reload()          # 再演算

    # ウィジェット
    def widgets(self):
        pass

    # 表示ウインドウ表示
    def viw_win(self):
        # if (self.viw_mas is None) or (not self.viw_mas.winfo_exists()):
        if self.viw_mas is None:
            self.viw_mas = tk.Toplevel(self.master)
            self.viw_app = ViewWin(self.viw_mas, self)
            self.viw_mas.focus_set()

    # 再演算
    def reload(self):
        # 現在時刻取得
        self.now.get_now()

        # カウントアップ
        if self.swc.cnt:                             # カウントが有効な場合
            if self.now.n > self.pnw:                # 時刻が進んでいる場合
                self.tmr.n += self.now.n - self.pnw  # 差分だけ進ませる

        # 時間表示
        self.swc.wtc.configure(text=self.tmr.out_txt())  # 表示タブの時間変更
        if self.viw_mas is not None:                     # 別ウインドウが存在する場合
            self.viw_app.drw_tmr()                       # 別ウインドウ描画

        # 再演算
        self.pnw = self.now.n
        self.master.after(2, self.reload)  # 0.002秒後再演算


# メニューバークラス
class MenuBar:
    def __init__(self, mw):
        # 定義
        self.mw = mw
        self.bar = tk.Menu(self.mw.master)  # メニューバー

        # 設定
        self.mw.master.configure(menu=self.bar)
        self.bar.add_command(label=lg.fil, command=pt(self.change, scn="FIL"))
        self.bar.add_command(label=lg.swc, command=pt(self.change, scn="TMR"))
        self.bar.add_command(label=lg.set, command=pt(self.change, scn="SET"))
        self.bar.add_command(label=lg.rsv, command=pt(self.change, scn="SCD"))
        self.bar.add_command(label=lg.hlp, command=pt(self.change, scn="HLP"))

    # タブ切り換え
    def change(self, scn):
        self.mw.fil.frm.pack_forget()
        self.mw.swc.frm.pack_forget()
        self.mw.stg.frm.pack_forget()
        self.mw.scd.frm.pack_forget()
        self.mw.hlp.frm.pack_forget()
        if scn == "FIL":
            self.mw.fil.frm.pack(expand=True, fill="both")
        elif scn == "TMR":
            self.mw.swc.frm.pack(expand=True, fill="both")
        elif scn == "SET":
            self.mw.stg.frm.pack(expand=True, fill="both")
        elif scn == "SCD":
            self.mw.scd.frm.pack(expand=True, fill="both")
        elif scn == "HLP":
            self.mw.hlp.frm.pack(expand=True, fill="both")
        else:
            print("MenuBar.change Error!")
            return 931
        return 0


# ストップウォッチクラス
class Watch:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.cnt = False                     # カウントしているか
        self.wnd = False                     # 別ウインドウ表示しているか
        self.frm = tk.Frame(self.mw.master)  # ストップウォッチタブのフレーム
        self.wtc = tk.Label(self.frm)        # 時計
        self.ssb = tk.Button(self.frm)       # スタート/ストップボタン
        self.rst = tk.Button(self.frm)       # リセットボタン
        self.dsp = tk.Button(self.frm)       # サブウインドウ表示ボタン

        self.widgets()

    # ウィジェット
    def widgets(self):
        # 設定
        self.wtc.configure(text=self.mw.tmr.out_txt(), font=("", 60))
        self.wtc.bind("<ButtonPress-1>", self.change)
        self.ssb.configure(text=lg.stt, font=("", 15), width=15, height=3)
        self.rst.configure(text=lg.rst, font=("", 15), width=15, height=3)
        self.dsp.configure(text=lg.viw, font=("", 15), width=32, height=1)

        # 関数割付
        self.ssb.configure(command=self.stt_stp)
        self.rst.configure(command=self.reset)
        self.dsp.configure(command=self.display)

        # 配置
        self.wtc.place(x=15, y=20)
        self.ssb.place(x=20, y=120)
        self.rst.place(x=210, y=120)
        self.dsp.place(x=22, y=210)

    # 時間変更
    def change(self, e, tim=None):
        if e is None:
            pass
        if tim is None:
            tim = fc.asktime(self.mw.tmr.out_txt())
        if tim is not None:
            self.mw.tmr.set_txt(tim)

    # 初期化
    def reset(self):
        self.mw.tmr.n = 0

    # 開始/停止
    def stt_stp(self):
        if self.cnt:                         # カウントしている場合
            self.cnt = False                 # カウント停止
            self.ssb.configure(text=lg.stt)  # 開始を表示
        else:                                # カウントしていない場合
            self.cnt = True                  # カウント開始
            self.ssb.configure(text=lg.stp)  # 停止を表示

    # 別ウインドウ表示
    def display(self):
        if self.wnd:                                 # 表示してる場合
            self.mw.viw_mas.destroy()                # ウインドウ破壊
            self.mw.viw_mas = None                   # マスター破壊
            self.dsp.configure(text=lg.viw)          # ボタンに表示を表示
            self.wnd = False                         # 表示していないフラグ
        else:                                        # 表示していない場合
            self.mw.viw_win()                        # ウインドウ表示
            self.mw.master.tkraise(self.mw.viw_mas)  # 表示ウインドウを前面へ
            self.dsp.configure(text=lg.hid)          # ボタンに非表示を表示
            self.wnd = True                          # 表示しているフラグ


# 設定クラス
class Setting:
    def __init__(self, mw: MainWin):
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 設定タブのフレーム
        self.add = tk.Button(self.frm)       # 行追加ボタン
        self.dlt = tk.Button(self.frm)       # 行削除ボタン

        self.scr = tk.Scrollbar(self.frm)    # スクロールバー
        self.tab = tk.Canvas(self.frm)       # 色設定表
        self.tit = tk.Canvas(self.frm)       # 表のタイトル
        self.tim = "00:00:00.00"             # 保存用
        self.clr = g.clr0                    # 保存用
        self.crt = 0                         # 現在の設定行
        self.row = g.row0                    # 行数
        self.txt = [""] * self.row * 5       # 表の要素

        self.txt[0] = "0"
        self.txt[1] = "00:00:00.00"
        self.txt[2] = g.clr0
        self.txt[3] = g.bgc0
        self.txt[4] = g.olc0

        self.widgets()
        self.table(self.row)

    # ウィジェット
    def widgets(self):
        # 設定
        self.tab.configure(
            width=351, height=g.row0*25+1, highlightthickness=0,
            scrollregion=(0, 0, 351, g.row0*25+1), yscrollcommand=self.scr.set
        )
        self.tab.bind("<ButtonPress>", self.click)
        self.scr.configure(command=self.tab.yview)
        self.tit.configure(width=351, height=25, bg="silver", highlightthickness=0)
        self.add.configure(text=lg.rad, width=10, command=pt(self.table, row=1))
        self.dlt.configure(text=lg.rdl, width=10, command=pt(self.table, row=-1))

        # タイトル行設定
        self.tit.create_text(35, 13, text="No.", font=("", 11))
        self.tit.create_text(105, 13, text=lg.tim, font=("", 11))
        self.tit.create_text(175, 13, text=lg.clr, font=("", 11))
        self.tit.create_text(245, 13, text=lg.bgc, font=("", 11))
        self.tit.create_text(315, 13, text="枠線色", font=("", 11))
        self.tit.create_rectangle(0, 0, 70, 24)
        self.tit.create_rectangle(70, 0, 140, 24)
        self.tit.create_rectangle(140, 0, 210, 24)
        self.tit.create_rectangle(210, 0, 280, 24)
        self.tit.create_rectangle(280, 0, 350, 24)

        # 配置
        self.add.place(x=190, y=g.row0*25+55)
        self.dlt.place(x=280, y=g.row0*25+55)
        self.tab.place(x=25, y=44)
        self.tit.place(x=25, y=20)
        self.scr.place(x=375, y=44, height=g.row*25+1)

    # 表生成
    def table(self, row, txt=None):
        if row in [1, -1]:   # 行数変更キーワード
            self.row += row  # 行数変更
        if txt is None:      # 表が指定されていない場合
            txt = self.txt   # 自身を保存
        self.txt = [""] * self.row * 5  # 配列初期化
        self.tab.delete("all")          # 表の描画初期化
        self.tab.configure(scrollregion=(0, 0, 351, self.row*25+1))  # 可動域変更
        for i in range(self.row*5):  # 行x列だけ繰り返し
            if i < len(txt):         # 保存した表にデータがある場合
                self.txt[i] = txt[i]
            self.tab.create_rectangle(
                i%5*70, i//5*25, i%5*70+70, i//5*25+25, fill="SystemButtonFace",
                tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%5*70+35, i//5*25+13, text=self.txt[i], font=("", 10),
                tags="t"+str(i)
            )  # 表の文字
            if i%5 in [2, 3, 4]:  # 色が入る列
                if self.txt[i] != "":  # 空白でない場合
                    self.tab.itemconfig("r"+str(i), fill=self.txt[i])
        if self.row == g.row0:                    # 行数最小の場合
            self.dlt.configure(state="disabled")  # 削除ボタン無効
        else:
            self.dlt.configure(state="normal")    # 削除ボタン有効

    # 表クリック
    def click(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量（ピクセル）
        x = (e.x - 2) // 70             # クリック列
        y = (e.y + int(d)) // 25        # クリック行

        if e.num == 1:  # 左クリック
            if x == 1:  # 時間変更
                if self.txt[5*y+x] != "":       # 既に入力されている場合
                    self.tim = self.txt[5*y+x]  # 入力値から変更
                elif g.in_zer:                  # 未記入で0を表示させたい場合
                    self.tim = "00:00:00.00"    # 0から変更
                tim = fc.asktime(self.tim)      # 時間変更
                if tim is not None:             # 時間が返った場合
                    self.tim = tim              # 今回値を保存
                    self.change(5*y+x, tim)     # 設定変更
            elif x in [2, 3, 4]:  # 色変更
                if self.txt[5*y+x] != "":       # 既に入力されている場合
                    self.clr = self.txt[5*y+x]  # 入力値から変更
                elif g.in_zer:                  # 未入力で0を表示させたい場合
                    self.clr = "#000000"        # 0から変更
                clr = cc.askcolor(self.clr, title=lg.ccr)  # 色変更
                self.clr = clr[1]               # 今回値を保存
                self.change(5*y+x, self.clr)    # 設定変更
        elif e.num == 3:  # 右クリック
            if y != 0:                          # 左端列でない場合
                self.change(5*y+x, "")          # 空白を入力

    # 設定変更
    def change(self, xy, txt):
        # 文字列変更
        self.txt[xy] = txt                          # 文字列を配列へ代入
        self.tab.itemconfig("t"+str(xy), text=txt)  # 文字列を表に表示

        # 背景色変更
        if xy % 5 in [2, 3, 4]:                         # 色変更列
            self.tab.itemconfig("r"+str(xy), fill=txt)  # 色を表背景に描画

        # 行が埋まっているか
        y = xy // 5  # 行番号
        g = ((self.txt[5*y+1] != "") and (self.txt[5*y+2] != "")
             and (self.txt[5*y+3] != "") and (self.txt[5*y+4] != ""))  # 行が埋まっている
        if g:  # 行が埋まっている場合
            self.txt[5*y] = str(y)
        else:
            self.txt[5*y] = ""
        self.tab.itemconfig("t"+str(5*y), text=self.txt[5*y])


# 予定クラス
class Schedule:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 予定タブのフレーム
        self.add = tk.Button(self.frm)       # 行追加ボタン
        self.dlt = tk.Button(self.frm)       # 行削除ボタン
        self.scr = tk.Scrollbar(self.frm)    # スクロールバー
        self.tab = tk.Canvas(self.frm)       # 予定表
        self.tit = tk.Canvas(self.frm)       # 表のタイトル
        self.tim = "00:00:00.00"             # 保存用
        self.crt = 0                         # 現在の設定行
        self.row = g.row0                    # 行数
        self.txt = [""] * self.row * 4       # 表の要素
        self.lbl = tk.Label(self.frm, text="未実装")
        
        self.widgets()
        self.table(self.row)

    # ウィジェット
    def widgets(self):
        # 設定
        self.tab.configure(
            width=321, height=g.row0*25+1, highlightthickness=0,
            scrollregion=(0, 0, 321, g.row0*25+1), yscrollcommand=self.scr.set
        )
        self.tab.bind("<ButtonPress>", self.click)
        self.scr.configure(command=self.tab.yview)
        self.tit.configure(width=321, height=25, bg="silver", highlightthickness=0)
        self.add.configure(text=lg.rad, width=10, command=pt(self.table, row=1))
        self.dlt.configure(text=lg.rdl, width=10, command=pt(self.table, row=-1))

        # タイトル行設定
        self.tit.create_text(40, 13, text="No.", font=("", 11))
        self.tit.create_text(120, 13, text="時刻", font=("", 11))
        self.tit.create_text(200, 13, text="設定", font=("", 11))
        self.tit.create_text(280, 13, text="値", font=("", 11))
        self.tit.create_rectangle(0, 0, 80, 24)
        self.tit.create_rectangle(80, 0, 160, 24)
        self.tit.create_rectangle(160, 0, 240, 24)
        self.tit.create_rectangle(240, 0, 320, 24)

        # 配置
        self.add.place(x=190, y=g.row0*25+55)
        self.dlt.place(x=280, y=g.row0*25+55)
        self.tab.place(x=40, y=44)
        self.tit.place(x=40, y=20)
        self.scr.place(x=360, y=44, height=g.row*25+1)
        self.lbl.place(x=10, y=10)
        
    # 表の生成
    def table(self, row, txt=None):
        if row in [1, -1]:   # 行数変更キーワード
            self.row += row  # 行数変更
        if txt is None:      # 表が指定されていない場合
            txt = self.txt   # 自身を保存
        self.txt = [""] * self.row * 4  # 配列初期化
        self.tab.delete("all")  # 表の描画初期化
        self.tab.configure(scrollregion=(0, 0, 321, self.row*25+1))  # 可動域変更
        for i in range(self.row*4):  # 行x列だけ繰り返し
            if i < len(txt):  # 保存した表にデータがある場合
                self.txt[i] = txt[i]
            self.tab.create_rectangle(
                i%4*80, i//4*25, i%4*80+80, i//4*25+25, fill="SystemButtonFace",
                tags="r"+str(i)
            )  # 表の格子
            self.tab.create_text(
                i%4*80+40, i//4*25+13, text=self.txt[i], font=("", 11),
                tags="t"+str(i)
            )  # 表の文字
        if self.row == g.row0:  # 行数最小の場合
            self.dlt.configure(state="disabled")  # 削除ボタン無効
        else:
            self.dlt.configure(state="normal")    # 削除ボタン有効

    # 表クリック
    def click(self, e):
        s = self.scr.get()              # スクロールバーの位置
        d = s[0] * (self.row * 25 + 2)  # スクロール量
        x = (e.x - 2) // 80             # クリック列
        y = (e.y + int(d)) // 25        # クリック行
        
        if e.num == 1:  # 左クリック
            if x == 1:  # 時間変更
                if self.txt[4*y+x] != "":  # 既に入力されている場合
                    self.tim = self.txt[4*y+x]  # 入力値から変更
                elif g.in_zer:                  # 未記入で0を表示させたい場合
                    self.tim = "00:00:00.00"    # 0から変更
                tim = fc.asktime(self.tim)      # 時間変更
                if tim is not None:             # 時間が返った場合
                    self.tim = tim              # 今回値を保存
                    self.change(4*y+x, tim)     # 設定変更

    # 設定変更
    def change(self, xy, txt):
        # 文字列変更
        self.txt[xy] = txt  # 文字列を配列へ代入
        self.tab.itemconfig("t"+str(xy), text=txt)  # 文字列を表に表示

        # 行が埋まっているか
        y = xy // 4  # 行番号
        g = ((self.txt[4*y+1] != "") and (self.txt[4*y+2] != "")
             and (self.txt[4*y+3] != ""))  # 行が埋まっている
        if g:  # 行が埋まっている場合
            self.txt[4*y] = str(y)
        else:
            self.txt[4*y] = ""
        self.tab.itemconfig("t"+str(4*y), text=self.txt[4*y])
                

# ヘルプクラス
class Help:
    def __init__(self, mw: MainWin):
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)
        self.lbl = tk.Label(self.frm, text="未実装")

        self.lbl.place(x=10, y=10)


# ファイルクラス
class File:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # ヘルプクラスのフレーム
        self.nwb = tk.Button(self.frm)       # 新規作成
        self.opn = tk.Button(self.frm)       # 開く
        self.sav = tk.Button(self.frm)       # 上書き保存
        self.sva = tk.Button(self.frm)       # 名前を付けて保存
        self.lbl = tk.Label(self.frm, text="未実装")

        self.widgets()

    def widgets(self):
        # 設定
        self.nwb.configure(text=lg.new, font=("", 15), width=15, height=3)
        self.opn.configure(text=lg.opn, font=("", 15), width=15, height=3)
        self.sav.configure(text=lg.sav, font=("", 15), width=15, height=3)
        self.sva.configure(text=lg.sva, font=("", 15), width=15, height=3)

        # 配置
        self.nwb.place(x=20, y=50)
        self.opn.place(x=210, y=50)
        self.sav.place(x=20, y=150)
        self.sva.place(x=210, y=150)
        self.lbl.place(x=10, y=10)


# 表示ウインドウ
class ViewWin(tk.Frame):
    def __init__(self: tk.Tk, master, mw):
        super().__init__(master)
        self.pack()

        # 定義
        self.mw = mw  # メインウインドウ
        self.wwd = 400  # ウインドウ幅
        self.whg = 300  # ウインドウ高
        # self.siz = self.wwd // 85  # 文字サイズ
        self.flc = "#00FF00"       # 文字色
        self.bkc = "white"         # 背景色
        self.olc = "white"         # 枠線色
        self.wid = 3               # 枠線幅
        self.cr1 = ":"             # 左コロン
        self.cr2 = ":"             # 右コロン
        self.cvs = tk.Canvas(self.master)
        self.widgets()
        self.event()

        # ウインドウの定義
        self.master.title(lg.twn)
        self.master.geometry("400x300")
        self.master.protocol("WM_DELETE_WINDOW", self.exit)

    # ウィジェット
    def widgets(self):
        # 設定
        self.cvs.configure(bg=self.bkc)

        # 7セグ描画
        t = ["A", "B", "C", "D", "E", "F", "G"]
        for i in range(6):
            for j in range(7):
                self.cvs.create_polygon(
                    1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, tags=t[j]+str(i),
                    width=self.wid, outline=self.olc
                )
        t = ["c1u", "c1d", "p1", "c2u", "c2d", "p2"]
        for i in range(6):
            self.cvs.create_rectangle(
                1, 1, 2, 2, tags=t[i], width=self.wid, outline=self.olc
            )
        self.drw_seg([0, 0, 0, 0, 0, 0])

        # 配置
        self.cvs.pack(fill=tk.BOTH, expand=True)

    # ウインドウ削除
    def exit(self):
        self.mw.swc.display()

    # イベント
    def event(self):
        def win_size(e):
            if e is not None:
                self.wwd = self.master.winfo_width()
                self.whg = self.master.winfo_height()
                self.drw_seg([None, None, None, None, None, None])

        self.master.bind("<Configure>", win_size)

    # 7セグ描画
    def drw_seg(self, seg: list):
        s = self.wwd / 400  # 倍率
        a = g.a0 * s        # セグの横幅
        b = g.b0 * s        # セグの高さ
        c = g.c0 * s        # セグの太さ
        z = [s*50, s*100, s*175, s*225, s*300, s*350]
        y = self.whg / 2
        bit = [
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
        for i in range(6):
            # 位置変更
            x = z[i]
            self.cvs.coords(
                "A"+str(i), x-a, y-b, x-a+c, y-b-c, x+a-c, y-b-c,
                x+a, y-b, x+a-c, y-b+c, x-a+c, y-b+c
            )
            self.cvs.coords(
                "B"+str(i), x+a, y-b, x+a+c, y-b+c, x+a+c, y-c,
                x+a, y, x+a-c, y-c, x+a-c, y-b+c
            )
            self.cvs.coords(
                "C"+str(i), x+a, y, x+a+c, y+c, x+a+c, y+b-c,
                x+a, y+b, x+a-c, y+b-c, x+a-c, y+c
            )
            self.cvs.coords(
                "D"+str(i), x-a, y+b, x-a+c, y+b-c, x+a-c, y+b-c,
                x+a, y+b, x+a-c, y+b+c, x-a+c, y+b+c
            )
            self.cvs.coords(
                "E"+str(i), x-a, y, x-a+c, y+c, x-a+c, y+b-c,
                x-a, y+b, x-a-c, y+b-c, x-a-c, y+c
            )
            self.cvs.coords(
                "F"+str(i), x-a, y-b, x-a+c, y-b+c, x-a+c, y-c,
                x-a, y, x-a-c, y-c, x-a-c, y-b+c
            )
            self.cvs.coords(
                "G"+str(i), x-a, y, x-a+c, y-c, x+a-c, y-c,
                x+a, y, x+a-c, y+c, x-a+c, y+c
            )

            # 色変更
            t = ["A", "B", "C", "D", "E", "F", "G"]
            for j in range(7):
                if seg[i] is None:
                    pass
                elif bit[seg[i]][j] == 1:
                    self.cvs.itemconfig(t[j]+str(i), fill=self.flc)
                else:
                    self.cvs.itemconfig(t[j]+str(i), fill=self.bkc)

        # コロン、ピリオド
        self.cvs.coords("c1u", s*138-c, y-(b/2)-c, s*138+c, y-(b/2)+c)
        self.cvs.coords("c1d", s*138-c, y+(b/2)-c, s*138+c, y+(b/2)+c)
        self.cvs.coords("p1", s*138-c, y+b-c, s*138+c, y+b+c)
        self.cvs.coords("c2u", s*262-c, y-(b/2)-c, s*262+c, y-(b/2)+c)
        self.cvs.coords("c2d", s*262-c, y+(b/2)-c, s*262+c, y+(b/2)+c)
        self.cvs.coords("p2", s*262-c, y+b-c, s*262+c, y+b+c)
        if self.cr1 == ".":
            self.cvs.itemconfig("c1u", fill=self.bkc, outline=self.bkc)
            self.cvs.itemconfig("c1d", fill=self.bkc, outline=self.bkc)
            self.cvs.itemconfig("p1",  fill=self.flc, outline=self.olc)
        elif self.cr1 == ":":
            self.cvs.itemconfig("c1u", fill=self.flc, outline=self.olc)
            self.cvs.itemconfig("c1d", fill=self.flc, outline=self.olc)
            self.cvs.itemconfig("p1",  fill=self.bkc, outline=self.bkc)
        if self.cr2 == ".":
            self.cvs.itemconfig("c2u", fill=self.bkc, outline=self.bkc)
            self.cvs.itemconfig("c2d", fill=self.bkc, outline=self.bkc)
            self.cvs.itemconfig("p2",  fill=self.flc, outline=self.olc)
        elif self.cr2 == ":":
            self.cvs.itemconfig("c2u", fill=self.flc, outline=self.olc)
            self.cvs.itemconfig("c2d", fill=self.flc, outline=self.olc)
            self.cvs.itemconfig("p2",  fill=self.bkc, outline=self.bkc)

    # 表示時間と連動
    def drw_tmr(self):
        lst = [0, 0, 0, 0, 0, 0]
        txt = self.mw.tmr.out_txt()  # --:--:--.--
        if self.mw.tmr.n < 180000:   # 30m未満の場合
            lst[0] = int(txt[3])     # --:@-:--.--
            lst[1] = int(txt[4])     # --:-@:--.--
            lst[2] = int(txt[6])     # --:--:@-.--
            lst[3] = int(txt[7])     # --:--:-@.--
            lst[4] = int(txt[9])     # --:--:--.@-
            lst[5] = int(txt[10])    # --:--:--.-@
            self.cr1 = ":"           # 左はコロン
            self.cr2 = "."           # 右はピリオド
        else:                        # 30m以上の場合
            lst[0] = int(txt[0])     # @-:--:--.--
            lst[1] = int(txt[1])     # -@:--:--.--
            lst[2] = int(txt[3])     # --:@-:--.--
            lst[3] = int(txt[4])     # --:-@:--.--
            lst[4] = int(txt[6])     # --:--:@-.--
            lst[5] = int(txt[7])     # --:--:-@.--
            self.cr1 = ":"           # 左はコロン
            self.cr2 = ":"           # 右もコロン
        self.drw_seg(lst)


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンス生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
