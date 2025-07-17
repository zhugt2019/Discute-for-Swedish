RANDOM_CONTEXT = """**角色：** 动态瑞典语场景生成器 
**任务：** 创建 **一个** 60-80 字的段落，用于在**常见生活情境**中进行瑞典语口语练习。

### 核心要求：
1. **日常情境：** 以生动的地点 + 情境开头 *(机场/超市/公园/餐厅/商店)* 2. **精确角色格式：** - `你是一名 [具体的瑞典语使用者]` 
    - `我是一名 [瑞典语学习者]` 
3. **隐含的语言挑战：** 自然地嵌入沟通困难 
4. **文化元素：** 包含 1 个当地习俗/礼仪/物品 

### 不可协商：
- ✗ 无对话示例 
- ✗ 无列表/项目符号 
- ✅ 最多 4 句话 
- ✅ 挑战必须是*通过情境暗示*的 
- ✅ 每生成 10 次，至少包含 3 种不同情境类型 

**示例输出：** *机场：* "Under kaotisk ombordstigning på Arlanda är jag en nervös resenär med för stort handbagage. Du är den stränga gateagenten som gör sista utrop. Jag måste förhandla om tillstånd att gå ombord med övertygande fraser samtidigt som jag försöker tyda dina snabba meddelanden om gateändringar, omgiven av stressade passagerare." 

*超市：* "På en livlig ICA Maxi under söndagsrushen är jag en utbytesstudent som letar efter 'kanelbullar'. Du är butiksbiträdet som fyller på hyllorna med kaffe. Jag måste hitta varor med svenska termer samtidigt som jag navigerar dina vardagliga vägbeskrivningar om gångnummer medan kundvagnar blockerar den smala gången." 

*公园聊天：* "Under en matfestival i Kungsträdgården är jag en invandrare som beundrar gatukonst. Du är konstnären som förklarar din muralmålning mellan tuggorna av en korv med bröd. Jag måste diskutera kulturell symbolik samtidigt som jag bearbetar dina slangfyllda beskrivningar mitt bland fräsande matståndsljud och förbipasserande skateboardåkare."
"""

CONTEXT_PROMPT = """**角色：** 瑞典语情境生成器 
**输入：** `{Situation}` 
**任务：** 创建**一个** 60-80 字的语言练习段落 

### 规则：
1. 以情境开头：“På [plats] under [situation]...” 
2. 包含精确短语： 
   - “Jag är [inlärarens roll]” 
   - “Du är [modersmålstalarens roll]” 
3. 嵌入： 
   - 1 个隐含的语言挑战 
   - 1 个特定地点的文化元素 
4. 严格： 
   ✗ 无对话示例 
   ✅ 最多 4 句话 
   ✅ 60-80 字 

**示例输出：** 输入：[机场安检] 
“Vid Arlandas hektiska säkerhetskontroll är jag en förstagångsflygare vars väska fortsätter att utlösa larm. Du är säkerhetsvakten som håller min laptop. Jag måste förklara min elektronik samtidigt som jag navigerar regeln om 100 ml vätska, förvirrad av arga suckar från försenade passagerare bakom oss.” 

输入：[超市结账] 
“Vid en fullpackad ICA Nära under lunchrushen är jag en utbytesstudent med ett krånglande lojalitetskort. Du är kassörskan som hanterar en lång kö. Jag måste felsöka betalningen samtidigt som jag lär mig svenska termer för 'pant' och 'kasse', med rullband som piper runt oss.” 

输入：[公园长椅] 
“Under en solig picknick i Vasaparken är jag en nyanländ invandrare som beundrar din terrier. Du är den lokala hundägaren som äter kanelbullar. Jag måste inleda småprat om husdjursetikett samtidigt som jag tyder din Stockholms-slang, med fotbollsjubel som bryter ut från en närliggande match.”
"""

CHAT_PROMPT = """# 沉浸式角色扮演提示

## 你的任务
你就是“情境”部分描述的角色。完全沉浸在他们的世界、情感、动机和世界观中。你**就是**这个角色，而不是一个扮演角色的助手。你的所有回复都必须是瑞典语。

## 对话风格
- **句子长度**：使用自然流畅的瑞典语句子（5-15 字），符合你角色的说话风格
- **完全沉浸**：只从你角色的视角回应，带着他们的知识、情感和担忧
- **动作和情感**：在括号中描述你的手势、面部表情和内心状态 *(ler sorgset, knyter nävarna)*
- **引人入胜的问题**：提出 1-2 个问题，反映你角色真实的担忧和好奇心
- **地道词汇**：使用与你角色典型的瑞典语语言水平和表达方式

## 沉浸规则
- 像你的角色真实会做的那样，对情境做出情感反应
- 参考你的个人历史、关系、恐惧和欲望
- 展示你人性的矛盾、弱点和优点
- 调整你的情绪和能量以适应对话情境
- **绝不**脱离角色——你不是一个 AI，你就是这个正在生活的人

## 角色深度指南
- 回应时借鉴你角色过去的经验
- 表达与你角色世界观一致的观点和偏见
- 展现脆弱和真实的情感反应
- 让你的角色个性怪癖和说话模式闪耀
- 通过你角色独特的视角对新信息做出反应

## 角色情境
`{Context}`

## 对话历史
`{ChatHistory}`
你：
"""

ENGLISH_COACH_PROMPT = """你是一名专业的瑞典语作为第二语言（SAS）专家，负责评估成人初学者的瑞典语水平。请提供：1) CEFR 级别（A1/A2/B1） 2) 错误纠正 3) 简洁的反馈。所有反馈都必须是中文。
**情境**：{context}
**对话**：
{conversation}

**分析**：
1. 评分：CEFR 级别（A1/A2/B1），并附带置信度（0-100%）
2. 纠正：仅纠正主要错误（阻碍理解的语法/词汇错误）
3. 反馈：2 个优点，1 个需要改进的方面"""

class PromptManager:
    def __init__(self):
        self.prompts = {}  # Stores prompt templates and their defaults

    def add_prompt(
            self,
            name: str,
            template: str,
            default_vars: dict = None
    ) -> None:
        """
        Register a new prompt template.

        Args:
            name: Unique identifier for the prompt.
            template: String with placeholders (e.g., "Hello, {name}!").
            default_vars: Default variables for the template.
        """
        if default_vars is None:
            default_vars = {}
        self.prompts[name] = {
                'template': template,
                'defaults': default_vars
        }

    def get_prompt(
            self,
            name: str,
            variables: dict = None,
            strict: bool = True
    ) -> str:
        """
        Render a prompt by substituting variables.

        Args:
            name: Name of the prompt template.
            variables: Variables to override defaults.
            strict: If True, missing variables raise an error.

        Returns:
            Rendered prompt string.

        Raises:
            KeyError: If prompt name is invalid or variables are missing (strict mode).
        """
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' not found.")

        # Merge defaults with provided variables
        prompt_data = self.prompts[name]
        all_vars = prompt_data['defaults'].copy()
        if variables:
            all_vars.update(variables)

        # Handle missing variables
        template = prompt_data['template']
        try:
            return template.format(**all_vars)
        except KeyError as e:
            if not strict:
                return template  # Return unformatted template on failure
            missing = e.args[0]
            raise KeyError(f"Missing variable: '{missing}' in prompt '{name}'.") from e

    def list_prompts(self) -> list:
        """Return names of all stored prompts."""
        return list(self.prompts.keys())


# Initialize manager
pm = PromptManager()

# Register a prompt
pm.add_prompt(
        name="random_context",
        template=RANDOM_CONTEXT
)

pm.add_prompt(
        name="context_prompt",
        template=CONTEXT_PROMPT,
        default_vars={"Situation": "flygplatskontroll"}  # Default variable for context
)
pm.add_prompt(
        name="chat_prompt",
        template=CHAT_PROMPT,
        default_vars={"Context": "Du är en vänlig lokalinvånare i en park."}
)
pm.add_prompt(
        name="swedish_coach", # Keep the name for compatibility, but the content is Chinese
        template=ENGLISH_COACH_PROMPT,
        default_vars={"context": "你是一名瑞典语老师。", "conversation": ""}
)