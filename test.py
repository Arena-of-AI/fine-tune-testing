import streamlit as st
import subprocess
import json

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"}
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

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        terminal_output.text(command_output)
        
        if button["name"] == "List of all fine-tunes tasks":
            parsed_output = parse_terminal_output(command_output)
            st.table(parsed_output)

            # 刪除模型區域
            st.write("---")
            st.subheader("Delete a Fine-tuned Model")
            delete_model = st.text_input("Model Name:")
            delete_button = st.button("Delete this fine-tuned model")
            delete_output = ""
            if delete_button:
                found_model = False
                for item in parsed_output:
                    if item["Model Name"] == delete_model:
                        found_model = True
                        break
                if not found_model:
                    st.error("Please enter a valid model name.")
                else:
                    delete_command = f"openai --api-key {api_key} api models.delete -i {delete_model}"
                    delete_output = execute_command(delete_command)
            
            # 顯示刪除結果
            if delete_output:
                st.write(delete_output)
