import argparse
import os
import sys
import time
from typing import Dict

from fastapi import FastAPI
from llama_cpp import Llama
from llama_cpp.llama_chat_format import (
    MoondreamChatHandler,
    NanoLlavaChatHandler,
)
from llama_cpp.server.app import create_app, get_server_settings, set_server_settings, get_models, get_event_publisher, get_llama_proxy, set_ping_message_factory
from llama_cpp.server.settings import (
    ConfigFileSettings,
    Settings,
    ModelSettings,
    ServerSettings,
)
from llama_cpp.server.cli import add_args_from_model, parse_model_from_args
from ray import serve
from ray.serve import Application
import requests
from starlette.requests import Request

serve.start()

    # "models": [
    #     {
    #         "chat_format": "moondream",
    #         "clip_model_path": "moondream2-mmproj-f16.gguf",
    #         "embedding": true,
    #         "hf_model_repo_id": "vikhyatk/moondream2",
    #         "model": "moondream2-text-model-f16.gguf",
    #         "model_alias": "moondream2",
    #         "n_ctx": 2048,
    #         "verbose": true
    #     },
    #     {
    #         "chat_format": "nanollava",
    #         "clip_model_path": "nanollava-mmproj-f16.gguf",
    #         "embedding": true,
    #         "hf_model_repo_id": "abetlen/nanollava-gguf",
    #         "model": "nanollava-text-model-f16.gguf",
    #         "model_alias": "nanoLLaVA",
    #         "n_ctx": 2048,
    #         "verbose": true
    #     }
    # ]

chat_format = "nanollava"
clip_model_path = "nanollava-mmproj-f16.gguf"
embedding = False
hf_model_repo_id = "abetlen/nanollava-gguf"
model = "nanollava-text-model-f16.gguf"
model_alias = "nanoLLaVA"
n_ctx = 2048
verbose = True

# settings = Settings(
#     # api_key="",
#     # api_key="sk-proj-abc123",
#     chat_format=chat_format,
#     clip_model_path=clip_model_path,
#     embedding=embedding,
#     hf_model_repo_id=hf_model_repo_id,
#     model=model,
#     model_alias=model_alias,
#     n_ctx=n_ctx,
#     verbose=verbose,
# )

# app = FastAPI()
# llama_cpp_server_app = create_app(
#     # settings=settings,
#     server_settings=server_settings,
#     model_settings=model_settings,
# )

def main():
    description = "🦙 Llama.cpp python server. Host your own LLMs!🚀"
    parser = argparse.ArgumentParser(description=description)

    add_args_from_model(parser, Settings)
    parser.add_argument(
        "--config_file",
        type=str,
        help="Path to a config file to load.",
    )
    server_settings: ServerSettings | None = None
    model_settings: list[ModelSettings] = []
    args = parser.parse_args()
    try:
        # Load server settings from config_file if provided
        config_file = os.environ.get("CONFIG_FILE", args.config_file)
        if config_file:
            if not os.path.exists(config_file):
                raise ValueError(f"Config file {config_file} not found!")
            with open(config_file, "rb") as f:
                # Check if yaml file
                if config_file.endswith(".yaml") or config_file.endswith(".yml"):
                    import yaml
                    import json

                    config_file_settings = ConfigFileSettings.model_validate_json(
                        json.dumps(yaml.safe_load(f))
                    )
                else:
                    config_file_settings = ConfigFileSettings.model_validate_json(f.read())
                server_settings = ServerSettings.model_validate(config_file_settings)
                model_settings = config_file_settings.models
        else:
            server_settings = parse_model_from_args(ServerSettings, args)
            model_settings = [parse_model_from_args(ModelSettings, args)]
    except Exception as e:
        print(e, file=sys.stderr)
        parser.print_help()
        sys.exit(1)
    assert server_settings is not None
    assert model_settings is not None
    app = create_app(
        server_settings=server_settings,
        model_settings=model_settings,
    )
    # uvicorn.run(
    #     app,
    #     host=os.getenv("HOST", server_settings.host),
    #     port=int(os.getenv("PORT", server_settings.port)),
    #     ssl_keyfile=server_settings.ssl_keyfile,
    #     ssl_certfile=server_settings.ssl_certfile,
    # )

    return app

llama_cpp_server_app = main()

server_settings = next(get_server_settings())
print('server_settings: ', server_settings)

@serve.deployment
# @serve.ingress(app)
@serve.ingress(llama_cpp_server_app)
class AgentDeployment:
    pass
    # def __init__(self, repo_id: str):
    #     if repo_id == "abetlen/nanollava-gguf":
    #         chat_handler = NanoLlavaChatHandler.from_pretrained(
    #             repo_id=repo_id,
    #             filename="*mmproj*",
    #         )

    #     elif repo_id == "vikhyatk/moondream2":
    #         chat_handler = MoondreamChatHandler.from_pretrained(
    #             repo_id=repo_id,
    #             filename="*mmproj*",
    #         )

    #     else:
    #         raise NotImplementedError

    #     self.model = Llama.from_pretrained(
    #         repo_id=repo_id,
    #         filename="*text-model*",
    #         chat_handler=chat_handler,
    #         embedding=True,
    #         n_ctx=2048, # n_ctx should be increased to accommodate the image embedding
    #         verbose=True,
    #     )

    #     self.tools = []

    # async def __call__(self, http_request: Request) -> Dict:
    #     input_json = await http_request.json()
    #     prompt = input_json["prompt"]
    #     max_tokens = input_json.get("max_tokens", 64)
    #     return self.model(prompt, max_tokens=max_tokens)

    @llama_cpp_server_app.get("/test")
    def root(self):
        return "Hello, world!"


# def agent_builder(args: Dict[str, str] = {}) -> Application:
#     repo_id = args.get("repo_id", "abetlen/nanollava-gguf")

#     # return AgentDeployment.bind(repo_id=repo_id)
#     return AgentDeployment.bind()

# def main():
#     serve.run(agent_builder(), route_prefix="/hello")

#     resp = requests.get("http://localhost:8000/hello")
#     assert resp.json() == "Hello, world!"

# if __name__ == "__main__":
#     main()

serve.run(AgentDeployment.bind(), route_prefix="/")

time.sleep(3600.0)
