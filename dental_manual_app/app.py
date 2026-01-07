"""
Dental Manual App - メインアプリケーション
動画から歯科マニュアルを自動生成するStreamlitアプリ

修正版: 出力ボタンを押してもページがリセットされない
"""
import streamlit as st
from state.session_state import app_state, AppState
from ui.tab_video_source import render_video_source_tab
from ui.tab_editor import render_output_section

# ページ設定
st.set_page_config(
    page_title="Dental Manual Generator",
    page_icon="🦷",
    layout="wide"
)

# セッション状態の初期化
AppState.initialize()

# 自動ロード処理
if not app_state.analysis_result:
    if app_state.load_from_disk():
        if app_state.analysis_result:
            st.toast("前回作業していた状態を復元しました", icon="📂")

# タイトル
st.title("🦷 Dental Manual Generator")
st.markdown("動画から歯科マニュアルを自動生成します")

# サイドバー設定
with st.sidebar:
    st.header("⚙️ 設定")

    # モデル選択
    selected_model = st.selectbox(
        "AIモデル",
        ["gemini-1.5-pro", "gemini-1.5-flash"],
        index=0
    )

    # マニュアルモード
    manual_mode = st.selectbox(
        "マニュアルモード",
        ["詳細", "簡易"],
        index=0
    )

    # 対象読者
    target_audience = st.text_input(
        "対象読者",
        value="歯科助手",
        placeholder="例: 歯科助手、新人スタッフ"
    )

# メインコンテンツ
tab1, tab2 = st.tabs(["📹 動画ソース", "✏️ 編集・出力"])

with tab1:
    render_video_source_tab(selected_model, manual_mode, target_audience)

with tab2:
    st.subheader("✏️ マニュアル編集")

    # ダミーデータ（実際の実装では解析結果を使用）
    if app_state.analysis_result:
        updated_data = app_state.analysis_result
    else:
        updated_data = {
            "steps": [
                {"title": "準備", "description": "必要な器具を準備します"},
                {"title": "施術", "description": "患者さんに施術を行います"},
                {"title": "後片付け", "description": "使用した器具を片付けます"}
            ]
        }

    # マニュアルタイトル
    manual_title = st.text_input(
        "マニュアルタイトル",
        value=st.session_state.get(AppState.KEY_MANUAL_TITLE, "新規マニュアル"),
        key="manual_title_input"
    )

    # マニュアル概要
    manual_summary = st.text_area(
        "マニュアル概要",
        value="このマニュアルは歯科助手向けの手順書です。",
        height=100
    )

    # 作成日
    import datetime
    creation_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # ステップ編集（簡易版）
    st.markdown("### 📝 手順")
    for i, step in enumerate(updated_data.get("steps", [])):
        with st.expander(f"ステップ {i+1}: {step.get('title', '')}"):
            step['title'] = st.text_input(
                "タイトル",
                value=step.get('title', ''),
                key=f"step_{i}_title"
            )
            step['description'] = st.text_area(
                "説明",
                value=step.get('description', ''),
                key=f"step_{i}_desc",
                height=100
            )

    # 出力セクション（修正版）
    st.markdown("---")
    render_output_section(
        updated_data=updated_data,
        image_paths=app_state.image_paths,
        manual_title=manual_title,
        creation_date=creation_date,
        manual_summary=manual_summary,
        key_prefix="main"
    )

# フッター
st.markdown("---")
st.markdown("Made with ❤️ for dental professionals")
