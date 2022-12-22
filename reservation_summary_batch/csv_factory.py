import csv
import itertools
from datetime import date
from . import dyconfig
from . import setup
from . import reserve_repository
from . import csv_factory

logger = setup.get_logger(__name__)
output_csv_dir = dyconfig.get("output_csv", "output_path")


def convert_reserve_to_csv(reserve_list_cursor, fromdate: date, todate: date) -> list[str]:
    reserve_list: list[dict[str, str]] = []
    latest_group_code: str = ""
    csv_filename_list: list[str] = []

    while True:
        latest_reserve_list = reserve_repository.get_reserve_list(
            reserve_list_cursor)

        if not latest_reserve_list:
            break

        for target_reserve in latest_reserve_list:
            target_group_code = target_reserve["MEMBER_GROUP_CODE"]

            if latest_group_code and target_group_code != latest_group_code:
                csv_filename = csv_factory.generate_summary_csv_file(
                    reserve_list=reserve_list,
                    fromdate=fromdate,
                    todate=todate,
                    member_group_code=latest_group_code)
                csv_filename_list.append(csv_filename)
                reserve_list = []

            reserve_list.append(target_reserve)
            latest_group_code = target_group_code

    if reserve_list:
        csv_filename = csv_factory.generate_summary_csv_file(
            reserve_list=reserve_list,
            fromdate=fromdate,
            todate=todate,
            member_group_code=latest_group_code)
        csv_filename_list.append(csv_filename)

    return csv_filename_list


def generate_summary_csv_file(reserve_list: list[dict[str, str]], fromdate: date, todate: date, member_group_code: str) -> str:
    output_csv_name = f"summary_reserve_{fromdate:%Y%m%d}_{todate:%Y%m%d}_{member_group_code}.csv"
    output_csv_fullpath = f"{output_csv_dir}/{output_csv_name}"
    logger.info("%s, size: %s", output_csv_name, len(reserve_list))
    fieldnames = [
        "MEMBER_CODE",
        "PLAN_CODE",
        "RESERVE_NUMBER",
        "ACTUAL_PRICE",
        "TOTAL_USE_POINT_AMOUNT"]
    csv_data_list = [{key: value for key, value in reserve.items(
    ) if key in fieldnames} for reserve in reserve_list]
    with open(output_csv_fullpath, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL)
        csvwriter.writeheader()
        csvwriter.writerows(csv_data_list)

    return output_csv_name
