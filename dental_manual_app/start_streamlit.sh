#!/bin/bash
# Streamlit版を起動するスクリプト

echo "🦷 Dental Manual App - Streamlit版を起動します..."
echo ""

# 仮想環境が存在するかチェック
if [ ! -d "venv" ]; then
    echo "📦 仮想環境を作成します..."
    python3 -m venv venv
fi

# 仮想環境をアクティベート
echo "🔧 仮想環境をアクティベートします..."
source venv/bin/activate

# 依存関係をインストール
echo "📥 依存関係をインストールします..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Streamlitアプリを起動
echo ""
echo "🚀 Streamlitアプリを起動します..."
echo "🌐 ブラウザが自動的に開きます"
echo ""
echo "停止するには Ctrl+C を押してください"
echo ""

streamlit run app.py
