from flask import Flask, render_template, request, redirect, url_for,jsonify,flash,session
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import pickle
import joblib
import numpy as np
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a strong secret key

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user_login'

mysql = MySQL(app)

# Load the trained model for fertilizer recommend
model = joblib.load('fertilizer_app.pkl')

# Load the dataset to fit LabelEncoders
data = pd.read_csv("./data/fertilizer_recommendation.csv")

# Initialize LabelEncoders and fit them with the dataset
le_soil = LabelEncoder()
le_crop = LabelEncoder()
le_fertilizer = LabelEncoder()  # For decoding the prediction
data['Soil Type'] = le_soil.fit_transform(data['Soil Type'])
data['Crop Type'] = le_crop.fit_transform(data['Crop Type'])
data['Fertilizer Name'] = le_fertilizer.fit_transform(data['Fertilizer Name'])


#loading models for yeild prediction
dtr = pickle.load(open('dtr.pkl','rb'))
preprocessor = pickle.load(open('preprocesser.pkl','rb'))




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE username = %s AND password = %s', (username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')
            return redirect(url_for('login',form='login'))

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['first-name']
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user_details WHERE username = %s', (username,))
        account = cursor.fetchone()

        # Validation logic
        if account:
            flash('Account already exists!', 'error')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters long!', 'error')
        elif not username or not password or not email:
            flash('Please fill out the form!', 'error')
        else:
            cursor.execute('INSERT INTO user_details (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            flash('Signup successful! Now login.', 'success')
            return redirect(url_for('login',form='login'))
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/crop-recommend', methods=['GET', 'POST'])
def crop_recommend():
    if request.method == 'POST':
        # Extract form data
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph_value = float(request.form['phValue'])
        rainfall = float(request.form['rainfall'])
        
        # Create a feature array in the same order as the training data
        values = [nitrogen, phosphorus, potassium, temperature, humidity, ph_value, rainfall]
        
        # Ensure values are within expected ranges
        if ph_value > 0 and ph_value <= 14 and temperature < 100 and humidity > 0:
            try:
                model = joblib.load('crop_app.pkl')  # Corrected model loading
                arr = [values]
                acc = model.predict(arr)
                return render_template('crop-recommend.html', prediction=str(acc[0]))
            except Exception as e:
                return f"An error occurred: {e}"
        else:
            return "Invalid input values provided. Please check your inputs."
    
    return render_template('crop-recommend.html')

@app.route('/yield-predict', methods=['GET', 'POST'])
def yield_predict():
    if request.method == 'POST':
        Year = request.form['Year']
        average_rain_fall_mm_per_year = request.form['average_rain_fall_mm_per_year']
        pesticides_tonnes = request.form['pesticides_tonnes']
        avg_temp = request.form['avg_temp']
        Area = request.form['Area']
        Item  = request.form['Item']

        features = np.array([[Year,average_rain_fall_mm_per_year,pesticides_tonnes,avg_temp,Area,Item]],dtype=object)
        transformed_features = preprocessor.transform(features)
        prediction = dtr.predict(transformed_features).reshape(1,-1)

        return render_template('yield-predict.html',prediction = prediction[0][0])
    
    return render_template('yield-predict.html')

@app.route('/weather-forecast')
def weather_forecast():
    return render_template('weather-forecast.html')

@app.route('/fertilizer-recommend', methods=['GET', 'POST'])
def fertilizer_recommend():
    if request.method == 'POST':
        # Extract form data
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        soil_moisture = float(request.form['soilMoisture'])
        soil_type = request.form['soilType']
        crop_type = request.form['cropType']
        nitrogen = float(request.form['nitrogen'])
        potassium = float(request.form['potassium'])
        phosphorous = float(request.form['phosphorous'])
        
        # Encode categorical features
        soil_type_encoded = le_soil.transform([soil_type])[0]
        crop_type_encoded = le_crop.transform([crop_type])[0]
        
        # Create a feature array
        features = [temperature, humidity, soil_moisture, soil_type_encoded, crop_type_encoded, nitrogen, potassium, phosphorous]
        
        # Make a prediction
        prediction_encoded = model.predict([features])[0]
        
        # Decode the prediction back to the original fertilizer name
        prediction = le_fertilizer.inverse_transform([prediction_encoded])[0]
        
        # Render the result in the template
        return render_template('fertilizer-recommend.html', recommendation=prediction)
    
    return render_template('fertilizer-recommend.html')

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'loggedin' in session:
        user_id = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT username, password, email, phone, location FROM user_details WHERE id=%s", (user_id,))
        account = cursor.fetchone()
        
        if request.method == 'POST':
            # Update profile details in the database
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            phone = request.form['phone']
            location = request.form['location']
            
            cursor.execute("""
                UPDATE user_details 
                SET username=%s, password=%s, email=%s, phone=%s, location=%s 
                WHERE id=%s
            """, (username, password, email, phone, location, user_id))
            mysql.connection.commit()
            flash('Profile saved successfully', 'success')
            return redirect(url_for('profile'))
        
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Here we would normally clear the session or any user-specific data
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
