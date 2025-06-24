import streamlit as st
import base64
from datetime import datetime
from pathlib import Path
from PIL import Image
import io

def apply_custom_css():
    """Apply custom CSS for dark theme and styling"""
    st.markdown("""
    <style>
        /* Hide Streamlit default elements */
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        
        /* Dark theme */
        .stApp {
            background: linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #0f0f0f 100%);
            color: white;
        }
        
        /* Header styling */
        .header-container {
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(75, 85, 99, 0.5);
            padding: 1rem;
            margin: -1rem -1rem 2rem -1rem;
            border-radius: 0 0 1rem 1rem;
        }
        
        .header-title {
            background: linear-gradient(90deg, #60A5FA, #A855F7);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 1.5rem;
            font-weight: bold;
            margin: 0;
        }
        
        /* Card styling */
        .card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(75, 85, 99, 0.5);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(8px);
        }
        
        .gradient-card {
            background: linear-gradient(135deg, rgba(79, 70, 229, 0.3) 0%, rgba(139, 92, 246, 0.3) 100%);
            border: 1px solid rgba(99, 102, 241, 0.2);
        }
        
        /* Navigation styling */
        .nav-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(12px);
            border-top: 1px solid rgba(75, 85, 99, 0.5);
            padding: 1rem;
            z-index: 1000;
        }
        
        .nav-button {
            background: transparent;
            border: none;
            color: #9CA3AF;
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            cursor: pointer;
            text-align: center;
            min-width: 80px;
        }
        
        .nav-button:hover {
            background: rgba(75, 85, 99, 0.5);
            color: white;
        }
        
        .nav-button.active {
            background: #2563EB;
            color: white;
        }
        
        /* Progress bar styling */
        .progress-bar {
            background: rgba(75, 85, 99, 0.5);
            border-radius: 1rem;
            height: 12px;
            overflow: hidden;
        }
        
        .progress-fill {
            background: linear-gradient(90deg, #3B82F6, #8B5CF6);
            height: 100%;
            border-radius: 1rem;
            transition: width 0.7s ease;
        }
        
        /* Status indicators */
        .status-success {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.5);
            color: #22C55E;
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            margin: 1rem 0;
        }
        
        .status-error {
            background: rgba(239, 68, 68, 0.2);
            border: 1px solid rgba(239, 68, 68, 0.5);
            color: #EF4444;
            padding: 0.75rem 1rem;
            border-radius: 1rem;
            margin: 1rem 0;
        }
        
        /* Connection indicator */
        .connection-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 1rem;
            font-size: 0.75rem;
        }
        
        .connection-connected {
            background: rgba(34, 197, 94, 0.2);
            color: #22C55E;
        }
        
        .connection-error {
            background: rgba(239, 68, 68, 0.2);
            color: #EF4444;
        }
        
        .connection-unknown {
            background: rgba(75, 85, 99, 0.2);
            color: #9CA3AF;
        }
        
        /* Stat boxes */
        .stat-box {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 1rem;
            padding: 1rem;
            text-align: center;
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Quest cards */
        .quest-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(75, 85, 99, 0.3);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        
        .quest-card.completed {
            border-top: 4px solid #22C55E;
        }
        
        .quest-card.in-progress {
            border-top: 4px solid #3B82F6;
        }
        
        .quest-card.todo {
            border-top: 4px solid #6B7280;
        }
        
        /* Resource cards */
        .resource-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(75, 85, 99, 0.5);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            backdrop-filter: blur(8px);
        }
        
        /* Modal styling */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.7);
            z-index: 2000;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
        }
        
        .modal-content {
            background: rgba(17, 24, 39, 0.95);
            border: 1px solid rgba(75, 85, 99, 0.5);
            border-radius: 1.5rem;
            width: 100%;
            max-width: 500px;
            max-height: 90vh;
            overflow-y: auto;
            backdrop-filter: blur(12px);
        }
        
        /* Avatar styling */
        .avatar-container {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            font-size: 3rem;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        /* Empty state styling */
        .empty-state {
            text-align: center;
            padding: 3rem 1rem;
            color: #9CA3AF;
        }
        
        .empty-state h3 {
            color: #D1D5DB;
            margin-bottom: 0.5rem;
        }
        
        /* Floating action button */
        .fab {
            position: fixed;
            bottom: 120px;
            right: 1.5rem;
            width: 64px;
            height: 64px;
            background: linear-gradient(135deg, #3B82F6, #8B5CF6);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
            cursor: pointer;
            border: 2px solid rgba(255, 255, 255, 0.1);
            z-index: 1000;
        }
        
        .fab:hover {
            transform: scale(1.1);
            box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
        }
        
        /* Button styles */
        .btn-primary {
            background: #2563EB;
            color: white;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 1rem;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;
        }
        
        .btn-primary:hover {
            background: #1D4ED8;
            transform: translateY(-1px);
        }
        
        .btn-success {
            background: rgba(34, 197, 94, 0.2);
            color: #22C55E;
            border: 1px solid rgba(34, 197, 94, 0.3);
            padding: 0.75rem 1.5rem;
            border-radius: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .btn-success:hover {
            background: rgba(34, 197, 94, 0.3);
        }
        
        /* Achievement styling */
        .achievement-card {
            background: rgba(17, 24, 39, 0.8);
            border: 1px solid rgba(75, 85, 99, 0.5);
            border-radius: 1.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .achievement-card.unlocked {
            border: 1px solid rgba(251, 191, 36, 0.3);
            box-shadow: 0 0 20px rgba(251, 191, 36, 0.1);
        }
        
        .achievement-card.locked {
            opacity: 0.7;
            filter: grayscale(50%);
        }
        
        /* Tier colors */
        .tier-bronze { color: #D97706; }
        .tier-silver { color: #6B7280; }
        .tier-gold { color: #F59E0B; }
        .tier-legendary { color: #8B5CF6; }
        
        /* Priority indicators */
        .priority-high { background: #EF4444; }
        .priority-medium { background: #F59E0B; }
        .priority-low { background: #6B7280; }
        
        /* Resource type colors */
        .type-asset { color: #22C55E; }
        .type-loan { color: #F97316; }
        .type-investment { color: #3B82F6; }
        .type-income { color: #10B981; }
        .type-expense { color: #EF4444; }
        
        /* Chat styling */
        .chat-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 1rem;
            border-radius: 1rem;
            background: rgba(0, 0, 0, 0.2);
        }
        
        .chat-message {
            background: rgba(75, 85, 99, 0.5);
            border-radius: 1rem;
            padding: 1rem;
            margin: 0.5rem 0;
            backdrop-filter: blur(4px);
        }
        
        .chat-message.achievement {
            background: rgba(34, 197, 94, 0.2);
            border: 1px solid rgba(34, 197, 94, 0.3);
        }
        
        /* Bottom padding for fixed navigation */
        .main-content {
            padding-bottom: 120px;
        }
    </style>
    """, unsafe_allow_html=True)

def display_status_messages():
    """Display success and error messages"""
    if st.session_state.success_message:
        st.markdown(f"""
        <div class="status-success">
            ✅ {st.session_state.success_message}
        </div>
        """, unsafe_allow_html=True)
        # Clear message after 3 seconds
        if 'success_time' not in st.session_state:
            st.session_state.success_time = datetime.now()
        elif (datetime.now() - st.session_state.success_time).seconds > 3:
            st.session_state.success_message = None
            del st.session_state.success_time
    
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="status-error">
            ❌ {st.session_state.error_message}
        </div>
        """, unsafe_allow_html=True)
        # Clear message after 5 seconds
        if 'error_time' not in st.session_state:
            st.session_state.error_time = datetime.now()
        elif (datetime.now() - st.session_state.error_time).seconds > 5:
            st.session_state.error_message = None
            del st.session_state.error_time

def render_header():
    """Render the application header"""
    # Connection status
    if st.session_state.connection_status['connected']:
        status_class = "connection-connected"
        status_text = "🟢 Đã kết nối"
    elif st.session_state.connection_status['tested']:
        status_class = "connection-error"
        status_text = "🔴 Lỗi kết nối"
    else:
        status_class = "connection-unknown"
        status_text = "⚪ Chưa kết nối"
    
    st.markdown(f"""
    <div class="header-container">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #3B82F6, #8B5CF6); border-radius: 0.75rem; display: flex; align-items: center; justify-content: center;">
                    ⚡
                </div>
                <div>
                    <h1 class="header-title">Level Up</h1>
                    <div style="color: #9CA3AF; font-size: 0.75rem;">RPG Self-Development</div>
                </div>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <div class="connection-indicator {status_class}">
                    {status_text}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_bottom_navigation():
    """Render bottom navigation"""
    nav_items = [
        {'id': 'dashboard', 'icon': '🏠', 'label': 'Trang chủ'},
        {'id': 'character', 'icon': '👤', 'label': 'Nhân vật'},
        {'id': 'quests', 'icon': '⚔️', 'label': 'Nhiệm vụ'},
        {'id': 'resources', 'icon': '💎', 'label': 'Nguồn vốn'},
        {'id': 'achievements', 'icon': '🏆', 'label': 'Danh hiệu'}
    ]
    
    # Create navigation buttons
    col1, col2, col3, col4, col5 = st.columns(5)
    
    for i, item in enumerate(nav_items):
        col = [col1, col2, col3, col4, col5][i]
        
        with col:
            if st.button(
                f"{item['icon']}\n{item['label']}", 
                key=f"nav_{item['id']}",
                help=item['label'],
                use_container_width=True
            ):
                st.session_state.active_tab = item['id']
                st.session_state.show_settings = False
                st.rerun()
    
    # Settings button
    if st.button("⚙️ Cài đặt", key="nav_settings", help="Cài đặt"):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()
    
    # Chat floating button
    if st.button("💬", key="chat_fab", help="Ghi chú & Suy nghĩ"):
        st.session_state.show_chat = True
        st.rerun()

def render_empty_state(icon, title, description, action_text=None, action_callback=None):
    """Render empty state component"""
    st.markdown(f"""
    <div class="empty-state">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
        <h3>{title}</h3>
        <p style="margin-bottom: 1.5rem; line-height: 1.5;">{description}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if action_text and action_callback:
        if st.button(action_text, key=f"empty_action_{title}"):
            action_callback()

def render_progress_bar(current, maximum, color="blue"):
    """Render a progress bar"""
    percentage = min(100, (current / maximum) * 100) if maximum > 0 else 0
    
    if color == "blue":
        gradient = "linear-gradient(90deg, #3B82F6, #8B5CF6)"
    elif color == "green":
        gradient = "linear-gradient(90deg, #22C55E, #16A34A)"
    elif color == "orange":
        gradient = "linear-gradient(90deg, #F97316, #EA580C)"
    else:
        gradient = "linear-gradient(90deg, #6B7280, #4B5563)"
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {percentage}%; background: {gradient};"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9CA3AF; margin-top: 0.25rem;">
        <span>Tiến độ</span>
        <span>{current} / {maximum}</span>
    </div>
    """, unsafe_allow_html=True)

def render_stat_box(icon, label, value, color="blue"):
    """Render a stat box component"""
    color_classes = {
        "red": "text-red-400",
        "orange": "text-orange-400", 
        "blue": "text-blue-400",
        "purple": "text-purple-400",
        "yellow": "text-yellow-400",
        "green": "text-green-400"
    }
    
    text_color = color_classes.get(color, "text-gray-400")
    
    st.markdown(f"""
    <div class="stat-box">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem; color: {text_color};">{icon}</div>
        <div style="font-size: 0.75rem; color: #9CA3AF; margin-bottom: 0.25rem;">{label}</div>
        <div style="font-size: 1.25rem; font-weight: bold; color: white;">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def render_difficulty_stars(difficulty):
    """Render difficulty stars"""
    stars = "⭐" * difficulty
    return f'<span style="color: #F59E0B;">{stars}</span>'

def render_priority_indicator(priority):
    """Render priority indicator"""
    colors = {
        'high': '#EF4444',
        'medium': '#F59E0B',
        'low': '#6B7280'
    }
    color = colors.get(priority, '#6B7280')
    return f'<div style="width: 8px; height: 8px; background: {color}; border-radius: 50%; display: inline-block;"></div>'

def format_currency(amount):
    """Format currency for Vietnamese locale"""
    if amount >= 1000000000:
        return f"{amount / 1000000000:.1f}B"
    elif amount >= 1000000:
        return f"{amount / 1000000:.1f}M"
    elif amount >= 1000:
        return f"{amount / 1000:.1f}K"
    else:
        return f"{amount:,.0f}".replace(',', '.')

def get_age_display(birth_year):
    """Calculate and format age display"""
    if not birth_year:
        return ""
    current_year = datetime.now().year
    age = current_year - birth_year
    return f"{age} tuổi"

def encode_image(image):
    """Encode image to base64 for display"""
    if image is None:
        return None
    
    # Convert PIL image to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def render_avatar(avatar_data, size=120):
    """Render avatar image or emoji placeholder"""
    if avatar_data:
        if avatar_data.startswith('data:image') or avatar_data.startswith('http'):
            # URL or base64 image
            st.markdown(f"""
            <div class="avatar-container" style="width: {size}px; height: {size}px;">
                <img src="{avatar_data}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;" />
            </div>
            """, unsafe_allow_html=True)
        else:
            # Emoji or text
            st.markdown(f"""
            <div class="avatar-container" style="width: {size}px; height: {size}px;">
                {avatar_data}
            </div>
            """, unsafe_allow_html=True)
    else:
        # Default avatar
        st.markdown(f"""
        <div class="avatar-container" style="width: {size}px; height: {size}px;">
            🧙‍♂️
        </div>
        """, unsafe_allow_html=True)

def render_achievement_card(achievement):
    """Render achievement card"""
    tier_colors = {
        'bronze': '#D97706',
        'silver': '#6B7280', 
        'gold': '#F59E0B',
        'legendary': '#8B5CF6'
    }
    
    tier_color = tier_colors.get(achievement.tier, '#6B7280')
    card_class = "achievement-card unlocked" if achievement.unlocked else "achievement-card locked"
    
    progress_bar = ""
    if not achievement.unlocked:
        progress_bar = f"""
        <div style="margin-top: 0.5rem;">
            <div style="display: flex; justify-content: space-between; font-size: 0.75rem; color: #9CA3AF; margin-bottom: 0.25rem;">
                <span>Tiến độ:</span>
                <span>{achievement.progress}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {achievement.progress}%;"></div>
            </div>
            {f'<div style="color: #6B7280; font-size: 0.75rem; margin-top: 0.25rem;">Điều kiện: {achievement.condition}</div>' if achievement.condition else ''}
        </div>
        """
    
    unlock_info = ""
    if achievement.unlocked:
        unlock_info = f"""
        <div style="color: #22C55E; font-size: 0.75rem; margin-top: 0.5rem;">
            🏆 Đạt được vào {achievement.unlocked_date or 'N/A'}
        </div>
        """
    
    st.markdown(f"""
    <div class="{card_class}">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <div style="font-size: 2.5rem;">{achievement.icon}</div>
            <div style="flex: 1;">
                <h3 style="color: {tier_color}; font-size: 1.125rem; font-weight: bold; margin: 0 0 0.5rem 0;">
                    {achievement.title}
                </h3>
                <p style="color: #D1D5DB; font-size: 0.875rem; margin: 0 0 0.5rem 0;">
                    {achievement.description}
                </p>
                {unlock_info}
                {progress_bar}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)