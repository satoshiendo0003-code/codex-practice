#!/bin/bash
# Dental Manual Generator - セットアップスクリプト

echo "🦷 Dental Manual Generator - セットアップ開始"
echo "================================================"
echo ""

# Python バージョン確認
echo "📍 Step 1/4: Python バージョン確認..."
python_version=$(python3 --version 2>&1)
if [ $? -eq 0 ]; then
    echo "✅ $python_version"
else
    echo "❌ Python 3がインストールされていません"
    echo "   https://www.python.org/downloads/ からインストールしてください"
    exit 1
fi
echo ""

# 依存関係インストール
echo "📍 Step 2/4: 依存関係をインストール中..."
if pip3 install -q -r requirements.txt; then
    echo "✅ 依存関係のインストール完了"
else
    echo "❌ インストールに失敗しました"
    exit 1
fi
echo ""

# ディレクトリ作成
echo "📍 Step 3/4: 必要なディレクトリを作成中..."
mkdir -p output/frames
mkdir -p uploads
mkdir -p downloads
mkdir -p state
echo "✅ ディレクトリ作成完了"
echo ""

# 環境設定ファイル確認
echo "📍 Step 4/4: 環境設定を確認中..."
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        echo "📝 .env.example を .env にコピーしました"
        cp .env.example .env
        echo "⚠️  .env ファイルを編集してAPIキーを設定してください"
    fi
else
    echo "✅ .env ファイルが存在します"
fi
echo ""

# セットアップ完了
echo "================================================"
echo "🎉 セットアップ完了！"
echo ""
echo "次のコマンドでアプリを起動できます:"
echo "  streamlit run app.py"
echo ""
echo "または:"
echo "  ./start_streamlit.sh"
echo ""
echo "📚 詳細なガイド:"
echo "  - クイックスタート: QUICKSTART.md"
echo "  - デプロイガイド: DEPLOYMENT_GUIDE.md"
echo "  - テストガイド: TEST_FEATURES.md"
echo ""
echo "本番環境: https://dental-manual-generator.streamlit.app/"
echo "================================================"
