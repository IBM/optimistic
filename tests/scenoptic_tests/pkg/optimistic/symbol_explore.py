import tests.scenoptic_tests.pkg.constants
from tests.scenoptic_tests.pkg.optimistic.util.registry import add_registry

def query_symbol():
    print('Hello query_symbol')
    return 'Halllo'


print(tests.scenoptic_tests.pkg.constants.EXISTS_SYMBOL)
add_registry()

