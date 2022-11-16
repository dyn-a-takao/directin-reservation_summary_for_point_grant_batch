#!/usr/bin/env python

import enum
import sys
from datetime import date
from . import setup
from . import member_group_repository
from . import reserve_repository
from . import csv_factory
from . import dbconnecter

logger = setup.get_logger(__name__)


class ResultCode(enum.IntEnum):
    SUCCESS = 0
    OTHER_ERROR = 1


def aggregate_reservation_for_point_grant() -> ResultCode:
    """
    fromdateからtodateまでの間に実績確定した予約の一覧を抽出する。
    """

    logger.info("reservation_summary_for_point_grant_batch Start...")

    fromdate = date.fromisoformat(sys.argv[1])
    todate = date.fromisoformat(sys.argv[2])

    member_group_codes = member_group_repository.get_member_group_codes()
    reserve_service_connection = dbconnecter.get_connection(
        "reserveServiceDB")

    with reserve_service_connection:
        reserve_map_by_group = reserve_repository.get_reserve_summary(
            connection=reserve_service_connection,
            member_group_codes=member_group_codes,
            fromdate=fromdate,
            todate=todate)

    for member_group_code, reserve_list in reserve_map_by_group:
        csv_factory.generate_summary_csv_file(
            reserve_list=list(reserve_list),
            fromdate=fromdate,
            todate=todate,
            member_group_code=member_group_code)

    logger.info("reservation_summary_for_point_grant_batch End")

    return ResultCode.SUCCESS


def main() -> ResultCode:
    try:
        return aggregate_reservation_for_point_grant()
    except Exception as exception:
        logger.error(exception)
        return ResultCode.OTHER_ERROR


if __name__ == "__main__":
    main()
