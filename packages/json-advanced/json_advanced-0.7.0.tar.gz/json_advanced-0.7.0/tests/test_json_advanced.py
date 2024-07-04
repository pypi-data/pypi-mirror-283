import json
import unittest

from json_advanced.json_encoder import JSONSerializer, dumps, json_deserializer, loads


class TestJSONSerialization(unittest.TestCase):
    def test_normal(self):
        data = {
            "str": "string",
            "int": 1,
            "float": 1.0,
            "bool": True,
            "none": None,
        }
        json_string = dumps(data)
        self.assertEqual(loads(json_string), data)
        print("test_normal passed")

    def test_path(self):
        from pathlib import Path

        data = {
            "path": Path("/path/to/file"),
        }
        json_string = dumps(data)
        self.assertEqual(Path(loads(json_string).get("path")), data.get("path"))
        print("test_path passed")

    def test_datetime(self):
        import datetime

        data = {
            "datetime": datetime.datetime.now(),
            "date": datetime.date.today(),
            "time": datetime.datetime.now().time(),
        }
        json_string = dumps(data)
        self.assertEqual(loads(json_string), data)
        print("test_datetime passed")

    def test_date(self):
        import datetime

        data = {
            "date": datetime.date.today(),
        }
        json_string = json.dumps(data, cls=JSONSerializer)
        self.assertEqual(json.loads(json_string, object_hook=json_deserializer), data)
        print("test_date passed")

    def test_time(self):
        import datetime

        data = {
            "time": datetime.datetime.now().time(),
        }
        json_string = json.dumps(data, cls=JSONSerializer)
        self.assertEqual(json.loads(json_string, object_hook=json_deserializer), data)
        print("test_time passed")

    def test_base64(self):
        data = {
            "bytes": b"bytes",
        }
        json_string = dumps(data)
        self.assertEqual(loads(json_string), data)
        print("test_base64 passed")

    def test_uuid(self):
        import uuid

        data = {
            "uuid": uuid.uuid4(),
        }
        json_string = dumps(data)
        self.assertEqual(loads(json_string), data)
        print("test_uuid passed")

    def test_dumps_loads(self):
        data = {
            "str": "string",
            "int": 1,
            "float": 1.0,
            "bool": True,
            "none": None,
        }
        json_string = dumps(data)
        self.assertEqual(loads(json_string), data)
        print("test_dumps_loads passed")


if __name__ == "__main__":
    unittest.main()
