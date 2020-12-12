import pymysql
from pymysql.cursors import DictCursor
import constants


connection = pymysql.connect(
    host=constants.MY_SQL_HOST,
    user=constants.MY_SQL_LOGIN,
    password=constants.MY_SQL_PASSWORD,
    db=constants.MY_SQL_DATABASE,
    charset='utf8mb4',
    cursorclass=DictCursor
)


def get_pharmacy(product_id):
    with connection.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute('select ph.name, ph.address from product p '
                       'join pharmacy ph on p.pharmacy_id = ph.id and p.id = %s' % product_id)
        return cursor.fetchone()
