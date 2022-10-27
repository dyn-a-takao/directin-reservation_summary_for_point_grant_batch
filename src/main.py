#!/usr/bin/env python

import sys
import logging
import dyconfig
import dbconnector
import csv
from datetime import date

LOG = logging.getLogger(__name__)

def main():
    """
    fromdateからtodateまでの間に実績確定した予約の一覧を抽出する。
    """
    print('reservation_summary_for_point_grant_batch Start...')

    fromdate = date.fromisoformat(sys.argv[1])
    todate = date.fromisoformat(sys.argv[2])
    config_file = 'config/batch.cfg'
    dyconfig.load(config_file)
    grace_days_after_checkout = dyconfig.get('reservation_summary_for_point_grant_batch', 'grace_days_after_checkout')
    connection = dbconnector.connect('reserveServiceDB')
    query = f'''
        SELECT MEMBER_CODE
            , PLAN_CODE
            , RESERVE_NUMBER
            , LODGING_TOTAL_PRICE
        FROM reserveServiceDB.RESERVE_INFO_MASTER 
        WHERE MEMBER_TYPE_KBN = 1
        AND '{fromdate}' <= DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY)
        AND '{todate}' > DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY);
    '''
    print(query)
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            reserve_list = cursor.fetchall()
    with open('output/aggregated.csv', 'w', newline='') as csvfile:
        sqlwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        sqlwriter.writerow(['member_code', 'plan_code', 'reserve_number', 'lodging_total_price'])
        sqlwriter.writerows(reserve_list)
    print(f'Number of temporary reservation: {len(reserve_list)}')
    print('reservation_summary_for_point_grant_batch End') 
    return len(reserve_list)

if __name__ == '__main__':
    main()
