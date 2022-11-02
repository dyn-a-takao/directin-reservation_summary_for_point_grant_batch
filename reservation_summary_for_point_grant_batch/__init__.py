#!/usr/bin/env python

import sys
import csv
import setup
import member_repository
import reserve_repository
import dyconfig
from datetime import date
from dbconnect import Dbconnector

def main():
    """
    fromdateからtodateまでの間に実績確定した予約の一覧を抽出する。
    """    
    logger = setup.get_logger()
    logger.info('reservation_summary_for_point_grant_batch Start...')

    fromdate = date.fromisoformat(sys.argv[1])
    todate = date.fromisoformat(sys.argv[2])

    member_group_codes = member_repository.get_member_group_codes()
    reserve_service_connection = Dbconnector.connect('reserveServiceDB')
    reserve_list = reserve_repository.get_reserve_summary(
        reserve_service_connection,
        member_group_codes=member_group_codes, 
        fromdate=fromdate, 
        todate=todate)
    
    output_csv_path = dyconfig.get('output_csv', 'output_path')
    output_csv_name = f'{output_csv_path}/aggregated_{fromdate}_{todate}.csv'
    with open(output_csv_name, 'w', newline='') as csvfile:
        sqlwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        sqlwriter.writerow(['member_code', 'plan_code', 'reserve_number', 'lodging_total_price'])
        sqlwriter.writerows(reserve_list)
    logger.info('reservation_summary_for_point_grant_batch End') 
    return len(reserve_list)

if __name__ == '__main__':
    main()
