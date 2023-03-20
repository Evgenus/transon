import pytest

from transon import (
    Transformer,
    TransformationError,
)

from . import base
from . import base_join


class JoinWithStaticNoOverrides(base_join.JoinWithStaticBase):
    data = {
        'a': 'b',
        'c': 'd',
    }
    result = {
        'a': 'b',
        'c': 'd',
    }


class JoinWithStaticWithOverrides(base_join.JoinWithStaticBase):
    data = {
        'c': 'd',
        'e': 'f',
    }
    result = {
        'a': 'default',
        'c': 'd',
        'e': 'f',
    }


class JoinTwoDictsNoCommonKeys(base_join.JoinTwoBase):
    data = {
        'first': {
            'a': 1,
            'b': 2,
        },
        'second': {
            'c': 3,
            'd': 4,
        },
    }
    result = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
    }


class JoinTwoDictsWithCommonKeys(base_join.JoinTwoBase):
    data = {
        'first': {
            'a': 1,
            'b': 2,
            'c': 5,
        },
        'second': {
            'c': 3,
            'd': 4,
        },
    }
    result = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
    }


class JoinTwoStrings(base_join.JoinTwoBase):
    data = {
        'first': 'hello ',
        'second': 'world!',
    }
    result = 'hello world!'


class JoinManyDynamicDicts(base.TableDataBaseCase):
    """
    TODO: Describe
    """
    tags = ['join', 'map:item', 'object']
    template = {
        '$': 'join',
        'items': {
            '$': 'join',
            'items': [
                {
                    '$': 'map',
                    'item': {
                        '$': 'object',
                        'key': {
                            '$': 'attr',
                            'name': 'key',
                        },
                        'value': {
                            '$': 'attr',
                            'name': 'value',
                        },
                    },
                },
                {
                    '$': 'map',
                    'item': {
                        '$': 'object',
                        'key': {
                            '$': 'attr',
                            'name': 'value',
                        },
                        'value': {
                            '$': 'attr',
                            'name': 'key',
                        },
                    },
                },
            ],
        },
    }
    data = [
        {'key': 'a', 'value': 'b'},
        {'key': 'c', 'value': 'd'},
    ]
    result = {
        'a': 'b',
        'b': 'a',
        'c': 'd',
        'd': 'c',
    }


def test_join_error():
    transformer = Transformer({
        '$': 'join',
        'items': [
            {'$': 'attr', 'name': 'dict'},
            {'$': 'attr', 'name': 'list'},
        ]
    })
    with pytest.raises(TransformationError):
        transformer.transform({
            'dict': {'a': 1},
            'list': ['b', 2],
        })
