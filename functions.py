import tkinter as tk
from functools import partial
from datetime import datetime
import os
import global_val as g


# 時間クラス
class Time:
    def __init__(self, n=0):
        self.n = n  # 00:00:00.00~99:59:59.99をint型に

    # テキストから時間を登録
    def set_txt(self, t: str):
        try:
            self.n = int(t[9:11])           # ms
            self.n += int(t[6:8]) * 100     # s
            self.n += int(t[3:5]) * 6000    # m
            self.n += int(t[0:2]) * 360000  # h
        except IndexError:
            print("Time.set_txt Error!", IndexError)
            return 901
        except ValueError:
            print("Time.set_txt Error!", ValueError)
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
        t = str(n % 100).zfill(2)                  # ---------ms
        t = str(n // 100 % 60).zfill(2) + "." + t  # ------ss.ms
        t = str(n // 60 % 60).zfill(2) + ":" + t   # ---mm:ss.ms
        t = str(n // 60 % 100).zfill(2) + ":" + t  # hh:mm:ss.ms
        return t

    # リスト出力
    def out_lst(self):
        # 出力数値の決定
        if self.n < 180000:  # 30m未満
            n = [
                self.n // 6000 % 60 // 10, self.n // 6000 % 10,  # 10m, 1m
                self.n // 100 % 60 // 10, self.n // 100 % 10,    # 10s, 1s
                self.n % 100 // 10, self.n % 10                  # 0.1s, 0.01s
            ]
        else:
            n = [
                self.n // 3600000, self.n // 360000 % 10,        # 10h, 1h
                self.n // 6000 % 60 // 10, self.n // 6000 % 10,  # 10m, 1m
                self.n // 100 % 60 // 10, self.n // 100 % 10,    # 10s, 1s
            ]

