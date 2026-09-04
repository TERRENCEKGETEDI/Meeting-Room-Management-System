import asyncio
import time
import httpx

BASE_URL = "http://127.0.0.1:8000/basic"


async def test_route(route: str):
    start = time.perf_counter()

    async with httpx.AsyncClient(timeout=15) as client:
        await asyncio.gather(
            client.get(f"{BASE_URL}{route}"),
            client.get(f"{BASE_URL}{route}"),
        )

    elapsed = time.perf_counter() - start

    print(f"{route}: {elapsed:.2f} seconds")


async def main():
    await test_route("/bad-async")
    await test_route("/good-async")


if __name__ == "__main__":
    asyncio.run(main())