import streamlit as st
import subprocess
import json

# 設置標題
st.title("Check All Your Tasks")

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
]

# 執行 CLI 指令
def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()
    return output.decode("utf-8")

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        st.table(json.loads(command_output)["data"])

        
# 新增段落和按鈕
st.title("Delete a Trained Model")
st.text("Please input the model name you want to delete")
model_name_input = st.text_input("Model Name:")
delete_button = st.button("Delete this fine-tuned model")

# 按鈕點擊事件
if delete_button:
    model_name = model_name_input.strip()
    if model_name:
        delete_command = f"openai --api-key {api_key} api models.delete -i {model_name}"
        delete_output = execute_command(delete_command)
        st.text(delete_output)
    else:
        st.error("Please enter a model name.")
