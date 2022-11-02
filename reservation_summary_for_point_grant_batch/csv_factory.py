import csv
import dyconfig

output_csv_path = dyconfig.get('output_csv', 'output_path')

def generate_summary_csv_file(reserve_list, fromdate, todate, member_group_code):
    output_csv_name = f'{output_csv_path}/aggregated_{fromdate::%Y%m%d}_{todate:%Y%m%d}_{member_group_code}.csv'
    with open(output_csv_name, 'w', newline='') as csvfile:
        sqlwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        sqlwriter.writerow(['MEMBER_CODE', 'PLAN_CODE', 'RESERVE_NUMBER', 'ACTUAL_PRICE', 'TOTAL_USE_POINT_AMOUNT'])
        sqlwriter.writerows(reserve_list)
