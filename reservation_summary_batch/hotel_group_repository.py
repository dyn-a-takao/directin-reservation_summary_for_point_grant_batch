import requests
from . import dyconfig
from . import setup

logger = setup.get_logger(__name__)
realm = dyconfig.get("hotel_group_repository", "realm")
base_url = dyconfig.get("hotel_group_repository", "cdp_api_root")
list_size = dyconfig.getint("hotel_group_repository", "list_size")
client_id = dyconfig.get("hotel_group_repository", "client_id")
client_secret = dyconfig.get("hotel_group_repository", "client_secret")


def get_member_group_codes() -> list[str]:
    access_token = _get_access_token()
    header = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    url = f"{base_url}/admin/realms/{realm}/cdp/realm/list"
    result_member_group_code_list: list[str] = []
    page = 1

    while True:
        logger.debug("page: %s, size: %s", page, list_size)

        parameters = {"page": page, "size": list_size}

        response = requests.get(url, params=parameters,
                                headers=header, verify=False)
        response.raise_for_status()
        logger.debug(response.text)
        member_group_list = response.json()

        logger.debug("result_size: %s", len(member_group_list))

        if not member_group_list:
            break

        member_group_code_list = [member["id"] for member in member_group_list]
        result_member_group_code_list.extend(member_group_code_list)
        page += 1

    return result_member_group_code_list


def _get_access_token() -> str:
    url = f"{base_url}/realms/{realm}/protocol/openid-connect/token"
    parameters = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    }
    header = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=parameters,
                             headers=header, verify=False)
    response.raise_for_status()
    response_json = response.json()
    access_token = response_json["access_token"]

    return access_token
