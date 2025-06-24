"""
Level Up - RPG Self-Development Configuration
Cấu hình toàn cục cho ứng dụng
"""

import os
from pathlib import Path
from typing import Dict, List

# Application Info
APP_NAME = "Level Up - RPG Self-Development"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Ứng dụng phát triển bản thân theo phong cách RPG"
APP_AUTHOR = "Level Up Team"

# File Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SETTINGS_FILE = BASE_DIR / "levelup_settings.json"
BACKUP_DIR = BASE_DIR / "backups"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

# Google Sheets Configuration
SHEETS_API_BASE_URL = "https://sheets.googleapis.com/v4/spreadsheets"
SHEET_RANGES = {
    'character': 'Character!A1:B25',
    'quests': 'Quests!A2:K1000',
    'achievements': 'Achievements!A2:I1000',
    'goals': 'Goals!A1:E100',
    'resources': 'Resources!A2:F10',
    'resource_details': 'ResourceDetails!A2:G1000',
    'chat': 'Chat!A2:E1000'
}

# Default Settings
DEFAULT_SETTINGS = {
    'sheet_id': '',
    'api_key': '',
    'auto_sync': False,
    'sync_interval': 5,  # minutes
    'theme': 'dark',
    'language': 'vi',
    'notifications': True,
    'backup_enabled': True,
    'backup_interval': 24  # hours
}

# Character Configuration
DEFAULT_CHARACTER = {
    'name': 'Hero',
    'avatar': '',
    'birth_year': None,
    'level': 1,
    'exp': 0,
    'exp_to_next': 100,
    'stats': {
        'WILL': 10,  # Ý chí
        'PHY': 10,   # Thể chất
        'MEN': 10,   # Tinh thần
        'AWR': 10,   # Nhận thức
        'EXE': 10    # Thực thi
    }
}

# Stat Configuration
STATS_CONFIG = {
    'WILL': {
        'name': 'Ý chí',
        'icon': '❤️',
        'color': 'red',
        'description': 'Quyết tâm, kiên trì, vượt qua khó khăn'
    },
    'PHY': {
        'name': 'Thể chất',
        'icon': '⚔️',
        'color': 'orange',
        'description': 'Sức khỏe, thể lực, năng lượng'
    },
    'MEN': {
        'name': 'Tinh thần',
        'icon': '🧠',
        'color': 'blue',
        'description': 'Tư duy, học hỏi, sáng tạo'
    },
    'AWR': {
        'name': 'Nhận thức',
        'icon': '👁️',
        'color': 'purple',
        'description': 'Quan sát, hiểu biết, nhạy bén'
    },
    'EXE': {
        'name': 'Thực thi',
        'icon': '⚡',
        'color': 'yellow',
        'description': 'Hành động, hoàn thành, hiệu quả'
    }
}

# Quest Configuration
QUEST_STATUSES = ['todo', 'in-progress', 'completed']
QUEST_PRIORITIES = ['low', 'medium', 'high']
QUEST_CATEGORIES = [
    'general', 'health', 'learning', 'work', 'finance', 
    'social', 'creative', 'spiritual', 'travel', 'hobby'
]

DIFFICULTY_CONFIG = {
    1: {'stars': '⭐', 'exp_range': (10, 20), 'label': 'Dễ'},
    2: {'stars': '⭐⭐', 'exp_range': (30, 40), 'label': 'Bình thường'},
    3: {'stars': '⭐⭐⭐', 'exp_range': (50, 70), 'label': 'Khó'},
    4: {'stars': '⭐⭐⭐⭐', 'exp_range': (80, 100), 'label': 'Rất khó'},
    5: {'stars': '⭐⭐⭐⭐⭐', 'exp_range': (100, 150), 'label': 'Cực khó'}
}

PRIORITY_CONFIG = {
    'high': {'color': '#EF4444', 'label': 'Cao', 'emoji': '🔴'},
    'medium': {'color': '#F59E0B', 'label': 'Trung bình', 'emoji': '🟡'},
    'low': {'color': '#6B7280', 'label': 'Thấp', 'emoji': '⚪'}
}

# Achievement Configuration
ACHIEVEMENT_TIERS = ['bronze', 'silver', 'gold', 'legendary']
ACHIEVEMENT_CATEGORIES = [
    'general', 'character', 'quests', 'resources', 'social', 
    'learning', 'milestone', 'special'
]

TIER_CONFIG = {
    'bronze': {
        'color': '#D97706',
        'emoji': '🥉',
        'label': 'Đồng',
        'description': 'Dễ đạt được'
    },
    'silver': {
        'color': '#6B7280',
        'emoji': '🥈',
        'label': 'Bạc',
        'description': 'Cần nỗ lực'
    },
    'gold': {
        'color': '#F59E0B',
        'emoji': '🥇',
        'label': 'Vàng',
        'description': 'Khó khăn'
    },
    'legendary': {
        'color': '#8B5CF6',
        'emoji': '👑',
        'label': 'Huyền thoại',
        'description': 'Cực kỳ hiếm'
    }
}

# Resource Configuration
DEFAULT_RESOURCES = [
    {
        'name': 'Xã hội',
        'icon': '👥',
        'color': 'from-blue-500 to-blue-600',
        'text_color': 'text-blue-400',
        'description': 'Xây dựng quan hệ, kết nối',
        'level': 1,
        'progress': 0,
        'next_milestone': '',
        'related_quests': 0
    },
    {
        'name': 'Tài chính',
        'icon': '💰',
        'color': 'from-green-500 to-green-600',
        'text_color': 'text-green-400',
        'description': 'Tiền bạc, đầu tư, tài sản',
        'level': 1,
        'progress': 0,
        'next_milestone': '',
        'related_quests': 0
    },
    {
        'name': 'Kiến tạo',
        'icon': '💡',
        'color': 'from-purple-500 to-purple-600',
        'text_color': 'text-purple-400',
        'description': 'Sáng tạo, kỹ năng, kiến thức',
        'level': 1,
        'progress': 0,
        'next_milestone': '',
        'related_quests': 0
    },
    {
        'name': 'Khám phá',
        'icon': '🧭',
        'color': 'from-orange-500 to-orange-600',
        'text_color': 'text-orange-400',
        'description': 'Trải nghiệm, học hỏi, chinh phục',
        'level': 1,
        'progress': 0,
        'next_milestone': '',
        'related_quests': 0
    }
]

RESOURCE_TYPES = ['asset', 'loan', 'investment', 'income', 'expense']

RESOURCE_TYPE_CONFIG = {
    'asset': {
        'icon': '💰',
        'color': '#22C55E',
        'label': 'Tài sản',
        'positive': True,
        'description': 'Những gì bạn sở hữu có giá trị'
    },
    'loan': {
        'icon': '📋',
        'color': '#F97316',
        'label': 'Khoản vay',
        'positive': False,
        'description': 'Số tiền bạn đang nợ'
    },
    'investment': {
        'icon': '📈',
        'color': '#3B82F6',
        'label': 'Đầu tư',
        'positive': True,
        'description': 'Tài sản đầu tư để sinh lời'
    },
    'income': {
        'icon': '💸',
        'color': '#10B981',
        'label': 'Thu nhập',
        'positive': True,
        'description': 'Nguồn thu nhập định kỳ'
    },
    'expense': {
        'icon': '💳',
        'color': '#EF4444',
        'label': 'Chi phí',
        'positive': False,
        'description': 'Chi tiêu và chi phí định kỳ'
    }
}

# Chat Configuration
CHAT_MESSAGE_TYPES = ['note', 'reminder', 'achievement']

MESSAGE_TYPE_CONFIG = {
    'note': {
        'icon': '💭',
        'color': '#9CA3AF',
        'label': 'Ghi chú',
        'description': 'Suy nghĩ cá nhân'
    },
    'reminder': {
        'icon': '⏰',
        'color': '#F59E0B',
        'label': 'Nhắc nhở',
        'description': 'Lời nhắc quan trọng'
    },
    'achievement': {
        'icon': '🎉',
        'color': '#22C55E',
        'label': 'Thành tựu',
        'description': 'Hoàn thành nhiệm vụ'
    }
}

# UI Configuration
THEME_CONFIG = {
    'dark': {
        'background': '#0f0f0f',
        'secondary_background': '#1a1a2e',
        'text_color': '#ffffff',
        'primary_color': '#3B82F6'
    },
    'light': {
        'background': '#ffffff',
        'secondary_background': '#f8fafc',
        'text_color': '#1f2937',
        'primary_color': '#2563EB'
    }
}

# Navigation Configuration
NAV_ITEMS = [
    {'id': 'dashboard', 'icon': '🏠', 'label': 'Trang chủ'},
    {'id': 'character', 'icon': '👤', 'label': 'Nhân vật'},
    {'id': 'quests', 'icon': '⚔️', 'label': 'Nhiệm vụ'},
    {'id': 'resources', 'icon': '💎', 'label': 'Nguồn vốn'},
    {'id': 'achievements', 'icon': '🏆', 'label': 'Danh hiệu'}
]

# Validation Rules
VALIDATION_RULES = {
    'character': {
        'name': {'min_length': 1, 'max_length': 50},
        'birth_year': {'min_value': 1900, 'max_value': 2025},
        'level': {'min_value': 1, 'max_value': 9999},
        'exp': {'min_value': 0, 'max_value': 999999},
        'stats': {'min_value': 1, 'max_value': 999}
    },
    'quest': {
        'title': {'min_length': 1, 'max_length': 200},
        'description': {'max_length': 1000},
        'difficulty': {'min_value': 1, 'max_value': 5},
        'reward_exp': {'min_value': 0, 'max_value': 9999}
    },
    'resource_detail': {
        'name': {'min_length': 1, 'max_length': 100},
        'amount': {'min_value': 0, 'max_value': 999999999999},
        'notes': {'max_length': 500}
    }
}

# Error Messages
ERROR_MESSAGES = {
    'connection_failed': 'Không thể kết nối với Google Sheets. Vui lòng kiểm tra cài đặt.',
    'invalid_api_key': 'API Key không hợp lệ hoặc không có quyền truy cập.',
    'sheet_not_found': 'Không tìm thấy Google Sheet với ID này.',
    'sync_failed': 'Đồng bộ dữ liệu thất bại. Vui lòng thử lại.',
    'validation_failed': 'Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.',
    'save_failed': 'Không thể lưu dữ liệu. Vui lòng thử lại.',
    'required_field': 'Trường này là bắt buộc.',
    'invalid_format': 'Định dạng dữ liệu không đúng.',
    'network_error': 'Lỗi kết nối mạng. Vui lòng kiểm tra internet.'
}

# Success Messages
SUCCESS_MESSAGES = {
    'connection_success': 'Kết nối Google Sheets thành công!',
    'sync_success': 'Đồng bộ dữ liệu thành công!',
    'save_success': 'Lưu dữ liệu thành công!',
    'quest_completed': 'Hoàn thành nhiệm vụ thành công!',
    'level_up': 'Chúc mừng! Bạn đã lên level!',
    'achievement_unlocked': 'Mở khóa danh hiệu mới!',
    'settings_saved': 'Cài đặt đã được lưu!',
    'data_updated': 'Cập nhật dữ liệu thành công!'
}

# Environment Variables
def get_env_var(key: str, default: str = '') -> str:
    """Get environment variable with fallback"""
    return os.getenv(key, default)

# Development Configuration
DEBUG = get_env_var('LEVELUP_DEBUG', 'False').lower() == 'true'
LOG_LEVEL = get_env_var('LEVELUP_LOG_LEVEL', 'INFO')
CACHE_TTL = int(get_env_var('LEVELUP_CACHE_TTL', '300'))  # 5 minutes

# Production Configuration
PRODUCTION = get_env_var('LEVELUP_ENV', 'development') == 'production'
MAX_REQUESTS_PER_MINUTE = int(get_env_var('LEVELUP_MAX_REQUESTS', '60'))
REQUEST_TIMEOUT = int(get_env_var('LEVELUP_TIMEOUT', '30'))

# Feature Flags
FEATURES = {
    'auto_backup': get_env_var('LEVELUP_AUTO_BACKUP', 'True').lower() == 'true',
    'notifications': get_env_var('LEVELUP_NOTIFICATIONS', 'True').lower() == 'true',
    'analytics': get_env_var('LEVELUP_ANALYTICS', 'False').lower() == 'true',
    'beta_features': get_env_var('LEVELUP_BETA', 'False').lower() == 'true'
}