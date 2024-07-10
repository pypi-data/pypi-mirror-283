#!/usr/bin/env python3

import asyncio
import asyncssh

hostname = 'localhost'
user = 'root'

async def f():
  async with asyncssh.connect(hostname, username=user) as c:
      async with c.create_process('sleep 300') as p:
        print('sleep')
        await asyncio.sleep(3)

        print('terminate')
        p.terminate()

        print('wait')
        await p.wait()

        print('done')

if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.run_until_complete(f())
  loop.close()
