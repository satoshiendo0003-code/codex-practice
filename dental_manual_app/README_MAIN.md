# 🦷 Dental Manual Generator

**動画から自動で歯科マニュアルを生成するAIアプリ**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://dental-manual-generator.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

---

## 🌟 主な機能

### ✨ NEW! スクリーンショット自動埋め込み
- 動画から重要なシーンを自動抽出
- AI が各手順に最適な画像を選択
- Word/PDF/PowerPoint に自動埋め込み

### 📹 動画ソース（3種類対応）
- ✅ **ファイルアップロード**: MP4/MOV/AVI（最大200MB）
- ✅ **YouTube**: URLから直接ダウンロード
- ✅ **Google Drive**: 10GB以上の大容量動画もOK

### 📄 出力形式（4種類）
- 📄 **Word** (.docx) - 編集・共有に便利
- 📕 **PDF** - 印刷・配布に最適
- 📊 **PowerPoint** (.pptx) - 研修・プレゼンに
- 🖼️ **画像カード** - SNS投稿用

### 🎨 カスタマイズ
- 対象読者設定（歯科助手、衛生士など）
- マニュアルモード（詳細/簡易）
- デザインテンプレート（Modern/Classic/Simple）

---

## 🚀 クイックスタート

### 方法1: 本番環境を使う（推奨・最速）

```
https://dental-manual-generator.streamlit.app/
```

1. 上記URLにアクセス
2. Google Gemini APIキーを入力（[取得方法](https://ai.google.dev/)）
3. 動画をアップロード
4. 分析開始 → マニュアル生成完了！

**所要時間**: 5分

---

### 方法2: ローカルで実行（開発者向け）

#### 自動セットアップ

```bash
git clone https://github.com/satoshiendo0003-code/codex-practice.git
cd codex-practice/dental_manual_app
./setup.sh
streamlit run app.py
```

#### 手動セットアップ

```bash
# 依存関係インストール
pip install -r requirements.txt

# アプリ起動
streamlit run app.py
```

ブラウザで http://localhost:8501 にアクセス

---

## 📚 ドキュメント

| ファイル | 内容 | 対象 |
|---------|------|------|
| [**QUICKSTART.md**](./QUICKSTART.md) | 5分で始めるガイド | 全員 |
| [**DEPLOYMENT_GUIDE.md**](./DEPLOYMENT_GUIDE.md) | Streamlit Cloudデプロイ手順 | 管理者 |
| [**TEST_FEATURES.md**](./TEST_FEATURES.md) | 機能テストチェックリスト | QA担当 |
| [**STATUS.md**](./STATUS.md) | プロジェクト現状まとめ | 開発者 |

---

## 🎥 使い方（簡易版）

### ステップ1: 動画準備
治療手順を撮影（3-10分推奨）

### ステップ2: アップロード
- ファイル直接 or
- YouTube URL or
- Google Drive URL

### ステップ3: AI分析
「分析開始」ボタン → 20-30秒待つ

### ステップ4: 確認・編集
自動生成された内容を確認・必要に応じて編集

### ステップ5: ダウンロード
好きな形式で生成してダウンロード

---

## 🖼️ スクリーンショット

### メイン画面
```
┌─────────────────────────────────────────┐
│ 🦷 Dental Manual Generator - 完全版    │
├─────────────────────────────────────────┤
│                                         │
│  📹 動画ソース・分析 | ✏️ 編集・出力   │
│                                         │
│  [動画アップロード]                     │
│  ○ ファイル  ○ YouTube  ○ Google Drive│
│                                         │
│  [🚀 分析開始]                          │
│                                         │
│  📸 抽出されたスクリーンショット        │
│  [画像1] [画像2] [画像3]                │
│                                         │
└─────────────────────────────────────────┘
```

### 編集画面
```
┌─────────────────────────────────────────┐
│ ステップ 1: 器具の準備                  │
│                                         │
│ [スクリーンショット画像]                │
│ ⏱️ タイムスタンプ: 0:45                │
│                                         │
│ 説明: スケーラーを手に取り...           │
│                                         │
│ 重要ポイント | ⚠️ 注意事項             │
│ • ポイント1  | • 注意1                  │
│ • ポイント2  | • 注意2                  │
└─────────────────────────────────────────┘
```

---

## 🛠️ 技術スタック

### フロントエンド
- **Streamlit** - WebUIフレームワーク

### AI・機械学習
- **Google Gemini 1.5 Flash** - 動画分析・マニュアル生成
- **OpenCV** - フレーム抽出

### ドキュメント生成
- **python-docx** - Word生成
- **ReportLab** - PDF生成
- **python-pptx** - PowerPoint生成
- **Pillow** - 画像処理・カード生成

### その他
- **yt-dlp** - YouTube動画ダウンロード
- **gdown** - Google Drive連携

---

## 📊 パフォーマンス

### 処理時間（5分動画の場合）

| 処理 | 時間 |
|------|------|
| フレーム抽出 | 5秒 |
| AI分析 | 20秒 |
| Word生成 | 2秒 |
| PDF生成 | 3秒 |
| PowerPoint生成 | 2秒 |
| **合計** | **32秒** |

### 対応動画サイズ

| ソース | 上限 |
|--------|------|
| ファイルアップロード | 200MB |
| YouTube | 動画による |
| Google Drive | **無制限** |

---

## 🎯 活用シーン

### 🏥 院内研修
手順動画 → PowerPoint生成 → スタッフ研修

### 📖 患者説明
治療動画 → PDF生成 → 待合室配置

### 📱 SNSマーケティング
簡単な治療 → 画像カード生成 → Instagram投稿

### 👨‍🏫 新人教育
ベテランの技 → Word生成 → 新人マニュアル

---

## 🔧 カスタマイズ

### フレーム抽出数を変更
`services/gemini_analyzer.py`
```python
frame_data = self.extract_frames(video_path, num_frames=12)  # 8→12に変更
```

### デフォルトテンプレート変更
`app.py`
```python
template_choice = st.selectbox(
    "テンプレート",
    ["modern", "classic", "simple"],
    index=0,  # 0=modern, 1=classic, 2=simple
)
```

### 出力ディレクトリ変更
`.env`ファイルを作成:
```env
OUTPUT_DIR=custom_output
FRAMES_DIR=custom_output/frames
```

---

## 🐛 トラブルシューティング

### よくある問題と解決策

**Q: ImportError: cv2**
```bash
pip install opencv-python-headless
```

**Q: APIキーエラー**
- モデル名が `models/gemini-1.5-flash` であることを確認
- APIキーが有効か確認: https://ai.google.dev/

**Q: Google Drive ダウンロード失敗**
- 共有設定を「リンクを知っている全員」に変更

**Q: Streamlit Cloud でエラー**
- `packages.txt` に `libgl1-mesa-glx` と `libglib2.0-0` が含まれているか確認
- Reboot app を実行

詳細: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md#トラブルシューティング)

---

## 📈 ロードマップ

### ✅ 完了
- [x] 基本的な動画分析・マニュアル生成
- [x] Word/PDF/PowerPoint/画像カード対応
- [x] YouTube/Google Drive対応
- [x] スクリーンショット自動埋め込み
- [x] Streamlit Cloud デプロイ

### 🚧 進行中
- [ ] `google.genai` パッケージへの移行（deprecation対応）

### 📝 今後の予定
- [ ] フレーム抽出数のUI設定
- [ ] 画像サイズ・配置カスタマイズ
- [ ] 複数動画の一括処理
- [ ] マニュアルテンプレート保存・再利用
- [ ] フレーム手動選択オプション

---

## 🤝 コントリビューション

バグ報告・機能リクエスト歓迎！

1. Issue を作成
2. Fork してブランチ作成
3. 変更をコミット
4. Pull Request を作成

---

## 📄 ライセンス

このプロジェクトは個人利用・商用利用ともに自由に使用できます。

---

## 📞 サポート

### ドキュメント
- 📘 [クイックスタート](./QUICKSTART.md)
- 🚀 [デプロイガイド](./DEPLOYMENT_GUIDE.md)
- 🧪 [テストガイド](./TEST_FEATURES.md)
- 📊 [ステータス](./STATUS.md)

### 連絡先
- **Email**: satoshiendo0003@gmail.com
- **本番環境**: https://dental-manual-generator.streamlit.app/
- **GitHub**: https://github.com/satoshiendo0003-code/codex-practice

---

## 🌟 謝辞

- **Google Gemini AI**: 動画分析エンジン
- **Streamlit**: UIフレームワーク
- **OpenCV**: 画像処理ライブラリ

---

<div align="center">

**Made with ❤️ for dental professionals**

[本番環境で試す](https://dental-manual-generator.streamlit.app/) | [ドキュメント](./QUICKSTART.md) | [サポート](mailto:satoshiendo0003@gmail.com)

</div>
