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
def shoot(message: str = 'Count to 10, with a comma between each number and no newlines. E.g., 1, 2, 3, ...'):
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")

    client = OpenAI(
        base_url=f"http://{host}:{port}/v1",
        api_key = "sk-no-key-required"
    )

    start_time = time.time()

    chat_completion_chunk_stream = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You an AI assistant. Your top priority is responding to user questions with truthful answers."},
            {"role": "user", "content": message},
        ],
        model="LLaMA_CPP",
        stream=True,
        stream_options={"include_usage": True}, # retrieving token usage for stream response
        temperature=0,
    )

    # response_time = time.time() - start_time

    # print(f"Full response received {response_time:.2f} seconds after request")
    # print(f"Full response received:\n{chat_completion}")

    # reply = chat_completion.choices[0].message
    # print(f"Extracted reply: \n{reply}")

    # reply_content = chat_completion.choices[0].message.content
    # print(f"Extracted content: \n{reply_content}")

    # create variables to collect the stream of chunks
    collected_chunks = []
    collected_messages = []
    # iterate through the stream of events
    for chunk in chat_completion_chunk_stream:
        chunk_time = time.time() - start_time  # calculate the time delay of the chunk
        collected_chunks.append(chunk)  # save the event response
        chunk_message = chunk.choices[0].delta.content  # extract the message
        collected_messages.append(chunk_message)  # save the message
        print(f"Message received {chunk_time:.2f} seconds after request: {chunk_message}")  # print the delay and text
        print(f"choices: {chunk.choices}\nusage: {chunk.usage}")
        print("****************")

    # print the time delay and text received
    print(f"Full response received {chunk_time:.2f} seconds after request")
    # clean None in collected_messages
    collected_messages = [m for m in collected_messages if m is not None]
    full_reply_content = ''.join(collected_messages)
    # print(f"Full conversation received: {full_reply_content}")

    typer.echo(full_reply_content)

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

@app.command()
def test(gpu_layers: int = 0):
    from ctransformers import AutoModelForCausalLM

    # Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
    llm = AutoModelForCausalLM.from_pretrained(
        # "jartine/rocket-3B-llamafile",
        "marella/gpt-2-ggml",
        # model_file="rocket-3b.Q4_K_M.llamafile",
        # model_type="stablelm",
        gpu_layers=gpu_layers,
    )

    print(llm("AI is going to"))
