from dataclasses import dataclass, field
from typing import Dict, Optional, List
from datetime import datetime

@dataclass
class Character:
    """Character data model"""
    name: str = ""
    avatar: str = ""
    birth_year: Optional[int] = None
    level: int = 1
    exp: int = 0
    exp_to_next: int = 100
    stats: Dict[str, int] = field(default_factory=lambda: {
        'WILL': 10,  # Ý chí
        'PHY': 10,   # Thể chất
        'MEN': 10,   # Tinh thần
        'AWR': 10,   # Nhận thức
        'EXE': 10    # Thực thi
    })
    
    def update_from_dict(self, data: Dict):
        """Update character from dictionary data"""
        if 'name' in data:
            self.name = data['name']
        if 'avatar' in data:
            self.avatar = data['avatar']
        if 'birth_year' in data:
            self.birth_year = data['birth_year']
        if 'level' in data:
            self.level = data['level']
        if 'exp' in data:
            self.exp = data['exp']
        if 'exp_to_next' in data:
            self.exp_to_next = data['exp_to_next']
        if 'stats' in data:
            self.stats.update(data['stats'])
    
    def get_age(self) -> Optional[int]:
        """Calculate current age"""
        if not self.birth_year:
            return None
        return datetime.now().year - self.birth_year
    
    def get_age_display(self) -> str:
        """Get formatted age display"""
        age = self.get_age()
        return f"{age} tuổi" if age else ""

@dataclass
class Quest:
    """Quest data model"""
    id: int = 0
    title: str = ""
    description: str = ""
    required_stat: str = "WILL"
    difficulty: int = 1  # 1-5 stars
    deadline: str = ""
    reward_exp: int = 0
    reward_stat: str = ""
    status: str = "todo"  # todo, in-progress, completed
    category: str = "general"
    priority: str = "medium"  # high, medium, low
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Quest':
        """Create Quest from dictionary"""
        return cls(
            id=data.get('id', 0),
            title=data.get('title', ''),
            description=data.get('description', ''),
            required_stat=data.get('required_stat', 'WILL'),
            difficulty=max(1, min(5, data.get('difficulty', 1))),
            deadline=data.get('deadline', ''),
            reward_exp=data.get('reward_exp', 0),
            reward_stat=data.get('reward_stat', ''),
            status=data.get('status', 'todo'),
            category=data.get('category', 'general'),
            priority=data.get('priority', 'medium')
        )
    
    def get_difficulty_stars(self) -> str:
        """Get difficulty as star string"""
        return "⭐" * self.difficulty
    
    def get_priority_color(self) -> str:
        """Get color for priority indicator"""
        colors = {
            'high': '#EF4444',
            'medium': '#F59E0B',
            'low': '#6B7280'
        }
        return colors.get(self.priority, '#6B7280')
    
    def get_status_color(self) -> str:
        """Get gradient color for status"""
        colors = {
            'completed': 'from-green-500 to-green-600',
            'in-progress': 'from-blue-500 to-blue-600',
            'todo': 'from-gray-500 to-gray-600'
        }
        return colors.get(self.status, 'from-gray-500 to-gray-600')
    
    def is_high_priority(self) -> bool:
        """Check if quest is high priority"""
        return self.priority == 'high'
    
    def is_completed(self) -> bool:
        """Check if quest is completed"""
        return self.status == 'completed'

@dataclass
class Achievement:
    """Achievement data model"""
    id: int = 0
    title: str = ""
    description: str = ""
    icon: str = "🏆"
    tier: str = "bronze"  # bronze, silver, gold, legendary
    unlocked: bool = False
    unlocked_date: str = ""
    progress: int = 0  # 0-100
    condition: str = ""
    category: str = "general"
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Achievement':
        """Create Achievement from dictionary"""
        return cls(
            id=data.get('id', 0),
            title=data.get('title', ''),
            description=data.get('description', ''),
            icon=data.get('icon', '🏆'),
            tier=data.get('tier', 'bronze'),
            unlocked=data.get('unlocked', False),
            unlocked_date=data.get('unlocked_date', ''),
            progress=max(0, min(100, data.get('progress', 0))),
            condition=data.get('condition', ''),
            category=data.get('category', 'general')
        )
    
    def get_tier_color(self) -> str:
        """Get color for achievement tier"""
        colors = {
            'bronze': '#D97706',
            'silver': '#6B7280',
            'gold': '#F59E0B',
            'legendary': '#8B5CF6'
        }
        return colors.get(self.tier, '#6B7280')
    
    def get_tier_emoji(self) -> str:
        """Get emoji for achievement tier"""
        emojis = {
            'bronze': '🥉',
            'silver': '🥈',
            'gold': '🥇',
            'legendary': '👑'
        }
        return emojis.get(self.tier, '🏆')

@dataclass
class Resource:
    """Resource data model"""
    name: str = ""
    icon: str = "💎"
    color: str = "from-blue-500 to-blue-600"
    text_color: str = "text-blue-400"
    description: str = ""
    level: int = 1
    progress: int = 0  # 0-100
    next_milestone: str = ""
    related_quests: int = 0
    
    def update_from_dict(self, data: Dict):
        """Update resource from dictionary data"""
        if 'level' in data:
            self.level = data['level']
        if 'progress' in data:
            self.progress = data['progress']
        if 'next_milestone' in data:
            self.next_milestone = data['next_milestone']
        if 'related_quests' in data:
            self.related_quests = data['related_quests']

@dataclass
class ResourceDetail:
    """Resource detail data model"""
    id: int = 0
    name: str = ""
    amount: float = 0.0
    type: str = "asset"  # asset, loan, investment, income, expense
    notes: str = ""
    date: str = ""
    status: str = "active"
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ResourceDetail':
        """Create ResourceDetail from dictionary"""
        return cls(
            id=data.get('id', 0),
            name=data.get('name', ''),
            amount=data.get('amount', 0.0),
            type=data.get('type', 'asset'),
            notes=data.get('notes', ''),
            date=data.get('date', ''),
            status=data.get('status', 'active')
        )
    
    def get_type_icon(self) -> str:
        """Get icon for resource type"""
        icons = {
            'asset': '💰',
            'loan': '📋',
            'investment': '📈',
            'income': '💸',
            'expense': '💳'
        }
        return icons.get(self.type, '💰')
    
    def get_type_color(self) -> str:
        """Get color for resource type"""
        colors = {
            'asset': '#22C55E',
            'loan': '#F97316',
            'investment': '#3B82F6',
            'income': '#10B981',
            'expense': '#EF4444'
        }
        return colors.get(self.type, '#22C55E')
    
    def get_type_label(self) -> str:
        """Get Vietnamese label for resource type"""
        labels = {
            'asset': 'Tài sản',
            'loan': 'Khoản vay',
            'investment': 'Đầu tư',
            'income': 'Thu nhập',
            'expense': 'Chi phí'
        }
        return labels.get(self.type, 'Tài sản')
    
    def is_positive(self) -> bool:
        """Check if this detail adds to total value"""
        return self.type in ['asset', 'income', 'investment']
    
    def get_contribution(self) -> float:
        """Get contribution to total (positive or negative)"""
        if self.is_positive():
            return self.amount
        else:
            return -self.amount

@dataclass
class Goal:
    """Goal data model"""
    title: str = ""
    progress: int = 0  # 0-100
    deadline: str = ""
    category: str = "general"
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Goal':
        """Create Goal from dictionary"""
        return cls(
            title=data.get('title', ''),
            progress=max(0, min(100, data.get('progress', 0))),
            deadline=data.get('deadline', ''),
            category=data.get('category', 'general')
        )

@dataclass
class ChatMessage:
    """Chat message data model"""
    id: int = 0
    text: str = ""
    timestamp: str = ""
    type: str = "note"  # note, reminder, achievement
    date: str = ""
    author: str = "user"
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ChatMessage':
        """Create ChatMessage from dictionary"""
        return cls(
            id=data.get('id', 0),
            text=data.get('text', ''),
            timestamp=data.get('timestamp', ''),
            type=data.get('type', 'note'),
            date=data.get('date', ''),
            author=data.get('author', 'user')
        )
    
    def get_type_icon(self) -> str:
        """Get icon for message type"""
        icons = {
            'note': '💭',
            'reminder': '⏰',
            'achievement': '🎉'
        }
        return icons.get(self.type, '💭')
    
    def get_formatted_datetime(self) -> str:
        """Get formatted date and time"""
        return f"{self.date} {self.timestamp}"

# Utility functions for data processing
def calculate_resource_total(details: List[ResourceDetail]) -> float:
    """Calculate total value for a resource"""
    total = 0.0
    for detail in details:
        if detail.status == 'active':
            total += detail.get_contribution()
    return total

def get_completed_quests_count(quests: List[Quest]) -> int:
    """Get count of completed quests"""
    return len([q for q in quests if q.is_completed()])

def get_unlocked_achievements_count(achievements: List[Achievement]) -> int:
    """Get count of unlocked achievements"""
    return len([a for a in achievements if a.unlocked])

def get_high_priority_quests(quests: List[Quest]) -> List[Quest]:
    """Get list of high priority incomplete quests"""
    return [q for q in quests if q.is_high_priority() and not q.is_completed()]

def get_quest_completion_rate(quests: List[Quest]) -> float:
    """Get quest completion rate as percentage"""
    if not quests:
        return 0.0
    completed = get_completed_quests_count(quests)
    return (completed / len(quests)) * 100

def get_achievement_unlock_rate(achievements: List[Achievement]) -> float:
    """Get achievement unlock rate as percentage"""
    if not achievements:
        return 0.0
    unlocked = get_unlocked_achievements_count(achievements)
    return (unlocked / len(achievements)) * 100