from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/json')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/item/<int:menu_item_id>/json')
def restaurantMenuItemJSON(restaurant_id, menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    item = session.query(MenuItem).filter_by(id = menu_item_id).one()
    return jsonify(MenuItem = item.serialize)

@app.route('/')
@app.route('/restaurants')
def restaurantsIndex():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)

@app.route('/restaurants/<int:restaurant_id>/menu/new-item', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name = request.form['name'],
                           restaurant_id = restaurant_id,
                           price = request.form['price'],
                           description = request.form['description'])
        session.add(new_item)
        session.commit()
        flash("New Item Created")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant_id = restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu/edit-item/<int:menu_item_id>',
           methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_item_id):
    menu_item = session.query(MenuItem).filter_by(id = menu_item_id).one()

    print(request.form)
    if request.method == 'POST':
        print(request.form['name'])
        print(request.form['price'])
        print(request.form['desc'])
        if request.form['name'] != '':
            menu_item.name = request.form['name']

        if request.form['price'] != '':
            menu_item.price = request.form['price']

        if request.form['desc'] != '':
            menu_item.description = request.form['desc']

        session.add(menu_item)
        session.commit()
        flash("Item Successfully Edited")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('edit_menu_item.html',
                               restaurant_id = restaurant_id,
                               menu_item = menu_item)

@app.route('/restaurants/<int:restaurant_id>/menu/delete-item/<int:menu_item_id>',
           methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_item_id):
    menu_item = session.query(MenuItem).filter_by(id = menu_item_id).one()
    if request.method == 'POST':
        session.delete(menu_item)
        session.commit()
        flash("Item Deleted")
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('delete_menu_item.html',
                               restaurant_id = restaurant_id,
                               menu_item = menu_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
