import streamlit as st
import subprocess
import json

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
    {"name": "Delete a fine-tuned model", "command": f"openai --api-key {api_key} api models.delete -i"}
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
        for i, item in enumerate(data["data"], start=1):
            row = {
                "No.": i,
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

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if button["name"] == "List of all fine-tunes tasks":
        if st.button(button["name"]):
            command_output = execute_command(button["command"])
            terminal_output.text(command_output)
            
            parsed_output = parse_terminal_output(command_output)
            st.table(parsed_output)

    elif button["name"] == "Delete a fine-tuned model":
        model_names = [item["Model Name"] for item in parsed_output]
        selected_model = st.selectbox("Select a model to delete:", model_names)

        if st.button(button["name"]):
            if selected_model:
                confirm_input = st.text_input("Are you sure? Type 'just do it' to confirm:")
                if confirm_input == "just do it":
                    command = f"{button['command']} {selected_model}"
                    command_output = execute_command(command)
                    terminal_output.text(command_output)
                else:
                    terminal_output.text("Deletion cancelled.")
            else:
                st.warning("Please select a model before deleting.")
