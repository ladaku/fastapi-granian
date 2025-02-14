from sqlmodel import create_engine, Session

DATABASE_URL = "postgresql://adminer:asdasd21@103.150.93.114:5432/bkp_new"
engine = create_engine(DATABASE_URL, echo=True)


def db_session():
    with Session(engine) as session:
        yield session