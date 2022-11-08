import dyconfig
import setup
import itertools
from datetime import date
from typing import Iterator

logger = setup.get_logger()

# プレースホルダ置き換え対象文字
PLACEHOLDER = "%s"


def get_reserve_summary(connection, member_group_codes: list[str], fromdate: date, todate: date):
    grace_days_after_checkout = dyconfig.get(
        "reserve_repository", "grace_days_after_checkout")
    member_group_code_format = ",".join(
        [PLACEHOLDER] * len(member_group_codes))
    query = f"""
        SELECT MEMBER_GROUP_CODE
            , MEMBER_CODE
            , PLAN_CODE
            , reserve.RESERVE_NUMBER
            , LODGING_TOTAL_PRICE + IFNULL(TOTAL_OPTION_PRICE, 0) + IFNULL(ACCOMMODATION_RECORD_ADJUSTMENT_PRICE, 0) AS `ACTUAL_PRICE`
            , IFNULL(TOTAL_USE_POINT_AMOUNT, 0) AS `TOTAL_USE_POINT_AMOUNT`
        FROM reserveServiceDB.RESERVE_INFO_MASTER reserve
        LEFT JOIN (
            SELECT RESERVE_NUMBER, SUM(AMOUNT) AS `TOTAL_USE_POINT_AMOUNT`
            FROM reserveServiceDB.USED_POINT
            WHERE KIND = 'PAYMENT'
            GROUP BY RESERVE_NUMBER
        ) point
            ON point.RESERVE_NUMBER
        LEFT JOIN (
            SELECT RESERVE_NUMBER, SUM(OPTION_RESERVE_NUM * OPTION_PRICE) AS `TOTAL_OPTION_PRICE`
            FROM reserveServiceDB.RESERVE_OPTION_TABLE
            GROUP BY RESERVE_NUMBER
        ) reserve_option
            ON reserve_option.RESERVE_NUMBER = reserve.RESERVE_NUMBER
        WHERE MEMBER_TYPE_KBN = 1
        AND RESERVE_CANCEL_KBN = 0
        AND {PLACEHOLDER} <= DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {PLACEHOLDER} DAY)
        AND {PLACEHOLDER} > DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {PLACEHOLDER} DAY)
        AND MEMBER_GROUP_CODE IN ({member_group_code_format});
    """
    query_term_list = [fromdate, grace_days_after_checkout,
                       todate, grace_days_after_checkout]+member_group_codes

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query, query_term_list)
        logger.debug(cursor._executed)
        reserve_map = cursor.fetchall()
    logger.info(f"Number of temporary reservation: {len(reserve_map)}")

    reserve_list_by_group = itertools.groupby(
        reserve_map, lambda reserve: reserve.pop("MEMBER_GROUP_CODE"))
    return reserve_list_by_group
