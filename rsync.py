import asyncio
import aiosqlite

async def consumer(db, row):
    cmd = f"rsync -az --password-file=/etc/rsyncpasswd root@192.168.1.105::backup/{row[1]}"
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout = asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE
    )
    stdout, stderr = proc.communicate()
    print(f"{cmd!r} exited with {proc.returncode}")
    if stdout:
        print(f"stdout: {stdout.decode()}")
    if stderr:
        print(f"stderr: {stderr.decode()}")
    await db.execute("update event set status='1' where id = ?", (row[0],))
    await db.commit()
    print(row)

async def producer():
    queue = asyncio.Queue()
    tasks = []

    async with aiosqlite.connect("async.db") as db: 
        while True:
            if queue.empty():
                sql = "select id, path from event where status='0'"
                async with db.execute(sql) as cursor:
                    async for row in cursor:
                        queue.put_nowait(row)
            if queue.empty():
                continue
            for _ in range(queue.qsize()):
                task = asyncio.create_task(consumer(db, queue.get_nowait()))
                tasks.append(task)
                print(f"Queue is empty: {queue.empty()}")
            await asyncio.gather(*tasks, return_exceptions=True)
            tasks.clear()
            print("tasks done...")


asyncio.run(producer())
        
        







