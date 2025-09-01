#!/usr/bin/env python3
"""
快速测试脚本 - 用于验证基础功能
"""

import os
import sys

def main():
    print("=" * 60)
    print("LinuxDo Auto Check-in - Quick Test")
    print("=" * 60)
    
    # 检查环境变量
    username = os.environ.get("LINUXDO_USERNAME")
    password = os.environ.get("LINUXDO_PASSWORD")
    
    if not username:
        print("❌ LINUXDO_USERNAME not found")
        return False
        
    if not password:
        print("❌ LINUXDO_PASSWORD not found")
        return False
    
    print(f"✅ Username: {username}")
    print(f"✅ Password: {'*' * len(password)}")
    
    # 测试依赖
    print("\nTesting dependencies...")
    
    dependencies = [
        ("DrissionPage", "DrissionPage"),
        ("loguru", "loguru"), 
        ("requests", "requests"),
        ("tabulate", "tabulate")
    ]
    
    all_deps_ok = True
    for module_name, display_name in dependencies:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: OK")
        except ImportError:
            print(f"❌ {display_name}: Missing")
            all_deps_ok = False
    
    if not all_deps_ok:
        print("\n❌ Some dependencies are missing. Run: pip install -r requirements.txt")
        return False
    
    # 检查文件
    print("\nChecking files...")
    
    required_files = [
        "main_optimized.py",
        "config.py",
        "turnstilePatch/manifest.json",
        "turnstilePatch/script.js"
    ]
    
    all_files_ok = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}: OK")
        else:
            print(f"❌ {file_path}: Missing")
            all_files_ok = False
    
    if not all_files_ok:
        print("\n❌ Some required files are missing")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 All tests passed! Ready to run the main program.")
    print("   Run: python main_optimized.py")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
