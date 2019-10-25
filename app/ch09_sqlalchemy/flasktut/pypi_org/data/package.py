import datetime
from typing import Iterable

import sqlalchemy as sa
import sqlalchemy.orm as orm

from pypi_org.data.modelbase import SqlAlchemyBase
from pypi_org.data.releases import Release


class Package(SqlAlchemyBase):
    # This class will be associated to one table in the db.
    # Inherits from singleton base class. (One base class for one database.)

    # Style: db table names are same as class, but lowercase and plural
    __tablename__ = 'packages'

    # The class' fields are each associated to a column in the db table (col name = field var name)
    id = sa.Column(sa.String, primary_key=True)  # primary keys automatically get an index
    created = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    summary = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)

    homepage = sa.Column(sa.String)
    docs_url = sa.Column(sa.String)
    package_url = sa.Column(sa.String)

    author_name = sa.Column(sa.String)
    author_email = sa.Column(sa.String, index=True)  # index improves++ perf for sorting, lookup...

    license = sa.Column(sa.String, index=True)

    # releases relationship
    # Set up this field's (db column's) relationship to some other db table
    releases: Iterable[Release] = orm.relation("Release", order_by=[
        Release.major_ver.desc(),
        Release.minor_ver.desc(),
        Release.build_ver.desc(),
    ], back_populates='package')  # user can now access relationship via Release.package

    def __repr__(self):
        return f'<Package {self.id}>'
