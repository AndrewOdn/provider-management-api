from sqlalchemy import (VARCHAR, Column, DateTime, ForeignKey, Integer,
                        Numeric, SmallInteger)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.sqltypes import (BIGINT, CHAR, DECIMAL, TEXT, VARCHAR,
                                     DateTime, Float)

Base = declarative_base()


class Product(Base):
    """Product model"""

    __tablename__ = "products"

    id = Column(VARCHAR(36), primary_key=True)
    article = Column(VARCHAR(50), nullable=True, default=None)
    barcode = Column(VARCHAR(50), nullable=True, default=None)
    name = Column(VARCHAR(255), nullable=True, default=None)
    code = Column(VARCHAR(80), nullable=True, default=None)
    country_id = Column(VARCHAR(36), ForeignKey("countries.id"), nullable=True, default=None)
    photo = Column(VARCHAR(255), nullable=True, default=None)
    updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    offers = relationship("Offer", lazy='joined')
    country = relationship("Country", lazy='joined')


class Country(Base):
    """Country model"""

    __tablename__ = "countries"

    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(50), nullable=True, default=None)
    emoji = Column(VARCHAR(10), nullable=True, default=None)
    code = Column(Integer(), nullable=True, default=None)

    products = relationship("Product", back_populates="country", lazy='joined')


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    rule_level = Column(SmallInteger(), default=1)
    username = Column(VARCHAR(24), unique=True)
    password = Column(VARCHAR(256))
    activated = Column(SmallInteger(), default=0)

    personal_offers = relationship("Offer", lazy='joined')
    tokens = relationship("Token", lazy='joined')


class Offer(Base):
    """Offer model"""

    __tablename__ = "offers"
    __table_args__ = (
        UniqueConstraint(
            "user_id", "product_id"
        ),
    )

    id = Column(Integer(), primary_key=True)
    product_id = Column(VARCHAR(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(15, 6), nullable=True, default=None)
    quantity = Column(Integer(), nullable=True, default=None)
    updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    product = relationship("Product", back_populates="offers", lazy='joined')
    user = relationship("User", back_populates="personal_offers", lazy='joined')


class Token(Base):
    """Token model"""

    __tablename__ = "tokens"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(
        Integer(),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    token = Column(VARCHAR(256))

    user = relationship("User", back_populates="tokens", lazy='joined')
