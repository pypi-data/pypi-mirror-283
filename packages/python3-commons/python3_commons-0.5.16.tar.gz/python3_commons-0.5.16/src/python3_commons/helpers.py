import datetime
import logging
import shlex

from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping

logger = logging.getLogger(__name__)


def date_from_string(string: str, fmt: str = '%d.%m.%Y') -> datetime.date:
    try:
        return datetime.datetime.strptime(string, fmt).date()
    except ValueError:
        return datetime.date.fromisoformat(string)


def datetime_from_string(string: str) -> datetime.datetime:
    try:
        return datetime.datetime.strptime(string, '%d.%m.%Y %H:%M:%S')
    except ValueError:
        return datetime.datetime.fromisoformat(string)


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + datetime.timedelta(days=n)


def tries(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for time in range(times if times > 0 else 1):
                # noinspection PyBroadException
                try:
                    return await f(*args, **kwargs)
                except Exception as exc:
                    if time >= times:
                        raise exc

        return wrapper

    return func_wrapper


def round_decimal(value: Decimal, decimal_places=2, rounding_mode=ROUND_HALF_UP) -> Decimal:
    try:
        return value.quantize(Decimal(10) ** -decimal_places, rounding=rounding_mode)
    except AttributeError:
        return value


def request_to_curl(url: str, method: str, headers: Mapping, body: bytes | None = None) -> str:
    curl_cmd = ['curl', '-i', '-X', method, shlex.quote(url)]

    for key, value in headers.items():
        header_line = f'{key}: {value}'
        curl_cmd.append('-H')
        curl_cmd.append(shlex.quote(header_line))

    if body is not None:
        curl_cmd.append('--data')
        curl_cmd.append(shlex.quote(body.decode('utf-8')))

    return ' '.join(curl_cmd)
