from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL, NumberRange
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
coffe_score = '☕️'
wifi_score =  '💪'
zero_score = '✘'
power_score = '🔌'

def generate_choices(type_of_score):
    choices = []
    for i in range(6):
        if i == 0:
            choices.append((i, zero_score))
        else:
            render_choice = ''
            for j in range(i):
                render_choice += type_of_score
            choices.append((i, render_choice))
    return choices

class CafeForm(FlaskForm):
    coffee_name = StringField('Coffee Name', validators=[DataRequired()])
    coffee_location_url = StringField('Location URL', validators=[DataRequired(), URL()])
    coffee_open_time = StringField('Open Time', validators=[DataRequired()])
    coffee_close_time = StringField('Close Time', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating',choices=generate_choices(coffe_score), validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating',choices = generate_choices(wifi_score), validators=[DataRequired()])
    power_outlet_rating = SelectField('Power Outlet Rating', choices=generate_choices(power_score),validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods = [ 'GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    if request.method == 'POST':
        if form.validate_on_submit():
            cafe_name = form.coffee_name.data
            location_url = form.coffee_location_url.data
            open_time = form.coffee_open_time.data
            close_time = form.coffee_close_time.data
            coffee_rating = int(form.coffee_rating.data)
            wifi_rating = int(form.wifi_rating.data)
            power_outlet_rating = int(form.power_outlet_rating.data)
            print(f'{cafe_name},{location_url},{open_time},{close_time},{coffee_rating},{wifi_rating},{power_outlet_rating}')
            with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                csv_writer.writerow([cafe_name, location_url, open_time, close_time, coffee_rating, wifi_rating, power_outlet_rating])
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
