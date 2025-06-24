import gspread
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class GoogleSheetsManager:
    """Manager for Google Sheets integration"""
    
    def __init__(self, sheet_id: str, api_key: str):
        self.sheet_id = sheet_id
        self.api_key = api_key
        self.base_url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}"
        
        # Sheet ranges
        self.ranges = {
            'character': 'Character!A1:B25',
            'quests': 'Quests!A2:K1000',
            'achievements': 'Achievements!A2:I1000',
            'goals': 'Goals!A1:E100',
            'resources': 'Resources!A2:F10',
            'resource_details': 'ResourceDetails!A2:G1000',
            'chat': 'Chat!A2:E1000'
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict:
        """Make HTTP request to Google Sheets API"""
        url = f"{self.base_url}{endpoint}?key={self.api_key}"
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            if response.status_code == 403:
                raise Exception("API Key không hợp lệ hoặc không có quyền truy cập")
            elif response.status_code == 404:
                raise Exception("Không tìm thấy Google Sheet với ID này")
            else:
                raise Exception(f"Lỗi kết nối: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test connection to Google Sheets"""
        try:
            self._make_request("")
            return True
        except Exception as e:
            raise e
    
    def read_range(self, range_name: str) -> List[List[str]]:
        """Read data from a specific range"""
        try:
            endpoint = f"/values/{range_name}"
            response = self._make_request(endpoint)
            return response.get('values', [])
        except Exception as e:
            print(f"Warning: Could not read range {range_name}: {str(e)}")
            return []
    
    def write_range(self, range_name: str, values: List[List[str]]) -> bool:
        """Write data to a specific range"""
        try:
            endpoint = f"/values/{range_name}?valueInputOption=RAW"
            data = {'values': values}
            self._make_request(endpoint, method='PUT', data=data)
            return True
        except Exception as e:
            raise Exception(f"Lỗi ghi dữ liệu: {str(e)}")
    
    def append_row(self, range_name: str, values: List[str]) -> bool:
        """Append a row to a sheet"""
        try:
            endpoint = f"/values/{range_name}:append?valueInputOption=RAW"
            data = {'values': [values]}
            self._make_request(endpoint, method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Lỗi thêm dữ liệu: {str(e)}")
    
    def read_character(self) -> Optional[Dict]:
        """Read character data from sheet"""
        try:
            data = self.read_range(self.ranges['character'])
            if not data:
                return None
            
            character = {
                'name': '',
                'avatar': '',
                'birth_year': None,
                'level': 1,
                'exp': 0,
                'exp_to_next': 100,
                'stats': {'WILL': 10, 'PHY': 10, 'MEN': 10, 'AWR': 10, 'EXE': 10}
            }
            
            for row in data:
                if len(row) >= 2:
                    key, value = row[0], row[1]
                    
                    if key == 'name':
                        character['name'] = value
                    elif key == 'avatar':
                        character['avatar'] = value
                    elif key == 'birthYear':
                        try:
                            character['birth_year'] = int(value) if value else None
                        except ValueError:
                            character['birth_year'] = None
                    elif key in ['level', 'exp', 'expToNext']:
                        try:
                            character[key.replace('expToNext', 'exp_to_next')] = int(value)
                        except ValueError:
                            pass
                    elif key == 'stats':
                        try:
                            character['stats'] = json.loads(value) if value else character['stats']
                        except json.JSONDecodeError:
                            pass
            
            return character
            
        except Exception as e:
            print(f"Warning: Could not read character data: {str(e)}")
            return None
    
    def update_character(self, character) -> bool:
        """Update character data in sheet"""
        try:
            values = [
                ['name', character.name],
                ['avatar', character.avatar],
                ['birthYear', str(character.birth_year) if character.birth_year else ''],
                ['level', str(character.level)],
                ['exp', str(character.exp)],
                ['expToNext', str(character.exp_to_next)],
                ['stats', json.dumps(character.stats)]
            ]
            return self.write_range('Character!A1:B7', values)
        except Exception as e:
            raise Exception(f"Lỗi cập nhật nhân vật: {str(e)}")
    
    def read_quests(self) -> List[Dict]:
        """Read quests data from sheet"""
        try:
            data = self.read_range(self.ranges['quests'])
            quests = []
            
            for i, row in enumerate(data):
                if len(row) > 0 and row[0]:  # Skip empty rows
                    quest = {
                        'id': i + 1,
                        'title': row[0] if len(row) > 0 else '',
                        'description': row[1] if len(row) > 1 else '',
                        'required_stat': row[2] if len(row) > 2 else 'WILL',
                        'difficulty': max(1, min(5, int(row[3]) if len(row) > 3 and row[3].isdigit() else 1)),
                        'deadline': row[4] if len(row) > 4 else '',
                        'reward_exp': int(row[5]) if len(row) > 5 and row[5].isdigit() else 0,
                        'reward_stat': row[6] if len(row) > 6 else '',
                        'status': row[7] if len(row) > 7 and row[7] in ['todo', 'in-progress', 'completed'] else 'todo',
                        'category': row[8] if len(row) > 8 else 'general',
                        'priority': row[9] if len(row) > 9 and row[9] in ['high', 'medium', 'low'] else 'medium'
                    }
                    quests.append(quest)
            
            return quests
            
        except Exception as e:
            print(f"Warning: Could not read quests: {str(e)}")
            return []
    
    def update_quest(self, quest) -> bool:
        """Update a specific quest in sheet"""
        try:
            # Find quest row and update
            quest_row = [
                quest.title, quest.description, quest.required_stat,
                str(quest.difficulty), quest.deadline, str(quest.reward_exp),
                quest.reward_stat, quest.status, quest.category, quest.priority
            ]
            
            range_name = f"Quests!A{quest.id + 1}:J{quest.id + 1}"
            return self.write_range(range_name, [quest_row])
            
        except Exception as e:
            raise Exception(f"Lỗi cập nhật nhiệm vụ: {str(e)}")
    
    def read_achievements(self) -> List[Dict]:
        """Read achievements data from sheet"""
        try:
            data = self.read_range(self.ranges['achievements'])
            achievements = []
            
            for i, row in enumerate(data):
                if len(row) > 0 and row[0]:  # Skip empty rows
                    achievement = {
                        'id': i + 1,
                        'title': row[0] if len(row) > 0 else '',
                        'description': row[1] if len(row) > 1 else '',
                        'icon': row[2] if len(row) > 2 else '🏆',
                        'tier': row[3] if len(row) > 3 and row[3] in ['bronze', 'silver', 'gold', 'legendary'] else 'bronze',
                        'unlocked': row[4] in ['TRUE', 'true', True] if len(row) > 4 else False,
                        'unlocked_date': row[5] if len(row) > 5 else '',
                        'progress': max(0, min(100, int(row[6]) if len(row) > 6 and row[6].isdigit() else 0)),
                        'condition': row[7] if len(row) > 7 else '',
                        'category': row[8] if len(row) > 8 else 'general'
                    }
                    achievements.append(achievement)
            
            return achievements
            
        except Exception as e:
            print(f"Warning: Could not read achievements: {str(e)}")
            return []
    
    def read_resources(self) -> List[Dict]:
        """Read resources data from sheet"""
        try:
            data = self.read_range(self.ranges['resources'])
            resources = []
            
            for row in data:
                if len(row) > 0 and row[0]:
                    resource = {
                        'name': row[0],
                        'level': max(1, int(row[1]) if len(row) > 1 and row[1].isdigit() else 1),
                        'progress': max(0, min(100, int(row[2]) if len(row) > 2 and row[2].isdigit() else 0)),
                        'next_milestone': row[3] if len(row) > 3 else '',
                        'related_quests': int(row[4]) if len(row) > 4 and row[4].isdigit() else 0
                    }
                    resources.append(resource)
            
            return resources
            
        except Exception as e:
            print(f"Warning: Could not read resources: {str(e)}")
            return []
    
    def read_resource_details(self) -> Dict[str, List[Dict]]:
        """Read resource details data from sheet"""
        try:
            data = self.read_range(self.ranges['resource_details'])
            details = {}
            
            for i, row in enumerate(data):
                if len(row) > 0 and row[0]:
                    resource_name = row[0]
                    if resource_name not in details:
                        details[resource_name] = []
                    
                    detail = {
                        'id': i + 1,
                        'name': row[1] if len(row) > 1 else '',
                        'amount': float(row[2]) if len(row) > 2 and row[2].replace('.', '').isdigit() else 0,
                        'type': row[3] if len(row) > 3 and row[3] in ['asset', 'loan', 'investment', 'income', 'expense'] else 'asset',
                        'notes': row[4] if len(row) > 4 else '',
                        'date': row[5] if len(row) > 5 else datetime.now().strftime('%d/%m/%Y'),
                        'status': row[6] if len(row) > 6 else 'active'
                    }
                    details[resource_name].append(detail)
            
            return details
            
        except Exception as e:
            print(f"Warning: Could not read resource details: {str(e)}")
            return {}
    
    def add_resource_detail(self, resource_name: str, detail: Dict) -> bool:
        """Add a new resource detail"""
        try:
            values = [
                resource_name,
                detail['name'],
                str(detail['amount']),
                detail['type'],
                detail['notes'],
                detail['date'],
                detail['status']
            ]
            return self.append_row('ResourceDetails!A:G', values)
        except Exception as e:
            raise Exception(f"Lỗi thêm chi tiết: {str(e)}")
    
    def read_chat(self) -> List[Dict]:
        """Read chat messages from sheet"""
        try:
            data = self.read_range(self.ranges['chat'])
            messages = []
            
            for i, row in enumerate(data):
                if len(row) > 0 and row[0]:
                    message = {
                        'id': i + 1,
                        'text': row[0],
                        'timestamp': row[1] if len(row) > 1 else '',
                        'type': row[2] if len(row) > 2 and row[2] in ['note', 'reminder', 'achievement'] else 'note',
                        'date': row[3] if len(row) > 3 else '',
                        'author': row[4] if len(row) > 4 else 'user'
                    }
                    messages.append(message)
            
            # Sort by date and time
            messages.sort(key=lambda x: (x['date'], x['timestamp']))
            return messages
            
        except Exception as e:
            print(f"Warning: Could not read chat: {str(e)}")
            return []
    
    def add_chat_message(self, message: Dict) -> bool:
        """Add a new chat message"""
        try:
            values = [
                message['text'],
                message['timestamp'],
                message['type'],
                message['date'],
                message['author']
            ]
            return self.append_row('Chat!A:E', values)
        except Exception as e:
            raise Exception(f"Lỗi thêm tin nhắn: {str(e)}")
    
    def read_goals(self) -> Optional[Dict]:
        """Read goals data from sheet"""
        try:
            data = self.read_range(self.ranges['goals'])
            goals = {
                'mission': '',
                'yearly': [],
                'quarterly': [],
                'monthly': []
            }
            
            for row in data:
                if len(row) >= 2:
                    goal_type = row[0]
                    title = row[1]
                    
                    if goal_type == 'mission' and title:
                        goals['mission'] = title
                    elif goal_type in ['yearly', 'quarterly', 'monthly'] and title:
                        goal = {
                            'title': title,
                            'progress': max(0, min(100, int(row[2]) if len(row) > 2 and row[2].isdigit() else 0)),
                            'deadline': row[3] if len(row) > 3 else '',
                            'category': row[4] if len(row) > 4 else 'general'
                        }
                        goals[goal_type].append(goal)
            
            return goals
            
        except Exception as e:
            print(f"Warning: Could not read goals: {str(e)}")
            return None