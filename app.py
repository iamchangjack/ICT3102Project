import flask
import flask_profiler
from flask_mysqldb import MySQL
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["flask_profiler"] ={
    "enabled": True,
    "storage" : {
        "engine": "sqlite"
    },
    "basicAuth": {
        "enabled": True,
        "username": "admin",
        "password": "group10"
    },
    "ignore" : [
      "^/static/.*"
    ]
}

app.config['MYSQL_HOST'] = 'ict3102.cbck7papyauj.ap-southeast-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'ict3102'

mysql = MySQL(app)


# Create some test data for our catalog in the form of a list of dictionaries.
# info should not be acquired this way - just a template.
# should be acquired by POST
locations = [
    {'id': 0,
     'MAC Address': 'F5C4AD39367E',
     'Physical Location': '3-05',
     'timestamp': '1111111111'},
    {'id': 1,
     'MAC Address': 'EDE5BB44F64',
     'Physical Location': '1-02',
     'timestamp': '2312312312'}
]

flask_profiler.init_app(app)

# home page. not important
@app.route('/', methods=['GET'])
def home():
    return '''<h1>3102 Group 10 FLASK SERVER</h1>
<p>Get info from phone</p>
<p>Push info to simulated HACS server</p>

<p> for location report in JSON:</p>
<p> this website url + /api/locations</p>

<p> to provide location (from phone):</p>
<p> this website url + /api/provide_location?macaddress="MAC"&location="LOC"&timestamp="TIME"</p>'''

# api for POST (pushes DATA to the server. store in some form - find a way to hold data temporarily, so can push to GET?)
# demo: http://127.0.0.1:5000/api/provide_location?id=3&macaddress=5123213&location=place23&timestamp=55124123
@app.route('/api/provide_location', methods=['GET', 'POST'])
@flask_profiler.profile()
def api_provide_location():

    macaddress = request.args.get('macaddress')
    location = request.args.get('location')
    timestamp = request.args.get('timestamp')

    # Creating a connection cursor
    cursor = mysql.connection.cursor()

    # Format sql string

    sql = "INSERT INTO Location(mac_address, location_name, time_stamp) VALUES(%s, %s, %s)"
    val = (macaddress, location, timestamp)

    print(sql)
    print(val)

    # Executing SQL Statements

    try:
        cursor.execute(sql, val)
    except Exception as e:
        return '''<p>Issue encountered. %s. Please check URL string values.</p>'''

    # Saving the Actions performed on the DB
    mysql.connection.commit()

    # Closing the cursor
    cursor.close()

    return '''<h1>done</h1>'''



# api for GET (receives some kind of request, returns data)
# in our case, we are returning location data - every data we have
# to access: http://127.0.0.1:5000/api/locations
@app.route('/api/locations', methods=['GET'])
@flask_profiler.profile()
def api_return_locations():

    cursor = mysql.connection.cursor()

    sql = "SELECT * FROM Location"

    cursor.execute(sql)

    rows = cursor.fetchall()

    cursor.close()

    return jsonify(rows)

if __name__ == '__main__':
    app.run()
