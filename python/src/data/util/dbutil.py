from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Optional
import os

from python.src.data.models.league import League

# an Engine, which the Session will use for connection resources
Engine = create_engine(os.environ["DATABASE_URL"], echo=True)

# create a configured "Session" class
session_factory = sessionmaker(bind=Engine)


def wrapped_session(needs_transaction: bool = False):
    def wrapper(func):
        def inner_func(*args, **kwargs):
            session = session_factory()
            try:
                ret = func(*[session, *args], **kwargs)
                if needs_transaction:
                    session.commit()
                return ret
            except RuntimeError:
                if needs_transaction:
                    session.rollback()
                raise
            finally:
                if needs_transaction:
                    session.close()
        return inner_func
    return wrapper


@wrapped_session(True)
def create_league(session: Session, name: str, commissioner_id: int) -> None:
    league = League(name, commissioner_id)
    session.add(league)


@wrapped_session()
def get_league(session: Session, league_id: int) -> Optional[League]:
    return session.query(League).filter_by(id=league_id).one_or_none()


@wrapped_session(True)
def update_league(session: Session, name: str, commissioner_id: int) -> None:
    league = League(name, commissioner_id)
    session.add(league)



