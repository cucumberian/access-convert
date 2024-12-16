from sqlalchemy import create_engine
from schema.db_connect_schema import DbConnectSchema


def get_engine(
    db_conn: DbConnectSchema,
):
    dsn = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
        db_conn.user,
        db_conn.password,
        db_conn.host,
        db_conn.port,
        db_conn.database,
    )
    return create_engine(dsn)
