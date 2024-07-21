import asyncio
import aiohttp
import random

async def send_request(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, "http://localhost:5000/home") for _ in range(10000)]
        responses = await asyncio.gather(*tasks)
    
    server_counts = {}
    for response in responses:
        server_id = response['message'].split(":")[1].strip()
        server_counts[server_id] = server_counts.get(server_id, 0) + 1
    
    return server_counts

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)