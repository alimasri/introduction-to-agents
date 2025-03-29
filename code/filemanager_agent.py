from pathlib import Path

from loguru import logger
from pydantic_ai import Agent

agent = Agent(
    name="filemanager",
    model="openai:gpt-4o-mini",
    system_prompt="""\
You are a File Manager. You have access to a file system with directories and files.
Analyze the user input and use your tools to perform the requested file operations.
""",
)


@agent.tool_plain
def read_file(file_path: str):
    logger.debug(f"Reading file: {file_path}")
    return Path(file_path).read_text()


@agent.tool_plain
def file_exists(file_path: str):
    logger.debug(f"Checking if file exists: {file_path}")
    return Path(file_path).exists()


@agent.tool_plain
def list_files(directory: str):
    logger.debug(f"Listing files in directory: {directory}")
    return [str(f) for f in Path(directory).iterdir() if f.is_file()]


@agent.tool_plain
def list_directories(directory: str):
    return [str(f) for f in Path(directory).iterdir() if f.is_dir()]


if __name__ == "__main__":
    response = agent.run_sync("Show me all the files under ~/Downloads")
    print(response.data)
