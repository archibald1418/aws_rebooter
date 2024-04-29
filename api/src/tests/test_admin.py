import http.server
import pytest
import datetime
from pprint import pprint
from http import HTTPStatus
import json
from typing import Literal

from . import TestClient, ADMIN, WEBHOOK_URL, TEST_USER


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
    "cmd,id", [
        pytest.param("/get", ADMIN),
        pytest.param("/garbage", ADMIN),
        pytest.param("/get", TEST_USER, marks=pytest.mark.xfail)
    ]
)
def test_admin_cmd(test_client: TestClient, cmd: str, id: int):
    response = test_client.post(url=WEBHOOK_URL, json=UpdateFake(cmd, id))
    # pprint(response.json())
    assert 'error' not in response.json()
    # pprint(response.json())
    # assert None, "Haha, the test is going great!"
