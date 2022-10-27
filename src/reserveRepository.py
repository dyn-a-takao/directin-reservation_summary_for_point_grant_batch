import dyconfig
from dbconnect import Dbconnector

class ReserveRepository:
    
    def __init__(self, logger):
        self.logger = logger

    def get_reserve_summary(self, fromdate, todate):
        grace_days_after_checkout = dyconfig.get('reserveRepository', 'grace_days_after_checkout')
        connection = Dbconnector.connect('reserveServiceDB')
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
        self.logger.debug(query)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                reserve_list = cursor.fetchall()
        self.logger.info(f'Number of temporary reservation: {len(reserve_list)}')

        return reserve_list
