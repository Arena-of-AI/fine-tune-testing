import streamlit as st
import subprocess
import json

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
    {"name": "Delete a fine-tuned model", "command": f"openai --api-key {api_key} api models.delete -i <FINE_TUNED_MODEL>"}
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
                "Status": item.get("status"),
                "Delete": False
            }
            rows.append(row)
        return rows
    except Exception as e:
        st.error(f"Error parsing terminal output: {str(e)}")
        return []

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 是否顯示表格
show_table = False

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
        
        if button["name"] == "List of all fine-tunes tasks":
            show_table = True
        
        if button["name"] == "Delete a fine-tuned model":
            show_table = False
            
            parsed_output = parse_terminal_output(command_output)
            delete_model_indices = [i for i, row in enumerate(parsed_output) if row["Delete"]]
            delete_model_ids = [parsed_output[i]["Model Name"] for i in delete_model_indices]
            
            if len(delete_model_indices) > 0:
                st.warning("Please select models to delete in the table.")
            
            for model_id in delete_model_ids:
                delete_command = f"openai --api-key {api_key} api models.delete -i {model_id}"
                execute_command(delete_command)
            
            st.success("Models deleted successfully.")
    
    if show_table:
        parsed_output = parse_terminal_output(command_output)
        table = st.table(parsed_output)
