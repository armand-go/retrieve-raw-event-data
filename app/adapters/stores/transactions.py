from sqlalchemy.orm import Session
from sqlalchemy.engine import Engine


class Transactions:
    __session: Session = None

    def __init__(self, engine: Engine):
        self.__engine = engine

    def instance(self) -> Session:
        if not self.__session:
            self.__session = Session(self.__engine)
        return self.__session

    def start(self) -> "Transactions":
        tx = Transactions(self.__engine)
        tx.__session = Session(self.__engine)
        return tx

    def commit(self) -> None:
        self.__session.commit()
        self.__session.close()
        self.__session = None

    def rollback(self) -> None:
        self.__session.rollback()
        self.__session.close()
        self.__session = None

    def clear(self) -> None:
        if self.__session:
            try:
                self.__session.expire_all()
            except Exception:
                pass

        self.__session = None
