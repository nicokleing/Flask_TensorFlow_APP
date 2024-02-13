from flask import Flask, render_template, session, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import numpy as np  
from tensorflow.keras.models import load_model
import joblib
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField



def return_prediction(model, scaler, sample_json):
    # Extracting features from the sample
    features = [sample_json['Pregnancies'], sample_json['Glucose'],
                sample_json['BloodPressure'], sample_json['SkinThickness'],
                sample_json['Insulin'], sample_json['BMI'],
                sample_json['DiabetesPedigreeFunction'], sample_json['Age']]

    # Reshaping and scaling the input data
    patient = np.array([features])
    patient = scaler.transform(patient)

    # Predicting with the model
    prediction = model.predict(patient)

    # Assuming a binary classification with a single output neuron
    class_ind = (prediction > 0.5).astype(int)  # Applying threshold
    classes = np.array(['Normal', 'Diabetes'])

    return classes[class_ind[0][0]]  # Adjust indexing based on your model's output shape




app = Flask(__name__)

app.config['SECRET_KEY'] = 'key1234'

# Cargando el modelo
model = load_model("final_data_model.h5")
scaler = joblib.load("data_scaler.pkl")


# Creamos la clase de WTForm
class DiabetesForm(FlaskForm):

    Pregnancies = StringField('Pregnancies')
    Glucose = StringField('Glucose')
    BloodPressure = StringField('BloodPressure')
    SkinThickness = StringField('SkinThickness')
    Insulin = StringField('Insulin')
    BMI = StringField('BMI')
    DiabetesPedigreeFunction = StringField('DiabetesPedigreeFunction')
    Age = StringField('Age')

    submit = SubmitField('Analyze')



@app.route('/', methods=['GET', 'POST'])
def index():

    # Create instance of the form.
    form = DiabetesForm()
    # If the form is valid on submission (we'll talk about validation next)
    if form.validate_on_submit():
        # Grab the data from the breed on the form.

        session['Pregnancies'] = form.Pregnancies.data
        session['Glucose'] = form.Glucose.data
        session['BloodPressure'] = form.BloodPressure.data
        session['SkinThickness'] = form.SkinThickness.data
        session['Insulin'] = form.Insulin.data
        session['BMI'] = form.BMI.data
        session['DiabetesPedigreeFunction'] = form.DiabetesPedigreeFunction.data
        session['Age'] = form.Age.data

        return redirect(url_for("prediction"))


    return render_template('home.html', form=form)


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    try:
        content = {
            'Pregnancies': float(session.get('Pregnancies', 0)),
            'Glucose': float(session.get('Glucose', 0)),
            'BloodPressure': float(session.get('BloodPressure', 0)),
            'SkinThickness': float(session.get('SkinThickness', 0)),
            'Insulin': float(session.get('Insulin', 0)),
            'BMI': float(session.get('BMI', 0)),
            'DiabetesPedigreeFunction': float(session.get('DiabetesPedigreeFunction', 0)),
            'Age': float(session.get('Age', 0))
        }
        results = return_prediction(model=model, scaler=scaler, sample_json=content)
    except ValueError as e:
        # Manejar el caso en que la conversión falle
        results = "Error en la entrada de datos: asegúrese de que todos los campos estén llenos correctamente."

    return render_template('prediction.html', results=results)

@app.route('/api/diabetes', methods=['POST'])
def api_diabetes():
    if request.method == 'POST':
        content = request.json
        results = return_prediction(model=model, scaler=scaler, sample_json=content)
        return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)