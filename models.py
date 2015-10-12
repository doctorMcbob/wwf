import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = "post"
    id = sa.Column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    title = sa.Column(
        sa.Unicode, nullable=False, unique=True
    )
    text = sa.Column(
        sa.Unicode, nullable=False
    )

    @classmethod
    def write(cls, title, text, session):
        instance = cls(title=title, text=text)
        session.add(instance)
        session.flush()
        return instance

    @classmethod
    def get_by_id(cls, post_id, session):
        return session.query(cls).filter(cls.id == post_id).one()

    @classmethod
    def get_by_title(cls, title, session):
        return session.query(cls).filter(cls.title == title).one()

    @classmethod
    def get_all(cls, session):
        return session.query(cls).all()

    def __repr__(self):
        return u"BlogPost: {}".format(self.title)

