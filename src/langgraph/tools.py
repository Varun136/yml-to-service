from langchain_community.agent_toolkits import FileManagementToolkit
import zipfile
from pathlib import Path

def get_file_management_tools(work_dir_name):
    
    tools = FileManagementToolkit(
        root_dir = work_dir_name,
        selected_tools=["read_file", "write_file", "list_directory"],
    ).get_tools()
    return tools



def zip_temp_dir(temp_dir: str, zip_name: str = "project") -> str:
    temp_path = Path(temp_dir)
    zip_path = Path.cwd() / f"{zip_name}.zip"

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in temp_path.rglob("*"):
            zipf.write(file, arcname=file.relative_to(temp_path))

    return str(zip_path)