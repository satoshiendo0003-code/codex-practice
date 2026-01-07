"""
状態管理モジュール
"""
import streamlit as st
from typing import Optional, Dict, List, Any

class AppState:
    # Keys
    KEY_API_KEY = 'api_key'
    KEY_API_KEY_VALID = 'api_key_valid'
    KEY_VIDEO_PATH = 'video_path'
    KEY_SOURCE_TYPE = 'source_type'
    KEY_ANALYSIS_RESULT = 'analysis_result'
    KEY_ANALYSIS_SUMMARY = 'analysis_summary'
    KEY_ANALYSIS_TRANSCRIPTION = 'analysis_transcription'
    KEY_IMAGE_PATHS = 'image_paths'
    KEY_MANUAL_TITLE = 'manual_title'
    KEY_TARGET_AUDIENCE = 'target_audience_input'

    @staticmethod
    def initialize():
        """セッション状態の初期化"""
        defaults = {
            AppState.KEY_VIDEO_PATH: None,
            AppState.KEY_API_KEY_VALID: False,
            AppState.KEY_ANALYSIS_RESULT: None,
            AppState.KEY_IMAGE_PATHS: {},
            AppState.KEY_MANUAL_TITLE: "新規マニュアル",
        }
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    @property
    def video_path(self) -> Optional[str]:
        return st.session_state.get(self.KEY_VIDEO_PATH)

    @video_path.setter
    def video_path(self, value: Optional[str]):
        st.session_state[self.KEY_VIDEO_PATH] = value

    @property
    def analysis_result(self) -> Optional[Dict]:
        return st.session_state.get(self.KEY_ANALYSIS_RESULT)

    @analysis_result.setter
    def analysis_result(self, value: Optional[Dict]):
        st.session_state[self.KEY_ANALYSIS_RESULT] = value

    @property
    def image_paths(self) -> Dict:
        return st.session_state.get(self.KEY_IMAGE_PATHS, {})

    @image_paths.setter
    def image_paths(self, value: Dict):
        st.session_state[self.KEY_IMAGE_PATHS] = value

    def to_dict(self) -> Dict[str, Any]:
        """状態を辞書に変換"""
        return {
            'video_path': self.video_path,
            'analysis_result': self.analysis_result,
            'image_paths': self.image_paths,
            'manual_title': st.session_state.get(self.KEY_MANUAL_TITLE),
        }

    def from_dict(self, data: Dict[str, Any]):
        """辞書から状態を復元"""
        if 'video_path' in data:
            self.video_path = data['video_path']
        if 'analysis_result' in data:
            self.analysis_result = data['analysis_result']
        if 'image_paths' in data:
            self.image_paths = data['image_paths']
        if 'manual_title' in data:
            st.session_state[self.KEY_MANUAL_TITLE] = data['manual_title']

    def save_to_disk(self):
        """状態をディスクに保存"""
        import json
        import os
        state_dir = "state"
        os.makedirs(state_dir, exist_ok=True)
        file_path = os.path.join(state_dir, "manual_state.json")
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save state: {e}")

    def load_from_disk(self) -> bool:
        """ディスクから状態を読み込み"""
        import json
        import os
        file_path = os.path.join("state", "manual_state.json")
        if not os.path.exists(file_path):
            return False
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.from_dict(data)
            return True
        except Exception as e:
            return False

app_state = AppState()
