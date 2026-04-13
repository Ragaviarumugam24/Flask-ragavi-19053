from flask import Flask, render_template, redirect, url_for, request, flash, session
import uuid

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Dummy products with more details
products = [
    {"id": 1, "name": "Basmati Rice (1kg)", "price": 60, "image": "rice.jpg", "category": "Grains"},
    {"id": 2, "name": "Wheat Flour (1kg)", "price": 50, "image": "flour.jpg", "category": "Grains"},
    {"id": 3, "name": "Sugar (1kg)", "price": 45, "image": "sugar.jpg", "category": "Essentials"},
    {"id": 4, "name": "Milk Packet (500ml)", "price": 30, "image": "milk.jpg", "category": "Dairy"},
    {"id": 5, "name": "Cooking Oil (1L)", "price": 120, "image": "oil.jpg", "category": "Essentials"},
    {"id": 6, "name": "Eggs (6 pcs)", "price": 35, "image": "eggs.jpg", "category": "Dairy"}
]

@app.route('/')
def home():
    return render_template('index.html', products=products)

@app.route('/add/<int:id>')
def add_to_cart(id):
    if 'cart' not in session:
        session['cart'] = []
    
    product = next((p for p in products if p['id'] == id), None)
    if product:
        session['cart'].append(product)
        session.modified = True
    flash(f'{product["name"]} added to cart!', 'success')
    return redirect(url_for('home'))

@app.route('/remove/<int:id>')
def remove_from_cart(id):
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['id'] != id]
        session.modified = True
    flash('Item removed from cart!', 'info')
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('cart.html', cart=cart_items, total=total)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        # Clear cart after successful checkout
        session.pop('cart', None)
        flash(f'Thank you {name}! Your order has been placed successfully.', 'success')
        return render_template('order_success.html', name=name)
    
    cart_items = session.get('cart', [])
    total = sum(item['price'] for item in cart_items)
    return render_template('checkout.html', cart=cart_items, total=total)

@app.route('/clear-cart')
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared!', 'info')
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(debug=True)