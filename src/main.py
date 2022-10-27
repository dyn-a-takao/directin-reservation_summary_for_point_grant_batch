#!/usr/bin/env python

from email import charset
import sys
import logging
import datetime
import mysql.connector
import dyconfig
import csv
from datetime import date

LOG = logging.getLogger(__name__)

def connect(name: str):
    connection = mysql.connector.connect(
        host=dyconfig.get(name, 'host'),
        port=dyconfig.getint(name, 'port'),
        user=dyconfig.get(name, 'user'),
        password=dyconfig.get(name, 'password'),
        database=dyconfig.get(name, 'database'),
        ssl_disabled=dyconfig.getboolean(name, 'ssl_disabled'))
    connection.autocommit = False
    return connection

def main():
    fromdate = date.fromisoformat(sys.argv[1])
    todate = date.fromisoformat(sys.argv[2])
    """
    fromdateからtodateまでの間に実績確定した予約の一覧を抽出する。
    """
    print('temporary-reservation-monitor Start...')

    # exclude_minutes=config.getint('temporary_reservation_monitor', 'JBI_exclude_minutes')
    # target_datetime = datetime.datetime.now() - datetime.timedelta(minutes=exclude_minutes)

    config_file = 'config/batch.cfg'
    dyconfig.load(config_file)
    grace_days_after_checkout = dyconfig.get('reservation_summary_for_point_grant_batch', 'grace_days_after_checkout')
    connection = connect('reserveServiceDB')
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
    print('temporary-reservation-monitor End') 
    return len(reserve_list)

if __name__ == '__main__':
    main()
