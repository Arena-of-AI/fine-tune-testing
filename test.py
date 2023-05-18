import streamlit as st
import subprocess
import json

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
    {"name": "Delete a fine-tuned model", "command": ""},
]

# 定義解析終端輸出的變數
parsed_output = []

# 執行 CLI 指令
def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

# 解析終端輸出
def parse_terminal_output(output):
    try:
        parsed_output = json.loads(output)
        return parsed_output["data"]
    except json.JSONDecodeError:
        return []

# 獲取所有 fine-tuned model 的名稱
def get_model_names():
    model_names = [item["Model Name"] for item in parsed_output]
    return model_names

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if button["name"] == "List of all fine-tunes tasks":
        if st.button(button["name"]):
            command_output = execute_command(button["command"])
            parsed_output = parse_terminal_output(command_output)
            table_data = []
            for index, item in enumerate(parsed_output):
                table_data.append(
                    {
                        "Model Name": item["fine_tuned_model"],
                        "Job ID": item["id"],
                        "Model": item["model"],
                        "Status": item["status"],
                    }
                )
            if table_data:
                st.table(table_data)
    elif button["name"] == "Delete a fine-tuned model":
        if st.button(button["name"]):
            model_names = get_model_names()
            selected_model = st.selectbox("Select a Model Name", model_names)
            if selected_model:
                confirm_message = st.text_input("Are you sure? Type 'just do it' to confirm.")
                if confirm_message == "just do it":
                    command = f"openai --api-key {api_key} api models.delete -i {selected_model}"
                    command_output = execute_command(command)
                    st.text(f"Command Output: {command_output}")
