import streamlit as st
import subprocess
import json

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
            delete_button_key = f"delete_{item.get('id')}"
            delete_button_label = f"Delete {item.get('fine_tuned_model')}"
            if st.button(delete_button_label, key=delete_button_key):
                confirm_message = "Are you sure? Please enter 'just do it':"
                user_input = st.text_input(confirm_message)
                if user_input.strip() == "just do it":
                    delete_command = f"openai --api-key {api_key} api models.delete -i {item.get('fine_tuned_model')}"
                    delete_output = execute_command(delete_command)
                    st.text(delete_output)
            
            row = {
                "Model Name": item.get("fine_tuned_model"),
                "Job ID": item.get("id"),
                "Model": item.get("model"),
                "Status": item.get("status"),
                "Delete": ""
            }
            rows.append(row)
        return rows
    except Exception as e:
        st.error(f"Error parsing terminal output: {str(e)}")
        return []

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
        
        if button["name"] == "List of all fine-tunes tasks":
            parsed_output = parse_terminal_output(command_output)
            
            # 創建簡化的表格資料
            table_data = []
            for row in parsed_output:
                table_data.append([row["Model Name"], row["Job ID"], row["Model"], row["Status"], row["Delete"]])
            
            # 顯示簡化的資訊表格
            st.table(table_data)
