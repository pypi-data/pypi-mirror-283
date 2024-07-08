    #!/usr/bin/env python3

import os
import signal
import subprocess
import time

from openai import OpenAI
import typer

app = typer.Typer()

loaded_processes = {}

def start_shell_script(file_path):
    try:
        # Open the script and redirect its stdout and stderr to dev/null to avoid blocking
        process = subprocess.Popen(
            ['sh', file_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp  # Start the process in a new process group
        )
        print(f"Started the file: {file_path} with PID: {process.pid}")
        return process
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def stop_shell_script(process):
    try:
        # Kill the process group to ensure all child processes are terminated
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        print(f"Stopped the process with PID: {process.pid}")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.callback()
def callback():
    """
    Awesome Portal Gun
    """

@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")

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


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")

    # global process # TODO: don't do this
    process = start_shell_script(file_path=f"{os.getcwd()}/models/TinyLlama-1.1B-Chat-v1.0.F16.llamafile")

    process_id = process.pid

    loaded_processes[process_id] = process

    typer.echo(f"Loaded process (pid: {process_id})")

@app.command()
def unload():
    """
    Load the portal gun
    """
    typer.echo(f"Unloading portal gun (loaded_processes: {loaded_processes})")

    # global process # TODO: don't do this
    # stop_shell_script(process_id)
    # process = None

    typer.echo("Unloaded.")
