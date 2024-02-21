import json
import os
import time
from http.client import HTTPResponse
from urllib.request import HTTPError, Request, urlopen

from persistence import CalculationsDB
from utils import get_logger


class Pushbullet:

    __slots__ = ["_access_token", "_target_type", "_target"]

    def __init__(
        self,
        access_token: str,
        target_type: str | None = None,
        target: str | None = None
    ) -> None:
        if access_token:
            self._access_token = access_token
            self._target_type = target_type
            self._target = target
        else:
            raise Exception("Missing Pushbullet access token")

    def note(self, msg: str, title: str | None = None) -> HTTPResponse:
        body = self._note_request_body(msg, title)
        request = self._note_request(body)

        return urlopen(request)

    def _note_request_body(
        self, msg: str, title: str | None
    ) -> dict[str, str]:
        body = {
            "type": "note",
            "body": msg
        }
        if title:
            body["title"] = title

        if self._target_type and self._target:
            body[self._target_type] = self._target

        return body

    def _note_request(self, body: dict[str, str]) -> Request:
        return Request(
            url="https://api.pushbullet.com/v2/pushes",

            data=json.dumps(body).encode(),

            headers={
                "Access-Token": self._access_token,
                "Content-Type": "application/json"
            },

            method="POST"
        )


def main():
    logger = get_logger("notification")
    push_interval = int(os.getenv("PUSH_INTERVAL", 5)) or 1

    try:
        pushbullet = Pushbullet(
            os.getenv("PUSHBULLET_ACCESS_TOKEN"),
            os.getenv("PUSHBULLET_TARGET_TYPE"),
            os.getenv("PUSHBULLET_TARGET")
        )
        calculations_db = CalculationsDB()
        count = calculations_db.get_calculations_count()
    except Exception as err:
        logger.error(err)
        count = None

    while count is not None:
        time.sleep(push_interval * 60)

        try:
            new_count = calculations_db.get_calculations_count()
        except Exception as err:
            logger.error(err)
            continue

        if count >= new_count:
            continue

        new_calculations = new_count - count

        msg = (f"You have {new_calculations} new calculation"
            + ("s" if new_calculations > 1 else ""))

        try:
            pushbullet.note(msg, "Calculator")
            count = new_count
        except HTTPError as err:
            logger.error(err.read().decode())


if __name__ == "__main__":
    main()