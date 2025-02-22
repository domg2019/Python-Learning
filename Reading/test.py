import pyttsx3

# 初始化引擎
engine = pyttsx3.init()

# 获取所有可用的声音ID
voices = engine.getProperty('voices')

# 选择一个声音，例如第一个声音（索引为0）
# 注意：索引可能会根据系统和已安装的声音而变化
engine.setProperty('voice', voices[0].id)

# 你可以通过循环遍历 voices 列表并打印出每个声音的详细信息来找到你想要的声音
for voice in voices:
    print(f"Voice: {voice.name} - {voice.langua}")

# 设置要说的文本
text = "Hello, this is a test."

# 告诉引擎说这段文本
engine.say(text)

# 运行等待直到所有命令都完成
engine.runAndWait()