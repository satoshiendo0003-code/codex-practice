# Dental Manual App - フル機能版

動画から歯科マニュアルを自動生成するStreamlitアプリケーション（Google Gemini AI搭載）

## 🎯 主要機能

### ✅ 実装済み機能

1. **動画アップロード**
   - ローカルファイル（MP4, MOV, AVI）のアップロード対応
   - YouTube URL入力（開発中）

2. **AI動画分析**
   - Google Gemini 1.5 Proによる動画分析
   - 動画からフレームを自動抽出
   - 手順、重要ポイント、注意事項を自動生成

3. **マニュアル編集**
   - タイトル・概要の編集
   - ステップごとの詳細編集
   - 重要ポイント・注意事項の追加・削除

4. **多様な出力形式**
   - ✅ Wordドキュメント（.docx）
   - ✅ PDFドキュメント（.pdf）
   - 🚧 PowerPoint（開発予定）
   - 🚧 画像カード（開発予定）

5. **状態管理**
   - セッション状態の自動保存
   - ページリロード時の復元
   - ディスクへの永続化

## 📁 ファイル構成

```
dental_manual_app/
├── app.py                           # メインアプリケーション（フル機能版）
├── preview.html                     # HTMLプレビュー版
├── requirements.txt                 # Python依存パッケージ
├── start_streamlit.sh              # 起動スクリプト
├── README_FULL.md                   # このファイル
├── state/
│   ├── __init__.py
│   └── session_state.py            # セッション状態管理
├── services/
│   ├── __init__.py
│   ├── gemini_analyzer.py          # Gemini API連携
│   └── document_generator.py       # Word/PDF生成
├── ui/
│   ├── __init__.py
│   ├── tab_video_source.py
│   └── tab_editor.py
├── uploads/                         # アップロードファイル保存先
├── output/                          # 生成ファイル出力先
└── state/                           # 状態ファイル保存先
```

## 🚀 セットアップ手順

### 1. 依存パッケージのインストール

```bash
cd dental_manual_app
pip install -r requirements.txt
```

### 2. Google Gemini APIキーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. 「Get API Key」をクリック
3. APIキーをコピー

### 3. アプリケーションの起動

```bash
streamlit run app.py
```

または

```bash
./start_streamlit.sh
```

## 📖 使い方

### ステップ1: APIキーの設定

1. アプリを起動
2. 左サイドバーの「🔑 Google Gemini API」セクションにAPIキーを入力
3. ✅マークが表示されればOK

### ステップ2: 動画をアップロード

1. 「📹 動画ソース・分析」タブを選択
2. 「ファイルアップロード」を選択
3. 動画ファイル（.mp4, .mov, .avi）をアップロード

### ステップ3: 動画を分析

1. 「🚀 分析開始」ボタンをクリック
2. AIが動画を分析します（数分かかる場合があります）
3. 分析完了後、結果プレビューが表示されます

### ステップ4: マニュアルを編集

1. 「✏️ 編集・出力」タブに移動
2. タイトル、概要、手順を自由に編集
3. 重要ポイントや注意事項を追加

### ステップ5: ドキュメントを生成

1. 「📄 Word生成」または「📕 PDF生成」をクリック
2. 生成完了後、ダウンロードボタンが表示されます
3. クリックしてダウンロード

## 🔧 技術スタック

- **フロントエンド**: Streamlit 1.28+
- **AI分析**: Google Gemini 1.5 Pro API
- **動画処理**: OpenCV
- **ドキュメント生成**:
  - Word: python-docx
  - PDF: ReportLab
- **状態管理**: Streamlit Session State + JSON

## 🐛 トラブルシューティング

### APIキーエラー

```
❌ 分析エラー: API key not valid
```

**解決方法**:
- APIキーが正しいか確認
- [Google AI Studio](https://makersuite.google.com/app/apikey)で新しいキーを発行

### 動画アップロードエラー

```
❌ 動画ファイルを読み込めませんでした
```

**解決方法**:
- サポート形式（.mp4, .mov, .avi）を確認
- ファイルサイズが大きすぎないか確認（推奨: 100MB以下）
- 動画が破損していないか確認

### Word/PDF生成エラー

```
❌ 生成エラー: ...
```

**解決方法**:
- `output/`ディレクトリの書き込み権限を確認
- 依存パッケージを再インストール: `pip install -r requirements.txt --upgrade`

## 📝 出力ボタンのリセット問題（修正済み）

### 問題
- Word/PDFボタンを押すとページがリセットされる
- 編集内容が失われる

### 修正内容
1. **コールバック関数の使用** (`app.py:304-346`)
   - `on_click`パラメータでコールバック関数を指定
   - ページ再実行前にセッション状態を保存

2. **セッション状態への確実な保存**
   - `st.session_state`に生成フラグと結果を保存
   - ディスクにも自動保存

3. **ダウンロードボタンの永続表示**
   - 生成フラグがある限りダウンロードボタンを表示
   - ページリロード後も利用可能

## 🎨 カスタマイズ

### AIモデルの変更

`app.py`の57行目を編集：

```python
selected_model = st.selectbox(
    "AIモデル",
    ["gemini-1.5-pro", "gemini-1.5-flash"],  # flashを追加
    index=0
)
```

### 抽出フレーム数の変更

`services/gemini_analyzer.py`の49行目を編集：

```python
frame_paths = self.extract_frames(video_path, num_frames=10)  # デフォルト: 8
```

### 出力ディレクトリの変更

`services/document_generator.py`の18行目を編集：

```python
def __init__(self, output_dir: str = "my_output"):
```

## 🔒 セキュリティ

- APIキーはセッション状態にのみ保存（ディスクには保存されません）
- アップロードファイルは`uploads/`に一時保存
- 生成ファイルは`output/`に保存

## 📄 ライセンス

MIT License

## 🙏 謝辞

- Google Gemini AI
- Streamlit
- python-docx
- ReportLab

---

Made with ❤️ for dental professionals
