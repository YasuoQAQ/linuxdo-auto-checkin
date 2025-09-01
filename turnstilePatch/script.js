// 增强版反检测脚本
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function getRandomFloat(min, max) {
    return Math.random() * (max - min) + min;
}

// 随机化鼠标坐标，支持更大屏幕
let screenX = getRandomInt(800, 2560);
let screenY = getRandomInt(400, 1440);

// 覆盖鼠标事件属性
Object.defineProperty(MouseEvent.prototype, 'screenX', { 
    value: screenX,
    writable: false,
    configurable: false
});

Object.defineProperty(MouseEvent.prototype, 'screenY', { 
    value: screenY,
    writable: false,
    configurable: false
});

// 覆盖 webdriver 属性
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
    configurable: true
});

// 覆盖 plugins
Object.defineProperty(navigator, 'plugins', {
    get: () => {
        const plugins = [];
        // 模拟常见插件
        plugins.push({
            name: 'Chrome PDF Plugin',
            filename: 'internal-pdf-viewer',
            description: 'Portable Document Format'
        });
        plugins.push({
            name: 'Chrome PDF Viewer',
            filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai',
            description: ''
        });
        plugins.push({
            name: 'Native Client',
            filename: 'internal-nacl-plugin',
            description: ''
        });
        return plugins;
    }
});

// 覆盖语言设置
Object.defineProperty(navigator, 'languages', {
    get: () => ['zh-CN', 'zh', 'en-US', 'en'],
    configurable: true
});

// 覆盖平台信息
Object.defineProperty(navigator, 'platform', {
    get: () => {
        const platforms = ['Win32', 'MacIntel', 'Linux x86_64'];
        return platforms[Math.floor(Math.random() * platforms.length)];
    },
    configurable: true
});

// 覆盖硬件并发数
Object.defineProperty(navigator, 'hardwareConcurrency', {
    get: () => getRandomInt(4, 16),
    configurable: true
});

// 覆盖设备内存
if ('deviceMemory' in navigator) {
    Object.defineProperty(navigator, 'deviceMemory', {
        get: () => [2, 4, 8, 16][Math.floor(Math.random() * 4)],
        configurable: true
    });
}

// 覆盖权限查询
if (navigator.permissions && navigator.permissions.query) {
    const originalQuery = navigator.permissions.query;
    navigator.permissions.query = function(parameters) {
        if (parameters.name === 'notifications') {
            return Promise.resolve({ 
                state: Notification.permission || 'default' 
            });
        }
        return originalQuery.call(this, parameters);
    };
}

// 覆盖 WebGL 指纹
const getParameter = WebGLRenderingContext.prototype.getParameter;
WebGLRenderingContext.prototype.getParameter = function(parameter) {
    // 随机化一些 WebGL 参数
    if (parameter === 37445) { // UNMASKED_VENDOR_WEBGL
        const vendors = ['Intel Inc.', 'NVIDIA Corporation', 'AMD'];
        return vendors[Math.floor(Math.random() * vendors.length)];
    }
    if (parameter === 37446) { // UNMASKED_RENDERER_WEBGL
        const renderers = [
            'Intel Iris OpenGL Engine',
            'NVIDIA GeForce GTX 1060',
            'AMD Radeon Pro 560'
        ];
        return renderers[Math.floor(Math.random() * renderers.length)];
    }
    return getParameter.call(this, parameter);
};

// 覆盖 Canvas 指纹
const toDataURL = HTMLCanvasElement.prototype.toDataURL;
HTMLCanvasElement.prototype.toDataURL = function() {
    // 添加微小的随机噪声
    const context = this.getContext('2d');
    if (context) {
        const imageData = context.getImageData(0, 0, this.width, this.height);
        const data = imageData.data;
        
        // 随机修改少量像素
        for (let i = 0; i < data.length; i += 4) {
            if (Math.random() < 0.001) { // 0.1% 的像素
                data[i] = Math.floor(Math.random() * 256);     // R
                data[i + 1] = Math.floor(Math.random() * 256); // G
                data[i + 2] = Math.floor(Math.random() * 256); // B
            }
        }
        
        context.putImageData(imageData, 0, 0);
    }
    
    return toDataURL.apply(this, arguments);
};

// 覆盖 AudioContext 指纹
if (typeof AudioContext !== 'undefined') {
    const originalCreateAnalyser = AudioContext.prototype.createAnalyser;
    AudioContext.prototype.createAnalyser = function() {
        const analyser = originalCreateAnalyser.call(this);
        const originalGetFloatFrequencyData = analyser.getFloatFrequencyData;
        
        analyser.getFloatFrequencyData = function(array) {
            originalGetFloatFrequencyData.call(this, array);
            // 添加微小的随机噪声
            for (let i = 0; i < array.length; i++) {
                array[i] += (Math.random() - 0.5) * 0.001;
            }
        };
        
        return analyser;
    };
}

// 覆盖时间精度
const originalNow = performance.now;
performance.now = function() {
    // 添加微小的随机延迟，降低时间精度
    return originalNow.call(this) + Math.random() * 0.1;
};

// 覆盖屏幕信息
Object.defineProperty(screen, 'width', {
    get: () => getRandomInt(1366, 3840),
    configurable: true
});

Object.defineProperty(screen, 'height', {
    get: () => getRandomInt(768, 2160),
    configurable: true
});

Object.defineProperty(screen, 'availWidth', {
    get: () => screen.width,
    configurable: true
});

Object.defineProperty(screen, 'availHeight', {
    get: () => screen.height - getRandomInt(30, 80), // 减去任务栏高度
    configurable: true
});

// 覆盖电池信息
if ('getBattery' in navigator) {
    const originalGetBattery = navigator.getBattery;
    navigator.getBattery = function() {
        return originalGetBattery.call(this).then(battery => {
            // 随机化电池信息
            Object.defineProperty(battery, 'level', {
                get: () => getRandomFloat(0.2, 1.0),
                configurable: true
            });
            
            Object.defineProperty(battery, 'charging', {
                get: () => Math.random() > 0.5,
                configurable: true
            });
            
            return battery;
        });
    };
}

// 添加真实的鼠标移动事件
let mouseX = getRandomInt(100, 800);
let mouseY = getRandomInt(100, 600);

document.addEventListener('DOMContentLoaded', function() {
    // 模拟随机鼠标移动
    setInterval(() => {
        mouseX += getRandomInt(-10, 10);
        mouseY += getRandomInt(-10, 10);
        
        mouseX = Math.max(0, Math.min(window.innerWidth, mouseX));
        mouseY = Math.max(0, Math.min(window.innerHeight, mouseY));
        
        const event = new MouseEvent('mousemove', {
            clientX: mouseX,
            clientY: mouseY,
            bubbles: true
        });
        
        document.dispatchEvent(event);
    }, getRandomInt(100, 500));
});

console.log('Enhanced anti-detection script loaded');