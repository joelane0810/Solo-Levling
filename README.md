# Level Up - RPG Self-Development (Python Version)

⚡ Ứng dụng phát triển bản thân theo phong cách RPG, được chuyển đổi từ React sang Python Streamlit.

## ✨ Tính năng

- 🎮 **Hệ thống RPG**: Level, EXP, Stats (WILL, PHY, MEN, AWR, EXE)
- ⚔️ **Quản lý nhiệm vụ**: Tạo, theo dõi và hoàn thành các nhiệm vụ với độ ưu tiên
- 🏆 **Hệ thống danh hiệu**: Unlock achievements theo tiến độ
- 💎 **4 nguồn vốn**: Xã hội, Tài chính, Kiến tạo, Khám phá
- 💬 **Ghi chú cá nhân**: Lưu trữ suy nghĩ và cảm xúc
- ☁️ **Đồng bộ Google Sheets**: Tự động sync dữ liệu
- 📱 **Giao diện responsive**: Dark theme, modern UI

## 🚀 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd levelup-python
```

### 2. Tạo virtual environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng

```bash
streamlit run main.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

## ⚙️ Cấu hình Google Sheets

### 1. Tạo Google Cloud Project

1. Truy cập [Google Cloud Console](https://console.cloud.google.com)
2. Tạo project mới hoặc chọn project có sẵn
3. Bật **Google Sheets API**
4. Tạo **API Key** trong mục Credentials

### 2. Tạo Google Sheet

1. Tạo Google Sheet mới
2. Tạo các sheet tabs sau:
   - `Character`
   - `Quests`
   - `Achievements`
   - `Goals`
   - `Resources`
   - `ResourceDetails`
   - `Chat`
3. Đặt quyền chia sẻ: "Anyone with the link can view" hoặc "edit"

### 3. Cấu trúc dữ liệu

#### Sheet "Character" (A1:B7)
```
name        | Hero
avatar      | https://example.com/avatar.jpg
birthYear   | 1995
level       | 5
exp         | 750
expToNext   | 1000
stats       | {"WILL":15,"PHY":12,"MEN":14,"AWR":13,"EXE":16}
```

#### Sheet "Quests" (A2:J)
```
Title | Description | RequiredStat | Difficulty | Deadline | RewardEXP | RewardStat | Status | Category | Priority
```

**Ví dụ:**
```
Tập thể dục | Chạy bộ 30 phút | PHY | 3 | Hôm nay | 50 | PHY +1 | todo | health | high
Đọc sách | Đọc 1 chương sách kỹ năng | MEN | 2 | Tuần này | 30 | MEN +1 | in-progress | learning | medium
```

#### Sheet "Achievements" (A2:I)
```
Title | Description | Icon | Tier | Unlocked | UnlockedDate | Progress | Condition | Category
```

**Ví dụ:**
```
First Steps | Hoàn thành nhiệm vụ đầu tiên | 🎯 | bronze | TRUE | 20/06/2025 | 100 | Complete 1 quest | general
Level Up | Đạt level 5 | ⬆️ | silver | FALSE | | 80 | Reach level 5 | character
```

#### Sheet "ResourceDetails" (A2:G)
```
ResourceName | DetailName | Amount | Type | Notes | Date | Status
```

**Ví dụ:**
```
Tài chính | Bản thân | 50000000 | asset | Tiền tiết kiệm | 24/06/2025 | active
Tài chính | Ba | 35000000 | asset | Hỗ trợ gia đình | 24/06/2025 | active
Xã hội | Bạn bè | 50 | asset | Số lượng bạn thân | 24/06/2025 | active
```

#### Sheet "Goals" (A1:E)
```
Type | Title | Progress | Deadline | Category
```

**Ví dụ:**
```
mission | Trở thành Full-stack Developer | | | career
yearly | Học 3 ngôn ngữ lập trình | 33 | 31/12/2025 | learning
quarterly | Tăng thu nhập 20% | 60 | 31/03/2025 | finance
monthly | Đọc 2 cuốn sách | 50 | 30/06/2025 | learning
```

#### Sheet "Chat" (A2:E)
```
Text | Timestamp | Type | Date | Author
```

**Ví dụ:**
```
Hôm nay cảm thấy rất tích cực! | 14:30 | note | 24/06/2025 | user
Hoàn thành nhiệm vụ tập thể dục | 15:45 | achievement | 24/06/2025 | user
```

## 📊 Hướng dẫn sử dụng

### 1. Kết nối Google Sheets

1. Mở ứng dụng và click **⚙️ Cài đặt**
2. Nhập **Google Sheet ID** (từ URL sheet)
3. Nhập **Google Sheets API Key**
4. Click **🔗 Kiểm tra kết nối**
5. Bật **Tự động đồng bộ** nếu muốn

### 2. Quản lý nhân vật

- Click **👤 Nhân vật** để xem thông tin
- Click **✏️ Chỉnh sửa** để cập nhật tên, avatar, năm sinh
- Theo dõi Level, EXP và 5 chỉ số cốt lõi

### 3. Làm nhiệm vụ

- Click **⚔️ Nhiệm vụ** để xem danh sách
- Click **✅ Hoàn thành** để hoàn thành nhiệm vụ
- Nhận EXP và có thể level up

### 4. Quản lý nguồn vốn

- Click **💎 Nguồn vốn** để xem 4 lĩnh vực
- Click **➕ Thêm chi tiết** để thêm tài sản/khoản vay
- Theo dõi tổng giá trị từng nguồn vốn

### 5. Ghi chú cá nhân

- Click **💬** (floating button) để mở chat
- Viết ghi chú, suy nghĩ, cảm xúc
- Tự động lưu tin nhắn thành tựu khi hoàn thành nhiệm vụ

## 🎮 Gameplay Mechanics

### Hệ thống Level & EXP
- Bắt đầu ở Level 1 với 0 EXP
- Hoàn thành nhiệm vụ để nhận EXP
- Mỗi level cần thêm 100 EXP (100, 200, 300...)
- Level up tự động khi đủ EXP

### 5 Chỉ số nhân vật
- **WILL** (Ý chí): Quyết tâm, kiên trì
- **PHY** (Thể chất): Sức khỏe, thể lực
- **MEN** (Tinh thần): Tư duy, học hỏi
- **AWR** (Nhận thức): Quan sát, hiểu biết
- **EXE** (Thực thi): Hành động, hoàn thành

### Độ khó nhiệm vụ
- ⭐ (1 sao): Dễ - 10-20 EXP
- ⭐⭐ (2 sao): Bình thường - 30-40 EXP
- ⭐⭐⭐ (3 sao): Khó - 50-70 EXP
- ⭐⭐⭐⭐ (4 sao): Rất khó - 80-100 EXP
- ⭐⭐⭐⭐⭐ (5 sao): Cực khó - 100+ EXP

### Ưu tiên nhiệm vụ
- 🔴 **High**: Ưu tiên cao, hiển thị trong dashboard
- 🟡 **Medium**: Ưu tiên trung bình
- ⚪ **Low**: Ưu tiên thấp

### Hạng danh hiệu
- 🥉 **Bronze**: Dễ đạt được
- 🥈 **Silver**: Cần nỗ lực
- 🥇 **Gold**: Khó khăn
- 👑 **Legendary**: Cực kỳ hiếm

## 🔧 Customization

### Thay đổi giao diện
Chỉnh sửa file `components/ui_components.py` để thay đổi CSS và theme.

### Thêm tính năng mới
- Tạo component mới trong `components/`
- Thêm data model trong `data_models.py`
- Cập nhật logic trong `main.py`

### Tích hợp API khác
Chỉnh sửa `components/google_sheets.py` để tích hợp với các service khác.

## 🐛 Troubleshooting

### Lỗi kết nối Google Sheets
1. Kiểm tra API Key có đúng không
2. Kiểm tra Sheet ID có đúng không
3. Đảm bảo đã bật Google Sheets API
4. Kiểm tra quyền chia sẻ của Sheet

### Ứng dụng chạy chậm
1. Tắt auto-sync nếu không cần thiết
2. Giảm tần suất đồng bộ
3. Kiểm tra kết nối internet

### Dữ liệu bị mất
1. Dữ liệu được lưu trên Google Sheets
2. Kiểm tra file `levelup_settings.json` để backup cài đặt
3. Sync lại từ Google Sheets

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📞 Support

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra phần Troubleshooting
2. Tạo Issue trên GitHub
3. Liên hệ qua email

---

**🎯 Hãy bắt đầu hành trình RPG Self-Development của bạn ngay hôm nay!**