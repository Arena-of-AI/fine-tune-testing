import streamlit as st
import subprocess

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": "openai --api-key {} api fine_tunes.list".format(api_key)},
    {"name": "Check the status", "command": "openai --api-key {} api fine_tunes.follow -i".format(api_key)},
    {"name": "Yes", "command": "openai --api-key {} api Y".format(api_key)},
    {"name": "No", "command": "openai --api-key {} api n".format(api_key)},
    {"name": "Delete a fine-tuned model", "command": "openai --api-key {} api models.delete -i <FINE_TUNED_MODEL>".format(api_key)},
    {"name": "Check All Status", "command": "openai --api-key {} FineTune.list()".format(api_key)}
]

# 執行 CLI 指令
def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
