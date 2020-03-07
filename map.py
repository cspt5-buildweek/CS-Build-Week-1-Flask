from uuid import uuid4
from random import choice, shuffle

import sys

import logging
logging.basicConfig(level=logging.DEBUG)


# values of dimensions should always be non-negative
# values of origin are expected to be within 0 and their respective dimension, inclusive.
def gen_map(rooms=10, dimensions=(10, 10), origin=(0, 0)):
    remaining = [rooms]
    map = {
        'rooms': {},
        'rooms_list': [],
        'halls_list': [],
        'dimensions': dimensions
    }

    generate_room(origin, map, remaining)
    map['start'] = map['rooms'][origin]

    timeout = 0
    while rooms > 0 and timeout < 1000:
        branch_node = choice(map['rooms_list'])
        possible_new_nodes = get_possible_new_neighbors(branch_node['location'], map)

        if not len(possible_new_nodes):  # no valid new positions adjacent to this room. skip, increment timeout
            timeout += 1
            continue

        shuffle(possible_new_nodes)
        generate_room(possible_new_nodes[0], map, branch_node['location'])

        rooms -= 1
        timeout = 0

    map['rooms'] = { str(room['id']): room for _, room in map['rooms'].items()}
    return map


# parent is the LOCATION of the parent node as a tuple (x, y)
def generate_room(location, map, parent=None):
    room = { 'id': uuid4(), 'name': f'room {location}', 'desc': '', 'location': location, 'halls': {} }

    map['rooms'][room['location']] = room
    map['rooms_list'].append(room)

    if parent is not None:
        link_rooms(parent, location, map)


def link_rooms(room_1, room_2, map):
    # room_1_dir, room_2_dir = get_dir(room_1, room_2)

    # map['rooms'][room_1]['halls'][room_1_dir]: map['rooms'][room_2]['id']
    pass


# accepts two "location" tuples, and returns a tuple where each entry describes the direction its neighbor is located in, relative to it
def get_dir(loc_1, loc_2):
    print(f'LOCATIONS: {loc_1}, {loc_2}', file=sys.stdout)
    sys.stdout.flush()

    if loc_1[0] == loc_2[0] and loc_1[1] == loc_2[1] - 1:
        return ('s', 'n')

    elif loc_1[0] == loc_2[1] and loc_1[1] == loc_2[1] + 1:
        return ('n', 's')

    elif loc_1[1] == loc_2[1] and loc_1[0] == loc_2[0] - 1:
        return ('e', 'w')

    elif loc_1[1] == loc_2[1] and loc_1[0] == loc_2[0] + 1:
        return ('w', 'e')


# I've chosen to follow svg coordinate conventions
# (x , y). Smaller values of x are west, larger east. Smaller values of y are north, larger south
def get_possible_new_neighbors(location, map):
    valid_locations = []

    if not map['rooms'].get((location[0], location[1] - 1)) and location[1] - 1 >= 0:  # North is unoccupied and in bounds
        valid_locations.append((location[0], location[1] - 1))

    if not map['rooms'].get((location[0], location[1] + 1)) and location[1] + 1 <= map['dimensions'][1]:  # South is unoccupied and in bounds
        valid_locations.append((location[0], location[1] + 1))

    if not map['rooms'].get((location[0] - 1, location[1])) and location[0] - 1 >= 0:  # West is unoccupied and in bounds
        valid_locations.append((location[0] - 1, location[1]))

    if not map['rooms'].get((location[0] + 1, location[1])) and location[0] + 1 <= map['dimensions'][0]:  # East is unoccupied and in bounds
        valid_locations.append((location[0] + 1, location[1]))

    return valid_locations
