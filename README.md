# modmmocker
A Proof of Concept mocker for PyMODM. This package seeks to resovle the ability to test a PyMODM project without needing to prop a test database for lightweight unit tests.

This mocker can be applied by wrapping a test in a decorator that takes:
* The `MongoModel` that will be mocked
* A list of dummy data or a JSON file with a list of dummy data

The dummy data should be represented as a list of dictionaries. A key in a dictionary corresponds to the field name, while the value will be the data that will be returned for a given field. If no `_id` is provided in a dictionary, then this mocker will automatically generate one.

# Examples
```python
class SomeModel(MongoModel):
    foo = fields.CharField()
    bar = fields.IntegerField()


mock_data = [
    dict(foo="abc", bar=123),
    dict(foo="def", bar=456),
    dict(foo="ghi", bar=789)]


class SomeModelTests(unittest.TestCase):
    @mock_queryset(SomeModel, mock_data)
    def test_query(self):
        results = list(SomeModel.objects.all())

        self.assertEqual(len(results), 3)
        self.assertTrue(isinstance(results[0], TestModel))
        self.assertEqual(results[0].foo, "abc")
        self.assertEqual(results[1].foo, "def")
        self.assertEqual(results[2].foo, "ghi")
```

# Future Development
* In its current state, this library depends on a fork of the `mongomock` library. This is due to several inconsistencies between `mongomock` and `PyMODM`. The resolution of these inconsistencies exceed the goals of the `mongomock` library. It would be in the best interest for the maturation of this library to move forward without such a heavy reliance upon a library that has a different set of goals.

# Known Issues
`__getitem__` is not able to retrieve the last element in the cursor. This is due to an inconsistency between the behaviors of  `mongomock` and `PyMODM`. As a work around for this issue, you can cast the queryset to a `list`.
