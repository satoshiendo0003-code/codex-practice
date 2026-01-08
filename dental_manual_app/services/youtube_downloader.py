"""
YouTube動画ダウンロードモジュール
"""
import yt_dlp
import os
from typing import Optional
import streamlit as st


class YouTubeDownloader:
    """YouTube動画をダウンロードするクラス"""

    def __init__(self, output_dir: str = "uploads"):
        """
        Args:
            output_dir: ダウンロード先ディレクトリ
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def download_video(self, url: str, progress_callback=None) -> Optional[str]:
        """
        YouTube動画をダウンロード

        Args:
            url: YouTubeのURL
            progress_callback: 進捗コールバック関数

        Returns:
            ダウンロードした動画ファイルのパス（失敗時はNone）
        """
        try:
            # yt-dlpのオプション設定
            ydl_opts = {
                'format': 'best[ext=mp4]/best',  # MP4形式を優先
                'outtmpl': os.path.join(self.output_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'noplaylist': True,  # プレイリストではなく単一動画のみ
            }

            # 進捗表示用のフック
            if progress_callback:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        try:
                            percent = d.get('_percent_str', '0%').strip()
                            speed = d.get('_speed_str', 'N/A')
                            eta = d.get('_eta_str', 'N/A')
                            progress_callback(f"ダウンロード中: {percent} (速度: {speed}, 残り: {eta})")
                        except:
                            progress_callback("ダウンロード中...")
                    elif d['status'] == 'finished':
                        progress_callback("ダウンロード完了！処理中...")

                ydl_opts['progress_hooks'] = [progress_hook]

            # ダウンロード実行
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # 動画情報を取得
                info = ydl.extract_info(url, download=True)

                # ファイル名を取得
                filename = ydl.prepare_filename(info)

                # ファイルが存在するか確認
                if os.path.exists(filename):
                    return filename
                else:
                    # 拡張子が違う可能性があるので探す
                    base_name = os.path.splitext(filename)[0]
                    for ext in ['.mp4', '.webm', '.mkv']:
                        test_path = base_name + ext
                        if os.path.exists(test_path):
                            return test_path

            return None

        except Exception as e:
            if progress_callback:
                progress_callback(f"エラー: {str(e)}")
            raise e

    def get_video_info(self, url: str) -> Optional[dict]:
        """
        YouTube動画の情報を取得（ダウンロードせずに）

        Args:
            url: YouTubeのURL

        Returns:
            動画情報の辞書
        """
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'view_count': info.get('view_count', 0),
                    'description': info.get('description', '')
                }

        except Exception as e:
            st.error(f"動画情報の取得に失敗: {str(e)}")
            return None

    @staticmethod
    def is_valid_youtube_url(url: str) -> bool:
        """
        YouTubeの有効なURLかチェック

        Args:
            url: チェックするURL

        Returns:
            有効な場合True
        """
        youtube_domains = [
            'youtube.com',
            'www.youtube.com',
            'youtu.be',
            'm.youtube.com'
        ]

        url_lower = url.lower()
        return any(domain in url_lower for domain in youtube_domains)
