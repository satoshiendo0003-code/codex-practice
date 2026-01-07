"""
エディタータブ（出力セクション）
修正版: 出力ボタンを押してもページがリセットされないように修正
"""
import streamlit as st
import os
from state.session_state import app_state

def render_output_section(updated_data, image_paths, manual_title, creation_date, manual_summary, key_prefix="bottom"):
    """
    出力セクションの描画

    修正点:
    1. st.formを使用してボタンクリック時のページリセットを防止
    2. コールバック関数を使用して状態を確実に保存
    3. セッション状態に生成フラグを保持
    """
    st.subheader("📤 出力")

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # 修正1: 生成処理をコールバック関数として定義
    def generate_word_callback():
        """Wordファイル生成のコールバック（ページ再実行前に実行される）"""
        try:
            # セッション状態に確実に保存
            st.session_state[f"{key_prefix}_updated_data"] = updated_data
            app_state.analysis_result = updated_data
            app_state.save_to_disk()

            # 生成処理（ダミー実装 - 実際のロジックはここに追加）
            docx_path = os.path.join(output_dir, "manual.docx")

            # ダミー: 実際にはpython-docxなどを使用してWordファイルを生成
            with open(docx_path, "w") as f:
                f.write(f"Manual Title: {manual_title}\n")
                f.write(f"Summary: {manual_summary}\n")
                f.write(f"Data: {str(updated_data)}\n")

            # 成功フラグを立てる
            st.session_state[f"{key_prefix}_gen_docx"] = True
            st.session_state[f"{key_prefix}_gen_success"] = True

        except Exception as e:
            st.session_state[f"{key_prefix}_gen_error"] = str(e)
            st.session_state[f"{key_prefix}_gen_success"] = False

    def generate_pdf_callback():
        """PDFファイル生成のコールバック"""
        try:
            st.session_state[f"{key_prefix}_updated_data"] = updated_data
            app_state.analysis_result = updated_data
            app_state.save_to_disk()

            pdf_path = os.path.join(output_dir, "manual.pdf")

            # ダミー: 実際にはReportLabなどを使用してPDFを生成
            with open(pdf_path, "w") as f:
                f.write(f"PDF: {manual_title}\n")

            st.session_state[f"{key_prefix}_gen_pdf"] = True
            st.session_state[f"{key_prefix}_gen_success"] = True

        except Exception as e:
            st.session_state[f"{key_prefix}_gen_error"] = str(e)
            st.session_state[f"{key_prefix}_gen_success"] = False

    # 修正2: st.formを使用してボタンのグループ化（オプション1）
    # フォームを使用すると、送信ボタンを押すまで他のウィジェットの変更が反映されない
    use_form = False  # Trueにするとフォームを使用

    if use_form:
        with st.form(key=f"{key_prefix}_output_form"):
            col1, col2 = st.columns(2)

            with col1:
                word_btn = st.form_submit_button("📄 Word生成", use_container_width=True)

            with col2:
                pdf_btn = st.form_submit_button("📕 PDF生成", use_container_width=True)

            if word_btn:
                generate_word_callback()
                st.rerun()

            if pdf_btn:
                generate_pdf_callback()
                st.rerun()
    else:
        # 修正3: on_clickコールバックを使用（オプション2 - 推奨）
        col1, col2 = st.columns(2)

        with col1:
            st.button(
                "📄 Word生成",
                key=f"{key_prefix}_btn_word",
                on_click=generate_word_callback,  # ← 重要: コールバックを指定
                use_container_width=True
            )

        with col2:
            st.button(
                "📕 PDF生成",
                key=f"{key_prefix}_btn_pdf",
                on_click=generate_pdf_callback,  # ← 重要: コールバックを指定
                use_container_width=True
            )

    # 修正4: 成功/エラーメッセージを表示
    if st.session_state.get(f"{key_prefix}_gen_success"):
        st.success("✅ 生成が完了しました！")
        # フラグをリセット（次回のために）
        st.session_state[f"{key_prefix}_gen_success"] = False

    if st.session_state.get(f"{key_prefix}_gen_error"):
        error_msg = st.session_state[f"{key_prefix}_gen_error"]
        st.error(f"❌ 生成エラー: {error_msg}")
        st.session_state[f"{key_prefix}_gen_error"] = None

    # 修正5: ダウンロードボタン（フラグがあれば常に表示）
    st.markdown("---")
    st.markdown("### 📥 ダウンロード")

    col1, col2 = st.columns(2)

    with col1:
        if st.session_state.get(f"{key_prefix}_gen_docx"):
            docx_path = os.path.join(output_dir, "manual.docx")
            if os.path.exists(docx_path):
                with open(docx_path, "rb") as f:
                    st.download_button(
                        "📄 Download Word",
                        data=f,
                        file_name="manual.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"{key_prefix}_download_word",
                        use_container_width=True
                    )

    with col2:
        if st.session_state.get(f"{key_prefix}_gen_pdf"):
            pdf_path = os.path.join(output_dir, "manual.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📕 Download PDF",
                        data=f,
                        file_name="manual.pdf",
                        mime="application/pdf",
                        key=f"{key_prefix}_download_pdf",
                        use_container_width=True
                    )
