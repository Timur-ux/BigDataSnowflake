import sys
sys.path.append("/".join(__file__.split("/")[:-2]))

from datetime import datetime
from db.api.location import get_city_id, get_country_id, get_state_id
from db.api.pet import get_pet_breed_id, get_pet_category_id, get_pet_type_id
from db.api.product import get_brand_id, get_color_id, get_material_id, get_product_cat_id
from db.database import connection
import asyncio
from sqlalchemy import Sequence, select
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.models import Brand, Breed, City, Color, Country, Customer, CustomerPet, Material, PetCategory, PetType, Product, ProductCategory, RawData, Sale, Seller, State, Store, Supplier


@connection
async def preprocessEnumValues(rows: list[RawData], session: AsyncSession):
    """Fetch unique countries, cities, states, brands etc"""
    countries = set()
    pet_types = set()
    breeds = set()
    product_category = set()
    cities = set()
    states = set()
    pet_categories = set()
    colors = set()
    brands = set()
    materials = set()
    for row in rows:
        countries.add(row.customer_country)
        pet_types.add(row.customer_pet_type)
        breeds.add(row.customer_pet_breed)
        product_category.add(row.product_category)
        cities.add(row.store_city)
        states.add(row.store_state)
        countries.add(row.store_country)
        pet_categories.add(row.pet_category)
        colors.add(row.product_color)
        brands.add(row.product_brand)
        materials.add(row.product_material)
        cities.add(row.supplier_city)
        countries.add(row.supplier_country)

    for c in countries:
        if c is not None:
            session.add(Country(name=c))
    for pet_type in pet_types:
        if pet_type is not None:
            session.add(PetType(name=pet_type))
    for breed in breeds:
        if breed is not None:
            session.add(Breed(name=breed))
    for cat in product_category:
        if cat is not None:
            session.add(ProductCategory(name=cat))
    for city in cities:
        if city is not None:
            session.add(City(name=city))
    for state in states:
        if state is not None:
            session.add(State(name=state))
    for cat in pet_categories:
        if cat is not None:
            session.add(PetCategory(name=cat))
    for color in colors:
        if color is not None:
            session.add(Color(name=color))
    for brand in brands:
        if brand is not None:
            session.add(Brand(name=brand))
    for material in materials:
        if material is not None:
            session.add(Material(name=material))
    await session.commit()
    return countries, pet_types, breeds, product_category, cities, states, pet_categories, colors, brands, materials


@connection
async def splitRawDataToFacts(session: AsyncSession):
    rawRows = list((await session.execute(select(RawData).order_by(RawData.id.asc()))).scalars().all())

    await preprocessEnumValues(rawRows)

    for i, row in enumerate(rawRows):
        if (i + 1) % 100 == 0:
            print(f"Processed {i+1} rows")
        customer = Customer(
            id=int(row.sale_customer_id) + (1000 * (i // 1000)
                                            ) if row.sale_customer_id is not None else None,
            first_name=row.customer_first_name,
            last_name=row.customer_last_name,
            email=row.customer_email,
            country_id=(await get_country_id(row.customer_country)),
            postal_code=row.customer_postal_code,
            age=int(row.customer_age)
        )
        customerPet = CustomerPet(
            customer_id=int(row.sale_customer_id) + (1000 * (i // 1000)),
            type_id=(await get_pet_type_id(row.customer_pet_type)),
            category_id=(await get_pet_category_id(row.pet_category)),
            name=row.customer_pet_name,
            breed_id=(await get_pet_breed_id(row.customer_pet_breed))
        )
        seller = Seller(
            id=int(row.sale_seller_id) + (1000 * (i // 1000)
                                          ) if row.sale_seller_id is not None else None,
            first_name=row.seller_first_name,
            last_name=row.seller_last_name,
            email=row.seller_email,
            country_id=(await get_country_id(row.seller_country)),
            postal_code=row.seller_postal_code
        )
        product = Product(
            id=int(row.sale_product_id) + (1000 * (i // 1000)
                                           ) if row.sale_product_id is not None else None,
            name=row.product_name,
            category_id=(await get_product_cat_id(row.product_category)),
            price=float(row.product_price),
            quantity=int(row.product_quantity),
            weight=float(row.product_weight),
            color_id=(await get_color_id(row.product_color)),
            size=row.product_size,
            brand_id=(await get_brand_id(row.product_brand)),
            material_id=(await get_material_id(row.product_material)),
            description=row.product_description,
            rating=float(row.product_rating),
            reviews=int(row.product_reviews),
            release_date=datetime.strptime(
                row.product_release_date, "%m/%d/%Y"),
            expiry_date=datetime.strptime(row.product_expiry_date, "%m/%d/%Y")
        )
        sale = Sale(
            date=datetime.strptime(row.sale_date, "%m/%d/%Y"),
            customer_id=int(row.sale_customer_id) + (1000 * (i // 1000)),
            seller_id=int(row.sale_seller_id) + (1000 * (i // 1000)),
            product_id=int(row.sale_product_id) + (1000 * (i // 1000)),
            quantity=int(row.sale_quantity),
            total_price=float(row.sale_total_price)
        )
        store = Store(
            name=row.store_name,
            location=row.store_location,
            city_id=(await get_city_id(row.store_city)),
            state_id=(await get_state_id(row.store_state)),
            country_id=(await get_country_id(row.store_country)),
            phone=row.store_phone,
            email=row.store_email
        )
        supplier = Supplier(
            name=row.supplier_name,
            contact=row.supplier_contact,
            email=row.supplier_email,
            phone=row.supplier_phone,
            address=row.supplier_address,
            city_id=(await get_city_id(row.supplier_city)),
            country_id=(await get_country_id(row.supplier_country))
        )
        session.add(customer)
        session.add(seller)
        session.add(product)
        session.add(supplier)
        session.add(store)
        await session.commit()
        session.add(sale)
        session.add(customerPet)


async def main():
    await splitRawDataToFacts()

if __name__ == "__main__":
    asyncio.run(main())
