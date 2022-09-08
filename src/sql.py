import asyncio
import sqlalchemy as sa

from aiomysql.sa import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import BIGINT, CHAR, DECIMAL, TEXT, VARCHAR, DateTime, Float

Base = declarative_base()
from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.sql.sqltypes import INTEGER, VARCHAR, SMALLINT

DB_HOST = '31.172.66.21'
DB_PORT = 3306
DB_NAME = 'marketplace_new'
DB_USER = 'OdnodvortsevAndrey'
DB_PASS = 'sk*o6j0YO5%'

DB_TEST_HOST = 'localhost'
DB_TEST_PORT = 3306
DB_TEST_NAME = 'marketplace_new'
DB_TEST_USER = 'root'
DB_TEST_PASS = ''

DB_LOCAL_HOST = 'localhost'
DB_LOCAL_PORT = 3306
DB_LOCAL_NAME = 'marketplace_new'
DB_LOCAL_USER = 'admin'
DB_LOCAL_PASS = '2001'

engine = create_async_engine(
    f"mysql+aiomysql://{DB_LOCAL_USER}:"
    f"{DB_LOCAL_PASS}@{DB_LOCAL_HOST}:"
    f"{DB_LOCAL_PORT}/{DB_LOCAL_NAME}"
)
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)


class Users(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True)
    rule_level = Column(SMALLINT, default=1)
    username = Column(VARCHAR(24), primary_key=True)
    password = Column(VARCHAR(24))
    activated = Column(SMALLINT, default=0)


class Tokens(Base):
    __tablename__ = "tokens"
    id = Column(INTEGER, primary_key=True)
    user_id = Column(VARCHAR(24))
    token = Column(VARCHAR(256))


class Marketplace(Base):
    __tablename__ = "marketplaces"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(50), unique=True)
    fee = Column(Float)
    extra_charge = Column(DECIMAL(10, 2))
    extra_charge_dbs = Column(DECIMAL(10, 2))
    extra_charge_express = Column(DECIMAL(10, 2))
    stone_difference = Column(DECIMAL(10, 2))
    stone_step_days = Column(Integer)
    extra_charge_drop = Column(DECIMAL(10, 2))
    moysklad_id = Column(CHAR(36), nullable=True, default=None)


class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255))
    moysklad_id = Column(CHAR(36), nullable=True, default=None)
    businesses = relationship("Business")


class Business(Base):
    __tablename__ = "businesses"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    name = Column(VARCHAR(255))
    email = Column(VARCHAR(255), nullable=True, default=None)
    password = Column(VARCHAR(255), nullable=True, default=None)
    token = Column(VARCHAR(255), nullable=True, default=None)
    enabled = Column(VARCHAR(1))
    session = Column(VARCHAR(255), nullable=True, default=None)
    organisation = relationship("Organization", back_populates="businesses")
    merchants = relationship("Merchant", back_populates="business")
    marketplace = relationship("Marketplace")


class Merchant(Base):
    __tablename__ = "merchants"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    business_id = Column(Integer, ForeignKey("businesses.id"))
    business = relationship("Business", back_populates="merchants")
    shops = relationship("Shop", back_populates="merchant")
    marketplace = relationship("Marketplace")
    orders = relationship("Order", back_populates="merchant")


class Shop(Base):
    __tablename__ = "shops"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"))
    merchant = relationship("Merchant", back_populates="shops")
    storages = relationship("Storage", back_populates="shop")
    marketplace = relationship("Marketplace")


class Storage(Base):
    __tablename__ = "storages"
    __table_args__ = (PrimaryKeyConstraint("id", "marketplace_id"),)
    id = Column(Integer, primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    shop_id = Column(Integer, ForeignKey("shops.id"))
    id_second = Column(BIGINT, nullable=True, default=None)
    type = Column(CHAR(1))
    dbs = Column(CHAR(1))
    express = Column(CHAR(1))
    alert = Column(VARCHAR(1))
    comission = Column(VARCHAR(1))
    set_prices = Column(VARCHAR(1))
    set_rests = Column(VARCHAR(1))
    set_small_rests = Column(VARCHAR(1))
    additional_charge = Column(DECIMAL(10, 2), nullable=True, default=None)
    priority_charge = Column(DECIMAL(10, 2), nullable=True, default=None)
    demand_warehouse_id = Column(
        Integer, ForeignKey("FK_storages_warehouses_3"), nullable=True, default=None
    )
    binded_warehouse_id = Column(
        Integer, ForeignKey("warehouses.id"), nullable=True, default=None
    )
    second_warehouse_id = Column(
        Integer, ForeignKey("FK_storages_warehouses_2"), nullable=True, default=None
    )
    moysklad_id = Column(CHAR(36), nullable=True, default=None)
    shop = relationship("Shop", back_populates="storages")
    marketplace = relationship("Marketplace")
    binded_warehouse = relationship("Warehouse")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "merchant_id", "id"),)
    id = Column(VARCHAR(50), primary_key=True)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), primary_key=True)
    storage_id = Column(Integer)
    customer_full_name = Column(TEXT, nullable=True, default=None)
    customer_address = Column(TEXT, nullable=True, default=None)
    creation_date = Column(DateTime)
    delivery_date = Column(DateTime, nullable=True, default=None)
    shipment_date = Column(DateTime, nullable=True, default=None)
    add_date = Column(DateTime, nullable=True, default=None)
    finished_date = Column(DateTime, nullable=True, default=None)
    sent_in_telegram = Column(TINYINT(1), nullable=True, default=None)
    merchant = relationship("Merchant", back_populates="orders")
    items = relationship("Item", back_populates="order")
    moysklad_id = Column(CHAR(36), nullable=True, default=None)
    demand_id = Column(CHAR(36), nullable=True, default=None)


class Item(Base):
    __tablename__ = "items"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "order_id", "good_id"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    order_id = Column(VARCHAR(50), ForeignKey("orders.id"), primary_key=True)
    good_id = Column(VARCHAR(50), ForeignKey("goods.id"), primary_key=True)
    quantity = Column(Integer)
    price = Column(DECIMAL(10, 2))
    final_price = Column(DECIMAL(10, 2))
    currency_code = Column(Integer, nullable=True, default=643)
    status_raw = Column(VARCHAR(50), nullable=True)
    status = Column(VARCHAR(50), nullable=True, default=None)
    offer = Column(VARCHAR(255), nullable=True)
    order = relationship("Order", back_populates="items")
    good = relationship("Good", back_populates="items")
    moysklad_id = Column(CHAR(36), nullable=True, default=None)
    need_update = Column(VARCHAR(50), nullable=True, default="Y")


class Good(Base):
    __tablename__ = "goods"
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    id = Column(VARCHAR(50), primary_key=True)
    name = Column(VARCHAR(255))
    slug = Column(VARCHAR(255), nullable=True)
    items = relationship("Item", back_populates="good")


class Product(Base):
    __tablename__ = "products"
    id = Column(CHAR(36), primary_key=True)
    name = Column(VARCHAR(255))
    code = Column(VARCHAR(255), nullable=True, default=None)
    article = Column(VARCHAR(255), nullable=True, default=None)
    last_update = Column(DateTime, nullable=True, default=None)
    serial = Column(TINYINT)
    moysklad_id = Column(CHAR(36))
    stocks = relationship("Stock", back_populates="product")
    stones = relationship("Stone", back_populates="product")


class Stock(Base):
    __tablename__ = "stocks"
    __table_args__ = (PrimaryKeyConstraint("product_id", "warehouse_id"),)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), primary_key=True)
    product_id = Column(VARCHAR(255), ForeignKey("products.id"), primary_key=True)
    stock = Column(Integer)
    price = Column(DECIMAL(10, 2))
    price_fake = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_min_sber = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_min_yandex = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_min_ozon = Column(DECIMAL(10, 2), nullable=True, default=None)
    last_update = Column(DateTime, nullable=True, default=None)
    is_stone = Column(TINYINT, nullable=True, default=None)
    price_fixed_sber = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_fixed_yandex = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_fixed_ozon = Column(DECIMAL(10, 2), nullable=True, default=None)
    demp_limit_sber = Column(DECIMAL(10, 2), nullable=True, default=None)
    demp_limit_yandex = Column(DECIMAL(10, 2), nullable=True, default=None)
    demp_limit_ozon = Column(DECIMAL(10, 2), nullable=True, default=None)
    days_stocks = Column(DECIMAL(10, 2), nullable=True, default=None)
    days_unsale = Column(Integer, nullable=True, default=None)
    price_stone_yandex = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_stone_sber = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_stone_ozon = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_sber_fbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_sber_dbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_sber_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_sber_drop = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_yandex_fbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_yandex_dbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_yandex_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_yandex_drop = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_ozon_fbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_ozon_dbs = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_ozon_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    extra_charge_ozon_drop = Column(DECIMAL(10, 2), nullable=True, default=None)
    product = relationship("Product", back_populates="stocks")
    warehouse = relationship("Warehouse")


class Stone(Base):
    __tablename__ = "stones"
    __table_args__ = (PrimaryKeyConstraint("product_id", "warehouse_id"),)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), primary_key=True)
    product_id = Column(VARCHAR(255), ForeignKey("products.id"), primary_key=True)
    price_demp_sber = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_demp_yandex = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_demp_ozon = Column(DECIMAL(10, 2), nullable=True, default=None)
    became_stone = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    product = relationship("Product", back_populates="stones", lazy='joined')
    warehouse = relationship("Warehouse", lazy='joined')


class MerchantProduct(Base):
    __tablename__ = "merchants_products"
    __table_args__ = (
        PrimaryKeyConstraint("marketplace_id", "merchant_id", "storage_id", "offer_id"),
    )
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), primary_key=True)
    storage_id = Column(BIGINT, ForeignKey("storages.id"), primary_key=True)
    category_id = Column(BIGINT, nullable=True, default=None)
    product_id = Column(BIGINT, nullable=True, default=None)
    name = Column(VARCHAR(255), nullable=True, default=None)
    shop_sku = Column(VARCHAR(50), nullable=True, default=None)
    offer_id = Column(VARCHAR(255), primary_key=True)
    barcode = Column(VARCHAR(255))
    dimensions = Column(VARCHAR(255), nullable=True, default=None)
    stock = Column(Integer, nullable=True, default=None)
    price = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_real = Column(DECIMAL(10, 2), nullable=True, default=None)
    price_old = Column(DECIMAL(10, 2), nullable=True, default=None)
    weight = Column(DECIMAL(10, 2), nullable=True, default=None)
    fee = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_second = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_shop_id = Column(Integer, nullable=True, default=None)
    min_price_express = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_express_second = Column(DECIMAL(10, 2), nullable=True, default=None)
    min_price_express_shop_id = Column(Integer, nullable=True, default=None)
    our_minimal = Column(VARCHAR(50))
    only_ours = Column(VARCHAR(50))
    min_price_last_update = Column(DateTime, nullable=True, default=None)
    visible = Column(CHAR(1), nullable=True, default=None)
    status = Column(VARCHAR(255), nullable=True, default=None)
    last_update = Column(DateTime, nullable=True, default=None)
    our_shop_count = Column(Integer, nullable=True, default=0)
    merchant = relationship("Merchant")
    storage = relationship("Storage")


class Warehouse(Base):
    __tablename__ = "warehouses"
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(255))
    type = Column(VARCHAR(50))
    priority = Column(Integer, nullable=True, default=None)
    moysklad_id = Column(CHAR(36), nullable=True, default=None)
    virtual_moysklad_id = Column(CHAR(36), nullable=True, default=None)


class AlertOrders(Base):
    __tablename__ = "alert_orders"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "merchant_id", "id"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    merchant_id = Column(Integer, ForeignKey("merchants.id"), primary_key=True)
    id = Column(BIGINT, primary_key=True)
    shipment_date_to = Column(DateTime, nullable=True)


class Sticker(Base):
    __tablename__ = "stickers"
    __table_args__ = (PrimaryKeyConstraint("marketplace_id", "order_id", "type"),)
    marketplace_id = Column(Integer, ForeignKey("marketplaces.id"), primary_key=True)
    order_id = Column(VARCHAR(50), ForeignKey("orders.id"), primary_key=True)
    type = Column(VARCHAR(50), primary_key=True)
    code = Column(VARCHAR(50))
    data = Column(VARCHAR(50))


object_list = [Stone, Warehouse, Product]


async def isinstance_list(item, l):
    for object_type in l:
        if isinstance(item, object_type):
            return True
    return False


async def dict_transform(data):
    for k, v in data.items():
        if await isinstance_list(v, object_list):
            data[k] = v.__dict__
    return data
