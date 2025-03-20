from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, DateTime, ForeignKey, ForeignKeyConstraint
from db.database import Base


class RawData(Base):
    __tablename__ = "raw_data"

    customer_first_name: Mapped[str | None]
    customer_last_name: Mapped[str | None]
    customer_age: Mapped[str | None]
    customer_email: Mapped[str | None]
    customer_country: Mapped[str | None]
    customer_postal_code: Mapped[str | None]
    customer_pet_type: Mapped[str | None]
    customer_pet_name: Mapped[str | None]
    customer_pet_breed: Mapped[str | None]
    seller_first_name: Mapped[str | None]
    seller_last_name: Mapped[str | None]
    seller_email: Mapped[str | None]
    seller_country: Mapped[str | None]
    seller_postal_code: Mapped[str | None]
    product_name: Mapped[str | None]
    product_category: Mapped[str | None]
    product_price: Mapped[str | None]
    product_quantity: Mapped[str | None]
    sale_date: Mapped[str | None]
    sale_customer_id: Mapped[str | None]
    sale_seller_id: Mapped[str | None]
    sale_product_id: Mapped[str | None]
    sale_quantity: Mapped[str | None]
    sale_total_price: Mapped[str | None]
    store_name: Mapped[str | None]
    store_location: Mapped[str | None]
    store_city: Mapped[str | None]
    store_state: Mapped[str | None]
    store_country: Mapped[str | None]
    store_phone: Mapped[str | None]
    store_email: Mapped[str | None]
    pet_category: Mapped[str | None]
    product_weight: Mapped[str | None]
    product_color: Mapped[str | None]
    product_size: Mapped[str | None]
    product_brand: Mapped[str | None]
    product_material: Mapped[str | None]
    product_description: Mapped[str | None]
    product_rating: Mapped[str | None]
    product_reviews: Mapped[str | None]
    product_release_date: Mapped[str | None]
    product_expiry_date: Mapped[str | None]
    supplier_name: Mapped[str | None]
    supplier_contact: Mapped[str | None]
    supplier_email: Mapped[str | None]
    supplier_phone: Mapped[str | None]
    supplier_address: Mapped[str | None]
    supplier_city: Mapped[str | None]
    supplier_country: Mapped[str | None]


class Customer(Base):
    __tablename__ = "customers"

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    postal_code: Mapped[str | None]
    age: Mapped[int]

    pet: Mapped["CustomerPet | None"] = relationship(back_populates="customer")
    country: Mapped["Country | None"] = relationship()


class CustomerPet(Base):
    __tablename__ = "customer_pets"

    type_id: Mapped[int | None] = mapped_column(ForeignKey("pet_types.id"))
    category_id: Mapped[int | None] = mapped_column(ForeignKey("pet_categories.id"))
    name: Mapped[str]
    breed_id: Mapped[int | None] = mapped_column(ForeignKey("breeds.id"))
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id"))

    customer: Mapped["Customer | None"] = relationship(back_populates="pet")
    type: Mapped["PetType | None"] = relationship()
    category: Mapped["PetCategory | None"] = relationship()
    breed: Mapped["Breed | None"] = relationship()


class Breed(Base):
    __tablename__ = "breeds"

    name: Mapped[str]


class PetType(Base):
    __tablename__ = "pet_types"

    name: Mapped[str]


class Seller(Base):
    __tablename__ = "sellers"

    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    postal_code: Mapped[str | None]

    country: Mapped["Country | None"] = relationship()


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("product_categories.id"))
    price: Mapped[float]
    quantity: Mapped[int]
    weight: Mapped[float]
    color_id: Mapped[int | None] = mapped_column(ForeignKey("colors.id"))
    size: Mapped[str]
    brand_id: Mapped[int | None] = mapped_column(ForeignKey("brands.id"))
    material_id: Mapped[int | None] = mapped_column(ForeignKey("materials.id"))
    description: Mapped[str]
    rating: Mapped[float]
    reviews: Mapped[int]
    release_date: Mapped[datetime] = mapped_column(DateTime)
    expiry_date: Mapped[datetime] = mapped_column(DateTime)

    category: Mapped["ProductCategory | None"] = relationship()
    color: Mapped["Color | None"] = relationship()
    brand: Mapped["Brand | None"] = relationship()
    material: Mapped["Material | None"] = relationship()


class Color(Base):
    __tablename__ = "colors"

    name: Mapped[str]


class Brand(Base):
    __tablename__ = "brands"

    name: Mapped[str]


class Material(Base):
    __tablename__ = "materials"

    name: Mapped[str]


class ProductCategory(Base):
    __tablename__ = "product_categories"

    name: Mapped[str]


class Sale(Base):
    __tablename__ = "sales"

    date: Mapped[datetime] = mapped_column(DateTime)
    customer_id: Mapped[int | None] = mapped_column(ForeignKey("customers.id"))
    seller_id: Mapped[int | None] = mapped_column(ForeignKey("sellers.id"))
    product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]
    total_price: Mapped[float]

    customer: Mapped["Customer | None"] = relationship()
    seller: Mapped["Seller | None"] = relationship()
    product: Mapped["Product | None"] = relationship()


class Store(Base):
    __tablename__ = "stores"

    name: Mapped[str]
    location: Mapped[str]
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"))
    state_id: Mapped[int | None] = mapped_column(ForeignKey("states.id"))
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))
    phone: Mapped[str]
    email: Mapped[str]

    city: Mapped["City | None"] = relationship()
    state: Mapped["State | None"] = relationship()
    country: Mapped["Country | None"] = relationship()


class City(Base):
    __tablename__ = "cities"

    name: Mapped[str]


class State(Base):
    __tablename__ = "states"

    name: Mapped[str]


class Country(Base):
    __tablename__ = "countries"

    name: Mapped[str]


class PetCategory(Base):
    __tablename__ = "pet_categories"

    name: Mapped[str]


class Supplier(Base):
    __tablename__ = "suppliers"

    name: Mapped[str]
    contact: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    address: Mapped[str]
    city_id: Mapped[int | None] = mapped_column(ForeignKey("cities.id"))
    country_id: Mapped[int | None] = mapped_column(ForeignKey("countries.id"))

    city: Mapped["City | None"] = relationship()
    country: Mapped["Country | None"] = relationship()

