from __future__ import unicode_literals, print_function, absolute_import, division
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from qtodb.database_model.tests.schema import Base


@pytest.fixture
def session():
    """
    Create an engine that stores data in memory.
    """
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()



