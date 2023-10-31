import requests
import yaml
import click
import json

from types import SimpleNamespace



@click.command()
@click.option('--servingfile', 
              default="servingfile.yaml")
@click.option('--host', 
              default="localhost")
def deploy(servingfile: str, host: str):
    """Deploy model using Dockerfile local or remote"""
    with open(servingfile, 'r') as file:
            data = yaml.safe_load(file)
            spec = SimpleNamespace(**data)
    # Copy model to production directory
    _, model_name = spec.model_name.split(":")
    url = f"http://{host}:8000/build_image"  # Modify with your actual endpoint
    files = {'file': open('master.zip', 'rb')}
    json_data = json.dumps({'modelname': model_name, 'port': 8090})
    data = {'data': json_data}
    response = requests.post(url, data=data, files=files)
    print("response", response.text)


if __name__ == '__main__':
    deploy()
