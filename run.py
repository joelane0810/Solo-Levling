#!/usr/bin/env python3
"""
Level Up - RPG Self-Development Application Launcher
Khởi chạy ứng dụng với cấu hình tối ưu
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Kiểm tra và cài đặt dependencies"""
    requirements_file = Path("requirements.txt")
    
    if not requirements_file.exists():
        print("❌ Không tìm thấy file requirements.txt")
        sys.exit(1)
    
    try:
        import streamlit
        print("✅ Streamlit đã được cài đặt")
    except ImportError:
        print("📦 Đang cài đặt dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Đã cài đặt xong dependencies")

def setup_environment():
    """Thiết lập môi trường"""
    # Tạo thư mục components nếu chưa có
    components_dir = Path("components")
    components_dir.mkdir(exist_ok=True)
    
    # Tạo file __init__.py trong components
    init_file = components_dir / "__init__.py"
    if not init_file.exists():
        init_file.write_text("")
    
    # Tạo thư mục utils nếu chưa có
    utils_dir = Path("utils")
    utils_dir.mkdir(exist_ok=True)
    
    # Tạo file __init__.py trong utils
    utils_init = utils_dir / "__init__.py"
    if not utils_init.exists():
        utils_init.write_text("")
    
    print("✅ Đã thiết lập môi trường")

def check_main_file():
    """Kiểm tra file main.py"""
    main_file = Path("main.py")
    if not main_file.exists():
        print("❌ Không tìm thấy file main.py")
        print("📝 Vui lòng tạo file main.py với nội dung từ hướng dẫn")
        sys.exit(1)
    
    print("✅ File main.py đã sẵn sàng")

def run_app():
    """Chạy ứng dụng Streamlit"""
    print("🚀 Đang khởi chạy Level Up - RPG Self-Development...")
    print("📱 Ứng dụng sẽ mở tại: http://localhost:8501")
    print("🛑 Nhấn Ctrl+C để dừng ứng dụng")
    print("-" * 50)
    
    # Cấu hình Streamlit
    os.environ["STREAMLIT_BROWSER_GATHER_USAGE_STATS"] = "false"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "main.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--theme.base", "dark",
            "--theme.primaryColor", "#3B82F6",
            "--theme.backgroundColor", "#0f0f0f",
            "--theme.secondaryBackgroundColor", "#1a1a2e",
            "--theme.textColor", "#ffffff"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Ứng dụng đã được dừng")
    except Exception as e:
        print(f"❌ Lỗi khởi chạy ứng dụng: {e}")

def main():
    """Hàm chính"""
    print("⚡ Level Up - RPG Self-Development ⚡")
    print("=" * 50)
    
    # Kiểm tra các điều kiện trước khi chạy
    check_dependencies()
    setup_environment()
    check_main_file()
    
    # Chạy ứng dụng
    run_app()

if __name__ == "__main__":
    main()