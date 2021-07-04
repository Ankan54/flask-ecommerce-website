from market import app
from flask import render_template,redirect,url_for,flash,request
from market.models import Item,User
from market.forms import RegisterForm,LoginForm,ItemForm,PurchaseItemForm, AddMoneyForm, SellItemForm
from market import db
from flask_login import login_user,logout_user, login_required,current_user

@app.route('/')
def root_page():
    return redirect(url_for('home_page'))


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form=PurchaseItemForm()
    sell_form= SellItemForm()
    if request.method == "POST":
        purchased_item= request.form.get('purchased_item')
        item_object= Item.query.filter_by(name=purchased_item).first()
        if item_object:
            if not current_user.can_purchase(item_object):
                flash('Sorry! You don\'t have enough money to make the purchase', category='warning')
            else:
                item_object.buy(current_user)
                flash('Congrats! You have purchased {} for Rs. {}'.format(item_object.name,item_object.price),category='success')
        
        sold_item= request.form.get('sold_item')
        item_object = Item.query.filter_by(name=sold_item).first()
        if item_object:
            if current_user.can_sell(item_object):
                item_object.sell(current_user)
                flash('Congrats! You have sold {} for Rs. {}'.format(item_object.name,item_object.price),category='success')
            else:
                flash('Sorry! Something went wrong', category='danger')
        
        return redirect(url_for('market_page'))

    if request.method == "GET":
        items= Item.query.filter_by(owner=None)
        owned_items= Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items= items,purchase_form=purchase_form,sell_form=sell_form, owned_items=owned_items)


@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user= User(username=form.username.data,
                       email=form.email.data,
                       password= form.password.data)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Registered Successfully! You are logged in as {}'.format(new_user.username),category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: # no error from validation
        for err_msg in form.errors.values():
            flash('Error:{}'.format(err_msg), category='danger')
    return render_template('register.html', form=form) 


@app.route('/login', methods=['GET','POST'])
def login_page():
    form= LoginForm()
    if form.validate_on_submit():
        input_user= User.query.filter_by(username=form.username.data).first()
        if input_user and input_user.check_password(input_pwd=form.password.data):
            login_user(input_user)
            flash('Success! You are logged in as {}'.format(input_user.username), category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Error: Username and password do not match',category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out!', category='info')
    return redirect(url_for('login_page'))

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/stock', methods=['GET','POST'])
def add_item():
    form = ItemForm()
    if form.validate_on_submit():
        new_item= Item(name=form.name.data, price=form.price.data,
                    description=form.description.data,barcode=form.barcode.data)
        db.session.add(new_item)
        db.session.commit()
        flash('Item {} is added successfully'.format(new_item.name),category='success')
        return redirect(url_for('admin_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash('Error:{}'.format(err_msg), category='danger')
    return render_template('stock.html',form=form)

@app.route('/add_money',methods=['GET','POST'])
@login_required
def add_money():
    form= AddMoneyForm()
    if form.validate_on_submit():
        current_user.add_money(form.amount.data)
        flash('Successfully added money. Current Wallet balance is Rs. {}'.format(current_user.budget),category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash('Error:{}'.format(err_msg), category='danger')
    return render_template('add_money.html', form=form)
