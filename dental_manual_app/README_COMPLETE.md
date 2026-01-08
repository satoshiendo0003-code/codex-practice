# Dental Manual App - 完全版 v2.0

動画から歯科マニュアルを自動生成（全機能搭載）

## 🎉 新機能

###  ✅ 追加実装した機能

#### 1. **PowerPoint生成** 📊
- python-pptxで完全なプレゼンテーションを生成
- スライドごとにステップを表示
- 重要ポイントと注意事項を視覚的に配置
- 3つのテンプレートから選択可能

#### 2. **画像カード生成** 🖼️
- SNS投稿用の画像カードを自動生成
- Instagram正方形サイズ（1080x1080px）
- タイトルカード + 各ステップカード
- テンプレートでデザイン変更可能

#### 3. **YouTube動画対応** 🎬
- yt-dlpで YouTube動画を直接ダウンロード
- 動画情報のプレビュー表示
- ダウンロード進捗の表示
- ダウンロード後すぐに分析可能

#### 4. **テンプレート機能** 🎨
- **Modern**: モダンなグラデーション（紫）
- **Classic**: 伝統的なデザイン（青・金）
- **Simple**: シンプルなデザイン（グレー）
- PowerPointと画像カードの両方に適用

## 📁 完全版ファイル構成

```
dental_manual_app/
├── app.py                               # メインアプリ（完全版）
├── app_old.py                           # 旧バージョン（バックアップ）
├── requirements.txt                     # 全依存パッケージ
├── README_COMPLETE.md                   # このファイル
├── services/
│   ├── gemini_analyzer.py              # Gemini API連携
│   ├── document_generator.py           # Word/PDF生成
│   ├── document_generator_extended.py  # PowerPoint/画像カード生成
│   └── youtube_downloader.py           # YouTube動画ダウンロード
├── state/
│   └── session_state.py                # セッション状態管理
├── ui/
│   ├── tab_video_source.py
│   └── tab_editor.py
└── output/                              # 生成ファイル出力先
```

## 🚀 セットアップ

### 1. 依存パッケージのインストール

```bash
cd dental_manual_app
pip install -r requirements.txt
```

**必須パッケージ:**
- `streamlit` - Webアプリフレームワーク
- `google-generativeai` - Gemini API
- `python-docx` - Word生成
- `python-pptx` - PowerPoint生成 🆕
- `reportlab` - PDF生成
- `Pillow` - 画像処理・カード生成 🆕
- `opencv-python` - 動画処理
- `yt-dlp` - YouTube動画ダウンロード 🆕

### 2. APIキー取得

[Google AI Studio](https://makersuite.google.com/app/apikey)でGemini APIキーを取得

### 3. アプリ起動

```bash
streamlit run app.py
```

## 📖 使い方ガイド

### 基本フロー

1. **APIキー設定** → サイドバーで入力
2. **テンプレート選択** → Modern/Classic/Simpleから選択
3. **動画アップロード** → ファイルまたはYouTube URL
4. **AI分析** → ボタンクリックで自動分析
5. **編集** → 必要に応じて内容を修正
6. **出力** → Word/PDF/PowerPoint/画像カードを生成

### YouTube動画の使い方

1. 「YouTubeリンク」を選択
2. YouTube URLを入力（例: `https://www.youtube.com/watch?v=xxxxx`）
3. 動画情報が表示される
4. 「YouTube動画をダウンロード」ボタンをクリック
5. ダウンロード完了後、「分析開始」ボタンで分析

### テンプレートの選択

**サイドバー**の「デザインテンプレート」で選択:

- **Modern** 🌈
  - 紫のグラデーション
  - モダンで洗練された印象
  - 推奨: 一般的な用途

- **Classic** 📘
  - 青と金の配色
  - 伝統的で信頼感のあるデザイン
  - 推奨: 公式文書

- **Simple** ⚪
  - グレー基調
  - シンプルで読みやすい
  - 推奨: 内部資料

### 出力形式の違い

| 形式 | 用途 | 特徴 |
|------|------|------|
| **Word** | 編集可能な文書 | テキスト編集・印刷に最適 |
| **PDF** | 配布用文書 | レイアウト固定・印刷品質 |
| **PowerPoint** | プレゼンテーション | スライドショー・研修用 |
| **画像カード** | SNS投稿 | Instagram/Facebook投稿用 |

## 🎯 各機能の詳細

### PowerPoint生成機能

**特徴:**
- タイトルスライド
- 概要スライド
- 必要な器具スライド
- 各ステップごとのスライド
- 重要ポイント・注意事項を視覚的に配置

**使い方:**
1. マニュアルを編集
2. 「📊 PowerPoint」ボタンをクリック
3. ダウンロードセクションから取得

**カスタマイズ:**
```python
# services/document_generator_extended.py の色設定を変更
templates = {
    "modern": {
        "primary": PptxRGBColor(102, 126, 234),  # お好みの色に変更
        ...
    }
}
```

### 画像カード生成機能

**特徴:**
- Instagram正方形（1080x1080px）
- タイトルカード + ステップカード（最大5枚）
- SNS投稿に最適なデザイン

**生成されるカード:**
1. `{タイトル}_card_title.png` - タイトルカード
2. `{タイトル}_card_step1.png` - ステップ1
3. `{タイトル}_card_step2.png` - ステップ2
4. ... (最大5ステップ)

**使い方:**
1. 「🖼️ 画像カード」ボタンをクリック
2. ダウンロードセクションに複数の画像が表示される
3. 個別にダウンロード

### YouTube動画ダウンロード機能

**対応URL形式:**
- `https://www.youtube.com/watch?v=xxxxx`
- `https://youtu.be/xxxxx`
- `https://m.youtube.com/watch?v=xxxxx`

**機能:**
- 動画情報の取得（タイトル、投稿者、長さ、再生回数）
- 進捗表示付きダウンロード
- MP4形式で保存

**注意事項:**
- 著作権のある動画のダウンロードには注意
- 長時間動画はダウンロードに時間がかかる場合があります
- インターネット接続が必要

## 🔧 トラブルシューティング

### PowerPoint生成エラー

```
❌ 生成エラー: ...
```

**解決方法:**
```bash
pip install --upgrade python-pptx
```

### 画像カード生成でフォントエラー

```
OSError: cannot open resource
```

**解決方法:**
- システムにフォントがインストールされているか確認
- コード内のフォントパスを変更:

```python
# services/document_generator_extended.py:220
title_font = ImageFont.truetype("/path/to/your/font.ttf", 80)
```

### YouTube動画ダウンロードエラー

```
❌ ダウンロードエラー: ...
```

**解決方法:**
```bash
# yt-dlpを最新版に更新
pip install --upgrade yt-dlp

# または
python -m pip install --force-reinstall yt-dlp
```

### 動画が長すぎてエラー

**解決方法:**
- 10分以下の動画を推奨
- フレーム数を減らす: `services/gemini_analyzer.py:49`

```python
frame_paths = self.extract_frames(video_path, num_frames=5)  # 8→5に変更
```

## 🎨 カスタマイズガイド

### 出力ディレクトリの変更

```python
# app.py の各ジェネレーター初期化部分
generator = ExtendedDocumentGenerator(output_dir="my_custom_output")
```

### カードサイズの変更

```python
# services/document_generator_extended.py:215
card_size = (1080, 1920)  # Instagram縦長サイズ
```

### テンプレートの追加

```python
# services/document_generator_extended.py:58
templates = {
    "modern": {...},
    "classic": {...},
    "simple": {...},
    "custom": {  # 新しいテンプレート
        "primary": PptxRGBColor(255, 100, 100),
        "secondary": PptxRGBColor(100, 100, 255),
        ...
    }
}
```

そしてapp.pyで:

```python
template_choice = st.selectbox(
    "テンプレート",
    ["modern", "classic", "simple", "custom"],  # customを追加
    ...
)
```

## 📊 パフォーマンス

| 処理 | 所要時間（目安） |
|------|-----------------|
| 動画アップロード（100MB） | 5-10秒 |
| YouTube動画ダウンロード（5分） | 30-60秒 |
| AI分析 | 1-3分 |
| Word生成 | 1-2秒 |
| PDF生成 | 2-3秒 |
| PowerPoint生成 | 2-4秒 |
| 画像カード生成（5枚） | 3-5秒 |

## 🔒 セキュリティ

- APIキーはセッション状態のみに保存
- ディスクには保存されません
- アップロードファイルは`uploads/`に保存
- 定期的なクリーンアップを推奨

## 📝 今後の拡張案

- [ ] SNS自動投稿機能
- [ ] 音声認識による文字起こし
- [ ] 多言語対応
- [ ] クラウドストレージ連携
- [ ] チーム共有機能

## 🙏 謝辞

- Google Gemini AI
- Streamlit
- python-docx
- python-pptx
- ReportLab
- Pillow
- yt-dlp

---

**完全版 v2.0** | Made with ❤️ for dental professionals
