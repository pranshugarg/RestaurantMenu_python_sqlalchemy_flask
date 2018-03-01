from flask import Flask, render_template , request, redirect , url_for , flash ,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databasesetup import Restaurant, Base, MenuItem

app = Flask(__name__)

## create session and connect to the database #####
engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
    Menu_Item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(Menu_Item=Menu_Item.serialize)


@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    #rendering template
    return render_template('restaurants.html',restaurants = restaurants)

@app.route('/restaurant/new', methods=['GET','POST'])
def newRestaurant():
  if request.method == 'POST':  
      newItem = Restaurant(name = request.form['name'])
      session.add(newItem)
      session.commit()
      flash("new restaurant created")
      return redirect(url_for('showRestaurants'))
  else:#######imp---these arguments are available in html file######
      return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit' , methods=['GET','POST'])
def editRestaurant(restaurant_id):
  editedItem = session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedItem.name = request.form['name']
      session.add(editedItem)
      session.commit()
      flash("requested restaurant edited")
      return redirect(url_for('showRestaurants'))
  else:
    return render_template('editRestaurant.html',restaurant_id=restaurant_id,i=editedItem)

@app.route('/restaurant/<int:restaurant_id>/delete' , methods=['GET','POST'])
def deleteRestaurant(restaurant_id):
  itemtodelete = session.query(Restaurant).filter_by(id = restaurant_id).one()
  if request.method == 'POST':
        session.delete(itemtodelete)
        session.commit()
        flash("requested restaurant deleted")
        return redirect(url_for('showRestaurants'))
  else:
      return render_template('deleteRestaurant.html',restaurant_id=restaurant_id,i=itemtodelete)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    #rendering template
    return render_template('menu.html',restaurant=restaurant, items = items, restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/new/' , methods=['GET','POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':  
    newItem = MenuItem(name = request.form['name'] ,restaurant_id= restaurant_id)
    session.add(newItem)
    session.commit()
    flash("new menu-item created")
    return redirect(url_for('restaurantMenu' , restaurant_id = restaurant_id))
  else:#######imp---these arguments are available in html file######
    return render_template('newmenuitem.html', restaurant_id=restaurant_id )

@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit' , methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
  editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedItem.name = request.form['name']
        editedItem.description = request.form['description']
        editedItem.price = request.form['price']
        editedItem.course = request.form['course']
      session.add(editedItem)
      session.commit()
      flash("requested menu-item edited")
      return redirect(url_for('restaurantMenu' , restaurant_id=restaurant_id))
  else:
    return render_template('editmenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,i=editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/' , methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
  itemtodelete = session.query(MenuItem).filter_by(id = menu_id).one()
  if request.method == 'POST':
      session.delete(itemtodelete)
      session.commit()
      flash("requested menu-item deleted")
      return redirect(url_for('restaurantMenu' , restaurant_id=restaurant_id))
  else:
    return render_template('deletemenuitem.html',restaurant_id=restaurant_id,menu_id=menu_id,i=itemtodelete)

if __name__ == '__main__':
   app.debug = True
#   app.secret_key = 'super_secret_key'
   app.run(host = '0.0.0.0' , port = 5000)  