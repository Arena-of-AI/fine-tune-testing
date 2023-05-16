import streamlit as st
import subprocess

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": "openai api fine_tunes.list"},
    {"name": "Check the status", "command": "openai api fine_tunes.follow -i"},
    {"name": "Yes", "command": "Y"},
    {"name": "No", "command": "n"},
    {"name": "Delete a fine-tuned model", "command": "openai api models.delete -i <FINE_TUNED_MODEL>"},
    {"name": "Check All Status", "command": "openai.FineTune.list()"}
]

# 執行 CLI 指令
def execute_command(command):
    command_with_api_key = f"{command} --api-key {api_key}"
    process = subprocess.Popen(command_with_api_key.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
