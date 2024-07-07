import asyncio
import json
import time
import websockets    


async def query_relays(self, query_dict, timeout=5):
    for relay in self.relays:
        try:
            async with websockets.connect(relay) as ws:
                query_ws = json.dumps(("REQ", "5326483051590112", query_dict))
                await ws.send(query_ws)
                print(f"Query sent to relay {relay}: {query_ws}")
                responses_received = 0
                start_time = time.time()
                response_limit = query_dict.get("limit", 3)
                while (
                    responses_received < response_limit
                    and (time.time() - start_time) < timeout
                ):
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=1)
                        self.print_color(f"Response from {relay}: {response}", "32")
                        responses_received += 1
                    except asyncio.TimeoutError:
                        self.print_color(
                            "No response within 1 second, continuing...", "31"
                        )
                        break
        except Exception as exc:
            self.print_color(f"Exception is {exc}, error querying {relay}", "31")