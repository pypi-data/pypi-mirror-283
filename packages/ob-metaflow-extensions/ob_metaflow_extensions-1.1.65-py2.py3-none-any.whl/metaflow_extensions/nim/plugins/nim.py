import os
import time
import json
import requests
from urllib.parse import urlparse
from metaflow.metaflow_config import SERVICE_URL
from metaflow.metaflow_config_funcs import init_config

auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]
nim_info_url = "https://" + auth_host + "/generate/nim"

NVCF_URL = "https://api.nvcf.nvidia.com"
NVCF_SUBMIT_ENDPOINT = f"{NVCF_URL}/v2/nvcf/pexec/functions"
NVCF_RESULT_ENDPOINT = f"{NVCF_URL}/v2/nvcf/pexec/status"

NVCF_CHAT_COMPLETION_MODELS = []
COREWEAVE_CHAT_COMPLETION_MODELS = []

conf = init_config()
if "METAFLOW_SERVICE_AUTH_KEY" in conf:
    headers = {"x-api-key": conf["METAFLOW_SERVICE_AUTH_KEY"]}
    res = requests.get(nim_info_url, headers=headers)
else:
    headers = json.loads(os.environ.get("METAFLOW_SERVICE_HEADERS"))
    res = requests.get(nim_info_url, headers=headers)

res.raise_for_status()
NGC_API_KEY = res.json()["nvcf"]["api_key"]
for model in res.json()["nvcf"]["functions"]:
    NVCF_CHAT_COMPLETION_MODELS.append(
        {
            "name": model["model_key"],
            "function-id": model["id"],
            "version-id": model["version"],
        }
    )
for model in res.json()["coreweave"]["containers"]:
    COREWEAVE_CHAT_COMPLETION_MODELS.append(
        {"name": model["nim_name"], "ip-address": model["ip_addr"]}
    )

COMMON_HEADERS = {"accept": "application/json", "Content-Type": "application/json"}
COREWEAVE_HEADERS = COMMON_HEADERS
NVCF_HEADERS = {**COMMON_HEADERS, "Authorization": f"Bearer {NGC_API_KEY}"}
POLL_INTERVAL = 1


class NimManager(object):
    def __init__(self, models, backend):
        if backend == "managed":
            nvcf_models = [m["name"] for m in NVCF_CHAT_COMPLETION_MODELS]
            cw_models = [m["name"] for m in COREWEAVE_CHAT_COMPLETION_MODELS]
            for m in models:
                if m not in nvcf_models and m not in cw_models:
                    raise ValueError(
                        f"Model {m} not supported by the Outerbounds @nim offering."
                        f"\nYou can choose from these options: {nvcf_models + cw_models}\n\n"
                        "Reach out to Outerbounds if there are other models you'd like supported."
                    )
            self.models = {}
            for m in models:
                if m in nvcf_models:
                    self.models[m] = NimChatCompletion(model=m, provider="NVCF")
                elif m in cw_models:
                    self.models[m] = NimChatCompletion(model=m, provider="CoreWeave")
        else:
            raise ValueError(
                f"Backend {backend} not supported by the Outerbounds @nim offering. Please reach out to Outerbounds."
            )


class NimChatCompletion(object):
    def __init__(self, model="meta/llama3-8b-instruct", provider="CoreWeave", **kwargs):
        self.compute_provider = provider
        self.invocations = []

        if self.compute_provider == "CoreWeave":
            cw_model_names = [m["name"] for m in COREWEAVE_CHAT_COMPLETION_MODELS]
            self.model = model
            self.ip_address = COREWEAVE_CHAT_COMPLETION_MODELS[
                cw_model_names.index(model)
            ]["ip-address"]
            self.endpoint = f"http://{self.ip_address}:8000/v1/chat/completions"

        elif self.compute_provider == "NVCF":
            nvcf_model_names = [m["name"] for m in NVCF_CHAT_COMPLETION_MODELS]
            self.model = model
            self.function_id = NVCF_CHAT_COMPLETION_MODELS[
                nvcf_model_names.index(model)
            ]["function-id"]
            self.version_id = NVCF_CHAT_COMPLETION_MODELS[
                nvcf_model_names.index(model)
            ]["version-id"]

    def __call__(self, **kwargs):

        if self.compute_provider == "CoreWeave":
            request_data = {"model": self.model, **kwargs}
            response = requests.post(
                self.endpoint, headers=COREWEAVE_HEADERS, json=request_data
            )
            response.raise_for_status()
            return response.json()

        elif self.compute_provider == "NVCF":

            request_data = {"model": self.model, **kwargs}
            request_url = f"{NVCF_SUBMIT_ENDPOINT}/{self.function_id}"

            response = requests.post(
                request_url, headers=NVCF_HEADERS, json=request_data
            )
            response.raise_for_status()
            if response.status_code == 202:
                invocation_id = response.headers.get("NVCF-REQID")
                self.invocations.append(invocation_id)
            elif response.status_code == 200:
                return response.json()

            def _poll():
                poll_request_url = f"{NVCF_RESULT_ENDPOINT}/{invocation_id}"
                poll_response = requests.get(poll_request_url, headers=NVCF_HEADERS)
                poll_response.raise_for_status()
                if poll_response.status_code == 200:
                    return poll_response.json()
                elif poll_response.status_code == 202:
                    return 202
                else:
                    raise Exception(
                        f"NVCF returned {poll_response.status_code} status code. Please contact Outerbounds."
                    )

            while True:
                data = _poll()
                if data and data != 202:
                    return data
                time.sleep(POLL_INTERVAL)
