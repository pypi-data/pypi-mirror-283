from betterproto import Casing

from maitai_gen.config import Config, InferenceLocations, ModelConfig

# TODO consider finding a source of truth where we don't need to deploy everytime a new model comes out
SERVER_PROVIDERS = ["groq", "openai"]
CLIENT_PROVIDERS = ["openai"]

MODELS = {
    "llama3-70b-8192": "groq",
    "llama3-8b-8192": "groq",
    "gpt-4o": "openai",
    "gpt-4o-2024-05-13": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4-turbo-2024-04-09": "openai",
    "gpt-4": "openai",
    "gpt-3.5-turbo": "openai",
    "claude-3-5-sonnet-20240620": "anthropic",
    "claude-3-opus-20240229": "anthropic",
    "claude-3-sonnet-20240229": "anthropic",
    "claude-3-haiku-20240307": "anthropic"
}

DEFAULT_CLIENT_MODEL = "gpt-4o"
DEFAULT_SERVER_MODEL = "llama3-70b-8192"


def get_default_config() -> Config:
    return Config(
        inference_location=InferenceLocations.SERVER,
        evaluation_enabled=True,
        apply_corrections=True,
        model='gpt-4o',
        temperature=1,
        streaming=False,
        response_format="text",
        stop=None,
        logprobs=False,
        max_tokens=None,
        n=1,
        frequency_penalty=0,
        presence_penalty=0,
        timeout=-1,
        context_retrieval_enabled=False,
    )


def reconcile_config_with_default(config_dict: dict) -> Config:
    default_config_json = get_default_config().to_pydict(casing=Casing.SNAKE)
    for key, value in default_config_json.items():
        if key not in config_dict:
            config_dict[key] = value
    return Config().from_pydict(config_dict)


def get_model_provider(model_name: str):
    return MODELS.get(model_name)


def get_models(providers):
    models = []
    for model_name, provider in MODELS.items():
        if provider in providers:
            models.append(model_name)
    return models


def get_available_models():
    model_config = ModelConfig(
        all_models=list(MODELS.keys()),
        client_models=get_models(CLIENT_PROVIDERS),
        server_models=get_models(SERVER_PROVIDERS),
        default_client_model=DEFAULT_CLIENT_MODEL,
        default_server_model=DEFAULT_SERVER_MODEL,
    )
    return model_config.to_pydict(casing=Casing.SNAKE)
