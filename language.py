# 言語クラス
class Language:
    def __init__(self, lg="ENG"):
        lg_list = ["ENG", "JPN"]
        for i in range(len(lg_list)):
            if lg_list[i] == lg:
                self.mwn = output(i, ["Count Up Timer", "カウントアップタイマー"])
                self.fil = output(i, ["File", "ファイル"])
                self.opn = output(i, ["Open", "開く"])
                self.sav = output(i, ["Save", "上書き保存"])
                self.sva = output(i, ["Save as", "名前を付けて保存"])
                self.set = output(i, ["Setting", "設定"])
                self.ext = output(i, ["Exit", "終了"])
                self.sim = output(i, ["Simulation", "シミュレーション"])
                self.run = output(i, ["Run", "実行"])
                self.stp = output(i, ["Stop", "停止"])
                self.viw = output(i, ["View", "表示"])
                self.prb = output(i, ["Practice Board", "実習盤"])
                self.ioa = output(i, ["I/O Allocation", "入出力割付表"])
                self.hlp = output(i, ["Help", "ヘルプ"])
                break


# 配列から1つ出力
def output(a, lst):
    return lst[a]
