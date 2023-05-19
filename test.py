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
        parsed_output = json.loads(output)
        simplified_output = []
        for item in parsed_output["data"]:
            simplified_item = {
                "Model Name": item["fine_tuned_model"],
                "Job ID": item["id"],
                "Model": item["model"],
                "Status": item["status"]
            }
            simplified_output.append(simplified_item)
        return simplified_output
    except json.JSONDecodeError:
        return []

# 顯示終端輸出表格
def display_output_table(output):
    if output:
        st.table(output)
    else:
        st.write("No data to display.")

# 顯示模型名稱列表
def display_model_names(model_names):
    st.write("Model Names:")
    for model_name in model_names:
        st.write(model_name)

# 顯示刪除模型的表單
def display_delete_form():
    st.subheader("Delete a Trained Model")
    model_name_input = st.text_input("Please input the model name you want to delete")
    delete_button = st.button("Delete this fine-tuned model")

    if delete_button:
        if model_name_input in model_names:
            command = f"openai --api-key {api_key} api models.delete -i {model_name_input}"
            execute_command(command)
            st.success("Model deleted successfully.")
        else:
            st.error("Please enter a valid model name.")

# 主程式
def main():
    st.title("Check All Your Tasks")
    st.subheader("List of all fine-tunes tasks")
    
    for button in cli_buttons:
        if st.button(button["name"]):
            command_output = execute_command(button["command"])
            simplified_output = parse_terminal_output(command_output)
            display_output_table(simplified_output)
            model_names = [item["Model Name"] for item in simplified_output]
            display_model_names(model_names)
    
    display_delete_form()

if __name__ == "__main__":
    main()
