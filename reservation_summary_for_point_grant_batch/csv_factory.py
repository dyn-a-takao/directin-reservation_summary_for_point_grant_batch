import csv
import dyconfig

output_csv_path = dyconfig.get("output_csv", "output_path")


def generate_summary_csv_file(reserve_list, fromdate, todate, member_group_code):
    output_csv_name = f"{output_csv_path}/summary_reserve_{fromdate:%Y%m%d}_{todate:%Y%m%d}_{member_group_code}.csv"
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
