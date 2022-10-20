"""Database models"""
import enum

from sqlalchemy import (
    JSON,
    VARCHAR,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    SmallInteger,
    Table,
)
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
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

# ProductFavourite = Table(
#     "products_favourites",
#     Base.metadata,
#     Column("user_id", Integer(), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
#     Column(
#         "product_id", VARCHAR(36), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True
#     ),
#     PrimaryKeyConstraint("user_id", "product_id", name="p_user_id_product_id"),
# )


class ProductFavourite(Base):
    """ProductFavouriteNew model"""
    __tablename__ = "products_favourites"
    __table_args__ = (PrimaryKeyConstraint("user_id", "product_id"),)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    product_id = Column(VARCHAR(36), ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)


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

    # offers = relationship("Offer")
    # country = relationship("Country")
    # brand = relationship("Brand")
    # segment = relationship("Segment")
    # category = relationship("Category")


class ProductTask(Base):
    """ProductTask model"""

    __tablename__ = "products_tasks"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    uuid = Column(VARCHAR(255), nullable=True, default=None)
    article = Column(VARCHAR(50), nullable=True, default=None)
    name = Column(VARCHAR(255), nullable=True, default=None)
    partner_id = Column(Integer(), ForeignKey("partners.id"), nullable=True, default=None)

    # partner = relationship("Partner")


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

    # partners = relationship("Partner", secondary=PartnerSegment, back_populates="segments")


class Country(Base):
    """Country model"""

    __tablename__ = "countries"

    id = Column(VARCHAR(36), primary_key=True)
    name = Column(VARCHAR(50), nullable=True, default=None)
    emoji = Column(VARCHAR(10), nullable=True, default=None)
    code = Column(Integer(), nullable=True, default=None)

    # products = relationship("Product", back_populates="country")


class Partner(Base):
    """Partner model"""

    __tablename__ = "partners"

    id = Column(Integer(), primary_key=True)
    name = Column(VARCHAR(255), nullable=False)

    # personal_offers = relationship("Offer")
    # segments = relationship("Segment", secondary=PartnerSegment, back_populates="partners")


class User(Base):
    """User model"""

    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    partner_id = Column(Integer(), ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    rule_level = Column(SmallInteger(), default=1)
    username = Column(VARCHAR(24), unique=True)
    email = Column(VARCHAR(128), unique=True)
    password = Column(VARCHAR(256))
    activated = Column(Boolean(), default=False)

    # tokens = relationship("Token")
    # favourites = relationship("User", secondary=ProductFavourite, back_populates="products")


class Offer(Base):
    """Offer model"""

    __tablename__ = "offers"

    id = Column(Integer(), primary_key=True)
    product_id = Column(VARCHAR(36), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    partner_id = Column(Integer(), ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    price = Column(Numeric(15, 6), nullable=True, default=None)
    quantity = Column(Integer(), nullable=True, default=None)
    need_update = Column(Boolean(), nullable=True, default=True)
    updated = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    # product = relationship("Product", back_populates="offers")
    # partner = relationship("Partner", back_populates="personal_offers")


class Token(Base):
    """Token model"""

    __tablename__ = "tokens"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(
        Integer(),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    token = Column(VARCHAR(256))

    # user = relationship("User", back_populates="tokens")


class Service(Base):
    """Service modal"""

    __tablename__ = "service"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    enabled = Column(Boolean(), nullable=False, default=False)
    log_days = Column(Integer(), nullable=False, default=30)


class WorkStatus(enum.Enum):
    """Work Status Enum"""

    PROCESSING = "processing"
    DONE = "done"


class ServiceMethod(enum.Enum):
    """Service Method Enum"""

    GET_BRANDS = "get_brands"
    GET_CATEGORIES = "get_categories"
    GET_SEGMENTS = "get_segments"
    GET_PRODUCTS = "get_products"
    GET_PARTNERS = "get_partners"
    GET_EMPLOYEES = "get_employees"
    GET_PARTNERS_SEGMENTS = "get_partners_segments"
    GET_PARTNERS_PRICES = "get_partners_prices"
    POST_PARTNER_PRICES = "post_partner_prices"
    GET_TASKS = "get_tasks"
    POST_TASKS = "post_tasks"


class ServiceEventLog(Base):
    """Service Log Model"""

    __tablename__ = "service_event_log"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    manual_mode = Column(Boolean(), nullable=False, default=False)
    method = Column(Enum(ServiceMethod), nullable=False)
    status = Column(Enum(WorkStatus), nullable=False, default=WorkStatus.PROCESSING)
    parameters = Column(JSON(), nullable=True, default=None)


class UserEvent(enum.Enum):
    """User Request Enum"""

    LOGIN = "login"
    LOGOUT = "logout"
    PASSWORD_RESET = "password_reset"
    SAVE_OFFERS = "save_offers"
    CREATE_TASK = "create_task"


class UserEventLog(Base):
    """User Log Model"""

    __tablename__ = "users_event_log"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    event = Column(Enum(UserEvent), nullable=False)
    partner_id = Column(Integer(), ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # partner = relationship("Partner")
    # user = relationship("User")


class OfferEventLog(Base):
    """Offer Event Log"""

    __tablename__ = "offers_event_log"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    created = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    partner_id = Column(Integer(), ForeignKey("partners.id", ondelete="CASCADE"), nullable=False)
    article = Column(VARCHAR(50), nullable=True, default=None)
    price = Column(Numeric(15, 6), nullable=True, default=None)
    quantity = Column(Integer(), nullable=True, default=None)

    # partner = relationship("Partner")
