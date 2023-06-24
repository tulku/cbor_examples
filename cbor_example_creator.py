import base64
import json
from datetime import datetime, timedelta, timezone

import cbor2
import numpy
import requests


def encode_b64(sensor):
    sensor = base64.b64encode(sensor)
    return sensor.decode("utf-8")


def to_cbor(message: list) -> bytes:
    return cbor2.dumps(message)


def to_json(message: list) -> str:
    return json.dumps(message)


def post_metric(message):
    requests.post(
        "http://localhost:8181/cbor",
        data=message,
        headers={"Content-Type": "application/cbor", "Device-Id": "123456"},
    )


def stringify_keys(content: list, prefix: str = "k"):
    out = []
    for element in content:
        out.append({f"{prefix}{str(k)}": v for k, v in element.items()})
    return out


def get_time(minutes: int = 0) -> float:
    return (datetime.now(tz=timezone.utc) - timedelta(minutes=minutes)).timestamp()


def gen_ex1(string_keys: bool = False):
    ex1 = [
        {
            261: True,
            259: "14ca85ed9",
            258: "002-2.1.x",
            264: 23.760,
            265: 68.934,
            263: 3,
            266: False,
            260: get_time(),
        }
    ]

    return ex1 if not string_keys else stringify_keys(ex1)


def gen_ex2(string_keys: bool = False):
    ex2 = [
        {
            787: 3.632,
            785: 30.0,
            786: 0,
            802: 0.256,
            801: -0.000183,
            804: 3.648,
            803: -0.000183,
            806: 3.632,
            805: 0.0697,
            260: get_time(),
        }
    ]

    return ex2 if not string_keys else stringify_keys(ex2)


def read_sensor_from_file(file_name):
    image = numpy.fromfile(file_name, dtype=numpy.float16)
    return image.tobytes()


def gen_ex3(string_keys: bool = False, b64: bool = True):
    raw_calibration = b"\xaa\xff"
    raw_data = read_sensor_from_file("f0008.bin")
    # raw_data = b'\x0e\xa0'
    sensor_data = raw_data if not b64 else encode_b64(raw_data)
    calibration = raw_calibration if not b64 else encode_b64(raw_calibration)

    sensor = [
        {
            6433: sensor_data,
            6434: calibration,
            6435: 23.435,
            6436: 24.290,
            6144: 0,
            6145: 0,
            260: get_time(),
        }
    ]

    return sensor if not string_keys else stringify_keys(sensor)


if __name__ == "__main__":
    all_strings = True

    ex1 = gen_ex1(all_strings)
    ex2 = gen_ex2(all_strings)
    ex3_raw = gen_ex3(all_strings, b64=False)
    ex3_b64 = gen_ex3(all_strings, b64=True)

    print("Example1:")
    print(f"cbor: {to_cbor(ex1)}")
    print(f"json: {to_json(ex1)}")
    print("Example2:")
    print(f"cbor: {to_cbor(ex2)}")
    print(f"json: {to_json(ex2)}")
    print("Example3:")
    print(f"cbor: {to_cbor(ex3_raw)}")
    print(f"json: {to_json(ex3_b64)}")

    send = True

    if send:
        messages = [ex1, ex2, ex3_raw]
        for message in messages:
            post_metric(to_cbor(message))
