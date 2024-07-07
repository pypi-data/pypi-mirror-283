    #!/usr/bin/env python3
from openai import OpenAI
import typer

app = typer.Typer()


# @app.


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def chat():
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
