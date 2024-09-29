from __future__ import annotations
from typing import TYPE_CHECKING
from tkinter import colorchooser
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


# グローバル変数開く
def o_gval():
    if os.path.exists(g.gpt):  # ファイルが存在するか
        with open(g.gpt, "r") as f:
            t = f.read().split()
            g.lg.__init__(t[0])
            g.clr0 = t[1]
            g.bgc0 = t[2]
            g.in_zer = bool(t[3])
            g.scn0 = t[4]
            g.row = int(t[5])
        return 0
    else:
        return 940


# グローバル変数保存
def s_gval():
    with open(g.gpt, "w") as f:
        t = g.lg.lg + " "  # 言語
        t += g.clr0 + " "  # 文字色初期値
        t += g.bgc0 + " "  # 背景色初期値
        t += str(g.in_zer) + " "  # 未記入セルの初期値
        t += g.scn0 + " "  # 場面初期値
        t += str(g.row) + " "  # 行数初期値
        f.write(t)


# コマンド入力
def command(e, mw: MainWin, cmd: str):
    cmd = cmd.split()
    err = 0

    # 色変更ウインドウ
    if cmd[0] == "clr":
        clr = colorchooser.askcolor(mw.clr, title=g.lg.ccr)
        mw.clr = clr[1]
        print(mw.clr)

    # コマンド欄非表示
    if cmd[0] == "cmd":
        if cmd[1] == "off":
            g.md_cmd = False
            mw.dsp_cmd()

    # アプリケーション終了
    elif cmd[0] == "exit":
        mw.master.destroy()

    # 開く
    elif cmd[0] == "open":
        try:
            mw.fl.open(cmd[1])
        except IndexError:
            print("function Line 242", IndexError)
            err = 941

    # タイマー初期化
    elif cmd[0] == "rst":
        mw.st.crt = 0
        mw.sc.crt = 0
        mw.tmr.set_int(0)

    # 保存
    elif cmd[0] == "save":
        try:
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
        mw.wt.frm.pack_forget()
        mw.st.frm.pack_forget()
        mw.sc.frm.pack_forget()
        try:
            if cmd[1] == "file":
                pass
            elif cmd[1] in ["tmr", "TMR"]:
                mw.scn = "TMR"
                mw.wt.frm.pack(expand=True, fill="both")
            elif cmd[1] in ["set", "SET"]:
                mw.scn = "SET"
                mw.st.frm.pack(expand=True, fill="both")
            elif cmd[1] in ["scd", "SCD"]:
                mw.scn = "SCD"
                mw.sc.frm.pack(expand=True, fill="both")
            elif cmd[1] == "help":
                pass
            else:
                err = 902
            mw.etr.lift()
        except IndexError:
            print("function Line 250", IndexError)
            command(e=None, mw=mw, cmd="scn "+mw.scn)
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
    elif cmd[0] == "ss":
        mw.cnt = not mw.cnt
        if mw.cnt:
            mw.wt.ssb.configure(text=g.lg.stp)
        else:
            mw.wt.ssb.configure(text=g.lg.stt)

    # タイマー開始
    elif cmd[0] == "start":
        mw.cnt = True
        mw.wt.ssb.configure(text=g.lg.stp)

    # タイマー停止
    elif cmd[0] == "stop":
        mw.cnt = False
        mw.wt.ssb.configure(text=g.lg.stt)

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
        mw.viw_win()
        mw.master.tkraise(mw.viw_mas)

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
910:時間入力時、文字数が適切でない
911:時間入力時、文字種が適切でない
920:色入力時、カラーコードが適切でない
940:ファイルが存在しない
941:開くコマンドの引数が適切でない
942:保存コマンドの引数が適切でない

"""