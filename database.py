from sqlalchemy import create_engine, Column, Integer, String, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Message(Base):
    __tablename__ = "message"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(String)
    thread_ts = Column(String)  # timestamp of parent thread
    role = Column(String)
    sender = Column(String)
    receiver = Column(String)
    content = Column(String)
    timestamp = Column(DateTime, default=text("CURRENT_TIMESTAMP"))


def create_session():
    engine = create_engine("sqlite:///mydb.sqlite3")
    Base.metadata.create_all(engine)

    # with engine.connect() as conn:
    #     # SQLAlchemyの機能をフルに活用できるため、executeメソッドが推奨される。
    #     # しかし、この例ではトリガーの作成に関して、SQLiteがサポートされていないために
    #     # executeがエラーを引き起こす。
    #     # そのため、exec_driver_sqlを使用して直接データベースドライバにSQL文を渡すことで、
    #     # 問題を回避する。
    #     # 既存の同名のトリガーが存在するかどうかを確認し、存在する場合は削除する
    #     conn.exec_driver_sql(
    #         """
    #         DROP TRIGGER IF EXISTS limit_rows_trigger;
    #         """
    #     )

    #     conn.exec_driver_sql(
    #         """
    #         CREATE TRIGGER limit_rows_trigger
    #         AFTER INSERT ON message
    #         WHEN (SELECT COUNT(*) FROM message) > 100
    #         BEGIN
    #             DELETE FROM message WHERE id IN (SELECT id FROM message ORDER BY timestamp ASC LIMIT (SELECT COUNT(*) - 5 FROM message));
    #         END;
    #         """
    #     )

    Session = sessionmaker(bind=engine)
    session = Session()
    return session
