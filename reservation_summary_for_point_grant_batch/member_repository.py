from symbol import parameters
import dyconfig
import requests
import json
import setup

logger = setup.get_logger(__name__)
base_path = dyconfig.get("member_repository", "crm_api_root")
action = dyconfig.get("member_repository", "member_group_code_api_path")


def get_member_group_codes() -> list[str]:
    return ["hoge", "huga", "M000000060", "M000000019"]
    url = f"{base_path}/{action}"

    parameters = {"hoge": "hoge", "huga": 10}

    response = requests.get(url, parameters)
    response.raise_for_status()
    result_member_group_codes = json.loads(response.text)

    return result_member_group_codes
