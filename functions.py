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

