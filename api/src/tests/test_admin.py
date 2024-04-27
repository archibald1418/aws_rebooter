import pytest
import datetime
from pprint import pprint

from . import TestClient, ADMIN, WEBHOOK_URL


class UpdateFake(dict):

    def __new__(cls, cmd: str, id: int):
        return {
            "message": {
                "chat": {
                    "first_name": "Piglet",
                    "id": id,
                    "last_name": "Oink",
                    "type": "private",
                    "username": "caralho",
                },
                "date": 42069,
                "entities": [{"length": 6, "offset": 0, "type": "bot_command"}],
                "from": {
                    "first_name": "Oleg",
                    "id": id,
                    "is_bot": False,
                    "language_code": "en",
                    "last_name": "Oink",
                    "username": "caralho",
                },
                "message_id": 42069,
                "text": cmd,
            },
            "update_id": 42069,
        }



@pytest.mark.parametrize(
    "cmd,id", [("/get", ADMIN), ("/garbage", ADMIN), ("/get", 42069)]
)
def test_admin_cmd(test_client: TestClient, cmd: str, id: int):
    response = test_client.post(url=WEBHOOK_URL, json=UpdateFake(cmd, id))
    pprint(response.json())
    print(response.status_code)
    assert None, "Haha, the test is going great!"
