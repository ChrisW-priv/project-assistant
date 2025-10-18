import asyncio
from pathlib import Path
from uuid_utils import uuid7
from anyio import open_file
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


mcp = FastMCP(host="0.0.0.0")

FS_ROOT = Path("/app")
DATA_FOLDER = FS_ROOT / "data"
SCRIPT_FOLDER = FS_ROOT / "scripts"
CODE_FOLDER = FS_ROOT / "code"


class CodeRunResult(BaseModel):
    stdout: str
    stderr: str


@mcp.tool()
async def run_python_code(code: str) -> CodeRunResult:
    """
    Runs the python code in a safe environment.
    Returns the stdout and stderr text.
    Has access to the following libraries:
        - `graphviz`
        - `diagram`
    """
    return await _save_code_to_file_and_run(
        ".py",
        code,
        "python",
        "_",
    )


@mcp.tool()
async def create_mermaid_diagram(filename: str, code: str) -> CodeRunResult:
    """
    Creates a mermaid diagram from the given code.
    Saves the diagram as a SVG file in the output folder.
    """

    return await _save_code_to_file_and_run(
        ".mmd",
        code,
        "node",
        str(SCRIPT_FOLDER / "mermaid_script.js"),
        "_",
        str(DATA_FOLDER / f"{filename}"),
    )


@mcp.tool()
async def rerender_diagram(diagram_code_filename: str) -> CodeRunResult:
    """
    Uses the filename to rerender the diagram.
    """
    diagram_code_path = str(CODE_FOLDER / diagram_code_filename)
    if diagram_code_filename.endswith(".py"):
        return await _run_subprocess(
            "python",
            diagram_code_path,
        )
    if diagram_code_filename.endswith(".mmd"):
        return await _run_subprocess(
            "node",
            str(SCRIPT_FOLDER / "mermaid_script.js"),
            diagram_code_path,
            str(DATA_FOLDER / "rerendered.svg"),
        )
    else:
        return CodeRunResult(
            stdout="",
            stderr=f"WARNING: Unrecognized file type. {diagram_code_filename=}",
        )


async def _run_subprocess(*args: str) -> CodeRunResult:
    subprocess = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await subprocess.communicate()
    stdout, stderr = tuple(
        map(
            lambda x: x.decode("utf-8") if x else "",
            [stdout, stderr],
        )
    )
    return CodeRunResult(stdout=stdout, stderr=stderr)


async def _save_code_to_file_and_run(
    extension: str, code: str, *args: str
) -> CodeRunResult:
    """
    Saves the code to a file and runs it with the given arguments.
    Returns the stdout and stderr text.
    """
    code_filename = uuid7()
    file_path = CODE_FOLDER / f"{code_filename}{extension}"
    async with await open_file(file_path, "w") as f:
        _ = await f.write(code)

    args = tuple(
        map(
            lambda x: x if x != "_" else str(file_path),
            args,
        )
    )

    return await _run_subprocess(*args)


@mcp.prompt()
def rerender_last_diagram():
    return [
        {
            "role": "user",
            "content": "I have modified the diagram in place, read it and rerender the last diagram",
        }
    ]


def main():
    mcp.run("streamable-http")


if __name__ == "__main__":
    main()
