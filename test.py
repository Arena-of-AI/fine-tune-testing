import streamlit as st
import subprocess
import json
import openai

# 设置标题
st.title("Check All Your Tasks")

# 输入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 初始化 OpenAI API
openai.api_key = api_key

# 定义 CLI 按钮
cli_buttons = [
    {"name": "List of all fine-tunes tasks", "command": f"openai --api-key {api_key} api fine_tunes.list"},
]

# 创建用于保存状态的类
class SessionState:
    def __init__(self):
        self.data = []
        self.show_table = False
        self.available_models = []

session_state = SessionState()

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

# 列出所有可選擇的模型
def list_available_models():
    models = openai.OpenAIApi().models()
    available_models = [model["id"] for model in models["models"] if model["status"] != "deleted"]
    return available_models



# 监听按钮点击事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        parsed_output = parse_terminal_output(command_output)
        session_state.data = parsed_output
        session_state.show_table = True
        st.text("Terminal Output:")
        st.code(command_output)

# 显示表格
if session_state.show_table:
    st.table(session_state.data)

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
        
        # 设置 show_table 为 True，以便在重新渲染时显示表格
        session_state.show_table = True
    else:
        st.error("Please enter a model name.")

# 顯示按鈕 "List Available Models"
if st.button("List Available Models"):
    session_state.available_models = list_available_models()

# 顯示可選擇的模型下拉選單
selected_model = st.selectbox("Select a model", session_state.available_models)

# 執行其他操作
# ...
