from __future__ import annotations
from typing import TYPE_CHECKING
import tkinter as tk
from functools import partial
from datetime import datetime
import os
import global_val as g

if TYPE_CHECKING:
    from application import MainWin


# 時間クラス
class Time:
    def __init__(self, n=0):
        self.n = n  # 00:00:00.00 ～ 99:59:59.99をint型に

    # int型から時間を登録
    def set_int(self, n: int):
        self.n = n

    # テキストから時間を登録
    def set_txt(self, t: str):
        try:
            self.n = int(t[9]) * 10 + int(t[10])  # ms
            self.n += (int(t[6]) * 10 + int(t[7])) * 100  # s
            self.n += (int(t[3]) * 10 + int(t[4])) * 6000  # m
            self.n += (int(t[0]) * 10 + int(t[1])) * 360000  # h
            return 0
        except IndexError:
            print("function Line 29", IndexError)
            return 910
        except ValueError:
            print("function Line 32", ValueError)
            return 911

    # 現在時刻取得
    def get_now(self):
        n = datetime.now()
        self.n = n.microsecond // 10000
        self.n += n.second * 100
        self.n += n.minute * 6000
        self.n += n.hour * 360000

    # テキスト出力
    def out_txt(self):
        n = self.n
        t = str(n%100).zfill(2)            # ---------ms
        n = n // 100
        t = str(n%60).zfill(2) + "." + t   # ------ss.ms
        n = n // 60
        t = str(n%60).zfill(2) + ":" + t   # ---mm:ss.ms
        n = n // 60
        t = str(n%100).zfill(2) + ":" + t  # hh:mm:ss.ms
        return t

    # 7セグ出力
    def out_seg(self, cvs, c, b, x, y, s):
        # 表示数値の決定
        if self.n < 180000:  # 30m未満
            n = [
                self.n // 6000 % 60 // 10, self.n // 6000 % 10,  # 10m, 1m
                self.n // 100 % 60 // 10, self.n // 100 % 10,  # 10s, 1s
                self.n % 100 // 10, self.n % 10  # 0.1s, 0.01s
            ]
        else:
            n = [
                self.n // 3600000, self.n // 360000 % 10,  # 10h, 1h
                self.n // 6000 % 60 // 10, self.n // 6000 % 10,  # 10m, 1m
                self.n // 100 % 60 // 10, self.n // 100 % 10,  # 10s, 1s
            ]

        # コロン, カンマの配置
        cvs.create_rectangle(
            -16*s+x, -4*s+y, -14*s+x, -2*s+y, fill=c, width=0
        )
        cvs.create_rectangle(
            -16*s+x, 2*s+y, -14*s+x, 4*s+y, fill=c, width=0
        )
        if self.n < 180000:  # 30m未満
            cvs.create_rectangle(
                14*s+x, 6*s+y, 16*s+x, 8*s+y, fill=c, width=0
            )
        else:
            cvs.create_rectangle(
                14*s+x, -4*s+y, 16*s+x, -2*s+y, fill=c, width=0
            )
            cvs.create_rectangle(
                14*s+x, 2*s+y, 16*s+x, 4*s+y, fill=c, width=0
            )

        # セグの定義
        seg = []
        x = [-36*s+x, -24*s+x, -6*s+x, 6*s+x, 24*s+x, 36*s+x]

        # セグの配置
        for i in range(6):
            seg.append(SevenSeg(num=n[i], clr=c, bgc=b))
            seg[i].place(cvs, x[i], y, s)


# 7セグクラス
class SevenSeg:
    def __init__(self, num=0, clr="black", bgc="white"):
        # 定義
        self.num = None  # 数値
        self.clr = None  # 文字色
        self.bgc = None  # 背景色
        self.seg = [None] * 7  # セグデータ
        self.cls = [None] * 7  # セグの色ONOFFデータ
        self.bit = [
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

        # 初期設定
        self.set_num(num)       # 数値
        self.set_clr(clr, bgc)  # 色
        self.set_bit()          # セグの設定

    # 数値の設定
    def set_num(self, num):
        self.num = num % 10  # 一の位
        self.set_bit()

    # 色の設定
    def set_clr(self, clr, bgc):
        self.clr = clr  # 文字色
        self.bgc = bgc  # 背景色
        self.set_bit()  # セグの設定

    def set_bit(self):
        for i in range(7):
            if self.bit[self.num][i] == 0:
                self.cls[i] = self.bgc
            else:
                self.cls[i] = self.clr

    # 配置
    def place(self, cvs,  x, y, s):
        self.set_bit()
        a = 3
        b = 5
        self.seg[0] = cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-3)*s+y, a*s+x, (-b-3)*s+y,
            (a+1)*s+x, (-b-2)*s+y, a*s+x, (-b-1)*s+y, -a*s+x, (-b-1)*s+y,
            fill=self.cls[0], outline=self.bgc, width=s/5
        )
        self.seg[1] = cvs.create_polygon(
            (a+1)*s+x, (-b-2)*s+y, (a+2)*s+x, (-b-1)*s+y, (a+2)*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, -s+y, a*s+x, (-b-1)*s+y,
            fill=self.cls[1], outline=self.bgc, width=s/5
        )
        self.seg[2] = cvs.create_polygon(
            (a+1)*s+x, y, (a+2)*s+x, s+y, (a+2)*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+1)*s+y, a*s+x, s+y,
            fill=self.cls[2], outline=self.bgc, width=s/5
        )
        self.seg[3] = cvs.create_polygon(
            (-a-1)*s+x, (b+2)*s+y, -a*s+x, (b+1)*s+y, a*s+x, (b+1)*s+y,
            (a+1)*s+x, (b+2)*s+y, a*s+x, (b+3)*s+y, -a*s+x, (b+3)*s+y,
            fill=self.cls[3], outline=self.bgc, width=s/5
        )
        self.seg[4] = cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, s+y, -a*s+x, (b+1)*s+y,
            (-a-1)*s+x, (b+2)*s+y, (-a-2)*s+x, (b+1)*s+y, (-a-2)*s+x, s+y,
            fill=self.cls[4], outline=self.bgc, width=s/5
        )
        self.seg[5] = cvs.create_polygon(
            (-a-1)*s+x, (-b-2)*s+y, -a*s+x, (-b-1)*s+y, -a*s+x, -s+y,
            (-a-1)*s+x, y, (-a-2)*s+x, -s+y, (-a-2)*s+x, (-b-1)*s+y,
            fill=self.cls[5], outline=self.bgc, width=s/5
        )
        self.seg[6] = cvs.create_polygon(
            (-a-1)*s+x, y, -a*s+x, -s+y, a*s+x, -s+y,
            (a+1)*s+x, y, a*s+x, s+y, -a*s+x, s+y,
            fill=self.cls[6], outline=self.bgc, width=s/5
        )


# コンボボックス
class Combobox:
    def __init__(
            self, mas, width=0, height=0, row=1, text="", tags="", font=11, lst=None
    ):
        self.mas = mas     # ボックス配置元
        self.wid = width   # 幅
        self.hei = height  # 高さ
        self.row = row     # 表示表の行数
        self.txt = text    # ボックステキスト
        self.tag = tags    # タグ
        self.fnt = font    # フォントサイズ
        if lst is None:
            self.lst = [""]
        else:
            self.lst = lst

        self.frm = tk.Frame(self.mas)                          # コンボボックスフレーム
        self.tab = tk.Canvas(self.frm, highlightthickness=0)   # タブ用キャンバス
        self.box = tk.Canvas(self.frm, highlightthickness=0)   # ボックス用キャンバス
        self.scr = tk.Scrollbar(self.frm, orient=tk.VERTICAL)  # タブ用スクロールバー

        self.widgets()
        self.box.bind("<ButtonPress-1>", self.click)
        self.tab.bind("<ButtonPress-1>", self.select)
        self.mas.bind("<ButtonPress-1>", self.clear)

    def widgets(self):
        # ウィジェット設定
        self.frm.configure(width=self.wid, height=self.hei)
        self.box.configure(width=self.wid, height=self.hei, cursor="hand2")
        self.box.create_rectangle(
            0, 0, self.wid-1, self.hei-1,
            fill="SystemButtonFace", width=1, outline="#000000"
        )
        self.box.create_text(
            self.wid/2, self.hei/2, tags="box",
            text=self.txt, font=("", self.fnt), activefill="dimgray"
        )

        # 配置
        self.box.place(x=0, y=0)  # キャンバス配置

    # ボックス配置
    def place(self, x, y):
        self.frm.place(x=x, y=y)

    # ボックスクリック
    def click(self, e):
        th = self.fnt * min(self.row, len(self.lst)) * 2 + 1  # 表の高さ
        sh = self.fnt * len(self.lst) * 2 + 1                 # 表の可動高さ
        self.frm.configure(width=self.wid+20, height=self.hei+th)
        self.tab.configure(
            width=self.wid, height=th, relief="flat", cursor="hand2",
            scrollregion=(0, 0, self.wid, sh), yscrollcommand=self.scr.set
        )
        self.scr.configure(bg="black", relief="flat", command=self.tab.yview)
        for i in range(len(self.lst)):
            self.tab.create_text(
                self.wid/2, i*self.fnt*2+self.fnt,
                text=self.lst[i], font=("", self.fnt), activefill="dimgray"
            )
            self.tab.create_rectangle(
                0, i*self.fnt*2, self.wid-1, i*self.fnt*2+(self.fnt*2),
            )

        # 配置
        self.tab.place(x=0, y=self.hei-1)
        self.scr.place(x=self.wid, y=self.hei, height=th)

    # ボックス内選択
    def select(self, e):
        s = self.scr.get()                       # スクロールバーの位置
        d = s[0] * self.fnt * len(self.lst) * 2  # スクロール量(ピクセル)
        n = (e.y + int(d)) // (self.fnt * 2)
        self.txt = self.lst[n]
        self.box.itemconfig(tagOrId="box", text=self.txt)
        self.clear(e)

    # ボックスタブ非表示
    def clear(self, e):
        self.tab.place_forget()
        self.scr.place_forget()
        self.frm.configure(width=self.wid, height=self.hei)


# 時間変更ウインドウ
class ChanTimeWin(tk.Frame):
    def __init__(self: tk.Tk, master, tim=None):
        super().__init__(master)
        self.pack()

        # 定義
        if tim is None:
            self.tim = Time()
        else:
            self.tim = Time(tim.n)
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
                command=partial(self.ps_ch, n=d[i])
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


# 文字型ブールをブール型へ
def tobool(txt):
    if txt == "True":
        return True
    elif txt == "False":
        return False
    else:
        return


# カラーコード判定
def color(clr):
    lst = [
        "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "a", "b", "c", "d", "e", "f"
    ]
    if clr in g.ccd:
        return True
    elif clr[0] == "#":
        for i in range(6):
            if clr[i] not in lst:
                return False
        return True
    else:
        return False


# グローバル変数開く
def o_gval():
    if os.path.exists(g.gpt):  # ファイルが存在するか
        with open(g.gpt, "r") as f:
            while True:
                t = f.readline().split()
                if t[0] == "END":
                    break
                elif t[0] == "lg":
                    g.lg.__init__(t[1])
                elif t[0] == "clr0":
                    g.clr0 = t[1]
                elif t[0] == "bgc0":
                    g.bgc0 = t[1]
                elif t[0] == "md_cmd":
                    g.md_cmd = tobool(t[1])
                elif t[0] == "in_zer":
                    g.in_zer = tobool(t[1])
                elif t[0] == "scn0":
                    g.scn0 = t[1]
                elif t[0] == "row":
                    g.row = int(t[1])
                elif t[0] == "ctn":
                    g.ctn = tobool(t[1])
        return 0
    else:
        return 940


# グローバル変数保存
def s_gval():
    with open(g.gpt, "w") as f:
        t = "lg " + g.lg.lg + "\n"             # 言語
        t += "clr0 " + g.clr0 + "\n"           # 文字色初期値
        t += "bgc0 " + g.bgc0 + "\n"           # 背景色初期値
        t += "md_cmd " + str(g.md_cmd) + "\n"  # コマンドモード
        t += "in_zer " + str(g.in_zer) + "\n"  # 未記入セルの初期値
        t += "scn0 " + g.scn0 + "\n"           # 場面初期値
        t += "row " + str(g.row) + "\n"        # 行数初期値
        t += "ctn " + str(g.ctn) + "\n"        # 前回の続き
        t += "END"
        f.write(t)


# コマンド入力
def command(e, mw: MainWin, cmd: str):
    cmd = cmd.split()
    err = 0

    # コマンド欄非表示
    if cmd[0] == "cmd":
        if cmd[1] == "off":
            g.md_cmd = False
            mw.dsp_cmd()

    # 起動変数（グローバル変数）変更
    elif cmd[0] == "configure":
        try:
            if cmd[1] == "lg":  # 言語変更（再起動が必要）
                if cmd[2] in g.lg.lg_list:
                    g.lg.lg = cmd[2]
                else:
                    err = 962
            elif cmd[1] == "clr0":  # 初期文字色
                if color(cmd[2]):
                    g.clr0 = cmd[2]
                else:
                    err = 920
            elif cmd[1] == "bgc0":  # 初期背景色
                if color(cmd[2]):
                    g.bgc0 = cmd[2]
                else:
                    err = 920
            # elif cmd[1] == "cmd":  # 初期コマンドモード
            #     if cmd[2] in ["True", "False"]:
            #         g.md_cmd = bool(cmd[2])
            #     else:
            #         err = 963
            elif cmd[1] == "zero":  # 未記入の表を選択
                if cmd[2] in ["True", "False"]:
                    g.in_zer = bool(cmd[2])
                else:
                    err = 963
            elif cmd[1] == "scn0":
                if cmd[2] in mw.mn.lst:
                    g.scn0 = cmd[2]
                else:
                    err = 964
            elif cmd[1] == "row0":  # 表に表示する行の数
                if 0 < int(cmd[2]) < 21:
                    g.row = int(cmd[2])
                else:
                    err = 965
            elif cmd[1] == "ctn":  # 続きから始めるか
                if cmd[2] in ["True", "False"]:
                    g.ctn = bool(cmd[2])
                else:
                    err = 963
            else:
                err = 961
        except IndexError:
            print("function Line 242", IndexError)
            err = 960

    # 現在値変更
    elif cmd[0] == "cur":
        try:
            tim = Time()
            err = tim.set_txt(cmd[1])
            if err == 0:
                mw.wt.change(None, tim)
        except IndexError:
            print("function Line 242", IndexError)
            err = 905

    # アプリケーション終了
    elif cmd[0] == "exit":
        mw.exit(e)

    # 新規作成
    elif cmd[0] == "new":
        mw.fl.new()

    # 開く
    elif cmd[0] == "open":
        try:
            if cmd[1].rfind(".cut") != len(cmd[1])-4:  # 拡張子を入力していない
                cmd[1] += ".cut"                       # 拡張子追加
            mw.fl.open(cmd[1])
        except IndexError:
            print("function Line 242", IndexError)
            err = 941

    # タイマー初期化
    elif cmd[0] in ["rst", "reset"]:
        mw.wt.reset(e)

    # 保存
    elif cmd[0] == "save":
        try:
            if cmd[1].rfind(".cut") != len(cmd[1])-4:  # 拡張子を入力していない
                cmd[1] += ".cut"                       # 拡張子追加
            mw.fl.save(cmd[1])
        except IndexError:
            print("function Line 250", IndexError)
            err = 942

    # 予定設定
    elif cmd[0] == "scd":
        if cmd[1] in ["+", "-"]:  # 行追加または行削除
            mw.sc.table(cmd[1])
        else:
            for i in range(mw.sc.row):  # 入力行探し
                if mw.sc.txt[3*i] == "":  # 設定行が未完成の場合
                    for j in range(1, 3):  # 1列ずつ設定
                        try:
                            if cmd[j] == "None":
                                err = mw.sc.change(3*i+j, "")
                            else:
                                err = mw.sc.change(3*i+j, cmd[j])
                        except IndexError:
                            print("function Line 256", IndexError)
                            err = 904
                        if err != 0:
                            break
                    break

    # 場面変更
    elif cmd[0] == "scn":
        try:
            if cmd[1] in mw.mn.lst:
                mw.mn.change(cmd[1])
            else:
                print("function Line 250")
                err = 902
            mw.etr.lift()
        except IndexError:
            print("function Line 250", IndexError)
            err = 901

    # 色設定
    elif cmd[0] == "set":
        if cmd[1] in ["+", "-"]:  # 行追加または行削除
            mw.st.table(cmd[1])
        else:
            for i in range(mw.st.row):  # 入力行探し
                if mw.st.txt[4*i] == "":  # 設定行が未完成の場合
                    for j in range(1, 4):  # 1列ずつ設定
                        try:
                            err = mw.st.change(4*i+j, cmd[j])
                        except IndexError:
                            print("function Line 261", IndexError)
                            err = 903
                        if err != 0:
                            break
                    break

    # タイマー開始/停止
    elif cmd[0] in ["ss", "start", "stop"]:
        mw.wt.stt_stp(cmd[0])

    # テスト
    elif cmd[0] == "test":
        if cmd[1] == "open":
            err = o_gval()
        elif cmd[1] == "save":
            s_gval()
        else:
            err = 999

    # 現在値変更
    elif cmd[0] == "tmr":
        err = mw.tmr.set_txt(cmd[1])
        print(mw.tmr.out_txt())

    # 表示ウインドウ表示
    elif cmd[0] == "view":
        mw.wt.display()
        # mw.viw_win()
        # mw.master.tkraise(mw.viw_mas)

    # 該当コマンドなし
    else:
        err = 900

    # エラー処理
    if err != 0:
        print("err", err)
    else:
        print(cmd[0], "cmd OK")
        if cmd[0] != "exit":
            mw.etr.delete(0, "end")
    return err


"""
エラーコード集

900:該当コマンドなし
901:場面変更コマンドの引数が適切でない
902:場面変更コマンドの引数が存在しない
903:設定コマンドの引数が適切でない
904:予約コマンドの引数が適切でない
905:現在値変更コマンドの引数が適切でない
910:時間入力時、文字数が適切でない
911:時間入力時、文字種が適切でない
920:色入力時、カラーコードが適切でない
940:ファイルが存在しない
941:開くコマンドの引数が適切でない
942:保存コマンドの引数が適切でない
960:構成変更コマンドの引数が適切でない
961:構成変更コマンドの項目が存在しない
962:構成変更コマンドの設定値が適切でない(ENG, JPN)
963:構成変更コマンドの設定値が適切でない(True, False)
964:構成変更コマンドの設定値が適切でない(タブ名)
965:構成変更コマンドの設定値が適切でない(1 ~ 20)


"""