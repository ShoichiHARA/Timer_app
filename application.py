import tkinter as tk
from tkinter import colorchooser
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
        self.now = fc.Time()  # 現在時刻
        self.tmr = fc.Time()  # 表示時間

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
        self.now.get_now()


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


# ストップウォッチクラス
class Watch:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # ストップウォッチタブのフレーム
        self.wtc = tk.Label(self.frm)        # 時計
        self.ssb = tk.Button(self.frm)       # スタート/ストップボタン
        self.rst = tk.Button(self.frm)       # リセットボタン
        self.dsp = tk.Button(self.frm)       # サブウインドウ表示ボタン

        self.widgets()

    def widgets(self):
        # 設定
        self.wtc.configure(text=self.mw.tmr.out_txt(), font=("", 60))
        self.ssb.configure(text=lg.stt, font=("", 15), width=15, height=3)
        self.rst.configure(text=lg.rst, font=("", 15), width=15, height=3)
        self.dsp.configure(text=lg.viw, font=("", 15), width=32, height=1)

        # 関数割付

        # 配置
        self.wtc.place(x=15, y=20)
        self.ssb.place(x=20, y=120)
        self.rst.place(x=210, y=120)
        self.dsp.place(x=22, y=210)


# 設定クラス
class Setting:
    def __init__(self,mw: MainWin):
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 設定タブのフレーム
        self.add = tk.Button(self.frm)       # 行追加ボタン
        self.dlt = tk.Button(self.frm)       # 行削除ボタン

        self.widgets()

    def widgets(self):
        # 設定
        self.add.configure(text=lg.rad, width=10)
        self.dlt.configure(text=lg.rdl, width=10)

        # 配置
        self.add.place(x=190, y=g.row0*25+55)
        self.dlt.place(x=280, y=g.row0*25+55)


# 予定クラス
class Schedule:
    def __init__(self, mw: MainWin):
        # 定義
        self.mw = mw
        self.frm = tk.Frame(self.mw.master)  # 予定タブのフレーム
        self.add = tk.Button(self.frm)       # 行追加ボタン
        self.dlt = tk.Button(self.frm)       # 行削除ボタン
        self.scr = tk.Scrollbar(self.frm)    # スクロールバー

        self.widgets()

    def widgets(self):
        # 設定
        self.add.configure(text=lg.rad, width=10)
        self.dlt.configure(text=lg.rdl, width=10)

        # 配置
        self.add.place(x=190, y=g.row0*25+55)
        self.dlt.place(x=280, y=g.row0*25+55)


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


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンス生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
