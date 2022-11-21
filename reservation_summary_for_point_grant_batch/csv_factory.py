import csv
import itertools
from datetime import date
from . import dyconfig
from . import setup
from . import reserve_repository
from . import csv_factory

logger = setup.get_logger(__name__)
output_csv_path = dyconfig.get("output_csv", "output_path")

KEY_NAME = "MEMBER_GROUP_CODE"


def convert_reserve_to_csv(reserve_list_cursor, fromdate: date, todate: date):
    reserve_list: list[dict[str, str]] = []
    while True:
        latest_reserve_list = reserve_repository.get_reserve_list(
            reserve_list_cursor)
        reserve_list += latest_reserve_list

        latest_group_code = ""
        if latest_reserve_list:
            latest_group_code = latest_reserve_list[-1][KEY_NAME]

        loaded_reserve_list = [
            reserve for reserve in reserve_list if reserve[KEY_NAME] != latest_group_code]
        reserve_list = [
            reserve for reserve in reserve_list if reserve[KEY_NAME] == latest_group_code]

        target_summary = itertools.groupby(
            loaded_reserve_list, lambda reserve: reserve.pop(KEY_NAME))

        for member_group_code, target_reserve_list in target_summary:
            csv_factory.generate_summary_csv_file(
                reserve_list=list(target_reserve_list),
                fromdate=fromdate,
                todate=todate,
                member_group_code=member_group_code)

        if not reserve_list:
            return


def generate_summary_csv_file(reserve_list: list[dict[str, str]], fromdate: date, todate: date, member_group_code: str) -> None:
    output_csv_name = f"{output_csv_path}/summary_reserve_{fromdate:%Y%m%d}_{todate:%Y%m%d}_{member_group_code}.csv"
    logger.info("%s, size: %s", output_csv_name, len(reserve_list))
    with open(output_csv_name, "w", newline="") as csvfile:
        fieldnames = [
            "MEMBER_CODE",
            "PLAN_CODE",
            "RESERVE_NUMBER",
            "ACTUAL_PRICE",
            "TOTAL_USE_POINT_AMOUNT"]
        csvwriter = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL)
        csvwriter.writeheader()
        csvwriter.writerows(reserve_list)
