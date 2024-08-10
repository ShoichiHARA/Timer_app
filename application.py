import tkinter as tk
from tkinter import ttk
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

        # ウインドウ設定
        self.master.title(self.lg.mwn)       # ウインドウタイトル
        self.master.geometry("800x600")      # ウインドウサイズ
        self.master.resizable(False, False)  # サイズ変更禁止
        self.widgets()                       # ウィジェット
        self.event()                         # イベント

    # ウィジェット
    def widgets(self: tk.Tk):
        pass

    # 終了
    def exit(self):
        self.master.destroy()

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

        def k_release(e):  # キーボード離した場合
            self.keys.remove(e.keysym)
            if e.keysym == "Escape":
                self.exit()  # プログラム終了

        self.master.bind("<ButtonPress>", m_press)
        self.master.bind("<ButtonRelease>", m_release)
        self.master.bind("<KeyPress>", k_press)
        self.master.bind("<KeyRelease>", k_release)


# アプリケーション
def application():
    root = tk.Tk()              # Tkinterインスタンスの生成
    app = MainWin(master=root)  # アプリケーション実行
    app.mainloop()              # ウインドウの描画
