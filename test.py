import streamlit as st
import subprocess
import json
import pandas as pd

# 輸入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定義 CLI 按鈕
cli_button = {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"}

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
                "Delete": item.get("fine_tuned_model")
            }
            rows.append(row)
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Error parsing terminal output: {str(e)}")
        return pd.DataFrame()

# 刪除模型
def delete_model(api_key, model_id):
    command = f"openai --api-key {api_key} api models.delete -i {model_id}"
    execute_command(command)

# 顯示終端輸出文本區域
terminal_output = st.empty()

# 監聽按鈕點擊事件
if st.button(cli_button["name"]):
    command_output = execute_command(cli_button["command"])
    terminal_output.text(command_output)

    if cli_button["name"] == "List of all fine-tunes tasks":
        parsed_output = parse_terminal_output(command_output)
        delete_buttons = parsed_output["Delete"].apply(lambda x: st.button(f"Delete {x}"))
        parsed_output["Delete"] = delete_buttons
        st.table(parsed_output)

# 檢查按鈕點擊事件
if "Delete" in parsed_output.columns:
    for index, row in parsed_output.iterrows():
        if row["Delete"]:
            delete_model(api_key, row['Model Name'])
