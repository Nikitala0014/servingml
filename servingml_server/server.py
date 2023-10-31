import shutil
import zipfile
import os
import asyncio
import json

from typing import Dict
from pydantic import BaseModel, Field, ValidationError
from fastapi import BackgroundTasks
from fastapi import FastAPI, File, UploadFile, Form


app = FastAPI()


class BuildData(BaseModel):
    modelname: str
    port: int = Field(default=8080, ge=1, le=65535)


async def exec_command(command, log_file_path):
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()

    with open(log_file_path, "a") as log_file:
        if stdout:
            log_file.write(f"[stdout]\n{stdout.decode()}\n")
        if stderr:
            log_file.write(f"[stderr]\n{stderr.decode()}\n")


async def docker_build_task(temp_dir: str, image_tag: str, port: int, log_file_path: str):
    try:
        # Step 1: Build the Docker image asynchronously
        build_command = f"docker build -t {image_tag} {temp_dir}"
        await exec_command(build_command, log_file_path)

        # Step 2: Run a container from the built image asynchronously
        run_command = f"docker run -d -p {port}:{port} {image_tag}"
        await exec_command(run_command, log_file_path)

    except Exception as e:
        # Log any errors during the build or run process
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Error during Docker operations: {e}\n")
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)


def background_docker_build_task(temp_dir, image_tag, port, log_file_path):
    asyncio.run(docker_build_task(temp_dir, image_tag, port, log_file_path))


@app.post("/deploy_project")
async def deploy_project(
    background_tasks: BackgroundTasks, 
    data: str = Form(...), 
    file: UploadFile = File(...)
) -> Dict[str, str]:
    try:
        build_data = json.loads(data)
        build_data = BuildData(**build_data)
    except (json.JSONDecodeError, ValidationError) as e:
        return {"error": f"Invalid input data: {str(e)}"}
    # Temporary directory to extract files
    temp_dir = "temp_docker_build"
    os.makedirs(temp_dir, exist_ok=True)

    temp_file_path = os.path.join(temp_dir, file.filename)

    # Save the uploaded file to disk
    with open(temp_file_path, "wb") as buffer:
        buffer.write(file.file.read())  # Read from SpooledTemporaryFile and write to disk

    # Extract the ZIP file
    with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Check if Dockerfile is present
    if not os.path.exists(os.path.join(temp_dir, 'Dockerfile')):
        return {"error": "Dockerfile not found in the zip"}

    # Build Docker image
    image_tag = f"{build_data.modelname}:latest"  # You can customize this
    background_tasks.add_task(
        background_docker_build_task, temp_dir, image_tag, build_data.port, "docker_build_log.txt",
    )
    return {"message": "Docker build started"}
