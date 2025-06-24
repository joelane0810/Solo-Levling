"""
Utility Functions for Level Up Application
Các hàm tiện ích dùng chung trong ứng dụng
"""

import json
import base64
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Currency and formatting utilities
def format_currency(amount: float) -> str:
    """Format currency for Vietnamese locale"""
    if amount >= 1000000000:
        return f"{amount / 1000000000:.1f}B"
    elif amount >= 1000000:
        return f"{amount / 1000000:.1f}M"
    elif amount >= 1000:
        return f"{amount / 1000:.1f}K"
    else:
        return f"{amount:,.0f}".replace(',', '.')

def format_datetime_vn(dt: datetime) -> str:
    """Format datetime for Vietnamese locale"""
    return dt.strftime("%d/%m/%Y %H:%M:%S")

def format_date_vn(dt: datetime) -> str:
    """Format date for Vietnamese locale"""
    return dt.strftime("%d/%m/%Y")

def format_time_vn(dt: datetime) -> str:
    """Format time for Vietnamese locale"""
    return dt.strftime("%H:%M")

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace"""
    return ' '.join(text.split()) if text else ""

# Age and date utilities
def calculate_age(birth_year: Optional[int]) -> Optional[int]:
    """Calculate current age from birth year"""
    if not birth_year:
        return None
    return datetime.now().year - birth_year

def get_age_display(birth_year: Optional[int]) -> str:
    """Get formatted age display"""
    age = calculate_age(birth_year)
    return f"{age} tuổi" if age else ""

def validate_birth_year(birth_year: int) -> bool:
    """Validate birth year"""
    current_year = datetime.now().year
    return 1900 <= birth_year <= current_year

# Resource calculation utilities
def calculate_resource_total(details: List[Dict]) -> float:
    """Calculate total value for a resource"""
    total = 0.0
    for detail in details:
        if detail.get('status') == 'active':
            amount = safe_float(detail.get('amount'))
            detail_type = detail.get('type', 'asset')
            
            if detail_type in ['asset', 'income', 'investment']:
                total += amount
            elif detail_type in ['loan', 'expense']:
                total -= amount
    
    return total

def calculate_quest_completion_rate(quests: List) -> float:
    """Calculate quest completion rate as percentage"""
    if not quests:
        return 0.0
    completed = len([q for q in quests if hasattr(q, 'status') and q.status == 'completed'])
    return (completed / len(quests)) * 100

def calculate_achievement_unlock_rate(achievements: List) -> float:
    """Calculate achievement unlock rate as percentage"""
    if not achievements:
        return 0.0
    unlocked = len([a for a in achievements if hasattr(a, 'unlocked') and a.unlocked])
    return (unlocked / len(achievements)) * 100

def get_high_priority_quests(quests: List) -> List:
    """Get list of high priority incomplete quests"""
    return [q for q in quests if hasattr(q, 'priority') and hasattr(q, 'status') and q.priority == 'high' and q.status != 'completed']

# Safe type conversion utilities
def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to int"""
    try:
        return int(value) if value else default
    except (ValueError, TypeError):
        return default

def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float"""
    try:
        return float(value) if value else default
    except (ValueError, TypeError):
        return default

def safe_bool(value: Any, default: bool = False) -> bool:
    """Safely convert value to bool"""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ['true', '1', 'yes', 'on']
    return bool(value) if value is not None else default

# JSON utilities
def parse_stats_json(stats_str: str) -> Dict[str, int]:
    """Parse stats JSON string safely"""
    try:
        stats = json.loads(stats_str) if stats_str else {}
        if not isinstance(stats, dict):
            return {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}
        
        # Ensure all required stats exist
        default_stats = {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}
        for stat in default_stats:
            if stat not in stats:
                stats[stat] = default_stats[stat]
            else:
                stats[stat] = safe_int(stats[stat], default_stats[stat])
        
        return stats
    except (json.JSONDecodeError, TypeError):
        return {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}

def save_json_file(data: Dict, file_path: str) -> bool:
    """Save data to JSON file safely"""
    try:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False

def load_json_file(file_path: str) -> Optional[Dict]:
    """Load data from JSON file safely"""
    try:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception:
        pass
    return None

# Image utilities
def encode_image_to_base64(image_path: str) -> Optional[str]:
    """Encode image file to base64 string"""
    try:
        with open(image_path, 'rb') as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            return f"data:image/png;base64,{encoded_string}"
    except Exception:
        return None

# URL validation utilities
def validate_url(url: str) -> bool:
    """Validate if string is a valid URL"""
    if not url:
        return False
    return url.startswith(('http://', 'https://'))

def validate_image_url(url: str) -> bool:
    """Validate if string is a valid image URL"""
    if not validate_url(url):
        return False
    
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')
    return any(url.lower().endswith(ext) for ext in image_extensions)

# Data validation utilities
def validate_quest_data(data: Dict) -> Dict:
    """Validate and clean quest data"""
    return {
        'id': safe_int(data.get('id')),
        'title': str(data.get('title', '')),
        'description': str(data.get('description', '')),
        'required_stat': data.get('required_stat', 'WILL') if data.get('required_stat') in ['WILL', 'PHY', 'MEN', 'AWR', 'EXE'] else 'WILL',
        'difficulty': max(1, min(5, safe_int(data.get('difficulty', 1)))),
        'deadline': str(data.get('deadline', '')),
        'reward_exp': safe_int(data.get('reward_exp')),
        'reward_stat': str(data.get('reward_stat', '')),
        'status': data.get('status', 'todo') if data.get('status') in ['todo', 'in-progress', 'completed'] else 'todo',
        'category': str(data.get('category', 'general')),
        'priority': data.get('priority', 'medium') if data.get('priority') in ['high', 'medium', 'low'] else 'medium'
    }

def validate_achievement_data(data: Dict) -> Dict:
    """Validate and clean achievement data"""
    return {
        'id': safe_int(data.get('id')),
        'title': str(data.get('title', '')),
        'description': str(data.get('description', '')),
        'icon': str(data.get('icon', '🏆')),
        'tier': data.get('tier', 'bronze') if data.get('tier') in ['bronze', 'silver', 'gold', 'legendary'] else 'bronze',
        'unlocked': safe_bool(data.get('unlocked')),
        'unlocked_date': str(data.get('unlocked_date', '')),
        'progress': max(0, min(100, safe_int(data.get('progress')))),
        'condition': str(data.get('condition', '')),
        'category': str(data.get('category', 'general'))
    }

def validate_resource_detail_data(data: Dict) -> Dict:
    """Validate and clean resource detail data"""
    return {
        'id': safe_int(data.get('id')),
        'name': str(data.get('name', '')),
        'amount': safe_float(data.get('amount')),
        'type': data.get('type', 'asset') if data.get('type') in ['asset', 'loan', 'investment', 'income', 'expense'] else 'asset',
        'notes': str(data.get('notes', '')),
        'date': str(data.get('date', datetime.now().strftime('%d/%m/%Y'))),
        'status': data.get('status', 'active') if data.get('status') in ['active', 'inactive'] else 'active'
    }

def validate_character_data(data: Dict) -> Dict:
    """Validate and clean character data"""
    return {
        'name': str(data.get('name', '')),
        'avatar': str(data.get('avatar', '')),
        'birth_year': safe_int(data.get('birth_year')) if data.get('birth_year') and validate_birth_year(safe_int(data.get('birth_year'))) else None,
        'level': max(1, safe_int(data.get('level', 1))),
        'exp': safe_int(data.get('exp')),
        'exp_to_next': max(1, safe_int(data.get('exp_to_next', 100))),
        'stats': data.get('stats', {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}) if isinstance(data.get('stats'), dict) else {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}
    }

# Default data creation utilities
def create_empty_character() -> Dict:
    """Create empty character with default values"""
    return {
        'name': '',
        'avatar': '',
        'birth_year': None,
        'level': 1,
        'exp': 0,
        'exp_to_next': 100,
        'stats': {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}
    }

def create_empty_quest() -> Dict:
    """Create empty quest with default values"""
    return {
        'id': 0,
        'title': '',
        'description': '',
        'required_stat': 'WILL',
        'difficulty': 1,
        'deadline': '',
        'reward_exp': 0,
        'reward_stat': '',
        'status': 'todo',
        'category': 'general',
        'priority': 'medium'
    }

def create_empty_achievement() -> Dict:
    """Create empty achievement with default values"""
    return {
        'id': 0,
        'title': '',
        'description': '',
        'icon': '🏆',
        'tier': 'bronze',
        'unlocked': False,
        'unlocked_date': '',
        'progress': 0,
        'condition': '',
        'category': 'general'
    }

def create_empty_resource_detail() -> Dict:
    """Create empty resource detail with default values"""
    return {
        'id': 0,
        'name': '',
        'amount': 0.0,
        'type': 'asset',
        'notes': '',
        'date': datetime.now().strftime('%d/%m/%Y'),
        'status': 'active'
    }

def get_default_resources() -> List[Dict]:
    """Get default resource configuration"""
    return [
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