# 📤 GitHub上传指南

## 方式1：网页版上传（推荐）

### 步骤1：创建仓库
1. 访问 https://github.com
2. 登录账号
3. 点击右上角 "+" → "New repository"
4. 设置：
   - 名称：`linuxdo-auto-checkin`
   - 描述：`LinuxDo自动签到工具`
   - 类型：Public
   - ✅ Add README file
5. 创建仓库

### 步骤2：上传文件
1. 在仓库页面点击 "uploading an existing file"
2. 将本项目所有文件拖拽上传
3. 写提交信息：`Initial commit`
4. 点击 "Commit changes"

## 方式2：Git命令行

```bash
# 进入项目目录
cd linuxdo-checkin-main

# 初始化Git
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit - LinuxDo auto checkin tool"

# 添加远程仓库（替换YOUR_USERNAME为你的GitHub用户名）
git remote add origin https://github.com/YOUR_USERNAME/linuxdo-auto-checkin.git

# 推送到GitHub
git push -u origin main
```

## 文件检查清单

确保上传以下文件：
- ✅ main_optimized.py
- ✅ config.py  
- ✅ run_fixed.py
- ✅ requirements.txt
- ✅ README.md
- ✅ DEPLOY.md
- ✅ .github/workflows/auto-checkin.yml
- ✅ turnstilePatch/manifest.json
- ✅ turnstilePatch/script.js

## 上传后检查

1. 确认所有文件都已上传
2. 检查 README.md 显示正常
3. 进入 Actions 选项卡，应该能看到工作流
