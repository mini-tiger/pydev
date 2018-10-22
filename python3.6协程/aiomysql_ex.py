import asyncio
import aiomysql


async def reqUser(conn,user):
    async with conn.cursor() as cur:
        await cur.execute("SELECT Host,User FROM user WHERE `User`='%s'" % user)
        print(cur.description)
        r = await cur.fetchall()
        print(r)
    return r


async def test_example(loop):
    ## 使用单链接方式
    # conn = await aiomysql.connect(host='192.168.43.11', port=3306,
    #                               user='falcon', password='123456', db='mysql',
    #                               loop=loop)

    ## 连接池方式
    pool = await aiomysql.create_pool(minsize=10, maxsize=100, host='192.168.43.11', port=3306,
                                  user='falcon', password='123456', db='mysql',
                                  loop=loop)

    conn = await pool.acquire() # 申请一个连接
    u1 = await reqUser(conn,"falcon")
    pool.release(conn) # 释放一个链接，

    conn = await  pool.acquire()  # 可以一直使用一个连接，这里是演示
    u2 = await reqUser(conn,"root")
    conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))