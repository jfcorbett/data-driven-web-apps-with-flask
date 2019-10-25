import sqlalchemy as sa
import sqlalchemy.orm as orm

from pypi_org.data.modelbase import SqlAlchemyBase

factory = None


# noinspection PyUnresolvedReferences
def global_init(db_file: str):
    global factory

    if factory:
        return

    if not db_file or not db_file.strip():
        raise IOError('Database file not found.')

    conn_str = 'sqlite:///' + db_file.strip()
    print(f'Connecting to db with {conn_str}')
    engine = sa.create_engine(conn_str, echo=False)
    factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import pypi_org.data.__all_data_models  # so SqlAlchemyBase is made aware of all data models

    SqlAlchemyBase.metadata.create_all(engine)
