from typing import List, Optional
import sqlalchemy.orm as orm
from pypi_org.data import db_session
from pypi_org.data.package import Package
from pypi_org.data.releases import Release


def get_latest_releases(limit = 10) -> List[Release]:
    session = db_session.create_session()

    # joinedload below makes sure each Release's package is
    # pulled in eagerly, so we don't have to re-query the db
    # lazily later to figure out what a given release's package is.
    releases = session.query(Release).\
        options(orm.joinedload(Release.package)).\
        order_by(Release.created_date.desc()).\
        limit(limit).\
        all()

    # safe to close, because we pulled in everything we need
    session.close()

    return releases


def get_package_count() -> int:
    session = db_session.create_session()
    return session.query(Package).count()


def get_release_count() -> int:
    session = db_session.create_session()
    return session.query(Release).count()


def get_package_by_id(package_id: str) -> Optional[Package]:
    if not package_id:
        return None
    package_id = package_id.strip().lower()

    session = db_session.create_session()
    package = session.query(Package).\
        options(orm.joinedload(Package.releases)).\
        filter(Package.id == package_id).\
        first()
    session.close()

    return package
