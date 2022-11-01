import dyconfig
from dbconnect import Dbconnector

class ReserveRepository:
    
    def __init__(self, logger):
        self.logger = logger

    def get_reserve_summary(self, member_group_codes, fromdate, todate):
        grace_days_after_checkout = dyconfig.get('reserveRepository', 'grace_days_after_checkout')
        connection = Dbconnector.connect('reserveServiceDB')
        member_group_code_term = ",".join([f"'{code}'" for code in member_group_codes])
        self.logger.debug(member_group_code_term)
        query = f'''
            SELECT MEMBER_CODE
                , PLAN_CODE
                , RESERVE_NUMBER
                , LODGING_TOTAL_PRICE
            FROM reserveServiceDB.RESERVE_INFO_MASTER 
            WHERE MEMBER_TYPE_KBN = 1
            AND '{fromdate}' <= DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY)
            AND '{todate}' > DATE_ADD(RESERVE_CHECKIN_DATE, INTERVAL RESERVE_LODGING_DATE_NUM + {grace_days_after_checkout} DAY)
            AND MEMBER_GROUP_CODE IN ({member_group_code_term});
        '''
        self.logger.debug(query)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                reserve_list = cursor.fetchall()
        self.logger.info(f'Number of temporary reservation: {len(reserve_list)}')

        return reserve_list
