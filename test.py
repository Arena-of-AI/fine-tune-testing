import streamlit as st
import subprocess
import json

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
    {"name": "Check the status", "command": f"openai --api-key {api_key} api fine_tunes.follow -i"},
    {"name": "Yes", "command": f"openai --api-key {api_key} api Y"},
    {"name": "No", "command": f"openai --api-key {api_key} api n"},
    {"name": "Delete a fine-tuned model", "command": f"openai --api-key {api_key} api models.delete -i <FINE_TUNED_MODEL>"},
    {"name": "Check All Status", "command": f"openai --api-key {api_key} FineTune.list()"}
]

# 執行 CLI 指令
def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

# 解析終端資訊並顯示簡化的資訊表格
def display_tasks(output):
    data = json.loads(output)
    simplified_data = []
    for task in data["data"]:
        simplified_task = {
            "Model Name": task["fine_tuned_model"],
            "Job ID": task["id"],
            "Model": task["model"],
            "Status": task["status"]
        }
        simplified_data.append(simplified_task)
    st.table(simplified_data)

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
        
        if button["name"] == "List of all fine-tunes tasks":
            display_tasks(command_output)
