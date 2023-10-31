import click
import yaml
import os
import shutil
import fs
import fnmatch

from typing import List
from fs.copy import copy_file
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader

from constants import SERVINGML_WORKING_DIR, MODEL_STORE_SKLEARN, MODEL_STORE_SKLEARN_WORKING


def _generate_dockerfile(app_module: str, requirements: List[str], output_path="Dockerfile") -> None:
    # Load the template environment
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('servingml/Dockerfile.j2')

    # Render the template with variables
    rendered_dockerfile = template.render(app_module=app_module, requirements=requirements)

    # Write the rendered template to a file
    with open(os.path.join(SERVINGML_WORKING_DIR, output_path), 'w') as f:
        f.write(rendered_dockerfile)


@click.command()
@click.option("--build_ctx", type=click.Path(), default=".", show_default=True, help="Path to the build context")
@click.option('--servingfile', 
              default="servingfile.yaml")
def build(build_ctx: str, servingfile: str):
    """Build Dockerfile for model"""
    
    # Create project dir
    if not os.path.exists(SERVINGML_WORKING_DIR):
        os.makedirs(SERVINGML_WORKING_DIR)
    else:
        try:
            shutil.rmtree(SERVINGML_WORKING_DIR)
            os.makedirs(SERVINGML_WORKING_DIR)
        except OSError as e:
            print(f"Error: {SERVINGML_WORKING_DIR} : {e.strerror}")
    with open(servingfile, 'r') as file:
        data = yaml.safe_load(file)
        spec = SimpleNamespace(**data)

    # Generate dockerfile using spec attributes
    _generate_dockerfile(spec.service, spec.packages)

    # Add files to the target directory
    ctx_fs = fs.open_fs(build_ctx)
    target_fs = fs.open_fs(SERVINGML_WORKING_DIR)
    for dir_path, _, files in ctx_fs.walk():
        for f in files:
            path = fs.path.combine(dir_path, f.name).lstrip("/")
            if any(fnmatch.fnmatch(path, pat) for pat in spec.exclude):
                continue  # Skip this file
            # Check if the file matches any of the include patterns
            if any(fnmatch.fnmatch(path, pat) for pat in spec.include):
                target_fs.makedirs(dir_path, recreate=True)
                copy_file(ctx_fs, path, target_fs, path)

    # Copy model to production directory
    framework, model_name = spec.model_name.split(":")
    if framework == "sklearn":
        model_path = os.path.join(MODEL_STORE_SKLEARN, f"{model_name}.pkl")
        if not os.path.exists(model_path):
            raise ValueError(
                f"Model {model_name} is not found at the sklearn model store. Make sure you saved it first."
            )
        target_path = os.path.join(MODEL_STORE_SKLEARN_WORKING, f"{model_name}.pkl")
        if not os.path.exists(MODEL_STORE_SKLEARN_WORKING):
            os.makedirs(MODEL_STORE_SKLEARN_WORKING)
        shutil.copyfile(model_path, target_path)
    
    # Save all as zip archive for further deploying
    shutil.make_archive("master", 'zip', SERVINGML_WORKING_DIR)


if __name__ == '__main__':
    build()
