import openai
import streamlit as st

# 读取 API 密钥
api_key = st.text_input("Enter your OpenAI API key", type="password")
openai.api_key = api_key

# 获取终端输出并显示表格
def list_fine_tuned_tasks():
    terminal_output = openai.FineTune.list()
    return terminal_output["data"]

# 解析终端输出为表格行列表
def parse_terminal_output(terminal_output):
    rows = []
    for task in terminal_output:
        hyperparams = task["hyperparams"]
        training_file = task["training_files"][0]["filename"]

        row = {
            "Time": task["created_at"],
            "Model Name": task["fine_tuned_model"],
            "Job ID": task["id"],
            "Parent Model": task["model"],
            "Status": task["status"],
            "Batch Size": hyperparams["batch_size"],
            "Learning Rate Multiplier": hyperparams["learning_rate_multiplier"],
            "Epochs": hyperparams["n_epochs"],
            "Prompt Loss Weight": hyperparams["prompt_loss_weight"],
            "Training File": training_file
        }
        rows.append(row)

    return rows

# 获取终端输出
tasks = list_fine_tuned_tasks()

# 解析终端输出为表格行列表
rows = parse_terminal_output(tasks)

# 显示表格
st.table(rows)
