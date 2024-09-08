# コマンド入力
def command(mw, cmd: str):
    cmd = cmd.split()
    err = 0

    # 予約設定
    if cmd[0] == "rsv":
        pass

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
        mw.etr.configure(textvariable="")  # 入力欄を初期化したい
        mw.etr.focus_set()  # 入力欄にフォーカスを設定したい
