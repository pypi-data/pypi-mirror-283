import argparse
import logging
from .create import Create

# ロガーの設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Roombaのポート
ROOMBA_PORT = "/dev/ttyACM0"

def main():
    """
    Roombaを制御するCLIアプリケーションのエントリーポイント。
    """

    # 引数のパーサーを作成
    parser = argparse.ArgumentParser(description='Roombaを遠隔操作するCLIツール')
    subparsers = parser.add_subparsers(dest='command', help='利用可能なコマンド')

    # driveコマンドのパーサー
    drive_parser = subparsers.add_parser('drive', help='Roombaの速度と角速度を設定します')
    drive_parser.add_argument('speed', type=float, help='Roombaの速度 (cm/s)')
    drive_parser.add_argument('deg', type=float, help='Roombaの角速度 (deg/s)')

    # 引数をパース
    args = parser.parse_args()

    try:
        # Roombaに接続
        logger.info(f"ポート {ROOMBA_PORT} に接続しています...")
        robot = Create(ROOMBA_PORT)
        logger.info("接続に成功しました！")

        # コマンドに応じて処理を実行
        if args.command == 'drive':
            # driveコマンドのパラメータを取得
            speed = args.speed
            deg = args.deg

            # Roombaの速度と角速度を設定
            logger.info(f"速度を設定します (速度: {speed}cm/s, 角速度: {deg}deg/s)")
            robot.go(speed, deg)

        else:
            logger.error("無効なコマンドです。")

    except Exception as e:
        logger.error(f"エラーが発生しました: {e}")

    finally:
        # 接続をクローズ
        if 'robot' in locals():
            robot.close()
        logger.info("接続をクローズしました。")

if __name__ == "__main__":
    main()
