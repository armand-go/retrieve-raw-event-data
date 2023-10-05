from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class Core:
    config: dict
    postgres: Engine

    def __init__(self, config: dict) -> None:
        self.config = config
        self.postgres = self.setup_sqlalchemy(config)

    def setup_sqlalchemy(self, config: dict) -> Engine:
        adapter = config['POSTGRES_ADAPTER']
        user = config['POSTGRES_USER']
        pwd = config['POSTGRES_PASSWORD']
        hostname = config['POSTGRES_HOST']
        port = config['POSTGRES_PORT']
        db = config['POSTGRES_DB']

        return create_engine(
            f"{adapter}://{user}:{pwd}@{hostname}:{port}/{db}",
            future=True,
            pool_size=25,
            max_overflow=30,
            pool_pre_ping=True,
            pool_recycle=8 * 60,  # seconds
        )
