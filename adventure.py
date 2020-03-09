from src import util

from flask import Flask, jsonify, request
from flask_migrate import Migrate
# from pusher import Pusher
# from decouple import config

from world import World
from items import Clothing, Weapon
# from models import db

from map import gen_map

from flask import Flask
from flask_cors import CORS, cross_origin

# Look up decouple for config variables
# pusher = Pusher(app_id=config('PUSHER_APP_ID'), key=config('PUSHER_KEY'), secret=config('PUSHER_SECRET'), cluster=config('PUSHER_CLUSTER'))

# world = World()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = util.get_db_connect_string()
# db.init_app(app)
# migrate = Migrate(app, db)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/map', methods=['GET'])
@cross_origin()
def map():
    return jsonify(gen_map(), 200)


def get_player_by_header(world, auth_header):
    if auth_header is None:
        return None

    auth_key = auth_header.split(" ")
    if auth_key[0] != "Token" or len(auth_key) != 2:
        return None

    player = world.get_player_by_auth(auth_key[1])
    return player


@app.route('/api/registration/', methods=['POST'])
def register():
    values = request.get_json()
    required = ['username', 'password1', 'password2']

    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400

    username = values.get('username')
    password1 = values.get('password1')
    password2 = values.get('password2')

    response = world.add_player(username, password1, password2)
    if 'error' in response:
        return jsonify(response), 500
    else:
        return jsonify(response), 201


@app.route('/', methods=['GET'])
def test():
    return jsonify('Welcome player!')


@app.route('/api/login/', methods=['POST'])
def login():
    values = request.get_json()
    required = ['username', 'password']

    if not all(k in values for k in required):
        response = {'message': 'Missing values'}
        return jsonify(response), 400

    username = values.get('username')
    password = values.get('password')

    response = world.authenticate_user(username, password)

    if 'error' in response:
        return jsonify(response), 500
    else:
        return jsonify(response), 200


@app.route('/api/adv/init/', methods=['GET'])
def init():
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    response = {
        'title': player.current_room.name,
        'description': player.current_room.description,
    }
    return jsonify(response), 200


@app.route('/api/adv/move/', methods=['POST'])
def move():
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    values = request.get_json()
    required = ['direction']

    if not all(k in values for k in required):
        response = {'message': "Missing Values"}
        return jsonify(response), 400

    direction = values.get('direction')
    if player.travel(direction):
        response = {
            'title': player.current_room.name,
            'description': player.current_room.description,
        }
        return jsonify(response), 200
    else:
        response = {
            'error': "You cannot move in that direction.",
        }
        return jsonify(response), 500


@app.route('/api/adv/take/', methods=['POST'])
def take_item():
    # create player variable
    # if no player, respond with error and 500
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    values = request.get_json()
    item = player.current_room.items

    # loop through player's inventory
    for item in player.inventory:
        if item.title == values['item_title']:
            # if player already has item, return jsonify message 'already have item'
            return jsonify(f"{player.username}, you currently have a {item.title} in your inventory."), 500

    for item in items:
        # if player doesn't have item
        if item.title == values['item_title']:
            # add item to player's inventory
            player.inventory.append(item)
            # remove item from current room's inventory
            player.current_room.items.remove(item)
            return jsonify(f"{player.username}, you picked up a {item.title}."), 200


@app.route('/api/adv/drop/', methods=['POST'])
def drop_item():
    # create player variable
    # if no player, respond with error and 500
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    values = request.json()
    inventory = player.inventory

    # loop through players inventory
    for item in inventory:
        if item.title == values['title']:
            # if player has item, remove item from players inventory
            player.inventory.remove(item)
            # add item to current rooms inventory
            player.current_room.items.append(item)
            # return jsonify message of dropped item
            return jsonify(
                f"{player.username}, you have dropped a {item.title} and it is no longer in your inventory."), 200


@app.route('/api/adv/inventory/', methods=['GET'])
def inventory():
    # create player variable
    # if no player, respond with error and 500
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    # create variable of empty list
    player_list = []
    # loop through players inventory
    for i in range(len(player.inventory)):
        # if there is an item, if clothing, or if weapon, append it and attrs to above list
        if (type(player.inventory[i]) is Item):
            player_list.append({'title': player.inventory[i].title, 'description': player.inventory[i].description,
                                'price': player.inventory[i].price})
        elif (type(player.inventory[i]) is Clothing):
            player_list.append({'title': player.inventory[i].title, 'description': player.inventory[i].description,
                                'price': player.inventory[i].price, 'clothing type': player.inventory[i].clothing_type,
                                'protection': player.inventory[i].protection})
        elif (type(player.inventory[i]) is Weapon):
            player_list.append({'title': player.inventory[i].title, 'description': player.inventory[i].description,
                                'price': player.inventory[i].price, 'weapon type': player.inventory[i].weapon_type,
                                'damage': player.inventory[i].damage})

    # return jsonify and 200
    return jsonify({'Current Iventory': player_list, 'Current Money': player.coin_pouch}), 200


@app.route('/api/adv/buy/', methods=['POST'])
def buy_item():
    # create player variable
    # if no player, respond with error and 500
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    values = request.get_json()
    # check to see if the player's current room is the store
    if player.current_room.store is not None:
        stock = player.current_room.store.in_stock
    else:
        return jsonify('This is not the store!'), 500
    # if player is in store check inventory
    for item in in_stock:
        if item.title == values['title']:
            # if player has enough money
            if item.price <= player.coin_pouch:
                # add item to players inventory
                player.inventory.append(item)
                # subtract item price from player's money attr
                player.coin_pouch -= item.price
                # remove item from store's stock
                player.current_room.store.in_stock.remove(item)
                return jsonify(
                    f"{player.username}, you have bought {item.title}. You now have {player.coin_pouch} coins left."), 200
            else:
                return jsonify(f"You do not have enough coins to buy a {item.title}.")


@app.route('/api/adv/sell/', methods=['POST'])
def sell_item():
    # create player variable
    # if no player, respond with error and 500
    player = get_player_by_header(world, request.headers.get("Authorization"))
    if player is None:
        response = {'error': "Malformed auth header"}
        return jsonify(response), 500

    values = request.get_json()

    # check to see if the player's current room is the store
    if player.current_room.store is not None:
        # if player is in store, check inventory
        inventory = player.inventory
        stock = player.current_room.store.in_stock
    else:
        return jsonify('This is not the store!'), 500

    # if player wants to sell item from inventory,
    for item in inventory:
        if item.title == values['title']:
            # remove item from players inventory
            player.inventory.remove(item)
            # add to store's inventory
            stock.append(item)
            # add price to player's price attr
            player.coin_pouch += item.price
            return jsonify(f"{player.username}, you have sold a {item.title}. You now have {player.coin_pouch} coins.")
        else:
            return jsonify("You can't sell that item here."), 500


@app.route('/api/adv/rooms/', methods=['GET'])
def rooms():
    # IMPLEMENT THIS
    response = {'error': "Not implemented"}
    return jsonify(response), 400


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
