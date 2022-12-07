import sys
import dataclasses
from typing import List, Iterable, Tuple

@dataclasses.dataclass
class Point:
    x: int = 0
    y: int = 0

    def clone(self):
        return dataclasses.replace(self)

    def __add__(self, other: 'Point'):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Point'):
        return Point(self.x - other.x, self.y - other.y)

    def __lt__(self, other: 'Point'):
        return self.y < other.y or (self.y == other.y and self.x < other.x)

    def __le__(self, other: 'Point'):
        return self.y < other.y or (self.y == other.y and self.x <= other.x)

    def __str__(self):
        return f'({self.x},{self.y})'


class Field:
    def __init__(self, width, height, default_value=None):
        self._width = width
        self._height = height
        self._data = [
            [default_value] * width
            for _ in range(height)
        ]

    def __getitem__(self, key):
        x, y = key
        return self._data[y][x]

    def __setitem__(self, key, value):
        """:key x, y coordinates"""
        x, y = key
        self._data[y][x] = value

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def reset(self, value):
        for y in range(self.height):
            for x in range(self.width):
                self._data[y][x] = value

    def iterate_4_neighbourhood(self, x: int, y: int, radius: int) -> Iterable[Tuple[int, int]]:
        for dy in range(radius):
            for dx in range(1, radius - dy + 1):
                if y >= dy and x >= dx:
                    yield x - dx, y - dy
                if y+dy < self.height and x+dx < self.width:
                    yield x + dx, y + dy
                if y+dx < self.height and x >= dy:
                    yield x - dy, y + dx
                if y >= dx and x+dy < self.width:
                    yield x + dy, y - dx

@dataclasses.dataclass
class OptimalLocation:
    shop_count: int = 0
    position: Point = dataclasses.field(default_factory=Point)


class Simulator:
    def __init__(self, city_width: int, city_length: int, shops: List[Point], queries: List[int]):
        self._shops = Field(city_width, city_length, 0)
        for s in shops:
            self._shops[s.x, s.y] += 1
        self._queries = queries

    def run(self)-> List[OptimalLocation]:
        result = [
            self._find_optimal_location(radius)
            for radius in self._queries
        ]
        return result

    def _find_optimal_location(self, radius):
        location = OptimalLocation()
        for y in range(self._shops.height):
            for x in range(self._shops.width):
                if self._shops[x, y] > 0:
                    continue
                p = Point(x, y)
                local_count = self._get_shop_count(radius, x, y)
                if location.shop_count > local_count:
                    continue
                if local_count > location.shop_count or location.position > p:
                    location.shop_count = local_count
                    location.position = p
        return location

    def _get_shop_count(self, radius, x, y):
        shop_count = 0
        for neighbour in self._shops.iterate_4_neighbourhood(x, y, radius):
            shop_count += self._shops[neighbour]
        return shop_count


MIN_GRID_SIZE = 1
MAX_GRID_SIZE = 1000
GRID_SIZE_BOUNDS = f'[{MIN_GRID_SIZE} .. {MAX_GRID_SIZE}]'

MIN_SHOP_COUNT = 0
MAX_SHOP_COUNT = 5105
SHOP_COUNT_BOUNDS = f'[{MIN_SHOP_COUNT} .. {MAX_SHOP_COUNT}]'

MIN_QUERY_COUNT = 1
MAX_QUERY_COUNT = 20
QUERY_COUNT_BOUNDS = f'[{MIN_QUERY_COUNT} .. {MAX_QUERY_COUNT}]'

MIN_WALK_DISTANCE = 0
MAX_WALK_DISTANCE = 106
WALK_DISTANCE_BOUNDS = f'[{MIN_WALK_DISTANCE} .. {MAX_WALK_DISTANCE}]'

POSITION_OUTPUT_OFFSET = Point(1, 1)

EXIT_FAIL = 1


def main(argv):
    f = sys.stdin
    case_number = 1
    while True:
        l = f.readline()
        if l is None:
            print('Unexpected EOF, cases list should be followed by line',
                  'of 4 zeros separated with whitespace')
            return  EXIT_FAIL

        l = l.split()
        try:
            if len(l) < 4:
                raise ValueError()
            dx, dy, shop_count, query_count = map(int, l)
        except ValueError:
            print('First line of each case should contain 4 integers:',
                  'city grid dimensions, coffee chop and query counts')
            return EXIT_FAIL

        if dx == dy == shop_count == query_count == 0:
            break

        print(f'\nCase {case_number}:')

        if not(MIN_GRID_SIZE <= dx <= MAX_GRID_SIZE
               and MIN_GRID_SIZE <= dy <= MAX_GRID_SIZE):
            print(f'City grid dimensions {dx}x{dy} are not within allowed',
                  'range:', GRID_SIZE_BOUNDS)
            return EXIT_FAIL

        if not(MIN_SHOP_COUNT <= shop_count <= MAX_SHOP_COUNT):
            print(f'Shop count {shop_count} is not within allowed range:',
                  SHOP_COUNT_BOUNDS)
            return EXIT_FAIL

        if not(MIN_QUERY_COUNT <= query_count <= MAX_QUERY_COUNT):
            print(f'Query count {query_count} is not within allowed range:',
                  QUERY_COUNT_BOUNDS)
            return EXIT_FAIL

        shops: List[Point] = []
        for i in range(shop_count):
            l = f.readline()
            if l is None:
                print(f'Unexpected EOF, shop list should have {shop_count}',
                      'lines with shop coordinates')
                return  EXIT_FAIL
            try:
                shop_x, shop_y = map(int, l.split())
            except ValueError:
                print('Each line in shop list should contain 2 integers - shop',
                      'coordinates')
                return EXIT_FAIL
            if not(MIN_GRID_SIZE <= shop_x <= dx
                   and MIN_GRID_SIZE <= shop_y <= dy):
                print(f'Shop coordinates ({shop_x}, {shop_y}) are outside of',
                      'the city bounds or in the wrong order')
                return EXIT_FAIL
            shops.append(Point(shop_x - 1, shop_y - 1))

        queries: List[int] = []
        for i in range(query_count):
            l = f.readline()
            if l is None:
                print(f'Unexpected EOF, query list should have {query_count}',
                      'lines with maximum walk distances')
                return  EXIT_FAIL
            try:
                query = int(l)
            except ValueError:
                print('Each line in query list should contain integer -',
                      'maximum walk distance for the query')
                return EXIT_FAIL
            if not(MIN_WALK_DISTANCE <= query <= MAX_WALK_DISTANCE):
                print(f'Walk distance {query} is not within allowed range:',
                      WALK_DISTANCE_BOUNDS)
                return EXIT_FAIL
            queries.append(query)

        s = Simulator(dx, dy, shops, queries)
        best_locations = s.run()
        for l in best_locations:
            print(l.shop_count, l.position+POSITION_OUTPUT_OFFSET)
        case_number += 1

if __name__ == '__main__':
    sys.exit(main(sys.argv))
