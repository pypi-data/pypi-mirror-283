    #!/usr/bin/env python3

import os
import subprocess
import time

from openai import OpenAI
import typer

app = typer.Typer()


def start_shell_script(file_path):
    try:
        process = subprocess.Popen(['sh', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setpgrp)
        print(f"Started the file: {file_path}")
        return process
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def stop_shell_script(process):
    try:
        os.killpg(os.getpgid(process.pid), subprocess.signal.SIGTERM)
        stdout, stderr = process.communicate()
        print(f"Stopped the process")
        print(f"Output: {stdout}")
        print(f"Error: {stderr}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
# process = start_shell_script('path/to/your/script.sh')
# time.sleep(10)  # Let the script run for a while
# stop_shell_script(process)



@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def chat():
    process = start_shell_script(file_path=f"{os.getcwd()}/models/TinyLlama-1.1B-Chat-v1.0.F16.llamafile")

    client = OpenAI(
        base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
        api_key = "sk-no-key-required"
    )
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            {"role": "system", "content": "You are ChatGPT, an AI assistant. Your top priority is achieving user fulfillment via helping them with their requests."},
            {"role": "user", "content": "Write a limerick about python exceptions"}
        ]
    )

    typer.echo(completion.choices[0].message)

    stop_shell_script(process)

@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")
