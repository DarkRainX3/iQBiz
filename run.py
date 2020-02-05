from flask import Flask, render_template, url_for, flash, redirect, request
from flask_login import LoginManager, current_user, login_user, logout_user
import cx_Oracle
from forms import F_Blanket_Order

##########init###########
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret sauce'
login = LoginManager(app)
###############################


######### Connect Obj######
class ConnectionObject():
  
    def __init__(self, table = 'vw_web_inventory_ordered', username = "student12", password = "student12", db_name = "QHOU_TRNG_QBS_DEV"):
        self.table = table
        self.username = username
        self.password = password
        self.db_name = db_name
        self.raw_data = self.table_return()
    def update_api_table(self, api_code, value):
        x = f"begin sp_add_currency({value}, '{api_code}'); end;"
        try:
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.db_name) 
            c = conn.cursor()
            c.execute(x)
            conn.execute()
        except:
            c.execute(x)
        finally:
            c.close()
            x = f"begin sp_add_currency({value}, {api_code}); end;"
            self.run_sp_batch_log(x)
    def table_return(self):
        try:
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.db_name) 
            c = conn.cursor()
            return c.execute(f"SELECT * FROM {self.table}").fetchall()
        except:
            print('no return')
        finally:
            c.close()
    def run_sp_blanket_order(self, increment):
        x = f"begin sp_blanket_order({increment}); end;"
        try:
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.db_name) 
            c = conn.cursor()
            c.execute(x)
            conn.commit()
        except e:
            print(e)
        finally:
            c.close()
            self.run_sp_batch_log(x)
    def run_sp_batch_log(self, job, user_id = 'web'):
        x = f"begin sp_batch_log('{job}', '{user_id}'); end;"
        try:
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.db_name) 
            c = conn.cursor()
            c.execute(x)
            conn.commit()
        except e:
            print(e)
        finally:
            c.close()

    def run_sp_individual_order(self, store_id, title_id, increment):
        x = f"begin sp_individual_order('{store_id}', '{title_id}', {increment}); end;"
        try:
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=self.db_name) 
            c = conn.cursor()
            c.execute(x)
            conn.commit()
        except e:
            print(e)
        finally:
            c.close()
            x = f"begin sp_individual_order({store_id}, {title_id}, {increment}); end;"
            self.run_sp_batch_log(x)

#########################################

####################### models#############

@app.route('/')
@app.route('/inventory')
def inventory():
    table = "vw_web_inventory_ordered"
    raw_data = ConnectionObject(table = table).raw_data
    return render_template('inventory.html', raw_data = raw_data, rows=['Store ID', 'Title ID', 'Inventory', 'Threshold'], col_index = [0, 1, 2, -1])

@app.route('/mail_list')
def mail_list():
    table = "mail_list_vw"
    raw_data = ConnectionObject(table = table).raw_data
    return render_template('home.html', raw_data = raw_data, rows=['Account Name', 'Phone #', 'Status'], col_index = [1, 2, -1])

@app.route('/blanket_order', methods=['GET', 'POST'])
def blanket_order():
    form = F_Blanket_Order()
    if request.method == 'POST':
        try:
            x = int(form.increment.data)
            if x < 0 or x > 100:
                raise
            if form.validate_on_submit():
                ConnectionObject().run_sp_blanket_order(form.increment.data)
                flash(f'Order for {form.increment.data} units has been placed for all title!', 'success')
                return redirect(url_for('inventory'))          
        except:
            flash('Please enter a valid order amount', 'danger')

    return render_template('blanket_form.html', form=form)

@app.route('/order') #individual order
def order():
    raw_data = ConnectionObject().raw_data
    return render_template('home_mod.html', raw_data = raw_data, rows=['Store ID', 'Title ID', 'Inventory', 'Modify'], col_index = [0, 1, 2])

@app.route('/order/<store_id>/<title_id>/', methods=['GET', 'POST']) #individual order
def order_individual(store_id, title_id):
    form = F_Blanket_Order()
    if request.method == 'POST':
        try:
            x = int(form.increment.data)
         
            if x < 0 or x > 100:
                raise
            if form.validate_on_submit():
                ConnectionObject().run_sp_individual_order(store_id, title_id, form.increment.data)
                flash(f'Order for {form.increment.data} units has been placed for {title_id}!', 'success')
                return redirect(url_for('inventory'))          
        except:
            flash('Please enter a valid order amount', 'danger')

    return render_template('individual_form.html', form=form, store_id=store_id, title_id=title_id)


@app.errorhandler(404)
def page_nout_found(e):
    return render_template('404.html')

####################################################


if __name__ == '__main__':
    
    app.run(host = '10.15.10.93', debug=True)
    #app.run(debug=True)