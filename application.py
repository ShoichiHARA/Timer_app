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

        self.swc = Watch(self)  # ストップウォッタブ
        self.stg = ""  # 設定タブ
        self.scd = ""  # 予定タブ
        self.hlp = ""  # ヘルプタブ
        self.fil = ""  # ファイルタブ
        self.men = MenuBar(self)  # メニューバー

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

        if scn == "FIL":
            self.mw.fil.frm.pack(expand=True, fill="both")
        elif scn == "TMR":
            self.mw.swc.frm.pack(expand=True, fill="both")


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


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンス生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
