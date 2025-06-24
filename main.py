import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials
import requests

# Import custom modules
from components.ui_components import *
from components.google_sheets import GoogleSheetsManager
from components.data_models import Character, Quest, Achievement, Resource
from components.renders import *
from utils.helpers import *

# Page config
st.set_page_config(
    page_title="Level Up - RPG Self-Development",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Apply custom CSS
apply_custom_css()

# Initialize session state
def initialize_session_state():
    defaults = {
        'active_tab': 'dashboard',
        'show_settings': False,
        'show_resource_modal': False,
        'show_character_modal': False,
        'show_chat': False,
        'selected_resource': None,
        'character': Character(),
        'quests': [],
        'achievements': [],
        'resources': [
            Resource("Xã hội", "👥", "from-blue-500 to-blue-600", "text-blue-400", "Xây dựng quan hệ, kết nối"),
            Resource("Tài chính", "💰", "from-green-500 to-green-600", "text-green-400", "Tiền bạc, đầu tư, tài sản"),
            Resource("Kiến tạo", "💡", "from-purple-500 to-purple-600", "text-purple-400", "Sáng tạo, kỹ năng, kiến thức"),
            Resource("Khám phá", "🧭", "from-orange-500 to-orange-600", "text-orange-400", "Trải nghiệm, học hỏi, chinh phục")
        ],
        'resource_details': {},
        'chat_messages': [],
        'goals': {'mission': '', 'yearly': [], 'quarterly': [], 'monthly': []},
        'settings': {
            'sheet_id': '',
            'api_key': '',
            'auto_sync': False,
            'sync_interval': 5
        },
        'connection_status': {'connected': False, 'tested': False, 'last_sync': None},
        'loading': False,
        'syncing': False,
        'error_message': None,
        'success_message': None,
        'sheets_manager': None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# Load settings from file
def load_settings():
    settings_file = Path("levelup_settings.json")
    if settings_file.exists():
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                saved_settings = json.load(f)
                st.session_state.settings.update(saved_settings)
        except Exception as e:
            st.session_state.error_message = f"Lỗi đọc cài đặt: {str(e)}"

# Save settings to file
def save_settings():
    try:
        settings_file = Path("levelup_settings.json")
        with open(settings_file, 'w', encoding='utf-8') as f:
            json.dump(st.session_state.settings, f, ensure_ascii=False, indent=2)
        st.session_state.success_message = "Cài đặt đã được lưu!"
    except Exception as e:
        st.session_state.error_message = f"Lỗi lưu cài đặt: {str(e)}"

# Main app logic
def main():
    initialize_session_state()
    load_settings()
    
    # Auto-connect if credentials exist
    if (st.session_state.settings['sheet_id'] and 
        st.session_state.settings['api_key'] and 
        not st.session_state.connection_status['tested']):
        test_connection()
    
    # Status messages
    display_status_messages()
    
    # Header
    render_header()
    
    # Main content based on active tab
    if st.session_state.show_settings:
        render_settings()
    else:
        if st.session_state.active_tab == 'dashboard':
            render_dashboard()
        elif st.session_state.active_tab == 'character':
            render_character()
        elif st.session_state.active_tab == 'quests':
            render_quests()
        elif st.session_state.active_tab == 'resources':
            render_resources()
        elif st.session_state.active_tab == 'achievements':
            render_achievements()
    
    # Bottom navigation
    render_bottom_navigation()
    
    # Modals
    if st.session_state.show_character_modal:
        render_character_modal()
    
    if st.session_state.show_resource_modal:
        render_resource_modal()
    
    if st.session_state.show_chat:
        render_chat_modal()
    
    # Auto-refresh for auto-sync
    if (st.session_state.settings['auto_sync'] and 
        st.session_state.connection_status['connected']):
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    main()