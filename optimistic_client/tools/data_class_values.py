import operator
from typing import Generator, Any, Tuple, Callable
from optimistic_client.load.csv_to_dict_37 import DictRecordTransform


def values(data_class) -> Generator[Any, None, None]:
    return (getattr(data_class, f) for f in data_class.__annotations__)


def values_by_schema(keys: Tuple) -> Callable[[DictRecordTransform], Tuple]:
    get_value_tuple = operator.attrgetter(*keys)
    return get_value_tuple
