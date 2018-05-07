import io
import copy
import inspect
import json
import mongomock
import mock
from bson import ObjectId
from pymodm import MongoModel
from pymodm.base.options import MongoOptions
from pymodm.queryset import QuerySet
from typing import Union

__all__ = ("mock_queryset",)


def mock_queryset(model: MongoModel=None, mock_data: list=None, filepath: str=None):
    """A wrapper for 'mock_queryset' that patches a Model's Manager"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            queryset = _mocker(model, mock_data, filepath)

            def mocker(*args):
                return queryset

            mock.patch.object(model.objects, "_queryset_class", mocker)
            func(*args, **kwargs)
        return wrapper
    return decorator


def _mocker(model: MongoModel, mock_data: list=None, filepath: str=None):
    """Mocks out a pyMODM QuerySet to return the data that is passed in"""
    if mock_data and filepath:
        raise ValueError("Can only provide one source of data")

    if filepath:
        with io.open(filepath) as file_:
            mock_data = json.load(file_)
    mock_data = handle_cls(model, mock_data)

    # build collection
    mock_collection = mongomock.MongoClient().db.collection
    mock_collection.insert_many(mock_data)

    # for mocking create functions
    model._mongometa = mock_options(model, mock_collection)

    class MockQuerySet(QuerySet):
        @property
        def _collection(self):
            return mock_collection

    return MockQuerySet(model)


def mock_options(model: MongoModel, mock_collection):
    class MockOptions(MongoOptions):
        @property
        def collection(self):
            return mock_collection

    meta = model._mongometa
    mock_meta = MockOptions()
    for name, attribute in inspect.getmembers(meta):
        if not inspect.ismethod(attribute) and not name.startswith("__"):
            try:
                setattr(mock_meta, name, getattr(meta, name))
            except AttributeError:
                pass
    return mock_meta


def handle_cls(model: MongoModel, mock_data: Union[list, dict]) -> Union[list, dict]:
    """Adds the '_cls' to the dictionaries if they do not have them"""
    def update(data: dict) -> None:
        if data.get("_cls") is None:
            data["_cls"] = model._mongometa.object_name
        if data.get("_id") is None:
            data["_id"] = ObjectId()

    data = copy.deepcopy(mock_data)
    if isinstance(mock_data, list):
        for row in data:
            update(row)
    else:
        update(data)
    return data
