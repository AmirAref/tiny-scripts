import asyncio
import logging
from pyrogram.client import Client
import pyrogram


API_ID=12345
API_HASH="abcdefgh:123456778"
CHAT_ID=-10012345678
proxy = {
     "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
     "hostname": "127.0.0.1",
     "port": 2080,
}
client = Client(name="downloader", api_id=API_ID, api_hash=API_HASH, proxy=proxy)
SEMPHORE = asyncio.Semaphore(10)

async def progress(current, total, file_name):
    print(f"{file_name} : {current * 100 / total:.1f}%")

async def download_file(message : pyrogram.types.Message, client : Client, semphore : asyncio.Semaphore = SEMPHORE ):
    # download media from file
    async with semphore:
        await client.download_media(message=message, progress=progress, progress_args=(message.document.file_name, ))



async def main():
    # start client
    await client.connect()
    # get messages ids
    try:
        messages = await client.get_messages(chat_id=CHAT_ID, message_ids=list(range(1, 50)))
        tasks = []
        for msg in messages:
            # check has media or not
            media = msg.media
            if not msg.media:
                continue
            # download task
            tasks.append(download_file(message=msg, client=client))

        # gathering tasks
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception as e:
        logging.error("Error fetching messages : ", exc_info=e)
    finally:
        await client.disconnect()


asyncio.run(main())
