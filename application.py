import tkinter as tk
from tkinter import ttk
import datetime
import language as lg


# 設定クラス
class Setting:
    def __init__(self):
        self.lg = "JPN"


# メインウインドウクラス
class MainWin(tk.Frame):
    def __init__(self: tk.Tk, master):
        super().__init__(master)  # 親クラス継承
        self.pack()               # 配置

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.keys = []                      # キーボードの状態
        self.bt0 = tk.Button(self.master, text="Button", command=self.tm_win)  # ボタン1

        # ウインドウの定義
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("400x300")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()                       # ウィジェット
        self.event()                         # イベント

        # サブウインドウの定義
        self.tm_mas = None
        self.tm_app = None

    # ウィジェット
    def widgets(self: tk.Tk):
        self.bt0.pack()

    # 終了
    def exit(self):
        self.master.destroy()

    # 表示ウインドウ表示
    def tm_win(self):
        if self.tm_mas is None:
            self.tm_mas = tk.Toplevel(self.master)
            self.tm_app = TMWin(self.tm_mas)
        elif not self.tm_mas.winfo_exists():
            self.tm_mas = tk.Toplevel(self.master)
            self.tm_app = TMWin(self.tm_mas)

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
                print(datetime.datetime.now())

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
    def __init__(self: tk.Tk, master):
        super().__init__(master)
        self.pack()

        # 定義
        self.set = Setting()                # 設定
        self.lg = lg.Language(self.set.lg)  # 言語
        self.frm = tk.Frame(self.master)  # フレーム

        # ウインドウの定義
        self.master.title(self.lg.twn)
        self.master.geometry("400x300")
        self.widgets()  # ウィジェット

    def widgets(self: tk.Tk):
        # フレームの設定
        self.frm.pack(fill=tk.BOTH, expand=True)


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
