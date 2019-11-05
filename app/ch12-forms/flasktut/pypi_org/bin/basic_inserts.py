import os

import pypi_org.data.db_session as db_session
from pypi_org.data.package import Package
from pypi_org.data.releases import Release


def main():
    init_db()
    while True:
        insert_a_package()


def insert_a_package():
    p = Package()
    p.id = input('Package id/name: ').strip().lower()
    p.summary = input('Package summary: ').strip()
    p.author_name = input('Author name: ').strip()
    p.license = input('License: ').strip()

    print("Release 1:")
    r = Release()
    r.major_ver = int(input('Major version: '))
    r.minor_ver = int(input('Minor version: '))
    r.build_ver = int(input('Build version: '))
    r.size = int(input('Size (bytes): '))
    p.releases.append(r)

    print("Release 2:")
    r = Release()
    r.major_ver = int(input('Major version: '))
    r.minor_ver = int(input('Minor version: '))
    r.build_ver = int(input('Build version: '))
    r.size = int(input('Size (bytes): '))
    p.releases.append(r)

    """
        id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    major_ver = sa.Column(sa.BigInteger, index=True)
    minor_ver = sa.Column(sa.BigInteger, index=True)
    build_ver = sa.Column(sa.BigInteger, index=True)

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    comment = sa.Column(sa.String)
    url = sa.Column(sa.String)
    size = sa.Column(sa.BigInteger)

    """

    session = db_session.create_session()
    # make a bunch of changes
    session.add(p)
    session.commit()
    print('****** commited!')


def init_db():
    top_folder = os.path.dirname(__file__)
    rel_file = os.path.join('..', 'db', 'pypi.sqlite')
    db_file = os.path.abspath(os.path.join(top_folder, rel_file))
    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
