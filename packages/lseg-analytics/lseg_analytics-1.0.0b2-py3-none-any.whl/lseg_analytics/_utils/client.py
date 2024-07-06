import json
import os

import requests
from corehttp.runtime.policies import (
    BearerTokenCredentialPolicy,
    NetworkTraceLoggingPolicy,
)

from lseg_analytics.auth.machine_token_credential import MachineTokenCredential
from lseg_analytics.exceptions import LibraryException
from lseg_analytics_basic_client import AnalyticsAPIClient

from .config import load_config

__all__ = [
    "Client",
]


def _get_proxy_port_from_file():
    port_file = f'{os.path.expanduser("~")}{os.path.sep}.lseg{os.path.sep}VSCode{os.path.sep}.portInUse'

    if os.path.isfile(port_file):
        with open(port_file) as f:
            port = f.read()
            print("get proxy port:" + port)

        try:
            return int(port)
        except:
            raise Exception(f"The port got from proxy port file is not a integer:{port}")
    else:
        raise Exception("Proxy port file does not find")


def _get_proxy_info():
    try:
        port = _get_proxy_port_from_file()
    except Exception as err:
        print(f"Failed to get proxy port from file:{err}")
        return False, None
    proxy_url = f"http://localhost:{port}"

    try:
        response = requests.get(f"{proxy_url}/status")
        if response.status_code == 200:
            data = json.loads(response.text)
            if "lsegProxyEnabled" in data:
                return data["lsegProxyEnabled"], proxy_url
            else:
                print(f"proxy responsed with bad data, detail:{data}")
                return False, None
        else:
            print(f"proxy responsed with bad status, detail:{response}")
            return False, None
    except Exception as err:
        print(f"got exception:{err}")
        return False, None


class Client:
    @classmethod
    def reload(cls):
        cls._instance = None

    def __new__(cls):
        if not getattr(cls, "_instance", None):
            cfg = load_config()
            authentication_policy = None
            if cfg.auth and cfg.auth.client_id and cfg.auth.token_endpoint and cfg.auth.client_secret:
                authentication_policy = BearerTokenCredentialPolicy(
                    credential=MachineTokenCredential(
                        client_id=cfg.auth.client_id,
                        client_secret=cfg.auth.client_secret,
                        auth_endpoint=cfg.auth.token_endpoint,
                        scopes=cfg.auth.scopes,
                    ),
                    scopes=cfg.auth.scopes,
                )
            else:
                if not os.getenv("LSEG_ANALYTICS_PROXY_DISABLED"):
                    Client.update_proxy_config(cfg)

            logging_policy = NetworkTraceLoggingPolicy()
            logging_policy.enable_http_logger = True
            cls._instance = AnalyticsAPIClient(
                endpoint=cfg.base_url,
                username=cfg.username,
                authentication_policy=authentication_policy,
                logging_policy=logging_policy,
            )
            if cfg.headers:
                for key, value in cfg.headers.items():
                    cls._instance._config.headers_policy.add_header(key, value)
        return cls._instance

    @staticmethod
    def update_proxy_config(cfg):
        is_proxy_on, proxy_url = _get_proxy_info()
        if is_proxy_on:
            cfg.base_url = proxy_url
        else:
            raise LibraryException(
                "Unable to authenticate to platform, please make sure either you logged in with VSCode LSEG extension or set environment variables for both LSEG_ANALYTICS_AUTH_CLIENT_ID and LSEG_ANALYTICS_AUTH_CLIENT_SECRET."
            )
