"""
Google Drive ダウンローダーモジュール
Google Driveから動画ファイルをダウンロード
"""
import gdown
import os
import re
from typing import Optional


class GoogleDriveDownloader:
    """Google Driveから動画をダウンロードするクラス"""

    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        """
        Google Drive URLからファイルIDを抽出

        Args:
            url: Google Drive URL

        Returns:
            ファイルID（抽出できない場合はNone）
        """
        # パターン1: https://drive.google.com/file/d/FILE_ID/view
        pattern1 = r'drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
        match = re.search(pattern1, url)
        if match:
            return match.group(1)

        # パターン2: https://drive.google.com/open?id=FILE_ID
        pattern2 = r'drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)'
        match = re.search(pattern2, url)
        if match:
            return match.group(1)

        # パターン3: 直接ファイルIDが渡された場合
        if re.match(r'^[a-zA-Z0-9_-]+$', url):
            return url

        return None

    @staticmethod
    def is_valid_gdrive_url(url: str) -> bool:
        """
        Google Drive URLが有効かチェック

        Args:
            url: チェックするURL

        Returns:
            有効な場合True
        """
        return GoogleDriveDownloader.extract_file_id(url) is not None

    @staticmethod
    def download_video(
        url: str,
        output_dir: str = "downloads",
        progress_callback=None
    ) -> Optional[str]:
        """
        Google Driveから動画をダウンロード

        Args:
            url: Google Drive URL
            output_dir: 出力ディレクトリ
            progress_callback: 進捗コールバック関数

        Returns:
            ダウンロードしたファイルのパス（失敗した場合はNone）
        """
        try:
            # ファイルIDを抽出
            file_id = GoogleDriveDownloader.extract_file_id(url)
            if not file_id:
                if progress_callback:
                    progress_callback("❌ 無効なGoogle Drive URLです")
                return None

            # 出力ディレクトリを作成
            os.makedirs(output_dir, exist_ok=True)

            # ダウンロードURL
            download_url = f"https://drive.google.com/uc?id={file_id}"

            if progress_callback:
                progress_callback("📥 Google Driveからダウンロード中...")

            # ダウンロード
            output_path = os.path.join(output_dir, f"gdrive_{file_id}.mp4")
            gdown.download(download_url, output_path, quiet=False)

            if os.path.exists(output_path):
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
                if progress_callback:
                    progress_callback(f"✅ ダウンロード完了: {file_size_mb:.1f}MB")
                return output_path
            else:
                if progress_callback:
                    progress_callback("❌ ダウンロードに失敗しました")
                return None

        except Exception as e:
            if progress_callback:
                progress_callback(f"❌ エラー: {str(e)}")
            return None
