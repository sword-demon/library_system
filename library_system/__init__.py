import pymysql

pymysql.install_as_MySQLdb()


def pymsql_monkey_patch():
    from django.db.backends.mysql.operations import DatabaseOperations

    def last_executed_query(self, cursor, sql, params):
        query = getattr(cursor, '_execute', None)
        if query is not None:
            query = query.encode(errors='replace')
        return query

    DatabaseOperations.last_executed_query = last_executed_query


pymsql_monkey_patch()
