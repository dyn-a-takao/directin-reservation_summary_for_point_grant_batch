import csv
import itertools
from datetime import date
from . import dyconfig
from . import setup
from . import reserve_repository
from . import csv_factory

logger = setup.get_logger(__name__)
output_csv_path = dyconfig.get("output_csv", "output_path")


def convert_reserve_to_csv(reserve_list_cursor, fromdate: date, todate: date):
    reserve_list: list[dict[str, str]] = []
    latest_group_code: str = ""

    while True:
        latest_reserve_list = reserve_repository.get_reserve_list(
            reserve_list_cursor)

        if not latest_reserve_list:
            break

        for target_reserve in latest_reserve_list:
            target_group_code = target_reserve["MEMBER_GROUP_CODE"]

            if latest_group_code and target_group_code != latest_group_code:
                csv_factory.generate_summary_csv_file(
                    reserve_list=reserve_list,
                    fromdate=fromdate,
                    todate=todate,
                    member_group_code=latest_group_code)
                reserve_list = []

            reserve_list.append(target_reserve)
            latest_group_code = target_group_code

    if reserve_list:
        csv_factory.generate_summary_csv_file(
            reserve_list=reserve_list,
            fromdate=fromdate,
            todate=todate,
            member_group_code=latest_group_code)


def generate_summary_csv_file(reserve_list: list[dict[str, str]], fromdate: date, todate: date, member_group_code: str) -> None:
    output_csv_name = f"{output_csv_path}/summary_reserve_{fromdate:%Y%m%d}_{todate:%Y%m%d}_{member_group_code}.csv"
    logger.info("%s, size: %s", output_csv_name, len(reserve_list))
    fieldnames = [
        "MEMBER_CODE",
        "PLAN_CODE",
        "RESERVE_NUMBER",
        "ACTUAL_PRICE",
        "TOTAL_USE_POINT_AMOUNT"]
    csv_data_list = [{key: value for key, value in reserve.items(
    ) if key in fieldnames} for reserve in reserve_list]
    with open(output_csv_name, "w", newline="") as csvfile:
        csvwriter = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL)
        csvwriter.writeheader()
        csvwriter.writerows(csv_data_list)
