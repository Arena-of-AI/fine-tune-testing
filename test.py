import streamlit as st
import subprocess
import json

# 创建或获取SessionState对象
def get_session_state():
    if "session_state" not in st.session_state:
        st.session_state.session_state = SessionState()
    return st.session_state.session_state

# 定义SessionState类
class SessionState:
    def __init__(self):
        self.data = []
        self.show_table = False

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

# 获取SessionState对象
session_state = get_session_state()

# 设置标题
st.title("Check All Your Tasks")

# 输入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 定义 CLI 按钮
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
]

# 监听按钮点击事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        parsed_output = parse_terminal_output(command_output)
        session_state.data = parsed_output
        session_state.show_table = True

# 显示表格
if session_state.show_table:
    st.table(session_state.data)
    st.text("Terminal Output:")
    st.code(command_output)

# 新增段落和按钮
st.title("Delete a Trained Model")
st.text("Please input the model name you want to delete")
model_name_input = st.text_input("Model Name:")
delete_button = st.button("Delete this fine-tuned model")

# 按钮点击事件
if delete_button:
    model_name = model_name_input.strip()
    if model_name:
        delete_command = f"openai --api-key {api_key} api models.delete -i {model_name}"
        delete_output = execute_command(delete_command)
        
        if not delete_output:
            st.error("Please enter a valid model name.")
        else:
            delete_response = json.loads(delete_output)
            if "deleted" in delete_response and delete_response["deleted"]:
                st.success("Deletion Succeeded")
            else:
                st.error("Deletion Failed")
        session_state.show_table = True
    else:
        st.error("Please enter a model name.")
