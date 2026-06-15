# Dental Manual Generator - デプロイ & テストガイド

## 📋 現在の状態（2026-06-15）

### ✅ 実装完了
- **スクリーンショット埋め込み機能**: 動画から自動抽出したフレームをマニュアルに埋め込み
- **Google Drive対応**: 10GB以上の大容量動画もダウンロード可能
- **マルチフォーマット出力**: Word/PDF/PowerPoint/画像カード
- **YouTube対応**: YouTube URLから直接動画をダウンロード

### 🚀 最新コミット
```
e0901ad - Add screenshot embedding feature to dental manual generator
ブランチ: claude/fix-antigravity-startup-AWziT
プッシュ済み: ✅
```

## 🌐 Streamlit Cloud デプロイ手順

### 方法1: 自動デプロイ（推奨）
Streamlit Cloudは通常2-5分以内にGitHubの変更を自動検知してデプロイします。

1. https://dental-manual-generator.streamlit.app/ にアクセス
2. 画面が自動的に更新されるのを待つ
3. 右下に「App is updating...」と表示される場合あり

### 方法2: 手動Reboot
即座に反映したい場合：

1. https://share.streamlit.io/ にGitHubアカウントでログイン
2. アプリ一覧から **dental-manual-generator** を選択
3. 画面右下の「⋮」メニュー → **Reboot app** をクリック
4. 1-2分待ってアプリが再起動

### 方法3: キャッシュクリア
新機能が反映されない場合：

1. Streamlit Cloud管理画面で該当アプリを選択
2. **Settings** → **Clear cache** をクリック
3. その後 **Reboot app** を実行

## 🧪 機能テスト手順

### 1. 基本動作確認

#### APIキー設定
1. アプリを開く
2. 左サイドバーの「APIキーを入力」欄にGoogle Gemini APIキーを入力
3. ✅ 「APIキーが設定されました」と表示されることを確認

#### 動画アップロード（ファイル）
1. 「動画ソース・分析」タブを選択
2. 「ファイルアップロード」を選択
3. MP4/MOV/AVIファイルをアップロード（最大200MB）
4. ✅ 「動画をアップロードしました」と表示

#### 動画分析
1. 「🚀 分析開始」ボタンをクリック
2. 「動画からフレームを抽出中...」→「AIが動画を分析中...」と進む
3. ✅ 「分析が完了しました！」と表示
4. ✅ 分析結果プレビューが表示される

### 2. スクリーンショット機能確認（NEW!）

#### フレーム抽出確認
1. 分析完了後、「📊 分析結果プレビュー」セクションを確認
2. ✅ 「📸 抽出されたスクリーンショット」セクションが表示
3. ✅ 最大3枚のフレームがプレビュー表示される

#### 編集画面でのプレビュー
1. 「✏️ 編集・出力」タブに移動
2. 各ステップのexpanderを開く
3. ✅ ステップの先頭にスクリーンショットが表示される
4. ✅ 「⏱️ タイムスタンプ: X:XX」が表示される

#### ドキュメント生成確認
1. 「📄 Word」ボタンをクリック
2. ✅ 「Wordの生成が完了しました！」と表示
3. ダウンロードボタンから.docxファイルをダウンロード
4. ✅ 各ステップにスクリーンショットが埋め込まれていることを確認

5. 同様に「📕 PDF」「📊 PowerPoint」でも確認
   - PDF: 画像が各ステップに挿入される
   - PowerPoint: 画像がスライド右側に配置される

### 3. Google Drive対応確認

#### 大容量動画ダウンロード
1. Google Driveに動画をアップロード（共有設定を「リンクを知っている全員」に変更）
2. 共有リンクをコピー（形式: `https://drive.google.com/file/d/FILE_ID/view`）
3. アプリで「Google Driveリンク」を選択
4. URLを貼り付け
5. ✅ 「有効なGoogle Drive URLです」と表示
6. 「📥 Google Driveから動画をダウンロード」をクリック
7. ✅ ダウンロード完了（ファイルサイズ表示）

### 4. YouTube対応確認

1. YouTubeの公開動画URLをコピー
2. アプリで「YouTubeリンク」を選択
3. URLを貼り付け
4. ✅ 動画情報（タイトル、投稿者、長さ、再生回数）が表示
5. 「📥 YouTube動画をダウンロード」をクリック
6. ✅ ダウンロード完了

## 🐛 トラブルシューティング

### Streamlit Cloudでエラー

#### ImportError: cv2
**原因**: OpenCVの依存関係が不足
**解決策**:
- `requirements.txt`に`opencv-python-headless>=4.8.0`があることを確認
- `packages.txt`に以下が含まれていることを確認:
  ```
  libgl1-mesa-glx
  libglib2.0-0
  ```
- Streamlit Cloud管理画面で「Reboot app」を実行

#### google.generativeai警告
**警告内容**: "All support for google.generativeai package has ended"
**影響**: 現在は動作するが、将来的にサポート終了
**対応**: 将来`google.genai`パッケージへの移行が必要（現時点では不要）

#### APIキーエラー
**エラー**: "404 models/gemini-1.5-pro is not found"
**解決策**:
- モデル名が`models/gemini-1.5-flash`であることを確認（prefixの`models/`が必須）
- APIキーが有効か確認（https://ai.google.dev/）

### ローカル環境でのエラー

#### cffi/cryptography エラー
```bash
pip install --ignore-installed cffi cryptography
```

#### Streamlitが起動しない
```bash
# ポートが既に使用されている場合
pkill -f streamlit
streamlit run app.py
```

## 📊 フレーム抽出の仕組み

### 技術詳細
1. **抽出数**: デフォルト8フレーム（動画全体から均等に抽出）
2. **保存先**: `output/frames/YYYYMMDD_HHMMSS/frame_0.jpg`
3. **タイムスタンプ**: FPSから計算（例: frame_3 → 動画の37.5%地点）
4. **AI選択**: Gemini AIが各ステップに最も関連するフレームを自動選択
5. **データ構造**:
   ```json
   {
     "path": "output/frames/20260615_112830/frame_3.jpg",
     "index": 3,
     "timestamp": 45.2
   }
   ```

### Geminiプロンプト
各ステップに`frame_index`（0-7）を指定するようAIに指示:
```json
{
  "step_number": 1,
  "title": "器具の準備",
  "frame_index": 0,
  "image_path": "output/frames/.../frame_0.jpg"
}
```

## 🔄 次回の改善案

### 優先度: 高
- [ ] フレーム抽出数をUI で設定可能にする（現在は固定8枚）
- [ ] 画像サイズ・配置のカスタマイズオプション
- [ ] `google.genai`パッケージへの移行

### 優先度: 中
- [ ] 複数動画の一括処理
- [ ] マニュアルテンプレートの保存・再利用
- [ ] ステップの並び替え機能

### 優先度: 低
- [ ] 動画プレビュー機能
- [ ] フレーム手動選択オプション
- [ ] エクスポート履歴管理

## 📞 サポート

### リポジトリ
- **GitHub**: satoshiendo0003-code/codex-practice
- **ブランチ**: claude/fix-antigravity-startup-AWziT

### 本番環境
- **URL**: https://dental-manual-generator.streamlit.app/
- **ホスティング**: Streamlit Cloud

### 連絡先
- **Email**: satoshiendo0003@gmail.com

---

最終更新: 2026-06-15
