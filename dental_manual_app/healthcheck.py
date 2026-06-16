#!/usr/bin/env python3
"""
Dental Manual App - ヘルスチェックスクリプト
全機能が正常に動作するか確認します
"""

import sys
import importlib
import os
from pathlib import Path

def print_header(text):
    """ヘッダーを表示"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_python_version():
    """Pythonバージョン確認"""
    version = sys.version_info
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ⚠️  Python 3.8以上を推奨")
        return False
    return True

def check_dependencies():
    """依存関係の確認"""
    required_packages = [
        'streamlit',
        'google.generativeai',
        'docx',
        'pptx',
        'reportlab',
        'PIL',
        'cv2',
        'yt_dlp',
        'gdown',
    ]

    results = {}
    for package in required_packages:
        try:
            if package == 'docx':
                importlib.import_module('docx')
            elif package == 'pptx':
                importlib.import_module('pptx')
            elif package == 'PIL':
                importlib.import_module('PIL')
            elif package == 'cv2':
                importlib.import_module('cv2')
            else:
                importlib.import_module(package)
            results[package] = True
            print(f"  ✓ {package:<25} インストール済み")
        except ImportError:
            results[package] = False
            print(f"  ✗ {package:<25} 未インストール")

    return all(results.values())

def check_services():
    """サービスモジュールの確認"""
    services = [
        'services.gemini_analyzer',
        'services.document_generator',
        'services.document_generator_extended',
        'services.youtube_downloader',
        'services.gdrive_downloader',
    ]

    results = {}
    for service in services:
        try:
            mod = importlib.import_module(service)
            results[service] = True
            module_name = service.split('.')[-1]
            print(f"  ✓ {module_name:<30} OK")
        except Exception as e:
            results[service] = False
            module_name = service.split('.')[-1]
            print(f"  ✗ {module_name:<30} エラー: {e}")

    return all(results.values())

def check_methods():
    """主要メソッドの存在確認"""
    print("\n  GeminiAnalyzer:")
    try:
        from services.gemini_analyzer import GeminiAnalyzer

        methods = ['extract_frames', 'analyze_video', '_attach_frames_to_steps']
        for method in methods:
            if hasattr(GeminiAnalyzer, method):
                print(f"    ✓ {method}")
            else:
                print(f"    ✗ {method} が見つかりません")
                return False
    except Exception as e:
        print(f"    ✗ GeminiAnalyzerのインポート失敗: {e}")
        return False

    print("\n  DocumentGenerator:")
    try:
        from services.document_generator import DocumentGenerator

        methods = ['generate_word', 'generate_pdf']
        for method in methods:
            if hasattr(DocumentGenerator, method):
                print(f"    ✓ {method}")
            else:
                print(f"    ✗ {method} が見つかりません")
                return False
    except Exception as e:
        print(f"    ✗ DocumentGeneratorのインポート失敗: {e}")
        return False

    print("\n  ExtendedDocumentGenerator:")
    try:
        from services.document_generator_extended import ExtendedDocumentGenerator

        methods = ['generate_powerpoint', 'generate_image_cards']
        for method in methods:
            if hasattr(ExtendedDocumentGenerator, method):
                print(f"    ✓ {method}")
            else:
                print(f"    ✗ {method} が見つかりません")
                return False
    except Exception as e:
        print(f"    ✗ ExtendedDocumentGeneratorのインポート失敗: {e}")
        return False

    return True

def check_files():
    """必要なファイルの確認"""
    required_files = [
        'app.py',
        'requirements.txt',
        'packages.txt',
        'QUICKSTART.md',
        'DEPLOYMENT_GUIDE.md',
        'TEST_FEATURES.md',
        'STATUS.md',
        'README_MAIN.md',
        'setup.sh',
        '.env.example',
    ]

    results = {}
    for file in required_files:
        exists = Path(file).exists()
        results[file] = exists
        status = "✓" if exists else "✗"
        print(f"  {status} {file}")

    return all(results.values())

def check_directories():
    """必要なディレクトリの確認（存在しなければ作成）"""
    required_dirs = [
        'services',
        'state',
        'ui',
        'output',
        'output/frames',
        'uploads',
        'downloads',
    ]

    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"  ✓ {dir_path}/")
        else:
            print(f"  → {dir_path}/ を作成中...")
            path.mkdir(parents=True, exist_ok=True)
            print(f"  ✓ {dir_path}/ 作成完了")

    return True

def main():
    """メイン処理"""
    print_header("🦷 Dental Manual App - ヘルスチェック")

    all_passed = True

    # Pythonバージョン
    print("📍 Pythonバージョン:")
    if not check_python_version():
        all_passed = False

    # 依存関係
    print_header("📦 依存関係")
    if not check_dependencies():
        all_passed = False
        print("\n  💡 修正方法: pip install -r requirements.txt")

    # サービスモジュール
    print_header("🔧 サービスモジュール")
    if not check_services():
        all_passed = False

    # メソッド確認
    print_header("⚙️  主要メソッド")
    if not check_methods():
        all_passed = False

    # ファイル確認
    print_header("📄 必須ファイル")
    if not check_files():
        all_passed = False

    # ディレクトリ確認
    print_header("📁 ディレクトリ構造")
    if not check_directories():
        all_passed = False

    # 結果表示
    print_header("結果")
    if all_passed:
        print("✅ すべてのチェックに合格しました！\n")
        print("次のコマンドでアプリを起動できます:")
        print("  streamlit run app.py\n")
        print("または:")
        print("  ./start_streamlit.sh\n")
        return 0
    else:
        print("❌ 一部のチェックに失敗しました\n")
        print("上記のエラーを修正してから再実行してください\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
