import streamlit.ReportThread as ReportThread
from streamlit.server.Server import Server

# 创建或获取SessionState对象
def get_session_state():
    session_id = ReportThread.get_report_ctx().session_id
    this_session = None
    current_server = Server.get_current()
    if hasattr(current_server, "_session_infos"):
        for session_info in current_server._session_infos.values():
            if session_info.session.id == session_id:
                this_session = session_info.session
    if this_session is None:
        raise RuntimeError("Couldn't get the session object.")
    if not hasattr(this_session, "_custom_session_state"):
        this_session._custom_session_state = SessionState()
    return this_session._custom_session_state

# 定义SessionState类
class SessionState:
    def __init__(self):
        self.data = []
        self.show_table = False

# 获取SessionState对象
session_state = get_session_state()

# ...

# 监听按钮点击事件
for button in cli_buttons:
    if st.button(button["name"]):
        command_output = execute_command(button["command"])
        parsed_output = parse_terminal_output(command_output)
        session_state.data = parsed_output
        session_state.show_table = True

# ...

# 显示表格
if session_state.show_table:
    st.table(session_state.data)
    st.text("Terminal Output:")
    st.code(command_output)

# ...

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
