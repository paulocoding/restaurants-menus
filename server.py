from flask import Flask
app = Flask(__name__)



# restaurants routes
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return 'This will show all the restaurants'


@app.route('/restaurant/new')
def newRestaurant():
    return 'This will be for making a new restaurant'


@app.route('/restaurant/<int:restaurant_id>/edit')
def editRestaurant(restaurant_id):
    return 'This will be for editing restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
    return 'This will be for deleting restaurant %s' % restaurant_id


# menu item routes
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
    return 'This will show the menu for restaurant %s' % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    return 'This will be for making a new menu'


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    return 'This will be for editing menu %s' % menu_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return 'This will be for deleting menu %s' % menu_id

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
