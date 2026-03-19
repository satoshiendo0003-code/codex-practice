"""
Dental Manual App - 完全拡張版
動画から歯科マニュアルを自動生成（全機能搭載）
"""
import streamlit as st
import os
from datetime import datetime
from state.session_state import app_state, AppState
from services.gemini_analyzer import GeminiAnalyzer
from services.document_generator import DocumentGenerator
from services.document_generator_extended import ExtendedDocumentGenerator
from services.youtube_downloader import YouTubeDownloader
from services.gdrive_downloader import GoogleDriveDownloader

# ページ設定
st.set_page_config(
    page_title="Dental Manual Generator - 完全版",
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
st.title("🦷 Dental Manual Generator - 完全版")
st.markdown("動画から歯科マニュアルを自動生成（PowerPoint/画像カード/YouTube対応）")

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

    st.markdown("---")

    # テンプレート選択
    st.subheader("🎨 デザインテンプレート")
    template_choice = st.selectbox(
        "テンプレート",
        ["modern", "classic", "simple"],
        index=0,
        help="Modern: モダンなグラデーション\nClassic: 伝統的なデザイン\nSimple: シンプルなデザイン"
    )

# メインコンテンツ
tab1, tab2 = st.tabs(["📹 動画ソース・分析", "✏️ 編集・出力"])

# タブ1: 動画ソース・分析
with tab1:
    st.subheader("🎥 動画ソース")

    # ソースタイプ選択
    source_type = st.radio(
        "動画の入力方法を選択",
        ["ファイルアップロード", "YouTubeリンク", "Google Driveリンク"],
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
            # YouTube URLの検証
            downloader = YouTubeDownloader()

            if downloader.is_valid_youtube_url(youtube_url):
                # 動画情報を表示
                with st.spinner("動画情報を取得中..."):
                    video_info = downloader.get_video_info(youtube_url)

                if video_info:
                    st.success("✅ 有効なYouTube URLです")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**タイトル**: {video_info['title']}")
                        st.write(f"**投稿者**: {video_info['uploader']}")
                    with col2:
                        duration_min = video_info['duration'] // 60
                        st.write(f"**長さ**: {duration_min}分")
                        st.write(f"**再生回数**: {video_info['view_count']:,}")

                    # ダウンロードボタン
                    if st.button("📥 YouTube動画をダウンロード", type="primary"):
                        progress_placeholder = st.empty()

                        def progress_callback(msg):
                            progress_placeholder.info(msg)

                        try:
                            video_path = downloader.download_video(
                                youtube_url,
                                progress_callback=progress_callback
                            )

                            if video_path:
                                app_state.video_path = video_path
                                st.success(f"✅ ダウンロード完了: {os.path.basename(video_path)}")
                                st.balloons()
                            else:
                                st.error("❌ ダウンロードに失敗しました")

                        except Exception as e:
                            st.error(f"❌ ダウンロードエラー: {str(e)}")

            else:
                st.error("❌ 有効なYouTube URLではありません")

    elif source_type == "Google Driveリンク":
        gdrive_url = st.text_input(
            "Google DriveのURLを入力",
            placeholder="https://drive.google.com/file/d/...",
            key="gdrive_url_input",
            help="共有リンクを「リンクを知っている全員」に設定してください"
        )

        if gdrive_url:
            # Google Drive URLの検証
            downloader = GoogleDriveDownloader()

            if downloader.is_valid_gdrive_url(gdrive_url):
                st.success("✅ 有効なGoogle Drive URLです")
                st.info("💡 ファイルサイズ制限なし！大きな動画も対応できます")

                # ダウンロードボタン
                if st.button("📥 Google Driveから動画をダウンロード", type="primary"):
                    progress_placeholder = st.empty()

                    def progress_callback(msg):
                        progress_placeholder.info(msg)

                    try:
                        video_path = downloader.download_video(
                            gdrive_url,
                            progress_callback=progress_callback
                        )

                        if video_path:
                            app_state.video_path = video_path
                            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
                            st.success(f"✅ ダウンロード完了: {file_size_mb:.1f}MB")
                            st.balloons()
                        else:
                            st.error("❌ ダウンロードに失敗しました")

                    except Exception as e:
                        st.error(f"❌ ダウンロードエラー: {str(e)}")
                        st.error("共有設定が「リンクを知っている全員」になっているか確認してください")

            else:
                st.error("❌ 有効なGoogle Drive URLではありません")
                st.info("💡 正しい形式: https://drive.google.com/file/d/FILE_ID/view")

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

            st.markdown(f"**タイトル**: {result.get('title', 'N/A')}")
            st.markdown(f"**概要**: {result.get('summary', 'N/A')}")
            st.markdown(f"**ステップ数**: {len(result.get('steps', []))}")

            if result.get('estimated_time'):
                st.markdown(f"**推定時間**: {result['estimated_time']}")

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
            with st.expander(f"ステップ {step.get('step_number', i+1)}: {step.get('title', '')}", expanded=False):
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
        st.subheader("📤 出力（全形式対応）")

        # 出力ボタン用のコールバック
        def generate_word_callback():
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = DocumentGenerator()
                word_path = generator.generate_word(updated_data, manual_title, manual_summary)

                st.session_state['gen_word'] = True
                st.session_state['gen_word_path'] = word_path
                st.session_state['gen_success'] = "Word"
            except Exception as e:
                st.session_state['gen_error'] = str(e)

        def generate_pdf_callback():
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = DocumentGenerator()
                pdf_path = generator.generate_pdf(updated_data, manual_title, manual_summary)

                st.session_state['gen_pdf'] = True
                st.session_state['gen_pdf_path'] = pdf_path
                st.session_state['gen_success'] = "PDF"
            except Exception as e:
                st.session_state['gen_error'] = str(e)

        def generate_powerpoint_callback():
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = ExtendedDocumentGenerator()
                pptx_path = generator.generate_powerpoint(
                    updated_data,
                    manual_title,
                    manual_summary,
                    template=template_choice
                )

                st.session_state['gen_pptx'] = True
                st.session_state['gen_pptx_path'] = pptx_path
                st.session_state['gen_success'] = "PowerPoint"
            except Exception as e:
                st.session_state['gen_error'] = str(e)

        def generate_image_cards_callback():
            try:
                st.session_state['updated_data'] = updated_data
                app_state.analysis_result = updated_data
                app_state.save_to_disk()

                generator = ExtendedDocumentGenerator()
                image_paths = generator.generate_image_cards(
                    updated_data,
                    manual_title,
                    template=template_choice
                )

                st.session_state['gen_images'] = True
                st.session_state['gen_images_paths'] = image_paths
                st.session_state['gen_success'] = "画像カード"
            except Exception as e:
                st.session_state['gen_error'] = str(e)

        # 出力ボタン（4列）
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.button(
                "📄 Word",
                on_click=generate_word_callback,
                key="btn_word",
                use_container_width=True,
                type="primary"
            )

        with col2:
            st.button(
                "📕 PDF",
                on_click=generate_pdf_callback,
                key="btn_pdf",
                use_container_width=True,
                type="primary"
            )

        with col3:
            st.button(
                "📊 PowerPoint",
                on_click=generate_powerpoint_callback,
                key="btn_pptx",
                use_container_width=True,
                type="primary"
            )

        with col4:
            st.button(
                "🖼️ 画像カード",
                on_click=generate_image_cards_callback,
                key="btn_images",
                use_container_width=True,
                type="primary"
            )

        # 成功/エラーメッセージ
        if st.session_state.get('gen_success'):
            format_name = st.session_state['gen_success']
            st.success(f"✅ {format_name}の生成が完了しました！")
            st.session_state['gen_success'] = None

        if st.session_state.get('gen_error'):
            st.error(f"❌ 生成エラー: {st.session_state['gen_error']}")
            st.session_state['gen_error'] = None

        # ダウンロードセクション
        st.markdown("---")
        st.subheader("📥 ダウンロード")

        col1, col2, col3, col4 = st.columns(4)

        # Word
        with col1:
            if st.session_state.get('gen_word') and st.session_state.get('gen_word_path'):
                word_path = st.session_state['gen_word_path']
                if os.path.exists(word_path):
                    with open(word_path, "rb") as f:
                        st.download_button(
                            "📄 Word",
                            data=f,
                            file_name=os.path.basename(word_path),
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            key="dl_word",
                            use_container_width=True
                        )

        # PDF
        with col2:
            if st.session_state.get('gen_pdf') and st.session_state.get('gen_pdf_path'):
                pdf_path = st.session_state['gen_pdf_path']
                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📕 PDF",
                            data=f,
                            file_name=os.path.basename(pdf_path),
                            mime="application/pdf",
                            key="dl_pdf",
                            use_container_width=True
                        )

        # PowerPoint
        with col3:
            if st.session_state.get('gen_pptx') and st.session_state.get('gen_pptx_path'):
                pptx_path = st.session_state['gen_pptx_path']
                if os.path.exists(pptx_path):
                    with open(pptx_path, "rb") as f:
                        st.download_button(
                            "📊 PowerPoint",
                            data=f,
                            file_name=os.path.basename(pptx_path),
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                            key="dl_pptx",
                            use_container_width=True
                        )

        # 画像カード
        with col4:
            if st.session_state.get('gen_images') and st.session_state.get('gen_images_paths'):
                image_paths = st.session_state['gen_images_paths']
                if image_paths:
                    st.write(f"🖼️ {len(image_paths)}枚生成")
                    for img_path in image_paths:
                        if os.path.exists(img_path):
                            with open(img_path, "rb") as f:
                                st.download_button(
                                    f"📥 {os.path.basename(img_path)}",
                                    data=f,
                                    file_name=os.path.basename(img_path),
                                    mime="image/png",
                                    key=f"dl_{os.path.basename(img_path)}",
                                    use_container_width=True
                                )

# フッター
st.markdown("---")
st.markdown("Made with ❤️ for dental professionals")
st.caption("Powered by Google Gemini AI | 完全版 v2.0")
