import requests
from . import dyconfig
from . import setup

logger = setup.get_logger(__name__)
base_path = dyconfig.get("member_repository", "crm_api_root")
action = dyconfig.get("member_repository", "member_group_code_api_path")


def get_member_group_codes() -> list[str]:
    url = f"{base_path}/{action}"

    parameters = {"hoge": "hoge", "huga": 10}

    response = requests.get(url, parameters)
    response.raise_for_status()
    logger.debug(response.text)
    result_member_group_codes = response.json()

    return result_member_group_codes
