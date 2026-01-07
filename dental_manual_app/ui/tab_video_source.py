"""
動画ソース選択タブ
"""
import streamlit as st
import os
from state.session_state import app_state

def render_video_source_tab(selected_model, manual_mode, target_audience):
    """動画ソース選択タブの描画"""
    st.subheader("🎥 動画ソース")

    source_type = st.radio(
        "動画の入力方法を選択",
        ["ファイルアップロード", "YouTubeリンク"],
        key="source_type_radio"
    )

    if source_type == "ファイルアップロード":
        uploaded_file = st.file_uploader(
            "動画ファイルをドラッグ＆ドロップ",
            type=["mp4", "mov"],
            key="video_uploader"
        )

        if uploaded_file:
            # ファイルを保存
            os.makedirs("uploads", exist_ok=True)
            video_path = os.path.join("uploads", uploaded_file.name)

            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            # 修正: タイムスタンプではなくファイルサイズと名前でID生成（リロード時の変化防止）
            video_identifier = f"upload_{uploaded_file.name}_{uploaded_file.size}"

            last_video_id = st.session_state.get('last_video_identifier', None)

            # 修正: 新しい動画がアップロードされた場合のみクリア
            if last_video_id != video_identifier and app_state.analysis_result:
                st.warning("新しい動画がアップロードされました。前回の解析結果はクリアされます。")
                app_state.analysis_result = None

            st.session_state['last_video_identifier'] = video_identifier
            app_state.video_path = video_path

            st.success(f"✅ 動画をアップロードしました: {uploaded_file.name}")

    elif source_type == "YouTubeリンク":
        youtube_url = st.text_input(
            "YouTubeのURLを入力",
            placeholder="https://www.youtube.com/watch?v=...",
            key="youtube_url_input"
        )

        if youtube_url:
            app_state.video_path = youtube_url
            st.success(f"✅ YouTubeリンクを設定しました")
