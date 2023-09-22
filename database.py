from sqlmodel import create_engine, SQLModel

sqlite_file_name = "bancoquestoes.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


#SQLModel.metadata.create_all(engine)
