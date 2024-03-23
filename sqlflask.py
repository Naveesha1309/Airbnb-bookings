from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)

# Configure SQLAlchemy with the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///airbnbamsterdam.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define SQLAlchemy Model
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realSum = db.Column(db.Float)
    room_type = db.Column(db.String(50))
    person_capacity = db.Column(db.Integer)
    biz = db.Column(db.Integer)
    cleanliness_rating = db.Column(db.Float)
    guest_satisfaction_overall = db.Column(db.Float)
    bedrooms = db.Column(db.Integer)

    def __repr__(self):
        return f'<Booking {self.id}>'

# Load data from CSV file and insert into database
def load_data_from_csv():
    df = pd.read_csv('amsterdam_weekdays_cleaned.csv')
    for index, row in df.iterrows():
        booking = Booking(realSum=row['realSum'],
                          room_type=row['room_type'],
                          person_capacity=row['person_capacity'],
                          biz=row['biz'],
                          cleanliness_rating=row['cleanliness_rating'],
                          guest_satisfaction_overall=row['guest_satisfaction_overall'],
                          bedrooms=row['bedrooms'])
        db.session.add(booking)
    db.session.commit()
    
# Create the database tables and load data from CSV only once
with app.app_context():
    db.create_all()
    if not Booking.query.first():  # Check if database is empty before loading
        load_data_from_csv()

# Routes

# Fetch all records
@app.route('/all_records', methods=['GET'])
def get_all_records():
    all_records = Booking.query.all()
    all_records_dict = [{'id': record.id, 'realSum': record.realSum, 'room_type': record.room_type,
                         'person_capacity': record.person_capacity, 'biz': record.biz,
                         'cleanliness_rating': record.cleanliness_rating,
                         'guest_satisfaction_overall': record.guest_satisfaction_overall,
                         'bedrooms': record.bedrooms} for record in all_records]
    return jsonify(all_records_dict)

# Fetch filter options
@app.route('/filter_options', methods=['GET'])
def get_filter_options():
    specific_columns = {
        'biz': [1, 0],
        'room_type': ['Apartment', 'Private', 'Shared'],
        'bedrooms': list(range(Booking.query.with_entities(Booking.bedrooms).distinct().count())),
        'person_capacity': list(range(Booking.query.with_entities(Booking.person_capacity).distinct().count())),
        'cleanliness_rating': list(range(11))
    }
    return jsonify(specific_columns)

# Filter data based on selected option
@app.route('/filter_data', methods=['GET'])
def filter_data():
    column_name = request.args.get('column_name')
    selected_option = request.args.get('selected_option')

    if column_name == 'biz':
        radio_option = request.args.get('radio_option')
        option_mapping = {'Yes': 1, 'No': 0}
        filtered_records = Booking.query.filter_by(biz=option_mapping[radio_option]).all()
    elif column_name in ['bedrooms', 'person_capacity']:
        selected_option = int(selected_option)
        filtered_records = Booking.query.filter_by(**{column_name: selected_option}).all()
    elif column_name == 'cleanliness_rating':
        if selected_option == 'Low':
            filtered_records = Booking.query.filter(Booking.cleanliness_rating < 4).all()
        elif selected_option == 'Medium':
            filtered_records = Booking.query.filter(Booking.cleanliness_rating >= 4, Booking.cleanliness_rating < 8).all()
        elif selected_option == 'High':
            filtered_records = Booking.query.filter(Booking.cleanliness_rating >= 8).all()
    else:
        selected_option = request.args.get('selected_option')
        filtered_records = Booking.query.filter_by(**{column_name: selected_option}).all()

    filtered_data = [{'id': record.id, 'realSum': record.realSum, 'room_type': record.room_type,
                      'person_capacity': record.person_capacity, 'biz': record.biz,
                      'cleanliness_rating': record.cleanliness_rating,
                      'guest_satisfaction_overall': record.guest_satisfaction_overall,
                      'bedrooms': record.bedrooms} for record in filtered_records]
    return jsonify(filtered_data)

# Add a new record
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    new_record = Booking(**data)
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'message': 'Record added successfully'}), 201

# Get unique values for the 'room_type' column
@app.route('/room_type_options', methods=['GET'])
def get_room_type_options():
    room_type_options = Booking.query.with_entities(Booking.room_type).distinct().all()
    room_type_options = [opt[0] for opt in room_type_options]
    return jsonify(room_type_options)

# Get unique values for the 'bedrooms' column
@app.route('/bedroom_options', methods=['GET'])
def get_bedroom_options():
    bedroom_options = list(range(1, Booking.query.with_entities(Booking.bedrooms).distinct().count() + 1))
    return jsonify(bedroom_options)

# Get unique values for the 'person_capacity' column
@app.route('/person_capacity_options', methods=['GET'])
def get_person_capacity_options():
    person_capacity_options = list(range(1, Booking.query.with_entities(Booking.person_capacity).distinct().count() + 1))
    return jsonify(person_capacity_options)

# Get unique values for the 'cleanliness_rating' column
@app.route('/cleanliness_rating_options', methods=['GET'])
def get_cleanliness_rating_options():
    cleanliness_rating_options = ['Low', 'Medium', 'High']
    return jsonify(cleanliness_rating_options)

# Delete a record by ID
@app.route('/delete_record/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    record = Booking.query.get(record_id)
    if record:
        db.session.delete(record)
        db.session.commit()
        return jsonify({"message": f"Record with ID {record_id} deleted successfully"}), 200
    else:
        return jsonify({"error": f"Record with ID {record_id} not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
