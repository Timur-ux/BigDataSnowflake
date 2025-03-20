import sys
sys.path.append("/".join(__file__.split("/")[:-2]))
from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession
from db.database import connection
from db.models import RawData
import asyncio


@connection
async def checkSaleIdsInconsistent(session: AsyncSession):
    print("Check if in some rows sale_..._id not equal to row id")
    values = (await session.execute(select(RawData.id, RawData.sale_seller_id, RawData.sale_product_id, RawData.sale_customer_id)))

    for id, seller_id, product_id, customer_id in values:
        if id < max(int(seller_id), int(product_id), int(customer_id)) + (1000 * ((id - 1) // 1000)):
            print(f"WARN: In row with id: {id} some id ref to future entities")
        if id > min(int(seller_id), int(product_id), int(customer_id)) + (1000 * ((id - 1) // 1000)):
            print(f"WARN: In row with id: {id} some id ref to past entities")
    print("Done, if no wanr messages up then all right")

async def main():
    await checkSaleIdsInconsistent()

if __name__ == "__main__":
    asyncio.run(main())
        
