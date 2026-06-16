#!/usr/bin/env python3
"""
Dental Manual Generator - CLI版
コマンドラインから直接マニュアルを生成
"""

import argparse
import os
import sys
from pathlib import Path

from services.gemini_analyzer import GeminiAnalyzer
from services.document_generator import DocumentGenerator
from services.document_generator_extended import ExtendedDocumentGenerator


def print_banner():
    """バナー表示"""
    print("""
╔════════════════════════════════════════════════════════════╗
║  🦷 Dental Manual Generator - CLI                         ║
║  動画から自動でマニュアルを生成                            ║
╚════════════════════════════════════════════════════════════╝
""")


def analyze_video(api_key, video_path, target_audience="歯科助手", manual_mode="詳細"):
    """動画を分析"""
    print(f"📹 動画を分析中: {video_path}")
    print(f"   対象: {target_audience}")
    print(f"   モード: {manual_mode}")
    print()

    analyzer = GeminiAnalyzer(api_key=api_key)

    print("⏳ フレーム抽出中...")
    result = analyzer.analyze_video(
        video_path=video_path,
        target_audience=target_audience,
        manual_mode=manual_mode
    )

    print("✅ 分析完了！")
    print(f"   タイトル: {result.get('title', 'N/A')}")
    print(f"   ステップ数: {len(result.get('steps', []))}")
    print(f"   推定時間: {result.get('estimated_time', 'N/A')}")
    print()

    return result


def generate_documents(result, output_dir="output", formats=None, template="modern"):
    """ドキュメント生成"""
    if formats is None:
        formats = ["word", "pdf"]

    os.makedirs(output_dir, exist_ok=True)

    title = result.get('title', '新規マニュアル')
    summary = result.get('summary', '')

    generated_files = []

    if "word" in formats:
        print("📄 Word生成中...")
        generator = DocumentGenerator(output_dir=output_dir)
        word_path = generator.generate_word(result, title, summary)
        generated_files.append(word_path)
        print(f"   ✅ {word_path}")

    if "pdf" in formats:
        print("📕 PDF生成中...")
        generator = DocumentGenerator(output_dir=output_dir)
        pdf_path = generator.generate_pdf(result, title, summary)
        generated_files.append(pdf_path)
        print(f"   ✅ {pdf_path}")

    if "pptx" in formats or "powerpoint" in formats:
        print("📊 PowerPoint生成中...")
        generator = ExtendedDocumentGenerator(output_dir=output_dir)
        pptx_path = generator.generate_powerpoint(result, title, summary, template=template)
        generated_files.append(pptx_path)
        print(f"   ✅ {pptx_path}")

    if "images" in formats or "cards" in formats:
        print("🖼️  画像カード生成中...")
        generator = ExtendedDocumentGenerator(output_dir=output_dir)
        image_paths = generator.generate_image_cards(result, title, template=template)
        generated_files.extend(image_paths)
        print(f"   ✅ {len(image_paths)}枚生成")

    print()
    return generated_files


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='動画から歯科マニュアルを自動生成',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # Word + PDF生成
  %(prog)s video.mp4 --api-key YOUR_KEY

  # PowerPointも生成
  %(prog)s video.mp4 --api-key YOUR_KEY --formats word pdf pptx

  # 全形式生成
  %(prog)s video.mp4 --api-key YOUR_KEY --formats all

  # 対象読者を指定
  %(prog)s video.mp4 --api-key YOUR_KEY --audience "新人歯科衛生士"

  # テンプレート変更
  %(prog)s video.mp4 --api-key YOUR_KEY --template classic

環境変数でAPIキーを設定:
  export GEMINI_API_KEY=your_api_key_here
  %(prog)s video.mp4
        """
    )

    parser.add_argument(
        'video',
        help='動画ファイルのパス（MP4/MOV/AVI）'
    )

    parser.add_argument(
        '--api-key',
        help='Google Gemini APIキー（環境変数 GEMINI_API_KEY でも可）'
    )

    parser.add_argument(
        '--formats', '-f',
        nargs='+',
        choices=['word', 'pdf', 'pptx', 'powerpoint', 'images', 'cards', 'all'],
        default=['word', 'pdf'],
        help='生成形式（デフォルト: word pdf）'
    )

    parser.add_argument(
        '--output', '-o',
        default='output',
        help='出力ディレクトリ（デフォルト: output）'
    )

    parser.add_argument(
        '--audience', '-a',
        default='歯科助手',
        help='対象読者（デフォルト: 歯科助手）'
    )

    parser.add_argument(
        '--mode', '-m',
        choices=['詳細', '簡易'],
        default='詳細',
        help='マニュアルモード（デフォルト: 詳細）'
    )

    parser.add_argument(
        '--template', '-t',
        choices=['modern', 'classic', 'simple'],
        default='modern',
        help='デザインテンプレート（デフォルト: modern）'
    )

    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='詳細メッセージを抑制'
    )

    args = parser.parse_args()

    # バナー表示
    if not args.quiet:
        print_banner()

    # APIキー取得
    api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("❌ エラー: APIキーが指定されていません")
        print()
        print("方法1: コマンドライン引数")
        print("  --api-key YOUR_KEY")
        print()
        print("方法2: 環境変数")
        print("  export GEMINI_API_KEY=your_key")
        print("  または .env ファイルに記載")
        print()
        return 1

    # 動画ファイル確認
    if not os.path.exists(args.video):
        print(f"❌ エラー: 動画ファイルが見つかりません: {args.video}")
        return 1

    # 形式処理
    formats = args.formats
    if 'all' in formats:
        formats = ['word', 'pdf', 'pptx', 'images']

    try:
        # 動画分析
        result = analyze_video(
            api_key=api_key,
            video_path=args.video,
            target_audience=args.audience,
            manual_mode=args.mode
        )

        # ドキュメント生成
        files = generate_documents(
            result=result,
            output_dir=args.output,
            formats=formats,
            template=args.template
        )

        # 完了メッセージ
        print("="*60)
        print("✅ 完了！")
        print(f"   生成ファイル数: {len(files)}")
        print(f"   出力先: {args.output}/")
        print("="*60)
        print()

        return 0

    except Exception as e:
        print(f"❌ エラー: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
