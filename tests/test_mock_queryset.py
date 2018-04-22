import unittest
from pymodm import MongoModel, fields, connect
from modmmocker import mock_queryset


connect("mongodb://localhost:27017/x")


class TestModel(MongoModel):
    foo = fields.CharField()
    bar = fields.IntegerField()


mock_data = [
    dict(foo="abc", bar=123),
    dict(foo="def", bar=456),
    dict(foo="ghi", bar=789)]


class MockManagerTests(unittest.TestCase):
    @mock_queryset(TestModel, mock_data)
    def test_all(self):
        results = list(TestModel.objects.all())

        self.assertEqual(len(results), 3)
        self.assertTrue(isinstance(results[0], TestModel))
        self.assertEqual(results[0].foo, "abc")
        self.assertEqual(results[1].foo, "def")
        self.assertEqual(results[2].foo, "ghi")

    @mock_queryset(TestModel, mock_data)
    def test_raw(self):
        results = list(TestModel.objects.raw({"bar": 456}))

        self.assertEqual(len(results), 1)
        self.assertTrue(isinstance(results[0], TestModel))
        self.assertEqual(results[0].foo, "def")

    @mock_queryset(TestModel, mock_data)
    def test_first(self):
        result = TestModel.objects.first()

        self.assertTrue(isinstance(result, TestModel))
        self.assertEqual(result.foo, "abc")
        self.assertEqual(result.bar, 123)

    @mock_queryset(TestModel, mock_data)
    def test_create(self):
        result = list(TestModel.objects.all())
        self.assertEqual(len(result), 3)

        TestModel.objects.create(**{"foo": "jkl", "bar": 0})

        result = list(TestModel.objects.all())
        self.assertEqual(len(result), 4)

    @mock_queryset(TestModel, mock_data)
    def test_update(self):
        TestModel.objects.raw({"bar": 456}).update({"$set": {"foo": "jkl"}})

        result = list(TestModel.objects.raw({"bar": 456}))
        self.assertTrue(isinstance(result[0], TestModel))
        self.assertEqual(result[0].foo, "jkl")
        self.assertEqual(result[0].bar, 456)

    @mock_queryset(TestModel, mock_data)
    def test_delete(self):
        results = list(TestModel.objects.all())
        self.assertEqual(len(results), 3)

        result = TestModel.objects.raw({"bar": 456}).delete()
        self.assertEqual(result, 1)

        results = list(TestModel.objects.all())
        self.assertEqual(len(results), 2)
