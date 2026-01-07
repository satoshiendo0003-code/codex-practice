# Dental Manual App - 修正版

動画から歯科マニュアルを自動生成するStreamlitアプリケーション

## 🐛 修正した問題

### 問題: 出力ボタンを押すとページがリセットされる

**症状:**
- WordボタンやPDFボタンを押すと、ページ全体がリセットされる
- 編集中のデータが失われる
- ダウンロードボタンが表示されない

### 原因

Streamlitの動作特性による問題：

1. **ボタンクリック時のページ再実行**
   - `st.button()`をクリックすると、Streamlitはスクリプト全体を再実行する
   - この時、ボタンのイベントハンドラ内で状態を保存していても、再実行時にデータが失われる可能性がある

2. **セッション状態の更新タイミング**
   - ボタンクリック内で`st.session_state`に値を設定しても、その値が次の再実行まで反映されない場合がある
   - `updated_data`などのローカル変数がページ再実行時に失われる

3. **フラグの管理不足**
   - 生成完了フラグが適切に管理されていないため、ダウンロードボタンが表示されない

## ✅ 修正内容

### 1. コールバック関数の使用 (`ui/tab_editor.py:23-50`)

**修正前:**
```python
if st.button("Word生成"):
    handle_generation("docx")
    st.success("Word生成完了")
```

**修正後:**
```python
def generate_word_callback():
    """コールバック関数（ページ再実行前に実行）"""
    st.session_state[f"{key_prefix}_updated_data"] = updated_data
    app_state.analysis_result = updated_data
    app_state.save_to_disk()
    # ... 生成処理 ...
    st.session_state[f"{key_prefix}_gen_docx"] = True

st.button(
    "📄 Word生成",
    on_click=generate_word_callback,  # ← 重要: コールバックを指定
    key=f"{key_prefix}_btn_word"
)
```

**効果:**
- `on_click`コールバックはページ再実行**前**に実行される
- セッション状態への保存が確実に行われる
- データの損失を防ぐ

### 2. セッション状態への確実な保存 (`ui/tab_editor.py:29-31`)

```python
# データをセッション状態に保存
st.session_state[f"{key_prefix}_updated_data"] = updated_data
app_state.analysis_result = updated_data
app_state.save_to_disk()  # ディスクにも保存
```

**効果:**
- ページ再実行時にデータが保持される
- アプリを閉じても状態が復元される

### 3. 生成フラグの管理 (`ui/tab_editor.py:43-48`)

```python
# 成功フラグを立てる
st.session_state[f"{key_prefix}_gen_docx"] = True
st.session_state[f"{key_prefix}_gen_success"] = True
```

**効果:**
- ダウンロードボタンが常に表示される
- 成功/エラーメッセージが適切に表示される

### 4. フォームの使用（オプション）(`ui/tab_editor.py:55-70`)

```python
with st.form(key=f"{key_prefix}_output_form"):
    word_btn = st.form_submit_button("📄 Word生成")
    if word_btn:
        generate_word_callback()
        st.rerun()
```

**効果:**
- フォーム内のボタンは送信時のみページを再実行する
- より予測可能な動作

## 📁 ファイル構成

```
dental_manual_app/
├── app.py                      # メインアプリケーション
├── state/
│   └── session_state.py       # セッション状態管理（修正済み）
├── ui/
│   ├── tab_video_source.py    # 動画ソース選択タブ（修正済み）
│   └── tab_editor.py          # エディタータブ（修正済み）
├── output/                     # 生成ファイルの出力先
└── README.md                   # このファイル
```

## 🚀 実行方法

```bash
cd dental_manual_app
streamlit run app.py
```

## 📚 修正のポイント

### Streamlitのボタンの正しい使い方

1. **コールバック関数を使う（推奨）**
   ```python
   st.button("クリック", on_click=callback_function)
   ```

2. **フォームを使う**
   ```python
   with st.form("my_form"):
       st.form_submit_button("送信")
   ```

3. **セッション状態を活用する**
   ```python
   st.session_state['key'] = value  # ページ再実行時も保持される
   ```

### 避けるべきパターン

```python
# ❌ 悪い例: ボタンクリック内で直接処理
if st.button("実行"):
    data = expensive_operation()  # ページ再実行時に失われる
    st.write(data)

# ✅ 良い例: コールバックで状態を保存
def on_click():
    st.session_state['data'] = expensive_operation()

st.button("実行", on_click=on_click)
if 'data' in st.session_state:
    st.write(st.session_state['data'])
```

## 🔍 デバッグのヒント

問題が発生した場合は、以下を確認してください：

1. **セッション状態の確認**
   ```python
   st.write(st.session_state)  # すべての状態を表示
   ```

2. **ボタンクリックの検出**
   ```python
   if st.button("テスト"):
       st.write("ボタンがクリックされました")  # 1回だけ表示される
   ```

3. **コールバックのデバッグ**
   ```python
   def callback():
       st.session_state['debug'] = "コールバック実行"
   ```

## 📝 今後の改善案

- [ ] python-docxを使用した実際のWord生成実装
- [ ] ReportLabを使用したPDF生成実装
- [ ] 画像の埋め込み機能
- [ ] より詳細なエラーハンドリング
- [ ] 進捗バーの表示
