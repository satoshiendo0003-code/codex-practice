"""
Gemini API連携モジュール
動画分析とマニュアル生成を担当
"""
import google.generativeai as genai
import cv2
import os
import tempfile
from typing import Dict, List, Optional
import streamlit as st


class GeminiAnalyzer:
    """Gemini APIを使用して動画を分析するクラス"""

    def __init__(self, api_key: str):
        """
        Args:
            api_key: Google Gemini API Key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-flash')

    def extract_frames(self, video_path: str, num_frames: int = 10, save_persistent: bool = True) -> List[Dict]:
        """
        動画からフレームを抽出

        Args:
            video_path: 動画ファイルのパス
            num_frames: 抽出するフレーム数
            save_persistent: 永続的なディレクトリに保存するか

        Returns:
            抽出したフレーム情報のリスト [{"path": str, "index": int, "timestamp": float}]
        """
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        if total_frames == 0:
            raise ValueError("動画ファイルを読み込めませんでした")

        # フレーム間隔を計算
        interval = max(1, total_frames // num_frames)

        frame_data = []
        frame_count = 0

        # 保存ディレクトリを作成
        if save_persistent:
            output_dir = os.path.join("output", "frames")
            os.makedirs(output_dir, exist_ok=True)
            # タイムスタンプでサブディレクトリを作成
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_dir = os.path.join(output_dir, timestamp)
            os.makedirs(save_dir, exist_ok=True)
        else:
            save_dir = tempfile.mkdtemp()

        while cap.isOpened() and len(frame_data) < num_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_count % interval == 0:
                frame_index = len(frame_data)
                frame_path = os.path.join(save_dir, f"frame_{frame_index}.jpg")
                cv2.imwrite(frame_path, frame)

                # タイムスタンプを計算
                timestamp_sec = frame_count / fps if fps > 0 else 0

                frame_data.append({
                    "path": frame_path,
                    "index": frame_index,
                    "timestamp": timestamp_sec
                })

            frame_count += 1

        cap.release()
        return frame_data

    def analyze_video(
        self,
        video_path: str,
        target_audience: str = "歯科助手",
        manual_mode: str = "詳細"
    ) -> Dict:
        """
        動画を分析してマニュアルを生成

        Args:
            video_path: 動画ファイルのパス
            target_audience: 対象読者
            manual_mode: マニュアルモード（詳細/簡易）

        Returns:
            分析結果の辞書
        """
        # フレームを抽出（永続保存）
        with st.spinner("動画からフレームを抽出中..."):
            frame_data = self.extract_frames(video_path, num_frames=8, save_persistent=True)

        # Gemini APIで分析
        with st.spinner("AIが動画を分析中..."):
            # フレーム画像をアップロード
            uploaded_files = []
            for frame_info in frame_data:
                uploaded_file = genai.upload_file(frame_info["path"])
                uploaded_files.append(uploaded_file)

            # プロンプトを作成
            prompt = self._create_analysis_prompt(target_audience, manual_mode, len(frame_data))

            # Gemini APIを呼び出し
            response = self.model.generate_content(
                [prompt] + uploaded_files,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                )
            )

            # 結果をパース
            result = self._parse_response(response.text)

            # フレームパスを各ステップに割り当て
            result = self._attach_frames_to_steps(result, frame_data)

            return result

    def _create_analysis_prompt(self, target_audience: str, manual_mode: str, num_frames: int) -> str:
        """分析用のプロンプトを作成"""
        detail_level = "詳細に" if manual_mode == "詳細" else "簡潔に"

        return f"""
あなたは歯科医療の専門家です。提供された{num_frames}枚の動画フレーム（フレーム0〜{num_frames-1}）から、{target_audience}向けの作業マニュアルを{detail_level}作成してください。

以下の形式でJSON形式で回答してください：

{{
    "title": "マニュアルのタイトル",
    "summary": "マニュアルの概要（2-3文）",
    "steps": [
        {{
            "step_number": 1,
            "title": "ステップのタイトル",
            "description": "ステップの詳細な説明",
            "key_points": ["重要ポイント1", "重要ポイント2"],
            "warnings": ["注意事項1", "注意事項2"],
            "frame_index": 0
        }}
    ],
    "required_tools": ["必要な器具1", "必要な器具2"],
    "estimated_time": "推定所要時間"
}}

重要：
- 実際の動画内容を詳細に観察して、具体的な手順を抽出してください
- 各ステップに最も関連するフレーム番号（0〜{num_frames-1}）を"frame_index"として指定してください
- {target_audience}が理解しやすい言葉を使用してください
- 安全性と正確性を最優先してください
- 必ずJSON形式で回答してください
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Geminiのレスポンスをパースして構造化データに変換"""
        import json
        import re

        # JSONブロックを抽出
        json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(1)
        else:
            # JSONマーカーがない場合は全体をパース
            json_text = response_text

        try:
            result = json.loads(json_text)
            return result
        except json.JSONDecodeError:
            # パースに失敗した場合はデフォルト値を返す
            return {
                "title": "動画マニュアル",
                "summary": "動画から抽出された手順書です。",
                "steps": [
                    {
                        "step_number": 1,
                        "title": "手順1",
                        "description": response_text[:200],
                        "key_points": [],
                        "warnings": [],
                        "frame_index": 0
                    }
                ],
                "required_tools": [],
                "estimated_time": "不明"
            }

    def _attach_frames_to_steps(self, result: Dict, frame_data: List[Dict]) -> Dict:
        """各ステップにフレーム画像のパスを割り当て"""
        steps = result.get("steps", [])

        for step in steps:
            frame_index = step.get("frame_index", 0)

            # frame_indexが範囲内かチェック
            if 0 <= frame_index < len(frame_data):
                frame_info = frame_data[frame_index]
                step["image_path"] = frame_info["path"]
                step["timestamp"] = frame_info["timestamp"]
            else:
                # 範囲外の場合は最初のフレームを使用
                if frame_data:
                    step["image_path"] = frame_data[0]["path"]
                    step["timestamp"] = frame_data[0]["timestamp"]

        return result
