<p align="center">
<img src="https://huggingface.co/datasets/MakiAi/IconAssets/resolve/main/SPARK.jpg" width="100%">
<br>
<h1 align="center">S.P.A.R.K</h1>
<h2 align="center">
  ～ Smart Programmable Agent for Roomba with Knowledge ～
<br>
  <img alt="PyPI - Version" src="https://img.shields.io/pypi/v/spark-roomba">
<img alt="PyPI - Format" src="https://img.shields.io/pypi/format/spark-roomba">
<img alt="PyPI - Implementation" src="https://img.shields.io/pypi/implementation/spark-roomba">
<img alt="PyPI - Status" src="https://img.shields.io/pypi/status/spark-roomba">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dd/spark-roomba">
<img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/spark-roomba">
<a href="https://github.com/Sunwood-ai-labs/SPARK" title="Go to GitHub repo"><img src="https://img.shields.io/static/v1?label=SPARK&message=Sunwood-ai-labs&color=blue&logo=github"></a>
<img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/Sunwood-ai-labs/SPARK">
<a href="https://github.com/Sunwood-ai-labs/SPARK"><img alt="forks - Sunwood-ai-labs" src="https://img.shields.io/github/forks/SPARK/Sunwood-ai-labs?style=social"></a>
<a href="https://github.com/Sunwood-ai-labs/SPARK"><img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/Sunwood-ai-labs/SPARK"></a>
<a href="https://github.com/Sunwood-ai-labs/SPARK"><img alt="GitHub Top Language" src="https://img.shields.io/github/languages/top/Sunwood-ai-labs/SPARK"></a>
<img alt="GitHub Release" src="https://img.shields.io/github/v/release/Sunwood-ai-labs/SPARK?color=red">
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/Sunwood-ai-labs/SPARK?sort=semver&color=orange">
<img alt="GitHub Actions Workflow Status" src="https://img.shields.io/github/actions/workflow/status/Sunwood-ai-labs/SPARK/publish-to-pypi.yml">
<br>
<p align="center">
  <a href="https://hamaruki.com/"><b>[🌐 Website]</b></a> •
  <a href="https://github.com/Sunwood-ai-labs"><b>[🐱 GitHub]</b></a>
  <a href="https://x.com/hAru_mAki_ch"><b>[🐦 Twitter]</b></a> •
  <a href="https://hamaruki.com/"><b>[🍀 Official Blog]</b></a>
</p>

</h2>

</p>

>[!IMPORTANT]
>このリポジトリのリリースノートやREADME、コミットメッセージの9割近くは[claude.ai](https://claude.ai/)や[ChatGPT4](https://chatgpt.com/)を活用した[AIRA](https://github.com/Sunwood-ai-labs/AIRA), [SourceSage](https://github.com/Sunwood-ai-labs/SourceSage), [Gaiah](https://github.com/Sunwood-ai-labs/Gaiah), [HarmonAI_II](https://github.com/Sunwood-ai-labs/HarmonAI_II)で生成しています。

## プロジェクト概要

SPARK (Smart Programmable Agent for Roomba with Knowledge) は、Roombaロボット掃除機を制御するためのPythonベースのCLIツールです。このプロジェクトは、Roombaの遠隔操作や自動化を可能にし、より柔軟な清掃プロセスの実現を目指しています。

## 機能

- Roombaの速度と角速度の制御
- コマンドラインインターフェース（CLI）を通じた操作
- ロギング機能によるデバッグと操作履歴の記録

## インストール

SPARKは、Poetry を使用して依存関係を管理しています。以下の手順でインストールできます：

```bash
pip install spark-roomba
```

## 使用方法

SPARKは、コマンドラインから以下のように使用できます：

```bash
spark-roomba drive <speed> <deg>
```

- `<speed>`: Roombaの速度（cm/s）
- `<deg>`: Roombaの角速度（deg/s）

例：
```bash
spark-roomba drive 20 45
```

この例では、Roombaを20 cm/sの速度で前進させ、同時に45 deg/sの角速度で回転させます。

## 開発環境のセットアップ

1. リポジトリをクローンします：
   ```
   git clone https://github.com/Sunwood-ai-labs/SPARK.git
   cd SPARK
   ```

2. Poetry をインストールします（まだの場合）：
   ```
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. プロジェクトの依存関係をインストールします：
   ```
   poetry install
   ```

4. 開発用の仮想環境を有効化します：
   ```
   poetry shell
   ```

## Docker を使用した開発

プロジェクトには Docker と docker-compose の設定が含まれています。以下のコマンドで開発環境を起動できます：

```bash
docker-compose up -d
```

これにより、Pythonと必要な依存関係がインストールされたコンテナが起動します。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。

## 貢献

プロジェクトへの貢献を歓迎します。バグ報告、機能リクエスト、プルリクエストなど、あらゆる形での貢献をお待ちしています。

## リンク

- [GitHub リポジトリ](https://github.com/Sunwood-ai-labs/SPARK)
- [PyPI パッケージ](https://pypi.org/project/spark-roomba/)
- [バグトラッカー](https://github.com/Sunwood-ai-labs/SPARK/issues)
