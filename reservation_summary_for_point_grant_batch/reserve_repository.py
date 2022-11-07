import dyconfig
import setup
import itertools

logger = setup.get_logger()


def get_reserve_summary(connection, member_group_codes, fromdate, todate):
    grace_days_after_checkout = dyconfig.get(
        'reserve_repository', 'grace_days_after_checkout')
    member_group_code_term = ",".join(
        [f"'{code}'" for code in member_group_codes])
    query = f'''
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
        AND '{fromdate}' <= DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY)
        AND '{todate}' > DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY)
        AND MEMBER_GROUP_CODE IN ({member_group_code_term});
    '''

    with connection.cursor(dictionary=True) as cursor:
        cursor.execute(query)
        logger.debug(cursor._executed)
        reserve_list = cursor.fetchall()
    logger.info(f'Number of temporary reservation: {len(reserve_list)}')

    reserve_map_by_group = itertools.groupby(
        reserve_list, lambda reserve: reserve.pop('MEMBER_GROUP_CODE'))
    return reserve_map_by_group
