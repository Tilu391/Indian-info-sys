from flask import Flask,render_template,request,redirect,url_for,session, flash
from  flask_mysqldb import MySQL
import bcrypt

#import yaml
 
app = Flask(__name__)

app.secret_key = 'secret'

#db = yaml.load(open('db.yaml'))


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin@00'
app.config['MYSQL_DB'] = 'indian_info_system'

mysql = MySQL(app)

def get_db_connection():
    return mysql.connection

    
@app.route('/state/<int:state_id>', methods=['GET', 'POST'])
def state_page(state_id):

    statepics = [
        {'img':'1.png'},{'img':'2.png'},{'img':'3.png'},
        {'img':'4.png'},{'img':'5.png'},{'img':'6.png'},{'img':'7.png'},
        {'img':'8.png'},{'img':'9.png'},{'img':'10.png'},{'img':'11.png'},
        {'12.png'},{'img':'13.png'},{'img':'14.png'},{'img':'15.png'},
        {'img':'16.png'},{'17.png'},{'img':'18.png'},{'img':'19.png'},{'img':'20.png'},
        {'img':'21.png'},{'img':'22.png'},{'img':'23.png'},{'img':'24.png'},
        {'img':'25.png'},{'img':'26.png'},{'img':'27.png'},{'img':'28.png'},{'img':'u1.png'},{'img':'u2.png'},{'img':'u3.png'},
        {'img':'u4.png'},{'img':'u5.png'},{'img':'u6.png'},
        {'img':'u7.png'},{'img':'u8.png'},
    ]
    


    cur = mysql.connection.cursor()
    cur.callproc('GetInfraData', (state_id,))
    results = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('GetHdiData',(state_id,))
    results1 = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('GetTouristData',(state_id,))
    results2 = cur.fetchall()
    cur.close()

    cur = mysql.connection.cursor()
    cur.callproc('GetOfficialData',(state_id,))
    results3 = cur.fetchall()

    state = {
        'State_ID': results[0][0],
        'State_Name': results[0][1],
    }

    cur.close()

    if state:
        return render_template('statepage.html', state=state, infra_data=results,hdi_data=results1,tour_data=results2,office_data=results3,statepics=statepics)
    else:
        return render_template('new_home.html', state_id=state_id)
    

@app.route('/book',methods=['GET','POST'])
def book_page():
    cover = [
        {'img':'1.png'},{'img':'2.png'},{'img':'3.png'},
        {'img':'4.png'},{'img':'5.png'}]
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()

    if request.method == 'POST':
        BookID = request.form.get('BookID')
        username = get_current_user_id()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO Cart (username, BookID) VALUES (%s, %s)", (username, BookID))
        mysql.connection.commit()
        cur.close()
    

    return render_template('book.html',books=books,cover=cover)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    BookID = request.form.get('BookID')
    username = get_current_user_id()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO Cart (username, BookID) VALUES (%s, %s)", (username, BookID))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('view_cart'))

@app.route('/cart')
def view_cart():
    username = get_current_user_id()
    cur = mysql.connection.cursor()
    cur.execute("SELECT books.* FROM books JOIN Cart ON books.BookID = Cart.BookID WHERE Cart.username = %s", (username,))
    cart_contents = cur.fetchall()
    cur.close()

    return render_template('cart.html', cart_contents=cart_contents)

@app.route('/checkout')
def checkout():
    username = get_current_user_id()
    cur = mysql.connection.cursor()

    cur.execute("SELECT books.* FROM books JOIN Cart ON books.BookID = Cart.BookID WHERE Cart.username = %s", (username,))
    cart_contents = cur.fetchall()

    

    # pet_price = 100
    # product_price = sum(item['product_price'] for item in cart_contents1)
    # service_fee = sum(item['service_fees'] for item in cart_contents3)
    

    
        
    
    
    cur.execute("DELETE FROM Cart WHERE user_id = %s", (username,))

    mysql.connection.commit()
    cur.close()

    return render_template('checkout.html',  cart_contents=cart_contents)

@app.route('/payment', methods=['GET', 'POST'])
def payment_page():
    if request.method == 'POST':
        paid_by = request.form.get('paid_by')
        amount_paid = request.form.get('amount_paid')
        payment_status = 'Paid'
        cart_id = 10

        cur = mysql.connection.cursor()

        # Assuming that you have a 'user_id' column in the 'payment' table
        user_id = get_current_user_id()

        cur.execute("""
            INSERT INTO payment (paid_by, amount_paid, payment_status, username)
            VALUES (%s, %s, %s, %s)
        """, (paid_by, amount_paid, payment_status, user_id))  # Fix: Removed extra placeholder
        mysql.connection.commit()
        cur.close()

        # Update the order status to 'Paid' or adjust as per your business logic

        return render_template('payment.html')

    return render_template('payment.html')



def get_current_user_id():
    if 'username' in session:
        return session['username']
    else:
        # If the user is not logged in, you might want to handle this case accordingly
        # For simplicity, return None here, and handle it in your actual implementation
        return None


@app.route('/states',methods=['GET','POST'])
def states_page():
    states = [
        {'StateID': 9, 'name':'Andhra Pradesh','img':'1.png'},{'StateID': 10, 'name':'Arunachal Pradesh','img':'2.png'},{'StateID': 11, 'name':'Assam','img':'3.png'},
        {'StateID': 12, 'name':'Bihar','img':'4.png'},{'StateID': 13, 'name':'Chhattisgarh','img':'5.png'},{'StateID': 14, 'name':'Goa','img':'6.png'},{'StateID': 15, 'name':'Gujarat','img':'7.png'},
        {'StateID': 16, 'name':'Haryana','img':'8.png'},{'StateID': 17, 'name':'Himachal Pradesh','img':'9.png'},{'StateID': 18, 'name':'Jharkhand','img':'10.png'},{'StateID': 19, 'name':'Karnataka','img':'11.png'},
        {'StateID': 20, 'name':'Kerala','img':'12.png'},{'StateID': 21, 'name':'Madhya Pradesh','img':'13.png'},{'StateID': 22, 'name':'Maharashtra','img':'14.png'},{'StateID': 23, 'name':'Manipur','img':'15.png'},
        {'StateID': 24, 'name':'Meghalaya','img':'16.png'},{'StateID': 25, 'name':'Mizoram','img':'17.png'},{'StateID': 26, 'name':'Nagaland','img':'18.png'},{'StateID': 27, 'name':'Odisha','img':'19.png'},{'StateID': 28, 'name':'Punjab','img':'20.png'},
        {'StateID': 29, 'name':'Rajasthan','img':'21.png'},{'StateID': 30, 'name':'Sikkim','img':'22.png'},{'StateID': 34, 'name':'Tamil Nadu','img':'23.png'},{'StateID': 33, 'name':'Telangana','img':'24.png'},
        {'StateID': 31, 'name':'Tripura','img':'25.png'},{'StateID': 35, 'name':'Uttarakhand','img':'26.png'},{'StateID': 32, 'name':'Uttar Pradesh','img':'27.png'},{'StateID': 36, 'name':'West Bengal','img':'28.png'},
    ]
    uts = [
        {'StateID': 1, 'name':'Andaman and Nicobar Islands','img':'u1.png'},{'StateID': 2, 'name':'Chandigarh','img':'u2.png'},{'StateID': 3, 'name':'Daman & Diu','img':'u3.png'},
        {'StateID': 4, 'name':'Delhi','img':'u4.png'},{'StateID': 5, 'name':'Jammu & Kashmir','img':'u5.png'},{'StateID': 6, 'name':'Ladakh','img':'u6.png'},
        {'StateID': 7, 'name':'Lakshadweep','img':'u7.png'},{'StateID': 8, 'name':'Puducherry','img':'u8.png'},
    ]

    if request.method == 'POST':
        state_id = request.form.get('state_id')

        if state_id and state_id.isdigit():
            return redirect(url_for('state_page', state_id=int(state_id)))

    return render_template('state.html', states=states, uts=uts)

@app.route('/tops')
def tops_page():

    cur = mysql.connection.cursor()
    cur.execute("SELECT GetAverageHDI()")
    ans = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT TotalInfraCost(%s)",('Karnataka',))
    ans1 = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT StateName FROM State ORDER BY Population DESC LIMIT 1 ")
    ans2 = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT OfficialName FROM StateGovernmentOfficial WHERE OfficeID = %s AND OfficialID=%s ", ('9','1'))
    ans3 = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT About FROM TouristAttraction WHERE AttractionName = %s",('Coorg',))
    ans4 = cur.fetchone()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("SELECT AttractionName FROM TouristAttraction WHERE About LIKE %s", ('%Blue city%',))
    ans5 = cur.fetchone()
    cur.close()

    

    

    question = [
        {'qna':'What is the average HDI of India ?','answer':ans[0],'id':'box1'},
        {'qna':'What is the total amount spent by Karnataka on Infrastructure ?','answer':ans1[0],'id':'box2'},
        {'qna':'Which State has the Highest Population in the Country ?','answer':ans2[0],'id':'box3'},
        {'qna':'Who is the Chief Minister Of Andhra Pradesh ?','answer':ans3[0],'id':'box4'},
        {'qna':'What is Coorg known for ?','answer':ans4[0],'id':'box5'},
        {'qna':'Which is called as Blue City of India ?','answer':ans5[0],'id':'box6'},

    ]
    return render_template('tops.html',question=question)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password'].encode('utf-8')
            confirm_password = request.form['confirm_password'].encode('utf-8')

            if password != confirm_password:
                flash('Password and confirmation password do not match.', 'error')
                return redirect(url_for('register_page'))

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

            cur = get_db_connection().cursor()

            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return redirect(url_for('register_page'))

            cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
            get_db_connection().commit()

            cur.close()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login', success_message='Registration successful! You can now log in.'))

        except Exception as e:
            flash('An error occurred during registration. Please try again.', 'error')
            return redirect(url_for('register_page'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = get_db_connection().cursor()

        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]

            flash('Login successful!', 'success')
            return redirect(url_for('states_page'))

        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/alogin', methods=['GET', 'POST'])
def alogin_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = get_db_connection().cursor()
        cur.execute("SELECT * FROM admins WHERE username = %s", (username,))
        user = cur.fetchone()

        cur.close()

        if user and bcrypt.checkpw(password, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['username'] = user[1]

            flash('Login successful!', 'success')
            return redirect(url_for('index'))

        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('alogin.html')



@app.route('/')
@app.route('/home')
def new_home():
    return render_template('new_home.html')

@app.route('/table/<table_name>')
def get_table_data(table_name):
    cur = mysql.connection.cursor()
    cur.callproc('GetTableData', [table_name])
    data = cur.fetchall()

    cur.close()

    return render_template('table_content.html', data=data)


@app.route('/tables')
def index():
    return render_template('index.html')

@app.route('/changes_page')
def changes_page():
    return render_template('change.html')


#CRUD OPERATIONS

@app.route('/delete_official', methods=['GET', 'POST'])
def delete_official():
    if request.method == 'POST':
        try:
            official_id = request.form['official_id']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM StateGovernmentOfficial WHERE OfficialID = %s", (official_id,))
            before_delete = cur.fetchone()

            sql = "DELETE FROM StateGovernmentOfficial WHERE OfficialID = %s"
            values = (official_id,)
            cur.execute(sql, values)
            mysql.connection.commit()
            
            cur.close()
            
            return render_template('index.html', before_delete=before_delete)

        except Exception as e:
            return "Error"

    return render_template('index.html')


@app.route('/update_state', methods=['GET', 'POST'])
def update_state():
    if request.method == 'POST':
        try:
            state_id = request.form['state_id']
            new_population = request.form['population']
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM State WHERE StateID = %s", (state_id,))
            before_update = cur.fetchone()

            sql = "UPDATE State SET Population = %s WHERE StateID = %s"
            values = (new_population, state_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', before_update=before_update)

        except Exception as e:
            return "Error"

    return render_template('index.html')


@app.route('/insert_infrastructure', methods=['GET', 'POST'])
def insert_infrastructure():
    if request.method == 'POST':
        try:
            infrastructure_id = request.form['infrastructure_id']
            infrastructure_name = request.form['infrastructure_name']
            state_id = request.form['state_id']
            cost = request.form['cost']

            cur = mysql.connection.cursor()

            sql = "INSERT INTO Infrastructure (InfrastructureID, InfrastructureName, StateID, CostInMillionINR) VALUES (%s, %s, %s, %s)"
            values = (infrastructure_id, infrastructure_name, state_id, cost)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()
            return render_template('index.html', success=True)

        except Exception as e:
            return render_template('index.html', success=False, error=str(e))

    return render_template('index.html', success=None)


@app.route('/update_hdi', methods=['GET', 'POST'])
def update_hdi():
    if request.method == 'POST':
        try:
            hdi_id = request.form['hdi_id']
            new_gdp = request.form['gdp']

            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM HDI WHERE HDIID = %s", (hdi_id,))
            before_update = cur.fetchone()

            sql = "UPDATE HDI SET GDPInMillionINR = %s WHERE HDIID = %s"
            values = (new_gdp, hdi_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', before_update=before_update)

        except Exception as e:
            return "Error"

    return render_template('index.html')


@app.route('/insert_tourist', methods=['GET', 'POST'])
def insert_tourist():
    if request.method == 'POST':
        try:
            attraction_id = request.form['attraction_id']
            attraction_name = request.form['attraction_name']
            about = request.form['about']
            entrance_fee = request.form['fee']
            state_id = request.form['state_id']

            cur = mysql.connection.cursor()

            sql = "INSERT INTO TouristAttraction (AttractionID, AttractionName, About, EntranceFeeInINR, StateID) VALUES (%s, %s, %s, %s, %s)"
            values = (attraction_id, attraction_name, about, entrance_fee, state_id)
            cur.execute(sql, values)
            mysql.connection.commit()

            cur.close()

            return render_template('index.html', success=True)

        except Exception as e:
            return "Error"

    return render_template('index.html', success=None)


