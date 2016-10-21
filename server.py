from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)
app.secret_key = 'v3ri_s3cr31'

#   Sample data:
# Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]
# Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree', 'id':'1'}

# DB connection setup

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Crud operations
def getRestaurants():
    return session.query(Restaurant).all()

def getRestaurant(restaurant_id):
    return session.query(Restaurant).filter_by(id=restaurant_id).one()

def createRestaurantDb(name):
    restaurant = Restaurant(name=name)
    session.add(restaurant)
    session.commit()
    return

def editRestaurantDb(restaurant_id, newname):
    restaurant = getRestaurant(restaurant_id)
    restaurant.name = newname
    session.add(restaurant)
    session.commit()
    return

def deleteRestaurantDb(restaurant_id):
    restaurant = getRestaurant(restaurant_id)
    items = getItems(restaurant_id)

    # deleting all menu items belonging to this restaurant
    for item in items:
        deleteItemDb(item.id)

    session.delete(restaurant)
    session.commit()
    return

def getItems(restaurant_id):
    return session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

def getItem(item_id):
    return session.query(MenuItem).filter_by(id=item_id).one()

def createItemDb(name, restaurant_id, description='', price='', course=''):
    menuitem = MenuItem(name=name, description=description, price=price,
                        course=course, restaurant_id=restaurant_id)
    session.add(menuitem)
    session.commit()
    return
def editItemDb(item_id, name, description='', price='', course=''):
    menuitem = getItem(item_id)
    menuitem.name = name
    menuitem.description = description
    menuitem.price = price
    menuitem.course = course
    session.add(menuitem)
    session.commit()
    return

def deleteItemDb(item_id):
    menuitem = getItem(item_id)
    session.delete(menuitem)
    session.commit
    return

# restaurants routes
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    return render_template('restaurants.html', restaurants=getRestaurants())


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'GET':
        return render_template('createrestaurant.html')
    if request.method == 'POST':
        createRestaurantDb(request.form['name'])
        flash('Restaurant created!')
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    if request.method == 'GET':
        return render_template('editrestaurant.html', restaurant=getRestaurant(restaurant_id))
    if request.method == 'POST':
        editRestaurantDb(restaurant_id=restaurant_id, newname=request.form['name'])
        flash('Restaurant edited!')
        return redirect(url_for('showRestaurants'))


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'GET':
        return render_template('deleterestaurant.html', restaurant=getRestaurant(restaurant_id))
    if request.method == 'POST':
        deleteRestaurantDb(restaurant_id)
        flash('Restaurant deleted!')
        return redirect(url_for('showRestaurants'))


# menu item routes
@app.route('/restaurant/<int:restaurant_id>/menu')
@app.route('/restaurant/<int:restaurant_id>')
def showMenu(restaurant_id):
    return render_template('restaurantmenu.html', restaurant=getRestaurant(restaurant_id), items=getItems(restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'GET':
        return render_template('createmenuitem.html', restaurant=getRestaurant(restaurant_id))
    if request.method == 'POST':
        createItemDb(name=request.form['name'],
                     description=request.form['desc'],
                     price=request.form['price'],
                     course=request.form['course'],
                     restaurant_id=restaurant_id)
        flash('Menu item created!')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        return render_template('editmenuitem.html', restaurant=getRestaurant(restaurant_id), item=getItem(menu_id))
    if request.method == 'POST':
        editItemDb(item_id=menu_id,
                   name=request.form['name'],
                   description=request.form['desc'],
                   price=request.form['price'],
                   course=request.form['course'])
        flash('Menu item edited!')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'GET':
        return render_template('deletemenuitem.html', restaurant=getRestaurant(restaurant_id), item=getItem(menu_id))
    if request.method == 'POST':
        deleteItemDb(menu_id)
        flash('Menu item deleted!')
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))


# JSON endpoints
@app.route('/restaurants/JSON')
def showRestaurantsJSON():return jsonify({'Restaurants': [r.serialize for r in getRestaurants()]})

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showRestaurantMenuJSON(restaurant_id):
    return jsonify({'MenuItems':[item.serialize for item in getItems(restaurant_id)]})

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def showRestaurantMenuItemJSON(restaurant_id, menu_id):
    return jsonify({'MenuItem':getItem(menu_id).serialize})

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
