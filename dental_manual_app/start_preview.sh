#!/bin/bash
# HTMLプレビュー版を起動するスクリプト

echo "🦷 Dental Manual App - プレビュー版を起動します..."
echo ""
echo "ブラウザで以下のURLを開いてください:"
echo "file://$(pwd)/preview.html"
echo ""
echo "または、Pythonでローカルサーバーを起動します..."
echo ""

# PythonでシンプルなHTTPサーバーを起動
if command -v python3 &> /dev/null; then
    echo "✅ Python3が見つかりました。サーバーを起動します..."
    echo "🌐 http://localhost:8000/preview.html でアクセスできます"
    echo ""
    echo "停止するには Ctrl+C を押してください"
    python3 -m http.server 8000
else
    echo "⚠️ Python3が見つかりません。"
    echo "preview.htmlファイルを直接ブラウザで開いてください。"
fi
