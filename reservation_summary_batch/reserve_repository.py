from datetime import date
from . import dyconfig
from . import setup

logger = setup.get_logger(__name__)

# プレースホルダ置き換え対象文字
PLACEHOLDER = "%s"


def get_reserve_summary_cursor(connection, member_group_codes: list[str], fromdate: date, todate: date):
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
            ON point.RESERVE_NUMBER = reserve.RESERVE_NUMBER
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
        AND MEMBER_GROUP_CODE IN ({member_group_code_format})
        ORDER BY MEMBER_GROUP_CODE
    """
    query_term_list = [fromdate, grace_days_after_checkout,
                       todate, grace_days_after_checkout]+member_group_codes

    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, query_term_list)
    logger.debug(cursor._executed)
    return cursor


def get_reserve_list(reserve_summary_cursor) -> list[dict[str, str]]:
    acquired_size = dyconfig.getint("reserve_repository", "acquired_size")
    reserve_list = reserve_summary_cursor.fetchmany(acquired_size)
    logger.info("Number of new reservation: %s", len(reserve_list))
    # logger.debug(reserve_list)
    return reserve_list
