import asyncio
import sqlalchemy as sa
from pymysql.err import ProgrammingError
from aiomysql.sa import create_engine
from aiomysql.sa.transaction import Transaction

metadata = sa.MetaData()

tbl = sa.Table('tbl', metadata,
               sa.Column('id', sa.Integer, primary_key=True),
               sa.Column('val', sa.String(255)))


async def insertVal(conn,value):
    trans = await conn.begin() # 会真正提交数据
    await conn.execute(tbl.insert().values(val=value))
    await trans.commit()

    # try:
    #     n = await conn.execute(tbl.insert().values(val=value)) # 不会真正提交至DB
    #     await n.close()
    # except ProgrammingError as e:
    #     print(e)


async def selectVal(conn):
    # print(dir(tbl))
    try:
        rows = await conn.execute(tbl.select())
        async for row in rows:  # 这里async 必须
            # print(dir(row))
            print(row.id, row.val)
    except ProgrammingError as e:
        print(e)

async def go(loop):
    engine = await create_engine(user='falcon', db='test',
                                 host='192.168.43.11', password='123456', loop=loop)

    async with engine.acquire() as conn:
        await insertVal(conn, "abc")
        await insertVal(conn, "abc1")
        # print(dir(conn))
        await selectVal(conn)

        # async for row in conn.execute(tbl.select()):
        #     print(row.id, row.val)

    engine.close()
    await engine.wait_closed()


loop = asyncio.get_event_loop()
loop.run_until_complete(go(loop))
