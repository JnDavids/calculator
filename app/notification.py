import time
import json

from logger import logger
from http.client import HTTPResponse
from urllib.request import Request, urlopen
from persist import CalcPersistenceInDB
from pushbullet_config import (
    PUSHBULLET_ACCESS_TOKEN,
    PUSHBULLET_TARGET
)


class Pushbullet:

    __slots__ = ["_access_token", "_target"]

    def __init__(
        self, access_token: str, target: dict[str, str]
    ) -> None:
        self._access_token = access_token
        self._target = target

    def create_push(
        self, msg: str, title: str | None = None
    ) -> HTTPResponse:
        body = self.get_send_push_request_body(msg, title)
        request = self.get_send_push_request(body)

        return urlopen(request)

    def get_send_push_request_body(
        self, msg: str, title: str | None
    ) -> dict[str, str]:
        body = {
            "type": "note",
            "body": msg,
            **self._target
        }
        if title:
            body["title"] = title

        return body

    def get_send_push_request(self, body: dict[str, str]) -> Request:
        return Request(
            url="https://api.pushbullet.com/v2/pushes",

            data=json.dumps(body).encode(),

            headers={
                "Access-Token": self._access_token,
                "Content-Type": "application/json"
            },

            method="POST"
        )


try:
    calculations_db = CalcPersistenceInDB()
    count = calculations_db.get_calculations_count()
except Exception as err:
    logger.error(err)
    count = None

while count is not None:
    time.sleep(60)

    try:
        new_count = calculations_db.get_calculations_count()
    except Exception as err:
        logger.error(err)
        continue

    if count >= new_count:
        continue

    new_calculations = new_count - count
    count = new_count

    msg = (f"You have {new_calculations} new calculation"
           + ("s" if new_calculations > 1 else ""))

    pushbullet = Pushbullet(PUSHBULLET_ACCESS_TOKEN, PUSHBULLET_TARGET)
    pushbullet.create_push(msg, "Calculator")