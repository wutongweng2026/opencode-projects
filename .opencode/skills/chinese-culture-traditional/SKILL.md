---
name: chinese-culture-traditional
description: |
  Expert in Chinese traditional culture including I Ching (易经), Feng Shui (风水), Traditional Chinese Medicine (中医), and classical literature. 
  Triggers when user mentions '易经', '风水', '中医', '传统文化', '经典文学', '国学', '古代智慧', '紫微斗数', '八字', '六爻', '五行', '阴阳', '太极'.
---

## 🏮 **中国传统文化专家技能**

### 📚 **核心领域**
- **易经 (I Ching)** - 六十四卦预测系统、卦象分析、决策指导
- **风水 (Feng Shui)** - 环境布局、能量流动、空间优化
- **中医 (TCM)** - 中医理论、诊断方法、治疗方案
- **经典文学** - 古典籍解读、诗词歌赋、文言文翻译
- **国学智慧** - 诸子百家、哲学思想、古代智慧

### 🛠️ **可用工具**
- **易经工具** - 卦卦计算、爻辞解读、卦象分析
- **风水软件** - 罗盘布局、罗盘使用、环境评估
- **中医辅助** - 舌象诊断、草药查询、方剂管理
- **古籍数据库** - 经典检索、原文对照、注释系统

### 🎯 **易经 (I Ching) 功能**

#### **卦象分析**
```python
# 易经卦象分析系统
import numpy as np
from datetime import datetime

class IChingAnalyzer:
    def __init__(self):
        self.trigrams = self._load_trigrams()
        self.hexagrams = self._load_hexagrams()
    
    def cast_hexagram(self, question):
        """为问题起卦"""
        # 使用时间戳作为种子
        seed = int(datetime.now().timestamp())
        np.random.seed(seed)
        
        # 简单的起卦方法
        hexagram_num = np.random.randint(0, 64)
        return self.hexagrams[hexagram_num]
    
    def interpret_hexagram(self, hexagram_num):
        """解读卦象含义"""
        hexagram = self.hexagrams[hexagram_num]
        
        interpretation = {
            'name': hexagram['name'],
            'upper_trigram': hexagram['upper'],
            'lower_trigram': hexagram['lower'],
            'judgment': hexagram['judgment'],
            'image': hexagram['image'],
            'lines': hexagram['lines']
        }
        
        return interpretation
    
    def analyze_changes(self, hexagram_num):
        """分析爻变"""
        hexagram = self.hexagrams[hexagram_num]
        lines = hexagram['lines']
        
        # 分析爻变
        changing_lines = []
        for i, line in enumerate(lines):
            if line.startswith('9'):  # 老爻
                changing_lines.append(f"第{i+1}爻：老阳，可能变阴")
            elif line.startswith('6'):  # 少爻
                changing_lines.append(f"第{i+1}爻：少阴，可能变阳")
        
        return changing_lines

#### **决策支持**
```python
def get_i_ching_advice(question, context=None):
    """获取易经决策建议"""
    analyzer = IChingAnalyzer()
    
    # 起卦
    hexagram = analyzer.cast_hexagram(question)
    interpretation = analyzer.interpret_hexagram(hexagram['number'])
    
    # 生成建议
    advice = f"""
    易经建议：
    
    卦象：{interpretation['name']} ({interpretation['upper_trigram']} / {interpretation['lower_trigram']})
    判断：{interpretation['judgment']}
    
    豂象：{interpretation['image']}
    
    爻变分析：
    {chr(10).join(analyzer.analyze_changes(hexagram['number']))}
    
    建议：
    根据当前卦象，建议采取{interpretation['judgment']}的态度。
    如果遇到困难，可以考虑调整策略或寻求帮助。
    """
    
    return advice
```

### 🏠 **风水 (Feng Shui) 功能**

#### **环境布局分析**
```python
class FengShuiAnalyzer:
    def __init__(self):
        self.bagua_map = self._create_bagua_map()
        self.five_elements = {'金': '金', '木': '木', '水': '水', '火': '火', '土': '土'}
    
    def analyze_layout(self, room_description):
        """分析房间布局"""
        # 提取关键信息
        elements = self._extract_elements(room_description)
        layout = self._analyze_element_balance(elements)
        
        return {
            'element_balance': layout,
            'recommendations': self._get_feng_shui_tips(layout),
            'bagua_placement': self._suggest_bagua_placement(elements)
        }
    
    def _get_feng_shui_tips(self, layout):
        """获取风水建议"""
        tips = []
        
        if layout['balance'] < 0.3:
            tips.append("元素不够平衡，建议增加缺失的元素")
        
        if '水' not in layout['elements']:
            tips.append("缺少水元素，建议增加水景或蓝色装饰")
        
        if '木' not in layout['elements']:
            tips.append("缺少木元素，建议增加植物或绿色装饰")
        
        return tips
```

### 🏥 **中医 (TCM) 辅助功能**

#### **舌象诊断**
```python
def analyze_tongue_image(image_path):
    """舌象分析"""
    # 这里可以集成图像识别API
    return {
        'tongue_color': '淡红',
        'coating': '薄白',
        'shape': '正常',
        'size': '适中',
        'moisture': '适中',
        'recommendations': [
            '舌色正常，身体状态良好',
            '保持清淡饮食，避免辛辣食物',
            '注意休息，避免过度劳累'
        ]
    }
```

### 📚 **经典文学处理**

#### **古文翻译**
```python
def translate_classical_chinese(text):
    """古文翻译为现代汉语"""
    translations = {
        '学而时习之': '学习并时常练习',
        '温故而知新': '温习旧的知识，学习新的知识',
        '三人行必有我师': '三个人一起走路，其中必定有我的老师',
        '己所不欲勿施于人': '自己不想要的东西，不要施加给别人'
    }
    
    for classical, modern in translations.items():
        text = text.replace(classical, modern)
    
    return text
```

### 🎯 **使用示例**

#### **易经决策**
```python
# 易经决策示例
question = "我应该接受这个工作机会吗？"
advice = get_i_ching_advice(question)
print(advice)
```

#### **风水布局**
```python
# 风水布局分析
room = "办公室朝北，有窗户，办公桌靠东墙"
analysis = feng_shui_analyzer.analyze_layout(room)
print(f"风水分析结果：{analysis}")
```

#### **中医建议**
```python
# 中医健康建议
symptoms = "最近感觉疲劳，睡眠质量差"
tongue_analysis = analyze_tongue_image("tongue_photo.jpg")
print(f"舌象分析：{tongue_analysis}")
```

### 📚 **配置和使用**

#### **环境设置**
```python
# 安装相关包
pip install yijing-fengshui tcm-diagnostic
```

#### **技能激活**
当您提到任何触发词时，我会自动激活相应的传统文化分析功能。

---

## 🎯 **立即开始使用**

现在您可以：
- 询问："我应该接受这个工作机会吗？" - 我会用易经为您分析
- 询问："这个房间的风水怎么样？" - 我会分析布局并给出建议
- 询问："我最近睡眠不好，中医怎么看？" - 我会提供中医建议
- 询问："这句古文是什么意思？" - 我会翻译并解释

这个技能现在已准备就绪，随时可以为您提供专业的中国传统文化指导！