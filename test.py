import streamlit as st
import json
from datetime import datetime

# 设置标题
st.title("Check All Your Tasks")

# 解析终端输出并显示简化的信息表格
def parse_terminal_output(output):
    try:
        data = json.loads(output)
        rows = []
        for item in data["data"]:
            task = item
            created_at = datetime.fromtimestamp(task["created_at"]).strftime("%Y-%m-%d %H:%M:%S")
            model_name = task["fine_tuned_model"]
            job_id = task["id"]
            parent_model = task["model"]
            status = task["status"]
            hyperparams = task["hyperparams"]
            batch_size = hyperparams.get("batch_size", "-")
            learning_rate_multiplier = hyperparams.get("learning_rate_multiplier", "-")
            epochs = hyperparams.get("n_epochs", "-")
            prompt_loss_weight = hyperparams.get("prompt_loss_weight", "-")
            training_files = task["training_files"]
            training_file = training_files[0] if training_files else None
            training_filename = training_file["filename"] if training_file else "-"
            row = {
                "Time": created_at,
                "Model Name": model_name,
                "Job ID": job_id,
                "Parent Model": parent_model,
                "Status": status,
                "Batch Size": batch_size,
                "Learning Rate Multiplier": learning_rate_multiplier,
                "Epochs": epochs,
                "Prompt Loss Weight": prompt_loss_weight,
                "Training File": training_filename
            }
            rows.append(row)
        return rows
    except Exception as e:
        st.error(f"Error parsing terminal output: {str(e)}")
        return []

# 获取终端输出并显示表格
def list_fine_tuned_tasks():
    terminal_output = """
    {
      "data": [
        {
          "created_at": 1683283409,
          "fine_tuned_model": "davinci:ft-personal-2023-05-05-10-47-20",
          "hyperparams": {
            "batch_size": 1,
            "learning_rate_multiplier": 0.1,
            "n_epochs": 4,
            "prompt_loss_weight": 0.01
          },
          "id": "ft-4WFUQn0unFswsRCAV8w7UpSV",
          "model": "davinci",
          "object": "fine-tune",
          "organization_id": "org-SN7ScKkJ0Q2dLzLYurmA7vyW",
          "result_files": [
            {
              "bytes": 463,
              "created_at": 1683283641,
              "filename": "compiled_results.csv",
              "id": "file-TqFa5p8ErGDJgtWIyTKt5VFM",
              "object": "file",
              "purpose": "fine-tune-results",
              "status": "processed",
              "status_details": null
            }
          ],
          "status": "succeeded",
          "training_files": [
            {
              "bytes": 211,
              "created_at": 1683283409,
              "filename": "training_data1_prepared.jsonl",
              "id": "file-Lf5v4vItvFza7m0SaNrYaDmz",
              "object": "file",
              "purpose": "fine-tune",
              "status": "processed",
              "status_details": null
            }
          ],
          "updated_at": 1683283642,
          "validation_files": []
        },
        {
          "created_at": 1684207819,
          "fine_tuned_model": "ada:ft-personal-2023-05-16-03-37-01",
          "hyperparams": {
            "batch_size": 1,
            "learning_rate_multiplier": 0.1,
            "n_epochs": 4,
            "prompt_loss_weight": 0.01
          },
          "id": "ft-p0rrrvi6cD6lwyqwBP9xEm9S",
          "model": "ada",
          "object": "fine-tune",
          "organization_id": "org-SN7ScKkJ0Q2dLzLYurmA7vyW",
          "result_files": [
            {
              "bytes": 558,
              "created_at": 1684208222,
              "filename": "compiled_results.csv",
              "id": "file-BlldzluINQZJ24amSca6Rp2P",
              "object": "file",
              "purpose": "fine-tune-results",
              "status": "processed",
              "status_details": null
            }
          ],
          "status": "succeeded",
          "training_files": [
            {
              "bytes": 221,
              "created_at": 1684207818,
              "filename": "train.jsonl",
              "id": "file-Mu5dVDLgWwdaKrJ9JKanp2D4",
              "object": "file",
              "purpose": "fine-tune",
              "status": "processed",
              "status_details": null
            }
          ],
          "updated_at": 1684208223,
          "validation_files": []
        }
      ],
      "object": "list"
    }
    """

    rows = parse_terminal_output(terminal_output)
    if rows:
        st.table(rows)

# 在Streamlit中运行代码
list_fine_tuned_tasks()
