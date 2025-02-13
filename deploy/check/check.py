import json
import os
import asyncio
import logging
from aiomcache import Client

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

memcached_host = os.environ.get("MEMCACHED_HOST") or "localhost"

alert_loop_time = os.environ.get("ALERT_PERIOD") or 3


async def alarm_data(mc, alerts_cached_data):
    try:
        task1_result = await mc.get(b"alerts")
        logger.debug("Task 1...")

        if task1_result:
            logger.debug("result")
            encoded_result = json.loads(task1_result.decode("utf-8"))
            logging.info(task1_result.decode("utf-8"))

        await asyncio.sleep(alert_loop_time)

    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        raise


async def main():
    mc = Client(memcached_host, 11211)  # Connect to your Memcache server
    alerts_cached_data = {}
    while True:
        try:
            print(f"task start")
            await alarm_data(mc, alerts_cached_data)

        except asyncio.CancelledError:
            print("Task canceled. Shutting down...")
            await mc.close()
            break

        except Exception as e:
            print(f"Caught an exception: {e}")

        finally:
            asyncio.sleep(1)


if __name__ == "__main__":
    try:
        logger.debug("Task 1: Doing some cool async stuff...")
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
