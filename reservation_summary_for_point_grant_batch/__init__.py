#!/usr/bin/env python

import sys
import setup
import member_repository
import reserve_repository
import csv_factory
from datetime import date
from dbconnect import Dbconnector

logger = setup.get_logger()

def main():
    """
    fromdateからtodateまでの間に実績確定した予約の一覧を抽出する。
    """
    logger.info('reservation_summary_for_point_grant_batch Start...')

    fromdate = date.fromisoformat(sys.argv[1])
    todate = date.fromisoformat(sys.argv[2])

    member_group_codes = member_repository.get_member_group_codes()
    reserve_service_connection = Dbconnector.connect('reserveServiceDB')

    with reserve_service_connection:
        reserve_map_by_group = reserve_repository.get_reserve_summary(
            connection=reserve_service_connection,
            member_group_codes=member_group_codes, 
            fromdate=fromdate, 
            todate=todate)

    for member_group_code, reserve_list in reserve_map_by_group:        
        csv_factory.generate_summary_csv_file(
            reserve_list=reserve_list,
            fromdate=fromdate,
            todate=todate,
            member_group_code=member_group_code)

    logger.info('reservation_summary_for_point_grant_batch End') 

if __name__ == '__main__':
    main()
