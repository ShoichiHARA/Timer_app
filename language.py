# 言語クラス
class Language:
    def __init__(self, lg="ENG"):
        lg_list = ["ENG", "JPN"]
        for i in range(len(lg_list)):
            if lg_list[i] == lg:
                self.mwn = output(i, ["Count Up Timer", "カウントアップタイマー"])
                self.twn = output(i, ["Timer", "表示ウインドウ"])
                self.fil = output(i, ["File", "ファイル"])
                self.opn = output(i, ["Open", "開く"])
                self.sav = output(i, ["Save", "上書き保存"])
                self.sva = output(i, ["Save as", "名前を付けて保存"])
                self.set = output(i, ["Setting", "設定"])
                self.ext = output(i, ["Exit", "終了"])
                self.sim = output(i, ["Simulation", "シミュレーション"])
                self.stt = output(i, ["Start", "開始"])
                self.stp = output(i, ["Stop", "停止"])
                self.rst = output(i, ["Reset", "初期化"])
                self.now = output(i, ["Now", "現在時刻"])
                self.ccr = output(i, ["Change text/background Color", "文字/背景 色変更"])
                self.rss = output(i, ["Reserved Start/Stop", "開始/停止 予約"])
                self.hlp = output(i, ["Help", "ヘルプ"])
                self.tim = output(i, ["Time", "時間"])
                self.clr = output(i, ["tx color", "文字色"])
                self.bgc = output(i, ["bg color", "背景色"])
                self.ook = output(i, ["ok", "決定"])
                self.dlt = output(i, ["delete", "削除"])
                self.ccl = output(i, ["cancel", "取消"])
                break


# 配列から1つ出力
def output(a, lst):
    return lst[a]
