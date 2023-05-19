import streamlit as st
import subprocess
import json

# 设置标题
st.title("Check All Your Tasks")

# 输入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定义 CLI 按钮
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
]

# 执行 CLI 指令
def execute_command(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode("utf-8")

# 解析终端输出并显示简化的信息表格
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

# 监听按钮点击事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        parsed_output = parse_terminal_output(command_output)
        st.table(parsed_output)

# 显示 model_names 列表
if "parsed_output" in locals():
    model_names = [item["Model Name"] for item in parsed_output]
    st.text(f"Model Names: {model_names}")
