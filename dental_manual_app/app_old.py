"""
Dental Manual App - フル機能版
動画から歯科マニュアルを自動生成するStreamlitアプリ
"""
import streamlit as st
import os
from datetime import datetime
from state.session_state import app_state, AppState
from services.gemini_analyzer import GeminiAnalyzer
from services.document_generator import DocumentGenerator

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

    # APIキー入力
    st.subheader("🔑 Google Gemini API")
    api_key = st.text_input(
        "APIキーを入力",
        type="password",
        value=st.session_state.get(AppState.KEY_API_KEY, ""),
        help="Google AI StudioでAPIキーを取得してください",
        key="api_key_input"
    )

    if api_key:
        st.session_state[AppState.KEY_API_KEY] = api_key
        st.session_state[AppState.KEY_API_KEY_VALID] = True
        st.success("✅ APIキーが設定されました")
    else:
        st.session_state[AppState.KEY_API_KEY_VALID] = False
        st.warning("⚠️ APIキーを入力してください")

    st.markdown("---")

    # モデル選択
    selected_model = st.selectbox(
        "AIモデル",
        ["gemini-1.5-pro", "gemini-1.5-flash"],
        index=0,
        help="推奨: gemini-1.5-pro"
    )

    # マニュアルモード
    manual_mode = st.selectbox(
        "マニュアルモード",
        ["詳細", "簡易"],
        index=0,
        help="詳細: より詳しい手順書を生成"
    )

    # 対象読者
    target_audience = st.text_input(
        "対象読者",
        value="歯科助手",
        placeholder="例: 歯科助手、新人スタッフ"
    )

# メインコンテンツ
tab1, tab2 = st.tabs(["📹 動画ソース・分析", "✏️ 編集・出力"])

# タブ1: 動画ソース・分析
with tab1:
    st.subheader("🎥 動画ソース")

    # ソースタイプ選択
    source_type = st.radio(
        "動画の入力方法を選択",
        ["ファイルアップロード", "YouTubeリンク"],
        key="source_type_radio",
        horizontal=True
    )

    video_path = None

    if source_type == "ファイルアップロード":
        uploaded_file = st.file_uploader(
            "動画ファイルをアップロード",
            type=["mp4", "mov", "avi"],
            key="video_uploader"
        )

        if uploaded_file:
            # ファイルを保存
            os.makedirs("uploads", exist_ok=True)
            video_path = os.path.join("uploads", uploaded_file.name)

            with open(video_path, "wb") as f:
                f.write(uploaded_file.read())

            # 動画識別子を生成
            video_identifier = f"upload_{uploaded_file.name}_{uploaded_file.size}"

            last_video_id = st.session_state.get('last_video_identifier', None)

            # 新しい動画がアップロードされた場合
            if last_video_id != video_identifier:
                st.session_state['last_video_identifier'] = video_identifier
                app_state.video_path = video_path
                st.success(f"✅ 動画をアップロードしました: {uploaded_file.name}")

                # 前回の解析結果をクリア
                if last_video_id is not None:
                    app_state.analysis_result = None
                    st.info("新しい動画がアップロードされました。下の「分析開始」ボタンを押してください。")

    elif source_type == "YouTubeリンク":
        youtube_url = st.text_input(
            "YouTubeのURLを入力",
            placeholder="https://www.youtube.com/watch?v=...",
            key="youtube_url_input"
        )

        if youtube_url:
            st.info("YouTube動画のダウンロード機能は現在開発中です。")
            st.info("現在はファイルアップロードをご利用ください。")

    st.markdown("---")

    # 分析ボタン
    st.subheader("🔍 動画分析")

    if not st.session_state.get(AppState.KEY_API_KEY_VALID, False):
        st.error("❌ APIキーを設定してください（左サイドバー）")
    elif not app_state.video_path:
        st.info("📹 動画をアップロードしてください")
    else:
        col1, col2 = st.columns([1, 3])

        with col1:
            analyze_button = st.button(
                "🚀 分析開始",
                type="primary",
                use_container_width=True
            )

        if analyze_button:
            try:
                # Gemini Analyzerを初期化
                analyzer = GeminiAnalyzer(api_key=st.session_state[AppState.KEY_API_KEY])

                # 動画を分析
                with st.spinner("AIが動画を分析しています..."):
                    result = analyzer.analyze_video(
                        video_path=app_state.video_path,
                        target_audience=target_audience,
                        manual_mode=manual_mode
                    )

                # 結果を保存
                app_state.analysis_result = result
                app_state.save_to_disk()

                st.success("✅ 分析が完了しました！")
                st.balloons()
                st.info("「✏️ 編集・出力」タブで結果を確認・編集できます")

            except Exception as e:
                st.error(f"❌ 分析エラー: {str(e)}")
                st.error("APIキーが正しいか確認してください")

        # 分析結果のプレビュー
        if app_state.analysis_result:
            st.markdown("---")
            st.subheader("📊 分析結果プレビュー")

            result = app_state.analysis_result

            st.markdown(f"**タイトル:** {result.get('title', 'N/A')}")
            st.markdown(f"**概要:** {result.get('summary', 'N/A')}")
            st.markdown(f"**ステップ数:** {len(result.get('steps', []))}")

            if result.get('estimated_time'):
                st.markdown(f"**推定時間:** {result['estimated_time']}")

# タブ2: 編集・出力
with tab2:
    st.subheader("✏️ マニュアル編集")

    if not app_state.analysis_result:
        st.info("📹 まず「動画ソース・分析」タブで動画を分析してください")
    else:
        # 編集フォーム
        result = app_state.analysis_result

        # マニュアルタイトル
        manual_title = st.text_input(
            "マニュアルタイトル",
            value=result.get('title', '新規マニュアル'),
            key="manual_title_edit"
        )

        # マニュアル概要
        manual_summary = st.text_area(
            "マニュアル概要",
            value=result.get('summary', ''),
            height=100,
            key="manual_summary_edit"
        )

        # 推定時間
        estimated_time = st.text_input(
            "推定所要時間",
            value=result.get('estimated_time', ''),
            key="estimated_time_edit"
        )

        # 必要な器具
        required_tools_text = "\n".join(result.get('required_tools', []))
        required_tools_input = st.text_area(
            "必要な器具（1行に1つ）",
            value=required_tools_text,
            height=100,
            key="required_tools_edit"
        )

        st.markdown("---")

        # ステップ編集
        st.subheader("📝 手順")

        steps = result.get('steps', [])
        edited_steps = []

        for i, step in enumerate(steps):
            with st.expander(f"ステップ {step.get('step_number', i+1)}: {step.get('title', '')}", expanded=True):
                step_title = st.text_input(
                    "ステップタイトル",
                    value=step.get('title', ''),
                    key=f"step_{i}_title"
                )

                step_description = st.text_area(
                    "説明",
                    value=step.get('description', ''),
                    height=150,
                    key=f"step_{i}_desc"
                )

                col1, col2 = st.columns(2)

                with col1:
                    key_points_text = "\n".join(step.get('key_points', []))
                    key_points = st.text_area(
                        "重要ポイント（1行に1つ）",
                        value=key_points_text,
                        height=100,
                        key=f"step_{i}_keypoints"
                    )

                with col2:
                    warnings_text = "\n".join(step.get('warnings', []))
                    warnings = st.text_area(
                        "⚠️ 注意事項（1行に1つ）",
                        value=warnings_text,
                        height=100,
                        key=f"step_{i}_warnings"
                    )

                # 編集後のステップを保存
                edited_steps.append({
                    'step_number': step.get('step_number', i+1),
                    'title': step_title,
                    'description': step_description,
                    'key_points': [p.strip() for p in key_points.split('\n') if p.strip()],
                    'warnings': [w.strip() for w in warnings.split('\n') if w.strip()]
                })

        # 編集後のデータを更新
        updated_data = {
            'title': manual_title,
            'summary': manual_summary,
            'estimated_time': estimated_time,
            'required_tools': [t.strip() for t in required_tools_input.split('\n') if t.strip()],
            'steps': edited_steps
        }

        st.markdown("---")

        # 出力セクション
        st.subheader("📤 出力")

        # 出力ボタン用のコールバック
        def generate_word_callback():
            """Wordファイル生成のコールバック"""
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = DocumentGenerator()
                word_path = generator.generate_word(
                    data=updated_data,
                    title=manual_title,
                    summary=manual_summary
                )

                st.session_state['gen_word'] = True
                st.session_state['gen_word_path'] = word_path
                st.session_state['gen_success'] = True

            except Exception as e:
                st.session_state['gen_error'] = str(e)
                st.session_state['gen_success'] = False

        def generate_pdf_callback():
            """PDFファイル生成のコールバック"""
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = DocumentGenerator()
                pdf_path = generator.generate_pdf(
                    data=updated_data,
                    title=manual_title,
                    summary=manual_summary
                )

                st.session_state['gen_pdf'] = True
                st.session_state['gen_pdf_path'] = pdf_path
                st.session_state['gen_success'] = True

            except Exception as e:
                st.session_state['gen_error'] = str(e)
                st.session_state['gen_success'] = False

        # 出力ボタン
        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "📄 Word生成",
                on_click=generate_word_callback,
                key="btn_generate_word",
                use_container_width=True,
                type="primary"
            )

        with col2:
            st.button(
                "📕 PDF生成",
                on_click=generate_pdf_callback,
                key="btn_generate_pdf",
                use_container_width=True,
                type="primary"
            )

        # 成功/エラーメッセージ
        if st.session_state.get('gen_success'):
            st.success("✅ 生成が完了しました！")
            st.session_state['gen_success'] = False

        if st.session_state.get('gen_error'):
            st.error(f"❌ 生成エラー: {st.session_state['gen_error']}")
            st.session_state['gen_error'] = None

        # ダウンロードセクション
        st.markdown("---")
        st.subheader("📥 ダウンロード")

        col1, col2 = st.columns(2)

        with col1:
            if st.session_state.get('gen_word') and st.session_state.get('gen_word_path'):
                word_path = st.session_state['gen_word_path']
                if os.path.exists(word_path):
                    with open(word_path, "rb") as f:
                        st.download_button(
                            "📄 Download Word",
                            data=f,
                            file_name=os.path.basename(word_path),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key="download_word",
                            use_container_width=True
                        )

        with col2:
            if st.session_state.get('gen_pdf') and st.session_state.get('gen_pdf_path'):
                pdf_path = st.session_state['gen_pdf_path']
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📕 Download PDF",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf",
                            key="download_pdf",
                            use_container_width=True
                        )

# フッター
st.markdown("---")
st.markdown("Made with ❤️ for dental professionals")
st.caption("Powered by Google Gemini AI")
