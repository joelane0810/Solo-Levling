"""
Render Functions for Level Up Application
Các hàm render UI components và pages
"""

import streamlit as st
import time
from datetime import datetime
from components.ui_components import *
from components.data_models import *
from utils.helpers import *

# Main Render Functions
def render_dashboard():
    """Render dashboard page"""
    if not st.session_state.connection_status['connected'] and st.session_state.connection_status['tested']:
        render_empty_state(
            "☁️", 
            "Chưa kết nối Google Sheets",
            "Kết nối với Google Sheets để bắt đầu hành trình RPG Self-Development của bạn. Tất cả dữ liệu sẽ được đồng bộ tự động.",
            "Kết nối ngay",
            lambda: setattr(st.session_state, 'show_settings', True) or st.rerun()
        )
        return
    
    if not st.session_state.connection_status['connected'] and not st.session_state.connection_status['tested']:
        render_empty_state(
            "🗄️",
            "Khởi tạo kết nối",
            "Vui lòng thiết lập kết nối Google Sheets để sử dụng ứng dụng.",
            "Cài đặt kết nối",
            lambda: setattr(st.session_state, 'show_settings', True) or st.rerun()
        )
        return
    
    # Welcome section
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: white; margin-bottom: 0.5rem;">
            Chào mừng trở lại, {st.session_state.character.name or 'Hero'}! 👋
        </h2>
        <p style="color: #9CA3AF;">Hãy cùng chinh phục những thử thách hôm nay</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Character Summary
    st.markdown('<div class="card gradient-card">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_avatar(st.session_state.character.avatar, 80)
    
    with col2:
        st.markdown(f"""
        <h3 style="color: white; margin: 0;">{st.session_state.character.name or 'Hero'}</h3>
        <div style="color: #8B5CF6; font-size: 0.9rem; margin-bottom: 0.5rem;">
            Level {st.session_state.character.level} • RPG Developer
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.character.birth_year:
            st.markdown(f'<div style="color: #9CA3AF; font-size: 0.8rem; margin-bottom: 1rem;">{st.session_state.character.get_age_display()}</div>', unsafe_allow_html=True)
        
        render_progress_bar(st.session_state.character.exp, st.session_state.character.exp_to_next)
    
    # Stats
    st.markdown("### Chỉ số nhân vật")
    stat_cols = st.columns(5)
    stat_icons = {'WILL': '❤️', 'PHY': '⚔️', 'MEN': '🧠', 'AWR': '👁️', 'EXE': '⚡'}
    stat_colors = {'WILL': 'red', 'PHY': 'orange', 'MEN': 'blue', 'AWR': 'purple', 'EXE': 'yellow'}
    
    for i, (stat, value) in enumerate(st.session_state.character.stats.items()):
        with stat_cols[i]:
            render_stat_box(stat_icons[stat], stat, value, stat_colors[stat])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Priority Quests
    high_priority_quests = [q for q in st.session_state.quests if q.priority == 'high' and q.status != 'completed']
    
    if high_priority_quests:
        st.markdown("### 🎯 Nhiệm vụ ưu tiên")
        
        for quest in high_priority_quests[:2]:  # Show top 2
            st.markdown('<div class="quest-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <div style="width: 8px; height: 8px; background: {quest.get_priority_color()}; border-radius: 50%;"></div>
                    <h4 style="color: white; margin: 0; font-size: 1.1rem;">{quest.title}</h4>
                </div>
                <p style="color: #D1D5DB; font-size: 0.9rem; margin-bottom: 1rem;">{quest.description}</p>
                <div style="display: flex; gap: 1rem; font-size: 0.8rem;">
                    <span>Độ khó: {quest.get_difficulty_stars()}</span>
                    <span style="color: #F97316;">⏰ {quest.deadline}</span>
                    <span style="color: #22C55E;">+{quest.reward_exp} EXP</span>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("✅ Hoàn thành", key=f"complete_{quest.id}", help="Hoàn thành nhiệm vụ"):
                    complete_quest(quest.id)
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    elif len(st.session_state.quests) == 0:
        render_empty_state(
            "🎯",
            "Chưa có nhiệm vụ nào",
            "Thêm nhiệm vụ trong Google Sheets (tab Quests) để bắt đầu cuộc phiêu lưu RPG của bạn.",
            "Xem hướng dẫn",
            lambda: setattr(st.session_state, 'active_tab', 'quests') or st.rerun()
        )
    else:
        render_empty_state(
            "✅",
            "Hoàn thành tuyệt vời!",
            "Bạn đã hoàn thành tất cả nhiệm vụ ưu tiên. Thêm nhiệm vụ mới để tiếp tục phát triển.",
            "Xem tất cả nhiệm vụ",
            lambda: setattr(st.session_state, 'active_tab', 'quests') or st.rerun()
        )
    
    # Stats overview
    st.markdown("### 📊 Thống kê tổng quan")
    stat_col1, stat_col2 = st.columns(2)
    
    completed_quests = len([q for q in st.session_state.quests if q.status == 'completed'])
    unlocked_achievements = len([a for a in st.session_state.achievements if a.unlocked])
    
    with stat_col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(59, 130, 246, 0.2), rgba(29, 78, 216, 0.2)); 
                    border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 1rem; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: white; margin-bottom: 0.25rem;">{completed_quests}</div>
            <div style="color: #93C5FD; font-size: 0.9rem;">Nhiệm vụ hoàn thành</div>
            <div style="color: #60A5FA; font-size: 0.75rem;">Tổng cộng</div>
        </div>
        """, unsafe_allow_html=True)
    
    with stat_col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(109, 40, 217, 0.2)); 
                    border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 1rem; padding: 1.5rem; text-align: center;">
            <div style="font-size: 2rem; font-weight: bold; color: white; margin-bottom: 0.25rem;">{unlocked_achievements}</div>
            <div style="color: #C4B5FD; font-size: 0.9rem;">Danh hiệu đạt được</div>
            <div style="color: #A78BFA; font-size: 0.75rem;">Tổng cộng</div>
        </div>
        """, unsafe_allow_html=True)

def render_character():
    """Render character page"""
    st.markdown("### 👤 Thông tin nhân vật")
    
    # Character card
    st.markdown('<div class="card gradient-card">', unsafe_allow_html=True)
    
    # Avatar and basic info
    col1, col2 = st.columns([1, 2])
    
    with col1:
        render_avatar(st.session_state.character.avatar, 120)
        if st.button("✏️ Chỉnh sửa", key="edit_character", help="Chỉnh sửa thông tin nhân vật"):
            st.session_state.show_character_modal = True
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <h2 style="color: white; margin: 0 0 0.5rem 0;">{st.session_state.character.name or 'Hero'}</h2>
        <div style="color: #8B5CF6; font-size: 1.1rem; margin-bottom: 0.5rem;">Level {st.session_state.character.level} RPG Developer</div>
        """, unsafe_allow_html=True)
        
        if st.session_state.character.birth_year:
            st.markdown(f'<div style="color: #9CA3AF; margin-bottom: 1rem;">{st.session_state.character.get_age_display()}</div>', unsafe_allow_html=True)
        
        st.markdown("**Kinh nghiệm**")
        render_progress_bar(st.session_state.character.exp, st.session_state.character.exp_to_next)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats
    st.markdown("### 📊 Chỉ số chi tiết")
    stat_cols = st.columns(5)
    stat_icons = {'WILL': '❤️', 'PHY': '⚔️', 'MEN': '🧠', 'AWR': '👁️', 'EXE': '⚡'}
    stat_colors = {'WILL': 'red', 'PHY': 'orange', 'MEN': 'blue', 'AWR': 'purple', 'EXE': 'yellow'}
    
    for i, (stat, value) in enumerate(st.session_state.character.stats.items()):
        with stat_cols[i]:
            render_stat_box(stat_icons[stat], stat, value, stat_colors[stat])
    
    # Recent achievements
    recent_achievements = [a for a in st.session_state.achievements if a.unlocked][-4:]
    if recent_achievements:
        st.markdown("### 🏆 Danh hiệu gần đây")
        
        ach_cols = st.columns(min(4, len(recent_achievements)))
        for i, achievement in enumerate(recent_achievements):
            with ach_cols[i]:
                st.markdown(f"""
                <div style="background: rgba(75, 85, 99, 0.5); border-radius: 1rem; padding: 1rem; text-align: center; border: 1px solid rgba(75, 85, 99, 0.3);">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{achievement.icon}</div>
                    <div style="color: {achievement.get_tier_color()}; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.25rem;">
                        {achievement.title}
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Personal info
    st.markdown("### 📋 Thông tin cá nhân")
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    info_data = [
        ("Tên nhân vật:", st.session_state.character.name or "Chưa đặt tên"),
        ("Năm sinh:", str(st.session_state.character.birth_year) if st.session_state.character.birth_year else "Chưa cập nhật"),
        ("Tuổi hiện tại:", st.session_state.character.get_age_display() or "Chưa xác định"),
        ("Tổng EXP kiếm được:", str(st.session_state.character.exp)),
        ("Nhiệm vụ hoàn thành:", f"{len([q for q in st.session_state.quests if q.status == 'completed'])}/{len(st.session_state.quests)}"),
        ("Tỷ lệ hoàn thành:", f"{(len([q for q in st.session_state.quests if q.status == 'completed']) / len(st.session_state.quests) * 100) if st.session_state.quests else 0:.0f}%"),
        ("Danh hiệu đạt được:", f"{len([a for a in st.session_state.achievements if a.unlocked])}/{len(st.session_state.achievements)}")
    ]
    
    for label, value in info_data:
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f'<span style="color: #9CA3AF;">{label}</span>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<span style="color: white; font-weight: bold;">{value}</span>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_quests():
    """Render quests page"""
    # Header
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### ⚔️ Nhiệm vụ")
        pending_quests = len([q for q in st.session_state.quests if q.status != 'completed'])
        st.markdown(f'<p style="color: #9CA3AF; font-size: 0.9rem;">{pending_quests} nhiệm vụ đang chờ</p>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Đồng bộ", key="sync_quests", help="Đồng bộ với Google Sheets"):
            if st.session_state.sheets_manager:
                sync_from_sheets()
                st.rerun()
    
    if len(st.session_state.quests) == 0:
        render_empty_state(
            "⚔️",
            "Chưa có nhiệm vụ nào",
            "Thêm nhiệm vụ trong Google Sheets tab 'Quests' với cấu trúc: Title | Description | RequiredStat | Difficulty | Deadline | RewardEXP | RewardStat | Status | Category | Priority",
            "Mở cài đặt",
            lambda: setattr(st.session_state, 'show_settings', True) or st.rerun()
        )
        
        st.markdown("""
        <div style="background: rgba(75, 85, 99, 0.5); border-radius: 1rem; padding: 1rem; margin-top: 1rem;">
            <div style="color: #9CA3AF; font-size: 0.8rem;">
                <strong>Ví dụ:</strong> "Tập thể dục | Chạy bộ 30 phút | PHY | 3 | Hôm nay | 50 | PHY +1 | todo | health | high"
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Quest list
    for quest in st.session_state.quests:
        st.markdown(f'<div class="quest-card {quest.status}">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Quest header
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.75rem;">
                <div style="width: 12px; height: 12px; background: {quest.get_priority_color()}; border-radius: 50%; flex-shrink: 0;"></div>
                <h3 style="color: white; margin: 0; font-size: 1.2rem; flex: 1;">{quest.title}</h3>
            </div>
            <p style="color: #D1D5DB; margin-bottom: 1rem; line-height: 1.4;">{quest.description}</p>
            """, unsafe_allow_html=True)
            
            # Quest details
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.markdown(f"""
                <div style="display: flex; gap: 1rem; font-size: 0.85rem;">
                    <span>Độ khó: {quest.get_difficulty_stars()}</span>
                    <span style="color: #F97316;">⏰ {quest.deadline}</span>
                </div>
                """, unsafe_allow_html=True)
            
            with detail_col2:
                st.markdown(f"""
                <div style="display: flex; gap: 1rem; font-size: 0.85rem;">
                    <span style="color: #60A5FA;">Yêu cầu: {quest.required_stat}</span>
                    <span style="color: #A78BFA;">{quest.category.title()}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Reward info
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(75, 85, 99, 0.5);">
                <span style="color: #9CA3AF; font-size: 0.85rem;">Phần thưởng:</span>
                <div>
                    <span style="color: #22C55E; font-weight: bold;">+{quest.reward_exp} EXP</span>
                    {f'<span style="color: #9CA3AF; font-size: 0.8rem; margin-left: 0.5rem;">{quest.reward_stat}</span>' if quest.reward_stat else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if quest.status != 'completed':
                if st.button("✅ Hoàn thành", key=f"complete_quest_{quest.id}", help="Hoàn thành nhiệm vụ"):
                    complete_quest(quest.id)
                    st.rerun()
            else:
                st.markdown('<div style="color: #22C55E; text-align: center; font-weight: bold;">✅ Hoàn thành</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

def render_resources():
    """Render resources page"""
    st.markdown("### 💎 Nguồn vốn phát triển")
    st.markdown('<p style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 2rem;">4 khía cạnh cốt lõi cho sự phát triển toàn diện</p>', unsafe_allow_html=True)
    
    for resource in st.session_state.resources:
        st.markdown('<div class="resource-card">', unsafe_allow_html=True)
        
        # Resource header
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="width: 60px; height: 60px; background: linear-gradient(135deg, {resource.color.replace('from-', '').replace(' to-', ', ')}); 
                        border-radius: 1rem; display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">
                {resource.icon}
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_value = calculate_resource_total(st.session_state.resource_details.get(resource.name, []))
            st.markdown(f"""
            <h3 style="color: white; margin: 0 0 0.25rem 0;">{resource.name}</h3>
            <p style="color: #D1D5DB; font-size: 0.9rem; margin: 0 0 0.5rem 0;">{resource.description}</p>
            """, unsafe_allow_html=True)
            
            if total_value > 0:
                st.markdown(f'<p style="color: {resource.text_color.replace("text-", "")}; font-weight: bold; margin: 0;">Tổng giá trị: {format_currency(total_value)} VND</p>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="color: white; font-size: 1.2rem; font-weight: bold;">Lv.{resource.level}</div>
                <div style="color: {resource.text_color.replace("text-", "")}; font-size: 0.75rem;">Cấp độ</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bar
        st.markdown("**Tiến độ đến level tiếp theo**")
        render_progress_bar(resource.progress, 100)
        
        # Resource details
        details = st.session_state.resource_details.get(resource.name, [])
        active_details = [d for d in details if d['status'] == 'active']
        
        st.markdown(f"**Chi tiết ({len(active_details)})**")
        
        if not active_details:
            st.markdown("""
            <div style="text-align: center; padding: 1rem; color: #6B7280;">
                <div style="font-size: 0.9rem; margin-bottom: 0.5rem;">Chưa có chi tiết nào</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"➕ Thêm chi tiết đầu tiên", key=f"add_first_{resource.name}"):
                st.session_state.selected_resource = resource.name
                st.session_state.show_resource_modal = True
                st.rerun()
        else:
            # Show details
            for detail in active_details[:3]:  # Show first 3
                col1, col2, col3 = st.columns([1, 4, 1])
                
                with col1:
                    type_icons = {'asset': '💰', 'loan': '📋', 'investment': '📈', 'income': '💸', 'expense': '💳'}
                    st.markdown(f'<div style="font-size: 1.2rem; text-align: center;">{type_icons.get(detail["type"], "💰")}</div>', unsafe_allow_html=True)
                
                with col2:
                    type_colors = {'asset': '#22C55E', 'loan': '#F97316', 'investment': '#3B82F6', 'income': '#10B981', 'expense': '#EF4444'}
                    st.markdown(f"""
                    <div style="color: white; font-weight: bold; margin-bottom: 0.25rem;">{detail['name']}</div>
                    <div style="display: flex; gap: 0.5rem; font-size: 0.8rem;">
                        <span style="color: {type_colors.get(detail['type'], '#22C55E')};">{format_currency(detail['amount'])} VND</span>
                        <span style="color: #6B7280;">•</span>
                        <span style="color: #9CA3AF; text-transform: capitalize;">{detail['type']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("✏️", key=f"edit_{detail['id']}", help="Chỉnh sửa"):
                        st.session_state.selected_resource = resource.name
                        st.session_state.resource_form = detail.copy()
                        st.session_state.show_resource_modal = True
                        st.rerun()
            
            if len(active_details) > 3:
                st.markdown(f'<div style="color: #9CA3AF; font-size: 0.8rem; text-align: center;">...và {len(active_details) - 3} chi tiết khác</div>', unsafe_allow_html=True)
            
            if st.button(f"➕ Thêm chi tiết", key=f"add_{resource.name}"):
                st.session_state.selected_resource = resource.name
                st.session_state.show_resource_modal = True
                st.rerun()
        
        # Resource info footer
        if resource.next_milestone:
            st.markdown(f'<div style="color: {resource.text_color.replace("text-", "")}; font-size: 0.8rem; text-align: center; margin-top: 1rem; background: rgba(75, 85, 99, 0.5); padding: 0.5rem; border-radius: 0.5rem;">Mốc tiếp: {resource.next_milestone}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Usage guide
    st.markdown("### 📋 Hướng dẫn cập nhật")
    st.markdown("""
    <div style="background: rgba(75, 85, 99, 0.5); border-radius: 1rem; padding: 1.5rem; margin-top: 1rem;">
        <p style="color: #D1D5DB; margin-bottom: 1rem;">Dữ liệu chi tiết nguồn vốn được lưu trong Google Sheets tab 'ResourceDetails':</p>
        <div style="background: rgba(0, 0, 0, 0.3); border-radius: 0.5rem; padding: 1rem; font-family: monospace; font-size: 0.8rem;">
            <div style="color: #E5E7EB;">ResourceName | DetailName | Amount | Type | Notes | Date | Status</div>
            <div style="color: #9CA3AF; margin-top: 0.5rem;">Tài chính | Bản thân | 50000000 | asset | Tiền tiết kiệm | 24/06/2025 | active</div>
            <div style="color: #9CA3AF;">Tài chính | Ba | 35000000 | asset | Hỗ trợ gia đình | 24/06/2025 | active</div>
        </div>
        <div style="color: #9CA3AF; font-size: 0.8rem; margin-top: 1rem;">
            <strong>Types:</strong> asset (tài sản), loan (khoản vay), investment (đầu tư), income (thu nhập), expense (chi phí)
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_achievements():
    """Render achievements page"""
    st.markdown("### 🏆 Danh hiệu & Thành tựu")
    
    unlocked_count = len([a for a in st.session_state.achievements if a.unlocked])
    total_count = len(st.session_state.achievements)
    
    st.markdown(f'<p style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 2rem;">{unlocked_count}/{total_count} đã mở khóa</p>', unsafe_allow_html=True)
    
    if len(st.session_state.achievements) == 0:
        render_empty_state(
            "🏆",
            "Chưa có danh hiệu nào",
            "Thêm danh hiệu trong Google Sheets tab 'Achievements' với cấu trúc: Title | Description | Icon | Tier | Unlocked | UnlockedDate | Progress | Condition | Category",
            "Cài đặt Google Sheets",
            lambda: setattr(st.session_state, 'show_settings', True) or st.rerun()
        )
        
        st.markdown("""
        <div style="background: rgba(75, 85, 99, 0.5); border-radius: 1rem; padding: 1rem; margin-top: 1rem;">
            <div style="color: #9CA3AF; font-size: 0.8rem;">
                <strong>Ví dụ:</strong> "First Steps | Hoàn thành nhiệm vụ đầu tiên | 🎯 | bronze | TRUE | 20/06/2025 | 100 | Complete 1 quest | general"
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Achievement stats
    st.markdown("### 📊 Thống kê theo hạng")
    stat_cols = st.columns(4)
    tiers = ['bronze', 'silver', 'gold', 'legendary']
    tier_colors = {'bronze': '#D97706', 'silver': '#6B7280', 'gold': '#F59E0B', 'legendary': '#8B5CF6'}
    
    for i, tier in enumerate(tiers):
        count = len([a for a in st.session_state.achievements if a.tier == tier and a.unlocked])
        with stat_cols[i]:
            st.markdown(f"""
            <div style="background: rgba(75, 85, 99, 0.5); border-radius: 1rem; padding: 1rem; text-align: center; border: 1px solid rgba(75, 85, 99, 0.5);">
                <div style="color: {tier_colors[tier]}; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.25rem;">{count}</div>
                <div style="color: #9CA3AF; font-size: 0.75rem; text-transform: capitalize;">{tier}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Achievement list
    st.markdown("### 🎖️ Danh sách danh hiệu")
    
    for achievement in st.session_state.achievements:
        render_achievement_card(achievement)

def render_settings():
    """Render settings page"""
    st.markdown("### ⚙️ Cài đặt")
    st.markdown('<p style="color: #9CA3AF; font-size: 0.9rem; margin-bottom: 2rem;">Kết nối và đồng bộ với Google Sheets</p>', unsafe_allow_html=True)
    
    # Connection status
    st.markdown("#### 📊 Trạng thái kết nối")
    
    if st.session_state.connection_status['last_sync']:
        last_sync = st.session_state.connection_status['last_sync']
        st.markdown(f'<p style="color: #9CA3AF; font-size: 0.85rem;">Đồng bộ lần cuối: {last_sync.strftime("%d/%m/%Y %H:%M:%S")}</p>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔗 Kiểm tra kết nối", key="test_connection", 
                    disabled=st.session_state.loading or not st.session_state.settings['sheet_id'] or not st.session_state.settings['api_key']):
            test_connection()
            st.rerun()
    
    with col2:
        if st.button("🔄 Đồng bộ ngay", key="sync_now", 
                    disabled=st.session_state.syncing or not st.session_state.connection_status['connected']):
            sync_from_sheets()
            st.rerun()
    
    with col3:
        if st.button("💾 Lưu cài đặt", key="save_settings"):
            save_settings()
            st.rerun()
    
    st.divider()
    
    # Google Sheets configuration
    st.markdown("#### 🔗 Cấu hình Google Sheets")
    
    with st.form("settings_form"):
        sheet_id = st.text_input(
            "Google Sheet ID *",
            value=st.session_state.settings['sheet_id'],
            placeholder="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms",
            help="Lấy từ URL: docs.google.com/spreadsheets/d/[SHEET_ID]/edit"
        )
        
        api_key = st.text_input(
            "Google Sheets API Key *",
            value=st.session_state.settings['api_key'],
            type="password",
            placeholder="AIzaSyD...",
            help="Tạo API Key tại Google Cloud Console"
        )
        
        auto_sync = st.checkbox(
            "Tự động đồng bộ",
            value=st.session_state.settings['auto_sync'],
            help="Đồng bộ định kỳ với Google Sheets"
        )
        
        if auto_sync:
            sync_interval = st.selectbox(
                "Tần suất đồng bộ",
                options=[1, 5, 15, 30, 60],
                index=[1, 5, 15, 30, 60].index(st.session_state.settings['sync_interval']),
                format_func=lambda x: f"Mỗi {x} phút" if x < 60 else f"Mỗi {x//60} giờ"
            )
        else:
            sync_interval = st.session_state.settings['sync_interval']
        
        if st.form_submit_button("💾 Lưu cài đặt", use_container_width=True):
            st.session_state.settings.update({
                'sheet_id': sheet_id,
                'api_key': api_key,
                'auto_sync': auto_sync,
                'sync_interval': sync_interval
            })
            save_settings()
            
            if sheet_id and api_key:
                test_connection()
            
            st.rerun()
    
    st.divider()
    
    # Setup guide
    st.markdown("#### 📋 Hướng dẫn thiết lập")
    
    with st.expander("1. Tạo Google Sheet mới"):
        st.markdown("""
        - Tạo Google Sheet mới
        - Tạo các sheet tabs: **Character**, **Quests**, **Achievements**, **Goals**, **Resources**, **ResourceDetails**, **Chat**
        - Đặt quyền "Anyone with the link can view" hoặc "edit"
        """)
    
    with st.expander("2. Lấy API Key"):
        st.markdown("""
        - Truy cập [Google Cloud Console](https://console.cloud.google.com)
        - Tạo project mới hoặc chọn project có sẵn
        - Bật Google Sheets API
        - Tạo API Key trong mục Credentials
        """)
    
    with st.expander("3. Cấu trúc dữ liệu"):
        st.markdown("""
        **Sheet "Quests" (A2:J):**
        ```
        Title | Description | RequiredStat | Difficulty | Deadline | RewardEXP | RewardStat | Status | Category | Priority
        ```
        
        **Sheet "Achievements" (A2:I):**
        ```
        Title | Description | Icon | Tier | Unlocked | UnlockedDate | Progress | Condition | Category
        ```
        
        **Sheet "ResourceDetails" (A2:G):**
        ```
        ResourceName | DetailName | Amount | Type | Notes | Date | Status
        ```
        
        **Sheet "Character" (A1:B):**
        ```
        name | Hero
        avatar | https://example.com/avatar.jpg
        birthYear | 1995
        level | 5
        exp | 750
        expToNext | 1000
        stats | {"WILL":15,"PHY":12,"MEN":14,"AWR":13,"EXE":16}
        ```
        """)

# Modal render functions
def render_character_modal():
    """Render character edit modal"""
    if not st.session_state.show_character_modal:
        return
    
    with st.container():
        st.markdown("### ✏️ Chỉnh sửa nhân vật")
        
        with st.form("character_form"):
            name = st.text_input(
                "Tên nhân vật *",
                value=st.session_state.character.name,
                placeholder="Nhập tên nhân vật...",
                max_chars=50
            )
            
            avatar = st.text_input(
                "Avatar URL",
                value=st.session_state.character.avatar,
                placeholder="https://example.com/avatar.jpg hoặc emoji 🧙‍♂️",
                help="Nhập URL ảnh hoặc emoji"
            )
            
            birth_year = st.number_input(
                "Năm sinh",
                min_value=1900,
                max_value=datetime.now().year,
                value=st.session_state.character.birth_year or datetime.now().year - 25,
                help="Tùy chọn - để trống nếu không muốn hiển thị tuổi"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Lưu thay đổi", use_container_width=True):
                    if not name.strip():
                        st.error("Vui lòng nhập tên nhân vật")
                    else:
                        # Update character
                        st.session_state.character.name = name
                        st.session_state.character.avatar = avatar
                        st.session_state.character.birth_year = birth_year if birth_year != datetime.now().year - 25 else None
                        
                        # Update to sheets if connected
                        if st.session_state.sheets_manager and st.session_state.connection_status['connected']:
                            try:
                                st.session_state.sheets_manager.update_character(st.session_state.character)
                                st.session_state.success_message = "Cập nhật nhân vật thành công!"
                            except Exception as e:
                                st.session_state.error_message = f"Lỗi cập nhật: {str(e)}"
                        
                        st.session_state.show_character_modal = False
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Hủy", use_container_width=True):
                    st.session_state.show_character_modal = False
                    st.rerun()

def render_resource_modal():
    """Render resource detail modal"""
    if not st.session_state.show_resource_modal or not st.session_state.selected_resource:
        return
    
    with st.container():
        st.markdown(f"### {'✏️ Chỉnh sửa' if 'id' in st.session_state.get('resource_form', {}) else '➕ Thêm'} chi tiết")
        st.markdown(f"**{st.session_state.selected_resource}**")
        
        with st.form("resource_form"):
            form_data = st.session_state.get('resource_form', {})
            
            name = st.text_input(
                "Tên chi tiết *",
                value=form_data.get('name', ''),
                placeholder="VD: Bản thân, Ba, Mượn mẹ..."
            )
            
            amount = st.number_input(
                "Số tiền (VND) *",
                min_value=0.0,
                value=float(form_data.get('amount', 0)),
                format="%.0f",
                step=1000000.0
            )
            
            type_options = ["asset", "loan", "investment", "income", "expense"]
            type_labels = ["💰 Tài sản", "📋 Khoản vay", "📈 Đầu tư", "💸 Thu nhập", "💳 Chi phí"]
            
            type_selected = st.selectbox(
                "Loại *",
                options=type_options,
                index=type_options.index(form_data.get('type', 'asset')),
                format_func=lambda x: type_labels[type_options.index(x)]
            )
            
            notes = st.text_area(
                "Ghi chú",
                value=form_data.get('notes', ''),
                placeholder="Mô tả chi tiết về nguồn vốn này...",
                height=100
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.form_submit_button("💾 Lưu", use_container_width=True):
                    if not name or not amount:
                        st.error("Vui lòng điền đầy đủ thông tin bắt buộc")
                    else:
                        # Create new detail
                        new_detail = {
                            'id': int(time.time()),
                            'name': name,
                            'amount': amount,
                            'type': type_selected,
                            'notes': notes,
                            'date': datetime.now().strftime('%d/%m/%Y'),
                            'status': 'active'
                        }
                        
                        # Update local state
                        if st.session_state.selected_resource not in st.session_state.resource_details:
                            st.session_state.resource_details[st.session_state.selected_resource] = []
                        
                        st.session_state.resource_details[st.session_state.selected_resource].append(new_detail)
                        
                        # Update to sheets if connected
                        if st.session_state.sheets_manager and st.session_state.connection_status['connected']:
                            try:
                                st.session_state.sheets_manager.add_resource_detail(st.session_state.selected_resource, new_detail)
                                st.session_state.success_message = "Thêm chi tiết thành công!"
                            except Exception as e:
                                st.session_state.error_message = f"Lỗi thêm chi tiết: {str(e)}"
                        
                        st.session_state.show_resource_modal = False
                        st.session_state.selected_resource = None
                        if 'resource_form' in st.session_state:
                            del st.session_state.resource_form
                        st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Hủy", use_container_width=True):
                    st.session_state.show_resource_modal = False
                    st.session_state.selected_resource = None
                    if 'resource_form' in st.session_state:
                        del st.session_state.resource_form
                    st.rerun()

def render_chat_modal():
    """Render chat modal"""
    if not st.session_state.show_chat:
        return
    
    with st.container():
        st.markdown("### 💬 Ghi chú & Suy nghĩ")
        st.markdown('<p style="color: #9CA3AF; font-size: 0.9rem;">Không gian riêng tư của bạn</p>', unsafe_allow_html=True)
        
        # Chat messages
        if st.session_state.chat_messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for message in st.session_state.chat_messages[-10:]:  # Show last 10 messages
                message_class = "achievement" if message['type'] == 'achievement' else ""
                icon = "🎉" if message['type'] == 'achievement' else "⏰" if message['type'] == 'reminder' else "💭"
                
                st.markdown(f"""
                <div class="chat-message {message_class}">
                    <div style="display: flex; align-items: start; gap: 0.75rem;">
                        <span style="font-size: 1.2rem;">{icon}</span>
                        <div style="flex: 1;">
                            <div style="color: white; line-height: 1.4;">{message['text']}</div>
                            <div style="color: #9CA3AF; font-size: 0.75rem; margin-top: 0.5rem;">{message['timestamp']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; color: #9CA3AF;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💬</div>
                <p>Chưa có ghi chú nào</p>
                <p style="font-size: 0.9rem;">Hãy chia sẻ suy nghĩ của bạn</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Chat input
        with st.form("chat_form"):
            message_text = st.text_area(
                "Chia sẻ suy nghĩ của bạn...",
                placeholder="Nhập ghi chú, suy nghĩ, hoặc cảm xúc của bạn...",
                height=100,
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([3, 1])
            
            with col2:
                if st.form_submit_button("📤 Gửi", use_container_width=True):
                    if message_text.strip():
                        new_message = {
                            'id': int(time.time()),
                            'text': message_text,
                            'timestamp': datetime.now().strftime("%H:%M"),
                            'type': 'note',
                            'date': datetime.now().strftime("%d/%m/%Y"),
                            'author': 'user'
                        }
                        
                        st.session_state.chat_messages.append(new_message)
                        
                        # Update to sheets if connected
                        if st.session_state.sheets_manager and st.session_state.connection_status['connected']:
                            try:
                                st.session_state.sheets_manager.add_chat_message(new_message)
                                st.session_state.success_message = "Ghi chú đã được lưu!"
                            except Exception as e:
                                st.session_state.error_message = f"Lỗi lưu ghi chú: {str(e)}"
                        
                        st.rerun()
            
            with col1:
                if st.form_submit_button("❌ Đóng", use_container_width=True):
                    st.session_state.show_chat = False
                    st.rerun()

# Global sync function
def sync_from_sheets():
    """Sync data from Google Sheets"""
    if not st.session_state.sheets_manager:
        return
    
    try:
        st.session_state.syncing = True
        st.session_state.error_message = None
        
        # Sync character data
        character_data = st.session_state.sheets_manager.read_character()
        if character_data:
            st.session_state.character.update_from_dict(character_data)
        
        # Sync quests
        quests_data = st.session_state.sheets_manager.read_quests()
        st.session_state.quests = [Quest.from_dict(q) for q in quests_data]
        
        # Sync achievements
        achievements_data = st.session_state.sheets_manager.read_achievements()
        st.session_state.achievements = [Achievement.from_dict(a) for a in achievements_data]
        
        # Sync resources
        resources_data = st.session_state.sheets_manager.read_resources()
        if resources_data:
            for i, resource in enumerate(st.session_state.resources):
                if i < len(resources_data):
                    resource.update_from_dict(resources_data[i])
        
        # Sync resource details
        st.session_state.resource_details = st.session_state.sheets_manager.read_resource_details()
        
        # Sync chat messages
        st.session_state.chat_messages = st.session_state.sheets_manager.read_chat()
        
        # Sync goals
        goals_data = st.session_state.sheets_manager.read_goals()
        if goals_data:
            st.session_state.goals = goals_data
        
        st.session_state.connection_status['last_sync'] = datetime.now()
        st.session_state.success_message = 'Đồng bộ thành công!'
        
    except Exception as e:
        st.session_state.error_message = f'Lỗi đồng bộ: {str(e)}'
        st.session_state.connection_status['connected'] = False
    finally:
        st.session_state.syncing = False

def complete_quest(quest_id):
    """Complete a quest and update character"""
    quest = next((q for q in st.session_state.quests if q.id == quest_id), None)
    if not quest or quest.status == 'completed':
        return
    
    # Update quest status
    quest.status = 'completed'
    
    # Update character EXP
    st.session_state.character.exp += quest.reward_exp
    
    # Level up check
    while st.session_state.character.exp >= st.session_state.character.exp_to_next:
        st.session_state.character.level += 1
        st.session_state.character.exp_to_next += 100
    
    # Add achievement message
    new_message = {
        'id': int(time.time()),
        'text': f'🎉 Hoàn thành: {quest.title} (+{quest.reward_exp} EXP)',
        'timestamp': datetime.now().strftime("%H:%M"),
        'type': 'achievement',
        'date': datetime.now().strftime("%d/%m/%Y"),
        'author': 'user'
    }
    st.session_state.chat_messages.append(new_message)
    
    # Update sheets if connected
    if st.session_state.sheets_manager and st.session_state.connection_status['connected']:
        try:
            st.session_state.sheets_manager.update_quest(quest)
            st.session_state.sheets_manager.update_character(st.session_state.character)
            st.session_state.sheets_manager.add_chat_message(new_message)
        except Exception as e:
            st.session_state.error_message = f'Lỗi cập nhật: {str(e)}'
    
    st.session_state.success_message = f'Hoàn thành nhiệm vụ: {quest.title}!'

def test_connection():
    """Test connection to Google Sheets"""
    if not st.session_state.settings['sheet_id'] or not st.session_state.settings['api_key']:
        st.session_state.error_message = 'Vui lòng nhập đầy đủ Sheet ID và API Key'
        return False
    
    try:
        st.session_state.loading = True
        st.session_state.error_message = None
        
        # Initialize Google Sheets manager
        from components.google_sheets import GoogleSheetsManager
        st.session_state.sheets_manager = GoogleSheetsManager(
            st.session_state.settings['sheet_id'],
            st.session_state.settings['api_key']
        )
        
        # Test connection
        if st.session_state.sheets_manager.test_connection():
            st.session_state.connection_status['connected'] = True
            st.session_state.connection_status['tested'] = True
            st.session_state.success_message = 'Kết nối thành công!'
            
            # Auto-sync after successful connection
            sync_from_sheets()
            return True
        else:
            raise Exception("Không thể kết nối")
            
    except Exception as e:
        st.session_state.connection_status['connected'] = False
        st.session_state.connection_status['tested'] = True
        st.session_state.error_message = f'Lỗi kết nối: {str(e)}'
        return False
    finally:
        st.session_state.loading = False

def save_settings():
    """Save settings to local file"""
    try:
        from utils.helpers import save_json_file
        save_json_file(st.session_state.settings, "levelup_settings.json")
        st.session_state.success_message = "Cài đặt đã được lưu!"
    except Exception as e:
        st.session_state.error_message = f"Lỗi lưu cài đặt: {str(e)}"