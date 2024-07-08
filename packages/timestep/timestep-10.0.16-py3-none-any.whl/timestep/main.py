    #!/usr/bin/env python3

import os
import signal
import subprocess
import time

from openai import OpenAI
import typer

app = typer.Typer()

host = '0.0.0.0'
port = 8080


def start_shell_script(file_path, *args):
    try:
        # Construct the command with the script and the additional arguments
        command = ['sh', file_path] + list(args)
        
        # Open the script and redirect its stdout and stderr to log files for debugging
        with open('script_output.log', 'w') as out, open('script_error.log', 'w') as err:
            process = subprocess.Popen(
                command,
                stdout=out,
                stderr=err,
                preexec_fn=os.setpgrp  # Start the process in a new process group
            )
        print(f"Started the file: {file_path} with PID: {process.pid}")
        return process
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def stop_shell_script(pid):
    try:
        # Kill the process group to ensure all child processes are terminated
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        print(f"Stopped the process with PID: {pid}")
    except Exception as e:
        print(f"An error occurred: {e}")


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot(message: str):
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")

    client = OpenAI(
        base_url=f"http://{host}:{port}/v1",
        api_key = "sk-no-key-required"
    )

    start_time = time.time()

    chat_completion = client.chat.completions.create(
        model="LLaMA_CPP",
        messages=[
            # {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": message},
        ],
        temperature=0,
    )

    response_time = time.time() - start_time

    print(f"Full response received {response_time:.2f} seconds after request")
    # print(f"Full response received:\n{chat_completion}")

    # reply = chat_completion.choices[0].message
    # print(f"Extracted reply: \n{reply}")

    reply_content = chat_completion.choices[0].message.content
    # print(f"Extracted content: \n{reply_content}")

    typer.echo(reply_content)

@app.command()
def load(llamafile_path=f"{os.getcwd()}/models/TinyLlama-1.1B-Chat-v1.0.F16.llamafile"):
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")

    process = start_shell_script(
        llamafile_path,
        '--host', host,
        '--path', '/zip/llama.cpp/server/public',
        '--port', f'{port}',
    )

    typer.echo(f"Loaded portal gun (PID: {process.pid})")


@app.command()
def unload(pid: int):
    """
    Unload the portal gun
    """
    typer.echo("Unloading portal gun")

    stop_shell_script(pid)

    typer.echo(f"Unloaded portal gun (PID: {pid})")
