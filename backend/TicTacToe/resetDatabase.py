from connection import Connection
import textwrap

def resetDatabase(database):
    session = Connection(database)

    # Create table and populate it
    session.execute(
        'CREATE TABLE IF NOT EXISTS shopping_cart ( '
            'userid text PRIMARY KEY, '
            'item_count int, '
            'last_update_timestamp timestamp '
        ') '
    )

    session.execute(
        'TRUNCATE TABLE shopping_cart '
    )

    session.execute(
        'INSERT INTO shopping_cart '
            '(userid, item_count, last_update_timestamp) '
            "VALUES ('9876', 2, toTimeStamp(now())) "
    )

    session.execute(
        'INSERT INTO shopping_cart '
            '(userid, item_count, last_update_timestamp) '
            "VALUES ('1234', 5, toTimeStamp(now())) "
    )

    data = session.query('SELECT userid, item_count FROM shopping_cart')
    session.close()

    return data
