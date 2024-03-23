#MAIN FLASK
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)




# Load your dataset
df = pd.read_csv('amsterdam_weekdays_cleanednew.csv')

######################################################### routes #################################################

# Define endpoint to fetch all records
@app.route('/all_records', methods=['GET'])
def get_all_records():
    all_records = df.to_dict(orient='records')
    return jsonify(all_records)

# Define endpoint to fetch filter options
@app.route('/filter_options', methods=['GET'])
def get_filter_options():
    # specific_columns = ['room_type', 'person_capacity', 'business', 'cleanliness_rating', 'bedrooms']
    specific_columns = {
        'business': [1, 0],
        'room_type': ['Apartment', 'Private', 'Shared'],
        'bedrooms': list(range(df['bedrooms'].min(), df['bedrooms'].max() + 1)),
        'person_capacity': list(range(df['person_capacity'].min(), df['person_capacity'].max() + 1)),
        'cleanliness_rating': list(range(11))  # 0 to 10
    }
    return jsonify(specific_columns)

# Define endpoint to filter data based on selected option
@app.route('/filter_data', methods=['GET'])
def filter_data():
    column_name = request.args.get('column_name')
    selected_option = request.args.get('selected_option')

    if column_name == 'business':
        radio_option = request.args.get('radio_option')
        option_mapping = {'Yes': 1, 'No': 0}
        filtered_df = df[df[column_name] == option_mapping[radio_option]]
    elif column_name in ['bedrooms','person_capacity']: 
        selected_option = int(selected_option)
        filtered_df = df[df[column_name] == int(selected_option)]    #bedroom size is int
    
    elif column_name == 'cleanliness_rating':
        if selected_option == 'Low':
            filtered_df = df[df[column_name].isin(range(0, 4))]
        elif selected_option == 'Medium':
            filtered_df = df[df[column_name].isin(range(4, 8))]
        elif selected_option == 'High':
            filtered_df = df[df[column_name].isin(range(8, 11))]



    else:
        selected_option=request.args.get('selected_option')
        filtered_df = df[df[column_name] == selected_option]       

    filtered_data = filtered_df.to_dict(orient='records')
    return jsonify(filtered_data)

# Define endpoint to add a new record
@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.json
    df.loc[len(df)] = data  # Append the new record to the DataFrame
    return jsonify({'message': 'Record added successfully'}), 201


# Define endpoint to get unique values for the 'room_type' column
@app.route('/room_type_options', methods=['GET'])
def get_room_type_options():
    room_type_options = list(df['room_type'].unique())
    return jsonify(room_type_options)

@app.route('/bedroom_options',methods=['GET'])
def get_bedroom_options():
    bedroom_options = list(range(df['bedrooms'].min(), df['bedrooms'].max() + 1))
    return jsonify(bedroom_options)

@app.route('/person_capacity_options', methods=['GET'])
def get_person_capacity_options():
    try:
        person_capacity_options = list(range(df['person_capacity'].min(), df['person_capacity'].max() + 1))
        return jsonify(person_capacity_options)
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/cleanliness_rating_options', methods=['GET'])
def get_cleanliness_rating_options():
    cleanliness_rating_options = ['Low','Medium','High']
    return jsonify(cleanliness_rating_options)


@app.route('/deleterecord',methods=['DELETE'])
def delete_row_by_srno():
    srno=request.args.get('srno')
    df.drop(int(srno)-1,inplace=True)
    return jsonify({"message":"Record deleted successfully"}),201


if __name__ == '__main__':
    app.run(debug=True)


# LESSON LEARNED
# SQL DATABASES are important because it helps us commit the changes made in the records
# SQL DATABASES are also necessary as we can use subqueries to filter out records based on conditions.
    
# DRAWBACKS OF THIS PROJECT UPTIL NOW
# no db used. So whenever we rerun flask, all changes are reverted.
# problem in deletion of row with sr.no. (but can be deleted through index id)
# but say after deleting certain IDs, it won't show continuous numbers as IDs.(like srno does)