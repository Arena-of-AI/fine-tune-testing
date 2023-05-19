import streamlit as st
import subprocess
import json

# 設定標題
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
    output, error = process.communicate()
    return output.decode("utf-8")

# 解析終端資訊並顯示簡化的資訊表格
def parse_terminal_output(output):
    try:
        data = json.loads(output)
        rows = []
        for item in data["data"]:
            row = {
                "Model Name": item.get("fine_tuned_model"),
                "Job ID": item.get("id"),
                "Model": item.get("model"),
                "Status": item.get("status")
            }
            rows.append(row)
        return rows
    except Exception as e:
        st.error(f"Error parsing terminal output: {str(e)}")
        return []

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        parsed_output = parse_terminal_output(command_output)
        st.table(parsed_output)

# 新增段落和按鈕
st.title("Delete a Trained Model")
st.text("Please input the model name you want to delete")
model_name_input = st.text_input("Model Name:")
delete_button = st.button("Delete this fine-tuned model")

# 按鈕點擊事件
if delete_button:
    model_name = model_name_input.strip()
    if model_name:
        model_names = [item["Model Name"] for item in parsed_output]
        if model_name in model_names:
            delete_command = f"openai --api-key {api_key} api models.delete -i {model_name}"
            delete_output = execute_command(delete_command)
            st.text(delete_output)
        else:
            st.error("Please enter a valid model name.")
    else:
        st.error("Please enter a model name.")
