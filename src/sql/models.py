"""Database models"""

from sqlalchemy import (
    VARCHAR,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    SmallInteger,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()


PartnerSegment = Table(
    "partners_segments",
    Base.metadata,
    Column(
        "partner_id", Integer(), ForeignKey("partners.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "segment_id", Integer(), ForeignKey("segments.id", ondelete="CASCADE"), primary_key=True
    ),
    PrimaryKeyConstraint("partner_id", "segment_id", name="p_partner_id_segment_id"),
)


class Product(Base):
    """Product model"""

    __tablename__ = "products"

    id = Column(VARCHAR(36), primary_key=True)
    article = Column(VARCHAR(50), nullable=True, default=None)
    barcode = Column(VARCHAR(50), nullable=True, default=None)
    name = Column(VARCHAR(255), nullable=True, default=None)
    code = Column(VARCHAR(80), nullable=True, default=None)
    country_id = Column(VARCHAR(36), ForeignKey("countries.id"), nullable=True, default=None)
    brand_id = Column(Integer(), ForeignKey("brands.id"), nullable=True, default=None)
    category_id = Column(Integer(), ForeignKey("categories.id"), nullable=True, default=None)
    segment_id = Column(Integer(), ForeignKey("segments.id"), nullable=True, default=None)
    updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    offers = relationship("Offer")
    country = relationship("Country")
    brand = relationship("Brand")
    segment = relationship("Segment")


class ProductTask(Base):
    """ProductTask model"""

    __tablename__ = "products_tasks"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    uuid = Column(VARCHAR(255), nullable=True, default=None)
    article = Column(VARCHAR(50), nullable=True, default=None)
    name = Column(VARCHAR(255), nullable=True, default=None)
    partner_id = Column(Integer(), ForeignKey("partners.id"), nullable=True, default=None)

    partner = relationship("Partner")


class Brand(Base):
    """Brand model"""

    __tablename__ = "brands"

    id = Column(Integer(), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)


class Category(Base):
    """Category model"""

    __tablename__ = "categories"

    id = Column(Integer(), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)


class Segment(Base):
    """Segment model"""

    __tablename__ = "segments"

    id = Column(Integer(), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)

    partners = relationship("Partner", secondary=PartnerSegment, backref="Segment")


class Country(Base):
    """Country model"""

    __tablename__ = "countries"

    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(50), nullable=True, default=None)
    emoji = Column(VARCHAR(10), nullable=True, default=None)
    code = Column(Integer(), nullable=True, default=None)

    products = relationship("Product", back_populates="country")


class Partner(Base):
    """Partner model"""

    __tablename__ = "partners"

    id = Column(Integer(), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)

    segments = relationship("Segment", secondary=PartnerSegment, backref="Partner")


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    rule_level = Column(SmallInteger(), default=1)
    username = Column(VARCHAR(24), unique=True)
    email = Column(VARCHAR(128), unique=True)
    password = Column(VARCHAR(256))
    activated = Column(SmallInteger(), default=0)

    personal_offers = relationship("Offer")
    tokens = relationship("Token")


class Offer(Base):
    """Offer model"""

    __tablename__ = "offers"

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

    product = relationship("Product", back_populates="offers")
    user = relationship("User", back_populates="personal_offers")


class Token(Base):
    """Token model"""

    __tablename__ = "tokens"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(
        Integer(),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    token = Column(VARCHAR(256))

    user = relationship("User", back_populates="tokens")
