'''from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the model and datasets
model = joblib.load('model.joblib')
dataset = pd.read_csv('Multi_diesease-(2000).csv')
doctor_data = pd.read_csv('doctors.csv')  # Load doctor data

# Valid credentials for login
valid_credentials = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5"
}

# Disease information dictionary
disease_info = {
    "Thalasse": {
        "description": (
            "Thalassemia is a condition where your body doesn’t make enough healthy red blood cells because of a problem in your genes. "
            "Red blood cells carry oxygen throughout your body, and when there aren't enough, you might feel very tired or weak. "
            "This condition can also make your body destroy red blood cells faster than it should, leading to anemia."
        ),
        "causes": "Thalassemia is inherited, meaning it’s passed down from parents to their children through genes.",
        "symptoms": (
            "People with thalassemia might feel very tired, look pale, or have trouble growing as quickly as other children. "
            "Sometimes, it can also change the shape of bones in the face and make the spleen or liver larger than usual."
        ),
        "advice": (
            "Treatment may include regular blood transfusions to replace unhealthy red blood cells and special medicine to remove extra iron from the body. "
            "It's important to see a blood specialist, called a hematologist, for proper care."
        ),
    },
    "Thromboc": {
        "description": (
            "Thrombocytopenia is when your blood doesn’t have enough platelets. "
            "Platelets are tiny cells that help your blood clot, so if you don’t have enough, you might bruise easily or bleed for a long time even from small cuts."
        ),
        "causes": (
            "This condition can happen because of certain illnesses that affect the immune system, infections like dengue or chickenpox, medicines, or problems with how the bone marrow makes blood cells."
        ),
        "symptoms": (
            "You may notice frequent bruises, gums or nose bleeding without reason, red spots on the skin, blood in your urine, or feeling very tired."
        ),
        "advice": (
            "Try to avoid injuries that might cause bleeding, and if the symptoms are serious, see a doctor right away. "
            "Treatment will depend on what’s causing the problem."
        ),
    },
    "Diabetes": {
        "description": (
            "Diabetes is a condition that happens when your body has trouble controlling sugar levels in your blood. "
            "Sugar gives your body energy, but too much of it can harm your organs over time. "
            "This is usually because your body doesn’t make enough of a hormone called insulin or because it doesn’t use insulin properly."
        ),
        "causes": (
            "Diabetes can be caused by factors like having family members with the condition, eating too much unhealthy food, being overweight, or not exercising enough."
        ),
        "symptoms": (
            "You might feel thirsty all the time, need to urinate a lot, lose weight unexpectedly, feel very tired, or notice that cuts and wounds take longer to heal."
        ),
        "advice": (
            "It’s important to check your blood sugar levels regularly, eat healthy foods, stay active, and see a diabetes specialist, called an endocrinologist, for advice on managing your condition."
        ),
    },
    "Healthy": {
        "description": (
            "Based on the information provided, there are no signs of any major health problems. "
            "This means your body is working well, and your lifestyle is likely supporting good health."
        ),
        "causes": (
            "A healthy body is often the result of eating nutritious foods, staying active, managing stress, and avoiding harmful habits like smoking or drinking too much alcohol."
        ),
        "symptoms": "There are no worrying symptoms at the moment. You might feel energetic and generally well.",
        "advice": (
            "Keep up the good work! Make sure to continue eating a balanced diet, exercising regularly, and getting enough sleep. "
            "Regular health check-ups are also important to catch any potential issues early."
        ),
    },
    "Anemia": {
        "description": (
            "Anemia happens when your body doesn’t have enough healthy red blood cells to carry oxygen to your tissues. "
            "This can make you feel tired or weak, and in some cases, it might even make your skin look pale."
        ),
        "causes": (
            "Anemia can happen if you don’t eat enough foods with iron or vitamins, lose blood (like from heavy periods), "
            "or have a health problem that affects how your body makes red blood cells."
        ),
        "symptoms": (
            "Feeling very tired, getting dizzy easily, having cold hands and feet, and looking pale are common signs of anemia. "
            "You might also notice shortness of breath when you’re active."
        ),
        "advice": (
            "Eating foods rich in iron, like spinach, beans, or red meat, can help. If the problem is severe, you may need iron supplements or other treatments. "
            "Visit a doctor to find out what’s causing the anemia and get the right care."
        ),
    },
}

# Root route that serves the homepage
@app.route('/')
def home():
    return render_template('home.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in valid_credentials and valid_credentials[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Enter valid Username and Password.")
    return render_template('login.html')

# Home route (symptom input)
@app.route('/h', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('predict.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        symptoms = [
            float(request.form['Glucose']),
            float(request.form['Cholesterol']),
            float(request.form['Hemoglobin']),
            float(request.form['Platelets']),
            float(request.form['White Blood Cells']),
            float(request.form['BMI']),
            float(request.form['Systolic Blood Pressure']),
            float(request.form['Triglycerides']),
            float(request.form['LDL Cholesterol']),
            float(request.form['Creatinine']),
            float(request.form['C-reactive Protein']),
        ]
        location = request.form['location']  # Get location input
        disease = model.predict([symptoms])[0]
        return redirect(url_for('result', disease=disease, location=location))

# Result route with doctor suggestions
@app.route('/result/<disease>/<location>')
def result(disease, location):
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Get disease info
    info = disease_info.get(disease, {
        "description": "Unknown disease.",
        "causes": "No information available.",
        "symptoms": "No symptoms recorded.",
        "advice": "Consult a healthcare professional."
    })
    # Filter doctor data
    doctors = doctor_data[(doctor_data['Disease'] == disease) & 
                          (doctor_data['Location'].str.contains(location, case=False))]
    
    return render_template(
        'result.html',
        disease=disease,
        description=info["description"],
        causes=info["causes"],
        symptoms=info["symptoms"],
        advice=info["advice"],
        doctors=doctors.to_dict(orient='records')  # Pass doctors as a list of dictionaries
    )
# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
'''
from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import pandas as pd

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the model and datasets
model = joblib.load('model.joblib')
dataset = pd.read_csv('Multi_diesease-(2000).csv')
doctor_data = pd.read_csv('doctors.csv')  # Load doctor data

# Valid credentials for login
valid_credentials = {
    "a":"a",
    "user1": "password1",
    "user2": "password2",
    "user3": "password3",
    "user4": "password4",
    "user5": "password5"
}

# Disease information dictionary
disease_info = {
    "Thalasse": {
        "description": (
            "Thalassemia is a condition where your body doesn’t make enough healthy red blood cells because of a problem in your genes. "
            "Red blood cells carry oxygen throughout your body, and when there aren't enough, you might feel very tired or weak. "
            "This condition can also make your body destroy red blood cells faster than it should, leading to anemia."
        ),
        "causes": "Thalassemia is inherited, meaning it’s passed down from parents to their children through genes.",
        "symptoms": (
            "People with thalassemia might feel very tired, look pale, or have trouble growing as quickly as other children. "
            "Sometimes, it can also change the shape of bones in the face and make the spleen or liver larger than usual."
        ),
        "advice": (
            "Treatment may include regular blood transfusions to replace unhealthy red blood cells and special medicine to remove extra iron from the body. "
            "It's important to see a blood specialist, called a hematologist, for proper care."
        ),
    },
    "Thromboc": {
        "description": (
            "Thrombocytopenia is when your blood doesn’t have enough platelets. "
            "Platelets are tiny cells that help your blood clot, so if you don’t have enough, you might bruise easily or bleed for a long time even from small cuts."
        ),
        "causes": (
            "This condition can happen because of certain illnesses that affect the immune system, infections like dengue or chickenpox, medicines, or problems with how the bone marrow makes blood cells."
        ),
        "symptoms": (
            "You may notice frequent bruises, gums or nose bleeding without reason, red spots on the skin, blood in your urine, or feeling very tired."
        ),
        "advice": (
            "Try to avoid injuries that might cause bleeding, and if the symptoms are serious, see a doctor right away. "
            "Treatment will depend on what’s causing the problem."
        ),
    },
    "Diabetes": {
        "description": (
            "Diabetes is a condition that happens when your body has trouble controlling sugar levels in your blood. "
            "Sugar gives your body energy, but too much of it can harm your organs over time. "
            "This is usually because your body doesn’t make enough of a hormone called insulin or because it doesn’t use insulin properly."
        ),
        "causes": (
            "Diabetes can be caused by factors like having family members with the condition, eating too much unhealthy food, being overweight, or not exercising enough."
        ),
        "symptoms": (
            "You might feel thirsty all the time, need to urinate a lot, lose weight unexpectedly, feel very tired, or notice that cuts and wounds take longer to heal."
        ),
        "advice": (
            "It’s important to check your blood sugar levels regularly, eat healthy foods, stay active, and see a diabetes specialist, called an endocrinologist, for advice on managing your condition."
        ),
    },
    "Healthy": {
        "description": (
            "Based on the information provided, there are no signs of any major health problems. "
            "This means your body is working well, and your lifestyle is likely supporting good health."
        ),
        "causes": (
            "A healthy body is often the result of eating nutritious foods, staying active, managing stress, and avoiding harmful habits like smoking or drinking too much alcohol."
        ),
        "symptoms": "There are no worrying symptoms at the moment. You might feel energetic and generally well.",
        "advice": (
            "Keep up the good work! Make sure to continue eating a balanced diet, exercising regularly, and getting enough sleep. "
            "Regular health check-ups are also important to catch any potential issues early."
        ),
    },
    "Anemia": {
        "description": (
            "Anemia happens when your body doesn’t have enough healthy red blood cells to carry oxygen to your tissues. "
            "This can make you feel tired or weak, and in some cases, it might even make your skin look pale."
        ),
        "causes": (
            "Anemia can happen if you don’t eat enough foods with iron or vitamins, lose blood (like from heavy periods), "
            "or have a health problem that affects how your body makes red blood cells."
        ),
        "symptoms": (
            "Feeling very tired, getting dizzy easily, having cold hands and feet, and looking pale are common signs of anemia. "
            "You might also notice shortness of breath when you’re active."
        ),
        "advice": (
            "Eating foods rich in iron, like spinach, beans, or red meat, can help. If the problem is severe, you may need iron supplements or other treatments. "
            "Visit a doctor to find out what’s causing the anemia and get the right care."
        ),
    },
}

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in valid_credentials and valid_credentials[username] == password:
            session['username'] = username
            return redirect(url_for('symptom_input'))
        return render_template('login.html', error="Invalid Username or Password.")
    return render_template('login.html')

# Symptom input route
@app.route('/symptom-input', methods=['GET', 'POST'])
def symptom_input():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            # Validate all inputs are provided
            required_fields = [
                'Glucose', 'Cholesterol', 'Hemoglobin', 'Platelets',
                'White Blood Cells', 'BMI', 'Systolic Blood Pressure',
                'Triglycerides', 'LDL Cholesterol', 'Creatinine', 'C-reactive Protein'
            ]
            symptoms = [float(request.form[field]) for field in required_fields]
            location = request.form.get('location', '').strip()
            
            if not location:
                return render_template('predict.html', error="Location is required.")

            # Predict disease
            disease = model.predict([symptoms])[0]
            return redirect(url_for('result', disease=disease, location=location))
        except ValueError:
            return render_template('predict.html', error="Invalid input. Please check your data.")
    return render_template('predict.html')

# Result route with doctor suggestions
@app.route('/result/<disease>/<location>')
def result(disease, location):
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get disease info
    info = disease_info.get(disease, {
        "description": "Unknown disease.",
        "causes": "No information available.",
        "symptoms": "No symptoms recorded.",
        "advice": "Consult a healthcare professional."
    })

    # Filter doctor data
    filtered_doctors = doctor_data[
        (doctor_data['Disease'].str.contains(disease, case=False, na=False)) &
        (doctor_data['Location'].str.contains(location, case=False, na=False))
    ]
    doctors = filtered_doctors.to_dict(orient='records') if not filtered_doctors.empty else []

    return render_template(
        'result.html',
        disease=disease,
        description=info["description"],
        causes=info["causes"],
        symptoms=info["symptoms"],
        advice=info["advice"],
        doctors=doctors,
        location=location
    )

# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
