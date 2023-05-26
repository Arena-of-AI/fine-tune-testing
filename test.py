import streamlit as st
import openai
from datetime import datetime

# 设置标题
st.title("Check All Your Tasks")

# 输入 OpenAI API KEY
api_key = st.text_input("Enter your OpenAI API KEY")

# 初始化 OpenAI API
openai.api_key = api_key

# 获取所有 fine-tuned 任务列表
def list_fine_tuned_tasks():
    fine_tuned_tasks = openai.FineTune.list()
    rows = []
    for task in fine_tuned_tasks["data"]:
        created_at = datetime.fromtimestamp(task["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
        training_file = task["training_files"][0] if task["training_files"] else None
        filename = training_file["filename"] if training_file else None
        model = task["model"]
        model_name = model["name"] if isinstance(model, dict) else "-"
        model_id = model["id"] if isinstance(model, dict) else "-"
        row = {
            "Model Name": model_name,
            "Job ID": task["id"],
            "Model": model_id,
            "Status": task["status"],
            "Created at": created_at,
            "Learning Rate Multiplier": task["learning_rate_multiplier"],
            "Number of Epochs": task["n_epochs"],
            "Prompt Loss Weight": task["prompt_loss_weight"],
            "Training File": filename if filename else "-"
        }
        rows.append(row)
    return rows


# 显示表格
if api_key:
    tasks = list_fine_tuned_tasks()
    st.table(tasks)
