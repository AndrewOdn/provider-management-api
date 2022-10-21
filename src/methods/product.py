from fastapi import HTTPException
from sqlalchemy import insert, delete
from src.sql.models import Offer, ProductFavourite
from sqlalchemy.exc import IntegrityError
from src.sql.connection import async_session


async def async_update_product(data, user_id):
    """Update/Insert products list func"""
    async with async_session() as session:
        session.begin()
        result = await session.execute(
            f"""SELECT partner_id FROM users WHERE users.id = {user_id}"""
        )
        for item in result:
            partner_id = item.partner_id
        for filters in data:
            product_id = str(filters.product_id)
            filters.price = float(filters.price) if filters.price and filters.price != "" else 0
            filters.quantity = float(filters.quantity) if filters.quantity and filters.quantity != "" else 0
            if filters.price != 0 or filters.quantity != 0:
                try:
                    upd = await session.execute(
                        f"""UPDATE offers SET price = {filters.price},
    quantity = {filters.quantity}
    WHERE offers.product_id = '{product_id}' AND offers.partner_id = {partner_id}"""
                    )
                except IntegrityError:
                    raise HTTPException(406,
                                        f"Нет такого товара в каталоге | {product_id} | отсутствует в прайс листе, невозможно выставить на него цену")
                if upd.rowcount == 0:
                    try:
                        await session.execute(
                            insert(Offer).values(
                                price=filters.price,
                                quantity=filters.quantity,
                                product_id=product_id,
                                partner_id=partner_id,
                            )
                        )
                    except IntegrityError:
                        raise HTTPException(406,
                                            f"Нет такого товара в каталоге | {product_id} | отсутствует в прайс листе, невозможно выставить на него цену")
                await session.commit()
            else:
                await session.execute(
                    delete(Offer)
                        .where(Offer.partner_id == partner_id)
                        .where(Offer.product_id == product_id)
                )
                await session.commit()
    return {"status": True}


async def async_remove_favorite(data, user_id):
    """Delete favorite products func"""
    async with async_session() as session:
        await session.execute(
            delete(ProductFavourite)
                .where(ProductFavourite.user_id == user_id)
                .where(ProductFavourite.product_id == str(data.product_id))
        )
        await session.commit()
    return {"status": True}


async def async_set_favorite(data, user_id):
    """Insert  favorite products func"""
    async with async_session() as session:
        result = await session.execute(
            f"""SELECT count(*) FROM products_favourites WHERE products_favourites.user_id = {user_id} and products_favourites.product_id = '{data.product_id}'"""
        )
        for item in result:
            count = item.count
        if count == 0:
            try:
                await session.execute(
                    insert(ProductFavourite).values(
                        user_id=user_id,
                        product_id=str(data.product_id),
                    )
                )
                await session.commit()
            except IntegrityError:
                raise HTTPException(406,
                                    f"Нет такого товара в каталоге {data.product_id} отсутствует в прайс листе, невозможно добавить в избранное")
    return {"status": True}


async def async_get_product(data, user_id):
    """Get products and offers list by filters func"""
    async with async_session() as session:
        async with session.begin():
            data.page_size = data.page_size if data.page_size else 20
            data.page = data.page if data.page else 0
            res = {'data': []}
            query = f"""SELECT CASE
            when products_favourites.product_id IS NOT null THEN true
            ELSE false
        END AS favorite, users.username AS Username, partners.name AS partner_name, segments.name AS segment_name,
countries.name AS countries_name, countries.emoji AS countries_emoji, countries.code AS countries_code, segments.id AS segment_id,
categories.name AS categories_name,categories.id AS categories_id, brands.name AS brands_name, brands.id AS brands_id, 
products.article AS product_article, products.barcode AS product_barcode, products.name AS product_name,
products.updated AS product_updated, products.id AS product_id,
offers.price AS offer_price, offers.quantity AS offer_quantity, offers.updated AS offer_updated FROM users
LEFT OUTER JOIN partners ON users.partner_id = partners.id AND users.id = {user_id}
LEFT OUTER JOIN partners_segments ON partners_segments.partner_id = partners.id
LEFT OUTER JOIN segments ON partners_segments.segment_id = segments.id
LEFT OUTER JOIN products ON products.segment_id = segments.id
LEFT OUTER JOIN brands ON products.brand_id = brands.id
LEFT OUTER JOIN categories ON products.category_id = categories.id
LEFT OUTER JOIN countries ON products.country_id = countries.id
LEFT OUTER JOIN offers ON products.id = offers.product_id AND offers.partner_id = users.partner_id
LEFT OUTER JOIN products_favourites ON products_favourites.product_id = products.id AND products_favourites.user_id = {user_id}"""
            prefix = " WHERE "
            for item in data:
                if isinstance(item[1], str):
                    if item[0] == 'search':
                        query += prefix + f"segments.name LIKE '%{item[1]}%' or brands.name LIKE '%{item[1]}%' " \
                                          f"or categories.name LIKE '%{item[1]}%' or products.name LIKE '%{item[1]}%' " \
                                          f"or products.id LIKE '%{item[1]}%' or products.article LIKE '%{item[1]}%'"

                    else:
                        query += prefix + f"{item[0].replace('_', '.')} = '{item[1]}'"
                    prefix = " AND "
                elif isinstance(item[1], bool):
                    if item[0] == 'favorite':
                        if item[1] is True:
                            query += prefix + f"products_favourites.product_id IS NOT null"
                        else:
                            query += prefix + f"products_favourites.product_id IS null"
                    elif item[0] == 'have_price':
                        if data.have_price is True:
                            query += prefix + "offers.price > 0"
                        else:
                            query += prefix + "(offers.price = 0 or offers.price is null)"
                    prefix = " AND "
                elif isinstance(item[1], (int, float)):
                    if item[0] == 'offer_price_asc':
                        address = 'offers.price >'
                    elif item[0] == 'offer_price_desc':
                        address = 'offers.price <'
                    elif item[0] == 'offer_quantity_asc':
                        address = 'offers.quantity >'
                    elif item[0] == 'offer_quantity_desc':
                        address = 'offers.quantity <'
                    elif item[0] != 'page' and item[0] != 'page_size':
                        address = item[0].replace('_', '.')
                    if 'address' in locals():
                        query += prefix + f"{address}= {item[1]}"
                        del address
                        prefix = " AND "
                # if "favorite" in data:
                #     query += prefix + f"products.id = '{data['product_id']}'"
                #     prefix = " AND "
                # if "have_price" in data:
                #     if data['have_price'] is True:
                #         query += prefix + "offers.price > 0"
                #     else:
                #         query += prefix + "(offers.price = 0 or offers.price is null)"
                #     prefix = " AND "
            query += f""" OFFSET {data.page * data.page_size}
                         LIMIT {data.page_size}"""

            result = await session.execute(query)

            for item in result:
                output = {
                    # "username": item.username,
                    # "partner_name": item.partner_name,
                    "product": {
                        "id": item.product_id,
                        "article": item.product_article,
                        "barcode": item.product_barcode,
                        "name": item.product_name,
                        "favourite": item.favorite,
                        "updated": str(item.product_updated),
                    },
                    "offer": {
                        "price": float(item.offer_price) if item.offer_price else None,
                        "quantity": item.offer_quantity,
                        "updated": str(item.offer_updated) if item.offer_updated else None,
                    },
                    "segment": {"id": item.segment_id, "name": item.segment_name},
                    "brand": {"id": item.brands_id, "name": item.brands_name},
                    "category": {"id": item.categories_id, "name": item.categories_name},
                    "country": {
                        "code": item.countries_code,
                        "emoji": item.countries_emoji,
                        "name": item.countries_name,
                    },
                }
                res['data'].append(output)
    query = query[query.find('LEFT OUTER JOIN partners'):query.find(' OFFSET')]
    query = "SELECT COUNT(products.id) FROM users " + query
    result = await session.execute(query)
    for item in result:
        total = item.count
    res['page'] = data.page + 1
    res['page_size'] = data.page_size
    res['total'] = total
    return res
