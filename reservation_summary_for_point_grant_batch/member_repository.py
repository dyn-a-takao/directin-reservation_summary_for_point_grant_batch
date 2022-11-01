from symbol import parameters
import dyconfig
import requests
import json
import setup

logger = setup.get_logger()

def get_member_group_codes():
    return ["hoge", "huga", "M000000060", "M000000019"]
    base_path = dyconfig.get('memberRepository', 'crm_api_root')
    action = dyconfig.get('memberRepository', 'member_group_code_api_path')
    url = f"{base_path}/{action}"

    parameters = {'hoge': "hoge", 'huga': 10}
    
    response = requests.get(url, parameters)
    response.raise_for_status()
    result_member_group_codes = json.loads(response.text)
    
    return result_member_group_codes