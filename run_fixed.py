#!/usr/bin/env python3
"""
修复版启动脚本 - 解决登录页面检测问题
"""

import os
import sys

def main():
    # 设置用户凭证（你之前输入的）
    os.environ["LINUXDO_USERNAME"] = "alenlsp"
    os.environ["LINUXDO_PASSWORD"] = "2TuJ6@c9xpFX4@z"
    
    print("=" * 60)
    print("LinuxDo Auto Check-in - Fixed Version")
    print("=" * 60)
    print("✅ Using credentials: alenlsp")
    print("🚀 Starting optimized version with fixes...")
    print("=" * 60)
    
    try:
        # 直接导入并运行优化版本
        from main_optimized import LinuxDoBrowserOptimized
        
        # 创建并运行浏览器实例
        browser = LinuxDoBrowserOptimized()
        success = browser.run()
        
        print("\n" + "=" * 60)
        if success:
            print("✅ 程序执行成功！")
        else:
            print("⚠️ 程序执行完成，但可能遇到了一些问题")
        print("=" * 60)
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    try:
        result = main()
        input("按回车键退出...")
        sys.exit(result)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0)
