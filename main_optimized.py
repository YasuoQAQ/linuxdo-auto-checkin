"""
cron: 0 */6 * * *
new Env("Linux.Do 签到")
优化版本 - 使用配置文件和增强的反检测机制
"""

import os
import random
import time
import functools
import sys
import requests
import re
import json
from loguru import logger
from DrissionPage import ChromiumOptions, Chromium
from tabulate import tabulate
from config import Config


def retry_decorator(retries=3, delay=1, backoff=1.5):
    """增强的重试装饰器"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:
                        logger.error(f"函数 {func.__name__} 最终执行失败: {str(e)}")
                        raise e
                    
                    wait_time = delay * (backoff ** attempt)
                    logger.warning(
                        f"函数 {func.__name__} 第 {attempt + 1}/{retries} 次尝试失败: {str(e)}"
                    )
                    logger.info(f"等待 {wait_time:.1f} 秒后重试...")
                    time.sleep(wait_time)
            return None
        return wrapper
    return decorator


class LinuxDoBrowserOptimized:
    """优化版 LinuxDo 浏览器类"""
    
    def __init__(self):
        self.config = Config()
        self.browser = None
        self.page = None
        self.setup_browser()
        
    def setup_browser(self):
        """设置浏览器配置"""
        try:
            EXTENSION_PATH = os.path.abspath(
                os.path.join(os.path.dirname(__file__), "turnstilePatch")
            )
            
            # 获取随机配置
            chrome_version = self.config.get_random_chrome_version()
            width, height = self.config.get_random_window_size()
            user_agent = self.config.get_random_user_agent()
            
            logger.info(f"使用 Chrome 版本: {chrome_version}")
            logger.info(f"窗口大小: {width}x{height}")
            
            # 创建浏览器选项
            co = ChromiumOptions()
            
            # 基础设置
            co.headless(self.config.HEADLESS)
            co.incognito(True)
            
            # 安全和性能设置
            co.set_argument("--no-sandbox")
            co.set_argument("--disable-dev-shm-usage")
            co.set_argument("--disable-gpu")
            co.set_argument("--disable-software-rasterizer")
            
            # 反检测设置
            co.set_argument("--disable-blink-features=AutomationControlled")
            co.set_argument("--disable-extensions-except=" + EXTENSION_PATH)
            co.set_argument("--load-extension=" + EXTENSION_PATH)
            co.set_argument("--disable-plugins-discovery")
            co.set_argument("--disable-web-security")
            co.set_argument("--disable-features=VizDisplayCompositor")
            co.set_argument("--no-first-run")
            co.set_argument("--no-default-browser-check")
            co.set_argument("--disable-default-apps")
            co.set_argument("--disable-component-extensions-with-background-pages")
            
            # 窗口和显示设置
            co.set_argument(f"--window-size={width},{height}")
            co.set_argument("--start-maximized")
            
            # 语言和地区设置
            co.set_argument("--lang=zh-CN")
            co.set_argument("--accept-lang=zh-CN,zh;q=0.9,en;q=0.8")
            
            # User-Agent 设置
            co.set_user_agent(user_agent)
            
            # 代理设置
            if self.config.PROXY_URL:
                co.set_argument(f"--proxy-server={self.config.PROXY_URL}")
                logger.info(f"使用代理: {self.config.PROXY_URL}")
            
            # 其他优化设置
            co.set_argument("--disable-background-timer-throttling")
            co.set_argument("--disable-backgrounding-occluded-windows")
            co.set_argument("--disable-renderer-backgrounding")
            co.set_argument("--disable-features=TranslateUI")
            co.set_argument("--disable-ipc-flooding-protection")
            
            # 创建浏览器实例
            self.browser = Chromium(co)
            self.page = self.browser.new_tab()
            
            # 注入反检测脚本
            self.inject_stealth_scripts()
            
            logger.success("浏览器初始化成功")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}")
            raise
    
    def inject_stealth_scripts(self):
        """注入反检测脚本"""
        stealth_js = """
        // 高级反检测脚本
        (() => {
            'use strict';
            
            // 覆盖 webdriver 属性
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
                configurable: true
            });
            
            // 删除 webdriver 相关属性
            delete navigator.__proto__.webdriver;
            
            // 覆盖 Chrome 运行时
            window.chrome = {
                runtime: {},
                loadTimes: function() {
                    return {
                        commitLoadTime: Math.random() * 1000 + 1000,
                        finishDocumentLoadTime: Math.random() * 1000 + 2000,
                        finishLoadTime: Math.random() * 1000 + 3000,
                        firstPaintAfterLoadTime: 0,
                        firstPaintTime: Math.random() * 1000 + 1500,
                        navigationType: 'Other',
                        npnNegotiatedProtocol: 'h2',
                        requestTime: Date.now() / 1000 - Math.random() * 10,
                        startLoadTime: Math.random() * 1000 + 500,
                        wasAlternateProtocolAvailable: false,
                        wasFetchedViaSpdy: true,
                        wasNpnNegotiated: true
                    };
                },
                csi: function() {
                    return {
                        pageT: Math.random() * 1000 + 2000,
                        startE: Date.now() - Math.random() * 10000,
                        tran: Math.floor(Math.random() * 20) + 1
                    };
                }
            };
            
            // 覆盖权限
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // 随机化 canvas 指纹
            const shift = {
                'r': Math.floor(Math.random() * 10) - 5,
                'g': Math.floor(Math.random() * 10) - 5,
                'b': Math.floor(Math.random() * 10) - 5,
                'a': Math.floor(Math.random() * 10) - 5
            };
            
            const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
            const originalToBlob = HTMLCanvasElement.prototype.toBlob;
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            
            HTMLCanvasElement.prototype.toDataURL = function() {
                if (this.width && this.height) {
                    const context = this.getContext('2d');
                    const imageData = context.getImageData(0, 0, this.width, this.height);
                    for (let i = 0; i < imageData.data.length; i += 4) {
                        imageData.data[i] = Math.max(0, Math.min(255, imageData.data[i] + shift.r));
                        imageData.data[i + 1] = Math.max(0, Math.min(255, imageData.data[i + 1] + shift.g));
                        imageData.data[i + 2] = Math.max(0, Math.min(255, imageData.data[i + 2] + shift.b));
                        imageData.data[i + 3] = Math.max(0, Math.min(255, imageData.data[i + 3] + shift.a));
                    }
                    context.putImageData(imageData, 0, 0);
                }
                return originalToDataURL.apply(this, arguments);
            };
            
            // 覆盖 WebGL
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {
                if (parameter === 37445) {
                    return 'Intel Inc.';
                }
                if (parameter === 37446) {
                    return 'Intel Iris OpenGL Engine';
                }
                return getParameter(parameter);
            };
            
            // 覆盖插件
            Object.defineProperty(navigator, 'plugins', {
                get: () => {
                    return [
                        {
                            0: {type: "application/x-google-chrome-pdf", suffixes: "pdf", description: "Portable Document Format"},
                            description: "Portable Document Format",
                            filename: "internal-pdf-viewer",
                            length: 1,
                            name: "Chrome PDF Plugin"
                        },
                        {
                            0: {type: "application/pdf", suffixes: "pdf", description: ""},
                            description: "",
                            filename: "mhjfbmdgcfjbbpaeojofohoefgiehjai",
                            length: 1,
                            name: "Chrome PDF Viewer"
                        }
                    ];
                }
            });
            
            // 覆盖语言
            Object.defineProperty(navigator, 'languages', {
                get: () => ['zh-CN', 'zh', 'en-US', 'en']
            });
            
            // 模拟真实的鼠标事件
            let mouseEvents = ['mousedown', 'mouseup', 'mousemove'];
            mouseEvents.forEach(eventType => {
                document.addEventListener(eventType, function(e) {
                    if (Math.random() < 0.01) {
                        console.debug(`Mouse event: ${eventType} at ${e.clientX}, ${e.clientY}`);
                    }
                }, true);
            });
            
            console.log('Enhanced stealth script injected successfully');
        })();
        """
        
        try:
            self.page.run_js(stealth_js)
            logger.success("反检测脚本注入成功")
        except Exception as e:
            logger.warning(f"反检测脚本注入失败: {str(e)}")
    
    @retry_decorator(retries=5, delay=3, backoff=1.5)
    def get_turnstile_token(self):
        """获取 Turnstile Token"""
        logger.info("开始处理 Turnstile 验证")
        
        # 重置 turnstile
        self.page.run_js("try { if (typeof turnstile !== 'undefined') turnstile.reset(); } catch(e) { }")
        
        # 等待页面稳定
        time.sleep(random.uniform(3, 5))
        
        for attempt in range(12):
            try:
                # 检查是否已有 token
                existing_token = self.page.run_js(
                    "try { return typeof turnstile !== 'undefined' ? turnstile.getResponse() : null; } catch(e) { return null; }"
                )
                
                if existing_token:
                    logger.success(f"获取到现有 Turnstile Token: {existing_token[:20]}...")
                    return existing_token
                
                # 查找 Turnstile 元素
                turnstile_elements = self.page.eles("[name='cf-turnstile-response']", timeout=2)
                if not turnstile_elements:
                    logger.debug("未找到 Turnstile 元素")
                    time.sleep(random.uniform(2, 4))
                    continue
                
                turnstile_element = turnstile_elements[0]
                logger.info("找到 Turnstile 验证元素")
                
                # 获取父元素
                parent_element = turnstile_element.parent()
                if not parent_element:
                    logger.warning("无法获取 Turnstile 父元素")
                    continue
                
                # 尝试处理 shadow DOM
                try:
                    shadow_root = parent_element.shadow_root
                    if shadow_root:
                        iframe = shadow_root.ele("iframe", timeout=3)
                        if iframe:
                            # 切换到 iframe 内容
                            iframe_doc = iframe.ele("body", timeout=3)
                            if iframe_doc and iframe_doc.shadow_root:
                                challenge_input = iframe_doc.shadow_root.ele("input", timeout=3)
                                if challenge_input:
                                    logger.info("找到验证按钮，准备点击")
                                    
                                    # 模拟人类行为
                                    time.sleep(random.uniform(1, 2))
                                    challenge_input.click()
                                    logger.info("已点击验证按钮")
                                    
                                    # 等待验证完成
                                    for wait_attempt in range(10):
                                        time.sleep(1)
                                        token = self.page.run_js(
                                            "try { return typeof turnstile !== 'undefined' ? turnstile.getResponse() : null; } catch(e) { return null; }"
                                        )
                                        if token:
                                            logger.success(f"验证成功，获取到 Token: {token[:20]}...")
                                            return token
                                        
                                        if wait_attempt % 3 == 0:
                                            logger.info(f"等待验证完成... ({wait_attempt + 1}/10)")
                except Exception as e:
                    logger.debug(f"处理 shadow DOM 时出错: {str(e)}")
                
                logger.info(f"第 {attempt + 1} 次尝试，等待重试...")
                time.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.warning(f"获取 Turnstile Token 时出错 (尝试 {attempt + 1}): {str(e)}")
                time.sleep(random.uniform(1, 3))
        
        logger.warning("未能获取到 Turnstile Token，继续尝试登录")
        return None
    
    @retry_decorator(retries=3, delay=5)
    def login(self):
        """登录功能 - 增强版本基于视觉识别"""
        logger.info("开始登录 LinuxDo")
        
        try:
            # 访问登录页面
            self.page.get(self.config.LOGIN_URL)
            logger.info("正在加载登录页面...")
            
            # 等待页面完全加载
            time.sleep(random.uniform(4, 6))
            
            # 检查页面是否正确加载
            page_title = self.page.title
            current_url = self.page.url.lower()
            
            logger.info(f"页面加载完成，标题: {page_title}")
            logger.info(f"当前URL: {current_url}")
            
            # 检查是否在正确的域名
            if "linux.do" not in current_url:
                logger.error(f"页面加载异常，当前URL: {self.page.url}")
                return False
            
            # 如果不在登录页面，尝试跳转到登录页面
            if "login" not in current_url:
                logger.info("当前不在登录页面，尝试跳转...")
                
                # 查找登录链接或按钮
                login_selectors = [
                    "a[href*='login']",
                    ".login",
                    ".sign-in", 
                    "[data-modal='login']",
                    ".header-login"
                ]
                
                login_found = False
                for selector in login_selectors:
                    elements = self.page.eles(selector, timeout=3)
                    if elements:
                        logger.info(f"找到登录入口: {selector}")
                        elements[0].click()
                        time.sleep(random.uniform(2, 4))
                        login_found = True
                        break
                
                if not login_found:
                    logger.warning("未找到登录入口，直接访问登录URL")
                    self.page.get(self.config.LOGIN_URL)
                    time.sleep(random.uniform(2, 4))
            
            # 检查是否在GitHub Actions环境中
            is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
            
            if not is_github_actions:
                # 只在非GitHub Actions环境中处理 Turnstile 验证
                turnstile_token = self.get_turnstile_token()
                if turnstile_token:
                    logger.info("Turnstile 验证成功")
            else:
                logger.info("GitHub Actions环境检测到，跳过Turnstile验证，直接使用JavaScript登录")
            
            # 尝试使用JavaScript直接登录（基于视觉识别的方法）
            return self.javascript_login()
            
            # 保存登录页面截图
            try:
                self.page.get_screenshot("login_debug.png")
                logger.debug("已保存登录页面截图")
            except:
                pass
            
            # 查找并填写用户名
            username_selectors = [
                "#login-account-name", 
                "[name='login']", 
                "input[type='text']",
                "input[placeholder*='用户名']",
                "input[placeholder*='邮箱']",
                "input[placeholder*='email']",
                ".login-form input[type='text']",
                "#username",
                "#email"
            ]
            username_input = None
            
            logger.info("正在查找用户名输入框...")
            for selector in username_selectors:
                elements = self.page.eles(selector, timeout=2)
                if elements:
                    logger.success(f"找到用户名输入框: {selector}")
                    username_input = elements[0]
                    break
                else:
                    logger.debug(f"未找到元素: {selector}")
            
            if not username_input:
                logger.error("未找到用户名输入框，尝试所有可能的输入框")
                # 尝试查找所有输入框
                all_inputs = self.page.eles("input", timeout=5)
                if all_inputs and len(all_inputs) >= 2:
                    logger.info(f"找到 {len(all_inputs)} 个输入框，使用第一个作为用户名")
                    username_input = all_inputs[0]
                else:
                    logger.error("完全找不到输入框")
                    return False
            
            # 清空并输入用户名
            username_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            # 模拟人类输入
            for char in self.config.USERNAME:
                username_input.input(char)
                time.sleep(random.uniform(0.08, 0.2))
            
            logger.info("用户名输入完成")
            time.sleep(random.uniform(0.5, 1.5))
            
            # 查找并填写密码
            password_selectors = [
                "#login-account-password", 
                "[name='password']", 
                "input[type='password']",
                "input[placeholder*='密码']",
                "input[placeholder*='password']",
                ".login-form input[type='password']",
                "#password"
            ]
            password_input = None
            
            logger.info("正在查找密码输入框...")
            for selector in password_selectors:
                elements = self.page.eles(selector, timeout=2)
                if elements:
                    logger.success(f"找到密码输入框: {selector}")
                    password_input = elements[0]
                    break
                else:
                    logger.debug(f"未找到元素: {selector}")
            
            if not password_input:
                logger.error("未找到密码输入框，尝试查找第二个输入框")
                # 尝试查找所有输入框
                all_inputs = self.page.eles("input", timeout=5)
                if all_inputs and len(all_inputs) >= 2:
                    logger.info(f"找到 {len(all_inputs)} 个输入框，使用第二个作为密码")
                    password_input = all_inputs[1]
                else:
                    logger.error("完全找不到密码输入框")
                    return False
            
            # 清空并输入密码
            password_input.clear()
            time.sleep(random.uniform(0.5, 1))
            
            # 模拟人类输入
            for char in self.config.PASSWORD:
                password_input.input(char)
                time.sleep(random.uniform(0.08, 0.2))
            
            logger.info("密码输入完成")
            time.sleep(random.uniform(1, 2))
            
            # 查找并点击登录按钮
            login_selectors = [
                "#login-button", 
                ".btn-primary", 
                "button[type='submit']", 
                ".login-button",
                "button:contains('登录')",
                "button:contains('登入')",
                "button:contains('Sign')",
                ".login-form button",
                "input[type='submit']",
                ".btn:contains('登录')"
            ]
            login_button = None
            
            logger.info("正在查找登录按钮...")
            for selector in login_selectors:
                elements = self.page.eles(selector, timeout=2)
                if elements:
                    logger.success(f"找到登录按钮: {selector}")
                    login_button = elements[0]
                    break
                else:
                    logger.debug(f"未找到元素: {selector}")
            
            if not login_button:
                logger.error("未找到登录按钮，尝试查找所有按钮")
                # 尝试查找所有按钮
                all_buttons = self.page.eles("button", timeout=5)
                if all_buttons:
                    logger.info(f"找到 {len(all_buttons)} 个按钮，使用最后一个")
                    login_button = all_buttons[-1]  # 通常登录按钮是最后一个
                else:
                    logger.error("完全找不到登录按钮")
                    return False
            
            logger.info("点击登录按钮")
            login_button.click()
            
            # 等待登录结果
            login_success = False
            for i in range(20):  # 增加等待时间
                time.sleep(2)
                
                # 检查是否登录成功 - 多种方式检测
                success_indicators = [
                    "#current-user",
                    ".header-dropdown-toggle",
                    ".user-menu",
                    "[data-user-card]"
                ]
                
                for indicator in success_indicators:
                    if self.page.eles(indicator, timeout=1):
                        logger.success("登录成功！")
                        return True
                
                # 检查当前 URL
                current_url = self.page.url.lower()
                if "login" not in current_url and "linux.do" in current_url:
                    logger.success("登录成功（URL 检测）")
                    return True
                
                # 检查错误信息
                error_selectors = [".alert-error", ".error", ".flash-error", "[class*='error']"]
                for selector in error_selectors:
                    error_elements = self.page.eles(selector, timeout=1)
                    if error_elements:
                        error_text = error_elements[0].text
                        if error_text.strip():
                            logger.error(f"登录失败，错误信息: {error_text}")
                            return False
                
                # 检查是否需要额外验证
                if any(keyword in current_url for keyword in ["challenge", "verify", "captcha"]):
                    logger.warning("可能需要额外验证，继续等待...")
                    time.sleep(5)
                    continue
                
                if i % 5 == 0:
                    logger.info(f"等待登录结果... ({i+1}/20)")
            
            logger.error("登录超时，未能确认登录状态")
            return False
            
        except Exception as e:
            logger.error(f"登录过程中出现异常: {str(e)}")
            return False
    
    def javascript_login(self):
        """使用JavaScript直接登录 - 基于页面视觉结构"""
        logger.info("尝试使用JavaScript直接登录...")
        
        try:
            # 等待页面完全加载
            for i in range(10):
                time.sleep(1)
                logger.info(f"等待页面渲染完成... ({i+1}/10)")
                
                # 检查是否有输入框
                input_count = self.page.run_js("return document.querySelectorAll('input').length;")
                if input_count >= 2:
                    logger.success(f"检测到 {input_count} 个输入框，开始登录")
                    break
                elif i == 9:
                    logger.warning("未检测到足够的输入框，强制尝试登录")
            
            # JavaScript登录脚本 - 修复async问题
            login_script = f"""
            (async function() {{
                try {{
                    console.log('开始JavaScript登录...');
                    
                    // 查找所有输入框
                    let inputs = document.querySelectorAll('input');
                    console.log('找到输入框数量:', inputs.length);
                    
                    if (inputs.length >= 2) {{
                        // 方法1: 直接填写前两个输入框
                        console.log('尝试填写输入框...');
                        
                        // 用户名输入框（第一个）
                        inputs[0].focus();
                        inputs[0].value = '{self.config.USERNAME}';
                        inputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                        inputs[0].dispatchEvent(new Event('change', {{ bubbles: true }}));
                        console.log('用户名填写完成');
                        
                        // 等待一下
                        await new Promise(resolve => setTimeout(resolve, 500));
                        
                        // 密码输入框（第二个）
                        inputs[1].focus();
                        inputs[1].value = '{self.config.PASSWORD}';
                        inputs[1].dispatchEvent(new Event('input', {{ bubbles: true }}));
                        inputs[1].dispatchEvent(new Event('change', {{ bubbles: true }}));
                        console.log('密码填写完成');
                        
                        // 等待一下
                        await new Promise(resolve => setTimeout(resolve, 1000));
                        
                        // 查找并点击登录按钮
                        let buttons = document.querySelectorAll('button');
                        console.log('找到按钮数量:', buttons.length);
                        
                        for (let btn of buttons) {{
                            if (btn.textContent.includes('登录') || btn.textContent.includes('Login') || btn.type === 'submit') {{
                                console.log('找到登录按钮，准备点击');
                                btn.click();
                                return '登录按钮已点击';
                            }}
                        }}
                        
                        // 如果没找到特定按钮，点击最后一个按钮
                        if (buttons.length > 0) {{
                            console.log('点击最后一个按钮');
                            buttons[buttons.length - 1].click();
                            return '点击了最后一个按钮';
                        }}
                        
                        // 尝试按Enter键提交
                        inputs[1].dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter'}}));
                        return '按Enter键提交';
                    }}
                    
                    // 方法2: 通过占位符查找
                    let emailInput = document.querySelector('input[placeholder*="邮件"], input[placeholder*="用户名"], input[placeholder*="email"], input[placeholder*="username"]');
                    let passwordInput = document.querySelector('input[type="password"], input[placeholder*="密码"], input[placeholder*="password"]');
                    
                    if (emailInput && passwordInput) {{
                        console.log('通过占位符找到输入框');
                        emailInput.focus();
                        emailInput.value = '{self.config.USERNAME}';
                        emailInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        
                        await new Promise(resolve => setTimeout(resolve, 500));
                        
                        passwordInput.focus();
                        passwordInput.value = '{self.config.PASSWORD}';
                        passwordInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        
                        // 查找提交按钮
                        let submitBtn = document.querySelector('button[type="submit"], input[type="submit"]');
                        if (submitBtn) {{
                            submitBtn.click();
                            return '通过占位符方法登录';
                        }}
                    }}
                    
                    return '未找到合适的输入框';
                    
                }} catch (error) {{
                    console.error('JavaScript登录出错:', error);
                    return 'JavaScript执行失败: ' + error.message;
                }}
            }})()
            """
            
            # 执行JavaScript登录
            try:
                result = self.page.run_js(login_script, as_expr=True)
                logger.info(f"JavaScript执行结果: {result}")
            except Exception as e:
                logger.warning(f"JavaScript执行出错，尝试简化版本: {e}")
                # 简化版本，不使用async
                simple_script = f"""
                try {{
                    console.log('使用简化JavaScript登录...');
                    let inputs = document.querySelectorAll('input');
                    console.log('找到输入框数量:', inputs.length);
                    
                    if (inputs.length >= 2) {{
                        inputs[0].focus();
                        inputs[0].value = '{self.config.USERNAME}';
                        inputs[0].dispatchEvent(new Event('input', {{ bubbles: true }}));
                        
                        inputs[1].focus();
                        inputs[1].value = '{self.config.PASSWORD}';
                        inputs[1].dispatchEvent(new Event('input', {{ bubbles: true }}));
                        
                        let buttons = document.querySelectorAll('button');
                        for (let btn of buttons) {{
                            if (btn.textContent.includes('登录') || btn.textContent.includes('Login')) {{
                                btn.click();
                                return '简化登录成功';
                            }}
                        }}
                        
                        if (buttons.length > 0) {{
                            buttons[buttons.length - 1].click();
                            return '点击最后按钮';
                        }}
                        
                        inputs[1].dispatchEvent(new KeyboardEvent('keydown', {{key: 'Enter'}}));
                        return '按Enter提交';
                    }}
                    return '未找到输入框';
                }} catch (error) {{
                    return 'JavaScript出错: ' + error.message;
                }}
                """
                result = self.page.run_js(simple_script)
                logger.info(f"简化JavaScript执行结果: {result}")
            
            # 等待登录结果
            logger.info("等待登录结果...")
            for i in range(15):
                time.sleep(2)
                
                current_url = self.page.url.lower()
                page_title = self.page.title
                
                logger.info(f"检查登录状态 ({i+1}/15): {current_url}")
                
                # 检查URL变化
                if "login" not in current_url:
                    logger.success("✅ 登录成功！URL已跳转")
                    return True
                
                # 检查是否有用户相关元素
                user_elements = [
                    "#current-user",
                    ".header-dropdown-toggle", 
                    ".user-menu",
                    "[data-user-card]",
                    ".user-avatar"
                ]
                
                for selector in user_elements:
                    if self.page.eles(selector, timeout=1):
                        logger.success(f"✅ 登录成功！找到用户元素: {selector}")
                        return True
                
                # 检查错误信息
                error_selectors = [".alert-error", ".error", ".flash-error"]
                for selector in error_selectors:
                    error_elements = self.page.eles(selector, timeout=1)
                    if error_elements:
                        error_text = error_elements[0].text
                        if error_text.strip():
                            logger.error(f"❌ 登录失败: {error_text}")
                            return False
            
            logger.warning("⚠️ 登录结果不确定，继续执行")
            return True
            
        except Exception as e:
            logger.error(f"JavaScript登录失败: {str(e)}")
            return False
    
    def browse_topics(self):
        """浏览主题 - 改进版本"""
        try:
            logger.info("开始浏览主题")
            
            # 首先尝试访问最新页面，通常更容易找到主题
            urls_to_try = [
                "https://linux.do/latest",
                "https://linux.do/",
                "https://linux.do/c/tech/8",
                "https://linux.do/c/life/7"
            ]
            
            topics = []
            
            for url in urls_to_try:
                try:
                    logger.info(f"尝试访问: {url}")
                    self.page.get(url)
                    time.sleep(random.uniform(4, 7))  # 增加等待时间
                    
                    # 等待页面动态内容加载
                    logger.info("等待页面动态内容加载...")
                    for wait_count in range(5):
                        time.sleep(2)
                        # 检查是否有链接加载出来
                        link_count = self.page.run_js("return document.querySelectorAll('a[href*=\"/t/\"]').length;")
                        if link_count > 5:
                            logger.success(f"检测到 {link_count} 个主题链接")
                            break
                        logger.debug(f"等待中... 当前链接数: {link_count}")
                    
                    # 使用更精确的选择器查找主题，优先使用旧项目中成功的选择器
                    topic_selectors = [
                        # 旧项目中成功的选择器（优先级最高）
                        "#list-area .title",
                        "#list-area .title a",
                        # Discourse 论坛的标准选择器
                        ".topic-list-item .main-link a",
                        ".topic-list .title a", 
                        ".topic-list-body .title a",
                        "tbody tr .main-link a",
                        # 通用选择器
                        "a[href*='/t/'][title]",
                        "a[href*='/t/']:not([href*='/edit']):not([href*='/raw'])",
                        # 备用选择器
                        ".topic-title a",
                        ".raw-topic-link"
                    ]
                    
                    for selector in topic_selectors:
                        elements = self.page.eles(selector, timeout=3)
                        if elements and len(elements) >= 3:  # 至少要有3个主题
                            # 过滤有效的主题链接
                            valid_topics = []
                            for element in elements:
                                href = element.attr("href")
                                text = element.text
                                if (href and "/t/" in href and 
                                    text and len(text.strip()) > 5 and  # 标题长度过滤
                                    not any(skip in href.lower() for skip in ['/edit', '/raw', '/print'])):
                                    valid_topics.append(element)
                            
                            if len(valid_topics) >= 3:
                                topics = valid_topics
                                logger.success(f"在 {url} 使用选择器 '{selector}' 找到 {len(topics)} 个有效主题")
                                break
                    
                    if topics:
                        break
                        
                except Exception as e:
                    logger.warning(f"访问 {url} 失败: {str(e)}")
                    continue
            
            # 如果仍然没找到，尝试用JavaScript查找
            if not topics:
                logger.warning("CSS选择器未找到主题，尝试JavaScript查找...")
                try:
                    js_topics = self.page.run_js("""
                        // 查找各种可能的主题链接
                        let links = [];
                        
                        // 方法1: 查找包含/t/的链接
                        document.querySelectorAll('a[href*="/t/"]').forEach(a => {{
                            if (a.textContent.trim() && a.href.includes('/t/')) {{
                                links.push(a);
                            }}
                        }});
                        
                        // 方法2: 查找标题类元素
                        document.querySelectorAll('.title, .topic-title, .main-link').forEach(el => {{
                            let link = el.querySelector('a') || el;
                            if (link.href && link.href.includes('/t/')) {{
                                links.push(link);
                            }}
                        }});
                        
                        // 去重
                        let uniqueLinks = [...new Set(links)];
                        console.log('JavaScript找到主题数量:', uniqueLinks.length);
                        
                        return uniqueLinks.length;
                    """)
                    
                    if js_topics > 0:
                        logger.info(f"JavaScript找到 {js_topics} 个主题链接")
                        # 重新用JavaScript获取的信息来查找元素
                        topics = self.page.eles('a[href*="/t/"]', timeout=5)
                        if topics:
                            logger.success(f"使用JavaScript方法找到 {len(topics)} 个主题")
                except Exception as e:
                    logger.debug(f"JavaScript搜索失败: {e}")
            
            if not topics:
                logger.warning("未找到主题列表，尝试访问具体版块...")
                # 尝试访问一些具体的版块
                sections = [
                    "https://linux.do/c/tech/8",
                    "https://linux.do/c/life/7", 
                    "https://linux.do/latest"
                ]
                
                for section_url in sections:
                    try:
                        logger.info(f"尝试访问版块: {section_url}")
                        self.page.get(section_url)
                        time.sleep(random.uniform(2, 4))
                        
                        # 在版块页面查找主题
                        section_topics = self.page.eles('a[href*="/t/"]', timeout=5)
                        if section_topics:
                            topics = section_topics
                            logger.success(f"在版块 {section_url} 找到 {len(topics)} 个主题")
                            break
                    except Exception as e:
                        logger.debug(f"访问版块 {section_url} 失败: {e}")
                        continue
                
                if not topics:
                    logger.warning("所有方法都未找到主题列表，跳过浏览任务")
                    return
            
            # 随机选择主题
            topic_count = random.randint(self.config.MIN_TOPICS, min(len(topics), self.config.MAX_TOPICS))
            selected_topics = random.sample(topics[:30], topic_count)  # 从前30个中选择
            
            logger.info(f"发现 {len(topics)} 个主题，随机选择 {topic_count} 个进行浏览")
            
            for i, topic in enumerate(selected_topics):
                try:
                    topic_url = topic.attr("href")
                    if not topic_url:
                        continue
                    
                    if topic_url.startswith("/"):
                        topic_url = self.config.HOME_URL.rstrip("/") + topic_url
                    
                    topic_title = topic.text[:50] if topic.text else "未知主题"
                    logger.info(f"浏览第 {i+1} 个主题: {topic_title}...")
                    
                    self.browse_single_topic(topic_url)
                    
                    # 随机等待
                    wait_time = random.uniform(3, 8)
                    logger.debug(f"等待 {wait_time:.1f} 秒...")
                    time.sleep(wait_time)
                    
                except Exception as e:
                    logger.warning(f"浏览主题时出错: {str(e)}")
                    continue
            
            logger.success("主题浏览完成")
            
        except Exception as e:
            logger.error(f"浏览主题失败: {str(e)}")
    
    @retry_decorator(retries=2, delay=2)
    def browse_single_topic(self, topic_url):
        """浏览单个主题 - 基于旧项目逻辑优化"""
        new_page = None
        try:
            logger.debug(f"正在打开主题: {topic_url}")
            new_page = self.browser.new_tab()
            new_page.get(topic_url)
            
            # 等待页面加载
            time.sleep(random.uniform(3, 5))
            
            # 检查页面是否正确加载
            page_title = new_page.title
            if not page_title or "error" in page_title.lower():
                logger.warning(f"页面加载异常: {page_title}")
                return False
            
            logger.debug(f"页面加载成功: {page_title[:50]}...")
            
            # 基于旧项目的点赞概率 (30%)
            if random.random() < 0.3:
                logger.debug("准备尝试点赞...")
                self.click_like(new_page)
            else:
                logger.debug("跳过点赞（基于随机概率）")
            
            # 浏览帖子内容
            logger.debug("开始浏览帖子内容...")
            self.browse_post_content(new_page)
            
            logger.debug("单个主题浏览完成")
            return True
            
        except Exception as e:
            logger.warning(f"浏览单个主题失败: {str(e)}")
            return False
        finally:
            if new_page:
                try:
                    new_page.close()
                    logger.debug("已关闭主题页面")
                except:
                    pass
    
    def browse_post_content(self, page):
        """浏览帖子内容 - 基于旧项目优化的滚动逻辑"""
        try:
            # 基于旧项目的稳定参数
            max_scrolls = 10  # 最多滚动10次
            prev_url = None
            
            logger.debug(f"开始浏览帖子内容，最多滚动 {max_scrolls} 次")
            
            for scroll_num in range(max_scrolls):
                # 使用旧项目中成功的滚动距离范围
                scroll_distance = random.randint(550, 650)  # 550-650像素
                
                logger.debug(f"向下滚动 {scroll_distance} 像素... ({scroll_num+1}/{max_scrolls})")
                page.run_js(f"window.scrollBy(0, {scroll_distance})")
                
                # 记录当前页面URL（防止页面跳转）
                current_url = page.url
                logger.debug(f"当前页面: {current_url}")
                
                # 基于旧项目的提前退出概率
                if random.random() < 0.03:  # 3%概率随机退出
                    logger.debug("🎲 随机提前退出浏览")
                    break
                
                # 检查是否到达页面底部
                try:
                    at_bottom = page.run_js(
                        "return window.scrollY + window.innerHeight >= document.body.scrollHeight - 100"
                    )
                    
                    # 如果到达底部且URL没有变化，退出
                    if current_url != prev_url:
                        prev_url = current_url
                    elif at_bottom and prev_url == current_url:
                        logger.debug("📄 已到达页面底部，退出浏览")
                        break
                        
                except Exception as e:
                    logger.debug(f"检查页面底部时出错: {e}")
                
                # 使用旧项目的等待时间范围
                wait_time = random.uniform(2, 4)  # 2-4秒等待
                logger.debug(f"等待 {wait_time:.2f} 秒...")
                time.sleep(wait_time)
            
            logger.debug("帖子内容浏览完成")
                
        except Exception as e:
            logger.warning(f"浏览帖子内容时出错: {str(e)}")
    
    def click_like(self, page):
        """点赞功能 - 基于旧项目的成功经验改进"""
        try:
            # 基于旧项目的精确选择器
            like_selectors = [
                # 旧项目中成功的选择器
                '.discourse-reactions-reaction-button[title="点赞此帖子"]',
                # 其他可能的点赞按钮选择器
                '.discourse-reactions-reaction-button:not(.reacted)',
                '.like-button:not(.liked)',
                '[data-action="like"]:not(.liked)',
                '.btn-like:not(.liked)',
                # 通用点赞按钮选择器
                'button[title*="点赞"]',
                'button[aria-label*="点赞"]',
                '.topic-post .actions button[title*="点赞"]'
            ]
            
            like_button_found = None
            
            for selector in like_selectors:
                try:
                    elements = page.eles(selector, timeout=2)
                    if elements:
                        # 检查按钮是否可点击且未被点赞
                        for element in elements:
                            # 检查按钮状态
                            button_text = element.text.lower() if element.text else ""
                            title_attr = element.attr("title") or ""
                            class_attr = element.attr("class") or ""
                            
                            # 确保是未点赞的按钮
                            if (not any(reacted in class_attr.lower() for reacted in ['reacted', 'liked', 'active']) and
                                not any(reacted in title_attr.lower() for reacted in ['已点赞', 'liked']) and
                                "点赞" in title_attr):
                                
                                like_button_found = element
                                logger.debug(f"找到可点赞按钮: {selector}")
                                break
                        
                        if like_button_found:
                            break
                            
                except Exception as e:
                    logger.debug(f"检查选择器 {selector} 时出错: {e}")
                    continue
            
            if like_button_found:
                try:
                    logger.info("找到未点赞的帖子，准备点赞")
                    
                    # 模拟人类行为：短暂等待
                    time.sleep(random.uniform(0.8, 1.5))
                    
                    # 点击点赞按钮
                    like_button_found.click()
                    
                    # 验证点赞是否成功
                    time.sleep(random.uniform(1, 2))
                    
                    # 检查是否点赞成功（按钮状态变化）
                    updated_class = like_button_found.attr("class") or ""
                    if any(reacted in updated_class.lower() for reacted in ['reacted', 'liked', 'active']):
                        logger.success("✅ 点赞成功")
                    else:
                        logger.info("点赞操作已执行")
                    
                    # 随机等待
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    logger.warning(f"点击点赞按钮时出错: {e}")
            else:
                logger.debug("未找到可点赞的内容或内容已点赞")
                
        except Exception as e:
            logger.debug(f"点赞操作失败: {str(e)}")
    
    def get_connect_info(self):
        """获取连接信息"""
        logger.info("获取连接信息")
        page = None
        try:
            page = self.browser.new_tab()
            page.get(self.config.CONNECT_URL)
            time.sleep(random.uniform(4, 6))
            
            # 查找表格
            table_selectors = ["table", ".table", "#connect-table"]
            table = None
            
            for selector in table_selectors:
                elements = page.eles(selector, timeout=5)
                if elements:
                    table = elements[0]
                    break
            
            if not table:
                logger.warning("未找到连接信息表格")
                return
            
            rows = table.eles("tr")
            if len(rows) <= 1:
                logger.info("连接信息为空（新账号可能需要等待几天）")
                return
            
            info = []
            for row in rows[1:]:  # 跳过表头
                cells = row.eles("td")
                if len(cells) >= 3:
                    project = cells[0].text.strip()
                    current = cells[1].text.strip()
                    requirement = cells[2].text.strip()
                    info.append([project, current, requirement])
            
            if info:
                print("-" * 50)
                print("Connect Info")
                print("-" * 50)
                print(tabulate(info, headers=["项目", "当前", "要求"], tablefmt="grid"))
                print("-" * 50)
            else:
                logger.info("连接信息为空")
                
        except Exception as e:
            logger.error(f"获取连接信息失败: {str(e)}")
        finally:
            if page:
                try:
                    page.close()
                except:
                    pass
    
    def send_notifications(self, browse_enabled):
        """发送通知"""
        status_msg = "✅ LinuxDo 每日签到成功"
        if browse_enabled:
            status_msg += " + 浏览任务完成"
        
        notification_count = 0
        
        # Gotify 通知
        if self.config.GOTIFY_URL and self.config.GOTIFY_TOKEN:
            try:
                response = requests.post(
                    f"{self.config.GOTIFY_URL}/message",
                    params={"token": self.config.GOTIFY_TOKEN},
                    json={
                        "title": "LinuxDo 签到通知",
                        "message": status_msg,
                        "priority": 2
                    },
                    timeout=self.config.TIMEOUT,
                )
                response.raise_for_status()
                logger.success("Gotify 通知发送成功")
                notification_count += 1
            except Exception as e:
                logger.error(f"Gotify 通知发送失败: {str(e)}")
        
        # Server酱³ 通知
        if self.config.SC3_PUSH_KEY:
            try:
                match = re.match(r"sct(\d+)t", self.config.SC3_PUSH_KEY, re.I)
                if not match:
                    logger.error("SC3_PUSH_KEY 格式错误，应为 sctXXXt 格式")
                else:
                    uid = match.group(1)
                    url = f"https://{uid}.push.ft07.com/send/{self.config.SC3_PUSH_KEY}"
                    params = {
                        "title": "LinuxDo 签到通知",
                        "desp": status_msg
                    }
                    
                    response = requests.get(url, params=params, timeout=self.config.TIMEOUT)
                    response.raise_for_status()
                    logger.success("Server酱³ 通知发送成功")
                    notification_count += 1
            except Exception as e:
                logger.error(f"Server酱³ 通知发送失败: {str(e)}")
        
        # Telegram 通知
        if self.config.TELEGRAM_TOKEN and self.config.TELEGRAM_USERID:
            try:
                url = f"https://api.telegram.org/bot{self.config.TELEGRAM_TOKEN}/sendMessage"
                data = {
                    "chat_id": self.config.TELEGRAM_USERID,
                    "text": f"🤖 LinuxDo 签到通知\n\n{status_msg}\n\n时间: {time.strftime('%Y-%m-%d %H:%M:%S')}",
                    "parse_mode": "Markdown"
                }
                
                response = requests.post(url, json=data, timeout=self.config.TIMEOUT)
                response.raise_for_status()
                logger.success("Telegram 通知发送成功")
                notification_count += 1
            except Exception as e:
                logger.error(f"Telegram 通知发送失败: {str(e)}")
        
        if notification_count == 0:
            logger.info("未配置通知方式，跳过通知发送")
        else:
            logger.info(f"已发送 {notification_count} 个通知")
    
    def cleanup(self):
        """清理资源"""
        try:
            if self.page:
                self.page.close()
            if self.browser:
                self.browser.quit()
            logger.info("浏览器资源已清理")
        except Exception as e:
            logger.warning(f"清理资源时出错: {str(e)}")
    
    def run(self):
        """主运行方法"""
        try:
            logger.info("=" * 60)
            logger.info("LinuxDo 自动签到程序启动")
            logger.info("=" * 60)
            logger.info(f"用户名: {self.config.USERNAME}")
            logger.info(f"浏览功能: {'启用' if self.config.BROWSE_ENABLED else '禁用'}")
            logger.info(f"无头模式: {'启用' if self.config.HEADLESS else '禁用'}")
            if self.config.PROXY_URL:
                logger.info(f"代理设置: {self.config.PROXY_URL}")
            logger.info("=" * 60)
            
            # 登录
            if not self.login():
                logger.error("登录失败，程序终止")
                return False
            
            logger.success("登录成功！")
            
            # 浏览任务
            if self.config.BROWSE_ENABLED:
                logger.info("开始执行浏览任务")
                self.browse_topics()
                logger.success("浏览任务完成")
            else:
                logger.info("浏览功能已禁用，跳过浏览任务")
            
            # 获取连接信息
            self.get_connect_info()
            
            # 发送通知
            self.send_notifications(self.config.BROWSE_ENABLED)
            
            logger.success("=" * 60)
            logger.success("程序执行完成")
            logger.success("=" * 60)
            return True
            
        except Exception as e:
            logger.error(f"程序执行过程中出现异常: {str(e)}")
            return False
        finally:
            self.cleanup()


def main():
    """主函数"""
    # 验证配置
    config_errors = Config.validate_config()
    if config_errors:
        logger.error("配置验证失败:")
        for error in config_errors:
            logger.error(f"  - {error}")
        sys.exit(1)
    
    # 创建并运行浏览器实例
    browser = None
    try:
        browser = LinuxDoBrowserOptimized()
        success = browser.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        logger.error(f"程序启动失败: {str(e)}")
        sys.exit(1)
    finally:
        if browser:
            browser.cleanup()


if __name__ == "__main__":
    main()
