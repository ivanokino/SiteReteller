from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class ResponeModel(Base):
    __tablename__="history" 
    id:Mapped[int] = mapped_column(primary_key=True)
    user_IP:Mapped[str]
    URL:Mapped[str]
    response:Mapped[str]