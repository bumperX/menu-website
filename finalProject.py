from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
import os

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBsession = sessionmaker(bind=engine)
session = DBsession()


# Update css file automatically
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# API creation
@app.route('/restaurants/JSON')
def restaurantsJSON():
	items = session.query(Restaurant).all()
	return jsonify(restaurantItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem=menuItem.serialize)


@app.route('/')
@app.route('/restaurant')
def showRestaurants():
	# return 'This page will show all my restaurants'
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	# return 'This page will be for making a new restaurants'
	if request.method == 'POST':
		newRestaurant = Restaurant(name=request.form['name'])
		session.add(newRestaurant)
		session.commit()
		flash('New Restaurant Created')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	# return 'This page will be for editting restaurant %s' % restaurant_id
	editRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editRestaurant.name = request.form['name']
			session.add(editRestaurant)
			session.commit()
			flash('Restaurant Successfully Edited')
			return redirect(url_for('showRestaurants'))
	else:
		return render_template('editRestaurant.html', restaurant_id=restaurant_id, 
			i=editRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	# return 'This page will be for deleting restaurant %s' % restaurant_id
	deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		session.delete(deleteRestaurant)
		session.commit()
		flash('Restaurant Successfully Deleted')
		return redirect(url_for('showRestaurants'))
	else:
		return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, 
			i=deleteRestaurant)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
	# return 'This page is the menu for restaurant %s' % restaurant_id
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one() 
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
	return render_template('menu.html', restaurant=restaurant, menu=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	# return 'This page is for making a new menu item for restaurant %s' % restaurant_id
	if request.method == 'POST':
		newItem = MenuItem(name=request.form['name'],
			description=request.form['description'],
			price=request.form['price'],
			course=request.form['course'],
			restaurant_id=restaurant_id)
		session.add(newItem)
		session.commit()
		flash('New Menu Item Created')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	# return 'This page is for editting menu item %s' % menu_id
	editItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editItem.name = request.form['name']
			session.add(editItem)
			session.commit()
			flash('Menu Item Successfully Edited')
			return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template("editMenuItem.html", restaurant_id=restaurant_id, 
		menu_id = menu_id, i = editItem)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	# return 'This page is for deleting menu item %s' % menu_id
	deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash('Menu Item Successfully Deleted')
		return redirect(url_for('showMenu', restaurant_id=restaurant_id))
	else:
		return render_template('deleteMenuItem.html', restaurant_id=restaurant_id,
			menu_id=menu_id, i=deleteItem)


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)