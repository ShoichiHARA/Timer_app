from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime

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
        except IndexError as err:
            print(err)
            return 901
        except ValueError as err:
            print(err)
            return 902

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


# コマンド入力
def command(mw: MainWin, cmd: str):
    cmd = cmd.split()
    err = 0

    # 予約設定
    if cmd[0] == "rsv":
        pass

    # 色設定
    elif cmd[0] == "set":
        for i in range(len(mw.set_tab)/4):
            if mw.set_tab.tab[i]["text"] == "":  # 行が未完成の場合
                for j in range(1, 3):  # 時間、文字色、背景色の順に登録
                    mw.set_tab.x = j
                    mw.set_tab.y = i
                    mw.set_tab.tab[4*i+j].update(cmd[j])  # 入力データが有効か判断する必要あり
                break
        mw.set_tab.update()

    # 現在値変更
    elif cmd[0] == "tmr":
        err = mw.tmr.set_txt(cmd[1])
        print(mw.tmr.out_txt())

    # 表示ウインドウ表示
    elif cmd[0] == "view":
        mw.viw_win()

    # エラー処理
    if err != 0:
        print("err", err)
    else:
        print("else")
        mw.etr.delete(0, "end")
        # mw.master.attributes("-topmost", True)
        # mw.master.attributes("-topmost", False)
        mw.master.focus_set()
        mw.etr.focus_set()  # 入力欄にフォーカスを設定したい