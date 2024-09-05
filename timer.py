from datetime import datetime


# 時間クラス
class Time:
    def __init__(self, h=None, m=None, s=None, ms=None):
        self.h = 0
        self.m = 0
        self.s = 0
        self.ms = 0  # 100msで1
        self.set_tmr(h, m, s, ms)

    # 時間をセット
    def set_tmr(self, h=None, m=None, s=None, ms=None):
        if h is not None:
            self.h = h
        if m is not None:
            self.m = m
        if s is not None:
            self.s = s
        if ms is not None:
            self.ms = ms

    # 文字列から時間をセット
    def inp_txt(self, txt):
        self.h = int(txt[0]) * 10 + int(txt[1])
        self.m = int(txt[3]) * 10 + int(txt[4])
        self.s = int(txt[6]) * 10 + int(txt[7])
        self.ms = int(txt[9])

    # 現在時刻を取得
    def get_now(self):
        t = datetime.now()
        self.h = t.hour
        self.m = t.minute
        self.s = t.second
        self.ms = t.microsecond // 100000

    # 時間をカウント
    def cnt_tmr(self):
        self.ms += 1
        self.chk_tmr()

    # 時間をコピー
    def cpy_tmr(self, tm):
        self.set_tmr(h=tm.h, m=tm.m, s=tm.s, ms=self.ms)

    # 時間を比較
    def cmp_tmr(self, tm):
        if self.h > tm.h:  # 引数より自身の方が大きい場合
            return 1       # 1を返す
        elif self.h < tm.h:  # 引数より自身の方が小さい場合
            return -1        # -1を返す
        elif self.m > tm.m:
            return 1
        elif self.m < tm.m:
            return -1
        elif self.s > tm.s:
            return 1
        elif self.s < tm.s:
            return -1
        elif self.ms > tm.ms:
            return 1
        elif self.ms < tm.ms:
            return -1
        return 0  # 同じの場合、0を返す

    # 文字列から時間を比較
    def cmp_txt(self, txt):
        tmr = Time()
        tmr.inp_txt(txt)
        return self.cmp_tmr(tmr)

    # 時間をチェック
    def chk_tmr(self):
        if self.ms >= 10:
            self.s += self.ms // 10  # 超えた分繰り上げ
            self.ms %= 10            # 繰り上げた分引く
        if self.ms < 0:
            while self.ms < 0:  # 正になるまで繰り返し
                self.ms += 10   # 足りない分繰り下げ
                self.s -= 1     # 繰り下げ
        if self.s >= 60:
            self.m += self.s // 60  # 超えた分繰り上げ
            self.s %= 60            # 繰り上げた分引く
        if self.s < 0:
            while self.s < 0:  # 正になるまで繰り返し
                self.s += 60   # 足りない分繰り下げ
                self.m -= 1    # 繰り下げ
        if self.m >= 60:
            self.h += self.m // 60  # 超えた分繰り上げ
            self.m %= 60            # 繰り上げた分引く
        if self.m < 0:
            while self.m < 0:  # 正になるまで繰り返し
                self.m += 60   # 足りない分繰り下げ
                self.h -= 1    # 繰り下げ
        if self.h >= 100:
            self.h %= 100
        if self.h < 0:
            while self.h < 0:       # 正になるまで繰り返し
                self.h += 100       # 足りない分足す

    # テキスト出力
    def out_txt(self):
        t = str(self.h).zfill(2) + ":" + str(self.m).zfill(2) + ":"
        t = t + str(self.s).zfill(2) + "." + str(self.ms)
        return t

    # 7セグ出力
    def out_seg(self, cvs, c, b, x, y, s):
        # セグの定義
        seg_h1 = SevenSeg(num=self.h//10, clr=c, bgc=b)
        seg_h0 = SevenSeg(num=self.h%10, clr=c, bgc=b)
        seg_m1 = SevenSeg(num=self.m//10, clr=c, bgc=b)
        seg_m0 = SevenSeg(num=self.m%10, clr=c, bgc=b)
        seg_s1 = SevenSeg(num=self.s//10, clr=c, bgc=b)
        seg_s0 = SevenSeg(num=self.s%10, clr=c, bgc=b)
        seg_ms = SevenSeg(num=self.ms, clr=c, bgc=b)

        # セグの配置
        seg_h1.place(cvs, -45*s+x, y, s)
        seg_h0.place(cvs, -33*s+x, y, s)
        cvs.create_rectangle(
            -25*s+x, -4*s+y, -23*s+x, -2*s+y,
            fill=c, width=0
        )
        cvs.create_rectangle(
            -25*s+x, 2*s+y, -23*s+x, 4*s+y,
            fill=c, width=0
        )
        seg_m1.place(cvs, -15*s+x, y, s)
        seg_m0.place(cvs, -3*s+x, y, s)
        cvs.create_rectangle(
            5*s+x, -4*s+y, 7*s+x, -2*s+y,
            fill=c, width=0
        )
        cvs.create_rectangle(
            5*s+x, 2*s+y, 7*s+x, 4*s+y,
            fill=c, width=0
        )
        seg_s1.place(cvs, 15*s+x, y, s)
        seg_s0.place(cvs, 27*s+x, y, s)
        cvs.create_rectangle(
            35*s+x, 6*s+y, 37*s+x, 8*s+y,
            fill=c, width=0
        )
        seg_ms.place(cvs, 45*s+x, y, s)


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
