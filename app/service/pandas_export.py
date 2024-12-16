import pandas as pd
from sqlalchemy.engine import Engine


def csv_to_db(
    csv_path: str,
    table_name: str,
    db_engine: Engine,
):
    df = pd.read_csv(csv_path, sep="\t", low_memory=False)
    df.to_sql(table_name, con=db_engine, if_exists="fail", index=False)
