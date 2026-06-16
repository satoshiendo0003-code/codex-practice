# 🖥️ CLI版 使用ガイド

コマンドラインから直接マニュアルを生成できます。  
バッチ処理、自動化、スクリプト統合に便利。

---

## 🚀 基本的な使い方

### 最小構成（Word + PDF生成）

```bash
python cli.py video.mp4 --api-key YOUR_GEMINI_API_KEY
```

### 環境変数でAPIキーを設定（推奨）

```bash
# 1回設定
export GEMINI_API_KEY=your_api_key_here

# 以降はAPIキー不要
python cli.py video.mp4
```

または `.env` ファイルに記載:
```bash
GEMINI_API_KEY=your_api_key_here
```

---

## 📋 コマンドオプション

### 必須パラメータ

```bash
python cli.py <動画ファイル>
```

例: `python cli.py dental_procedure.mp4`

### オプションパラメータ

| オプション | 短縮 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `--api-key` | - | 環境変数 | Gemini APIキー |
| `--formats` | `-f` | `word pdf` | 生成形式 |
| `--output` | `-o` | `output` | 出力ディレクトリ |
| `--audience` | `-a` | `歯科助手` | 対象読者 |
| `--mode` | `-m` | `詳細` | マニュアルモード |
| `--template` | `-t` | `modern` | デザインテンプレート |
| `--quiet` | `-q` | - | 詳細メッセージ抑制 |

---

## 📄 生成形式の指定

### 利用可能な形式

- `word` - Word文書 (.docx)
- `pdf` - PDF文書
- `pptx` または `powerpoint` - PowerPoint (.pptx)
- `images` または `cards` - 画像カード（SNS用）
- `all` - すべての形式

### 例

#### Word + PDF（デフォルト）
```bash
python cli.py video.mp4
```

#### PowerPointも追加
```bash
python cli.py video.mp4 --formats word pdf pptx
```

#### すべての形式を生成
```bash
python cli.py video.mp4 --formats all
```

#### PDFのみ
```bash
python cli.py video.mp4 --formats pdf
```

---

## 🎨 カスタマイズ

### 対象読者を変更

```bash
python cli.py video.mp4 --audience "新人歯科衛生士"
```

### マニュアルモード

```bash
# 詳細モード（デフォルト）
python cli.py video.mp4 --mode 詳細

# 簡易モード
python cli.py video.mp4 --mode 簡易
```

### デザインテンプレート

```bash
# Modern（デフォルト）
python cli.py video.mp4 --template modern

# Classic
python cli.py video.mp4 --template classic

# Simple
python cli.py video.mp4 --template simple
```

### 出力先を変更

```bash
python cli.py video.mp4 --output custom_output
```

---

## 🔄 バッチ処理

### 複数動画を一括処理

```bash
#!/bin/bash
# batch_process.sh

export GEMINI_API_KEY=your_key_here

for video in videos/*.mp4; do
    echo "Processing: $video"
    python cli.py "$video" --formats all
done

echo "All done!"
```

実行:
```bash
chmod +x batch_process.sh
./batch_process.sh
```

### ディレクトリごとに整理

```bash
#!/bin/bash
# organized_batch.sh

export GEMINI_API_KEY=your_key_here

for video in videos/*.mp4; do
    # ファイル名から拡張子を除去
    basename=$(basename "$video" .mp4)
    
    # 専用ディレクトリに出力
    python cli.py "$video" \
        --output "manuals/$basename" \
        --formats all
done
```

---

## 🛠️ 実用例

### 1. 院内研修用PowerPoint生成

```bash
python cli.py training_video.mp4 \
    --formats pptx \
    --audience "スタッフ全員" \
    --template modern \
    --output training_materials
```

### 2. 患者説明用PDF

```bash
python cli.py procedure.mp4 \
    --formats pdf \
    --audience "患者様" \
    --mode 簡易 \
    --output patient_guides
```

### 3. SNS投稿用画像カード

```bash
python cli.py simple_procedure.mp4 \
    --formats images \
    --template modern \
    --output social_media
```

### 4. 全形式一括生成（アーカイブ用）

```bash
python cli.py important_procedure.mp4 \
    --formats all \
    --audience "歯科助手" \
    --mode 詳細 \
    --template classic \
    --output archive/$(date +%Y%m%d)
```

---

## 🔧 自動化・スケジューリング

### cron で定期実行

```bash
# crontab -e で編集

# 毎日午前2時に処理
0 2 * * * cd /path/to/dental_manual_app && python cli.py /path/to/daily_video.mp4
```

### Watchフォルダ監視

```bash
#!/bin/bash
# watch_folder.sh

WATCH_DIR="videos/inbox"
PROCESSED_DIR="videos/processed"

export GEMINI_API_KEY=your_key_here

while true; do
    for video in "$WATCH_DIR"/*.mp4; do
        if [ -f "$video" ]; then
            echo "New video detected: $video"
            
            # マニュアル生成
            python cli.py "$video" --formats all
            
            # 処理済みフォルダに移動
            mv "$video" "$PROCESSED_DIR/"
            
            echo "Processed: $video"
        fi
    done
    
    # 10秒待機
    sleep 10
done
```

---

## 📊 出力例

### 実行ログ

```
╔════════════════════════════════════════════════════════════╗
║  🦷 Dental Manual Generator - CLI                         ║
║  動画から自動でマニュアルを生成                            ║
╚════════════════════════════════════════════════════════════╝

📹 動画を分析中: dental_procedure.mp4
   対象: 歯科助手
   モード: 詳細

⏳ フレーム抽出中...
✅ 分析完了！
   タイトル: 歯石除去の基本手順
   ステップ数: 5
   推定時間: 15分

📄 Word生成中...
   ✅ output/歯石除去の基本手順.docx
📕 PDF生成中...
   ✅ output/歯石除去の基本手順.pdf

============================================================
✅ 完了！
   生成ファイル数: 2
   出力先: output/
============================================================
```

### 生成されたファイル

```
output/
├── 歯石除去の基本手順.docx
├── 歯石除去の基本手順.pdf
├── 歯石除去の基本手順.pptx
├── 歯石除去の基本手順_card_title.png
├── 歯石除去の基本手順_card_step1.png
├── 歯石除去の基本手順_card_step2.png
└── frames/
    └── 20260616_130102/
        ├── frame_0.jpg
        ├── frame_1.jpg
        └── ...
```

---

## 🐛 トラブルシューティング

### エラー: APIキーが指定されていません

```bash
# 解決策1: コマンドで指定
python cli.py video.mp4 --api-key YOUR_KEY

# 解決策2: 環境変数
export GEMINI_API_KEY=your_key
python cli.py video.mp4

# 解決策3: .envファイル
echo "GEMINI_API_KEY=your_key" > .env
python cli.py video.mp4
```

### エラー: 動画ファイルが見つかりません

```bash
# パスを確認
ls -la video.mp4

# 絶対パスで指定
python cli.py /full/path/to/video.mp4
```

### 警告: google.generativeai deprecation

現在は動作します（将来的に `google.genai` への移行が必要）

---

## ⚡ パフォーマンス

### 処理時間（5分動画）

| 処理 | 時間 |
|------|------|
| フレーム抽出 | 5秒 |
| AI分析 | 20秒 |
| Word生成 | 2秒 |
| PDF生成 | 3秒 |
| PowerPoint生成 | 2秒 |
| **合計** | **32秒** |

### メモリ使用量

- 最小: 200MB
- 通常: 500MB
- 最大: 1GB（長時間動画）

---

## 🔗 統合例

### Python スクリプトから呼び出し

```python
import subprocess

result = subprocess.run([
    'python', 'cli.py',
    'video.mp4',
    '--formats', 'word', 'pdf',
    '--audience', '新人スタッフ'
], capture_output=True, text=True)

if result.returncode == 0:
    print("Success!")
else:
    print(f"Error: {result.stderr}")
```

### シェルスクリプトに統合

```bash
#!/bin/bash

# 動画をダウンロード
youtube-dl -o video.mp4 "https://youtube.com/..."

# マニュアル生成
python cli.py video.mp4 --formats all

# 生成物をメール送信
mail -s "マニュアル完成" staff@clinic.com < output/
```

---

## 📚 関連ドキュメント

- **Web UI版**: [QUICKSTART.md](./QUICKSTART.md)
- **デプロイ**: [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
- **テスト**: [TEST_FEATURES.md](./TEST_FEATURES.md)

---

## 💡 ヒント

### 1. エイリアスで簡単に

```bash
# ~/.bashrc または ~/.zshrc
alias dental-gen='python /path/to/cli.py'

# 使用例
dental-gen video.mp4 --formats all
```

### 2. デフォルト設定

```bash
# よく使う設定を環境変数化
export DENTAL_AUDIENCE="歯科助手"
export DENTAL_TEMPLATE="modern"

# スクリプトで使用
python cli.py video.mp4 \
    --audience "$DENTAL_AUDIENCE" \
    --template "$DENTAL_TEMPLATE"
```

### 3. ログファイル保存

```bash
python cli.py video.mp4 2>&1 | tee manual_generation.log
```

---

**CLI版とWeb UI版の使い分け**:
- CLI: バッチ処理、自動化、スクリプト統合
- Web UI: 手動操作、プレビュー確認、編集が必要な場合

両方使えます！🚀
