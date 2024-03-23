import streamlit as st
import requests



# Set page title and favicon
st.set_page_config(page_title="Airbnb Amsterdam Weekdays", page_icon=":house_with_garden:")
# Define header style
st.markdown("<h3 style='text-align: center; color: #DEC6F8;'>Airbnb Amsterdam Weekdays Data</h3>", unsafe_allow_html=True)



# Make a request to the Flask API to get filter options
filter_options_response = requests.get('http://localhost:5000/filter_options')

if filter_options_response.status_code == 200:
    filter_options = filter_options_response.json()
    # Insert 'All' as a default column
    filter_options['All'] = ['All']
else:
    st.error('Failed to fetch filter options from API')

# Display a selectbox to choose filter options
# column_name = st.selectbox('Select Filter', filter_options)
column_name = st.selectbox('Select Filter', list(filter_options.keys()))

selected_option=None
radio_option=None
selected_cleanliness_rating_level=None

# Check if the selected column is 'All' and handle accordingly
if column_name == 'All':
    response = requests.get('http://localhost:5000/all_records')
    if response.status_code == 200:
        filtered_data = response.json()
        total_rows = len(filtered_data)

        # Apply CSS styles to center-align the container div
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <div style="overflow-y: auto; height: 250px; width: 800px;">
                    <table style="margin: 0 auto; text-align: center;">
                        <thead>
                            <tr>
                                {''.join(f'<th>{key}</th>' for key in filtered_data[0].keys())}
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(f"<tr>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>" for row in filtered_data)}
                        </tbody>
                    </table>
                </div>
            </div>
            <p style="text-align: center;">Total Rows: {total_rows}</p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error('Failed to fetch all records from API')
else:
    # Depending on the selected column, display appropriate filter options and filter data
    if column_name == 'biz':
        radio_option = st.radio('Select Option', ['Yes', 'No'])


    elif column_name == 'room_type':
        # Make a request to the Flask API to get unique values for the 'room_type' column
        room_type_options_response = requests.get('http://localhost:5000/room_type_options')

        if room_type_options_response.status_code == 200:
            room_type_options = room_type_options_response.json()
            selected_option = st.selectbox(f'Select {column_name} Filter', room_type_options)

        else:
            st.error('Failed to fetch room type options from API')

    elif column_name == 'bedrooms':
        # Make a request to the Flask API to get unique values for the 'bedrooms' column
        bedroom_options_response = requests.get('http://localhost:5000/bedroom_options')

        if bedroom_options_response.status_code == 200:
            bedroom_options = bedroom_options_response.json()
            selected_option = st.selectbox(f'Select {column_name} Filter', bedroom_options)
        else:
            st.error('Failed to fetch room type options from API')

    elif column_name == 'person_capacity':
        # Make a request to the Flask API to get unique values for the 'person_capacity' column
        person_capacity_options_response = requests.get('http://localhost:5000/person_capacity_options')

        if person_capacity_options_response.status_code == 200:
            person_capacity_options = person_capacity_options_response.json()
            selected_option = st.selectbox(f'Select {column_name} Filter', person_capacity_options)
        else:
            st.error('Failed to fetch room type options from API')

    elif column_name=='cleanliness_rating':

        # Make a request to the Flask API to get filter options
        cleanliness_rating_options_response = requests.get('http://localhost:5000/cleanliness_rating_options')

        if cleanliness_rating_options_response.status_code == 200:
            cleanliness_rating_options = cleanliness_rating_options_response.json()
            # Display a selectbox to choose cleanliness rating options
            selected_cleanliness_rating_level = st.selectbox('Select Cleanliness Rating Level', cleanliness_rating_options)
            
        else:
            st.error('Failed to fetch cleanliness rating options from API')

    



# Make a request to the Flask API to filter data based on user selections
if selected_option is not None or radio_option is not None or selected_cleanliness_rating_level is not None:
    response = requests.get('http://localhost:5000/filter_data', params={'column_name': column_name, 'selected_option': selected_option, 'radio_option': radio_option, 'selected_cleanliness_rating_level': selected_cleanliness_rating_level})

    if response.status_code == 200:
        filtered_data = response.json()
        total_rows = len(filtered_data)

        # Apply CSS styles to center-align the container div
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <div style="overflow-y: auto; height: 250px; width: 800px;">
                    <table style="margin: 0 auto; text-align: center;">
                        <thead>
                            <tr>
                                {''.join(f'<th>{key}</th>' for key in filtered_data[0].keys())}
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(f"<tr>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>" for row in filtered_data)}
                        </tbody>
                    </table>
                </div>
            </div>
            <p style="text-align: center;">Total Rows: {total_rows}</p>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error('Failed to fetch filtered data from API main')

if st.button("Add new Record"):
    st_add_button=True
else:
    st_add_button=False

if st_add_button:

    # Add Record Section
    st.header("Add Record")

    # Create input fields for each column
    add_record_data = {}
    for column_name, options in filter_options.items():
        if column_name == 'cleanliness_rating':
            add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
        elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'biz']:
            add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
        else:
            add_record_data[column_name] = st.text_input(f'Enter {column_name}')

    # Add input fields for additional columns
    add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
    add_record_data['realSum'] = st.text_input('Enter Price')

    # Add a button to submit the record
    if st.button('Submit'):
        response = requests.post('http://localhost:5000/add_record', json=add_record_data)
        if response.status_code == 201:
            st.success('Record added successfully')
        else:
            st.error('Failed to add record')

        # Update the existing table with the new record
        response = requests.get('http://localhost:5000/filter_data', params=add_record_data)
        if response.status_code == 200:
            filtered_data = response.json()
            st.table(filtered_data)
        else:
            st.error('Failed to fetch filtered data from API main')


########### ADD TEST CASES FROM STREAMLITAPP.PY
            
############################################ add new record button test 1 #################################################


    # Display the "Add new record" button outside the form
            
    #fixed it using sessions. Found auto-add of session named: "FormSubmitter:addrecord-Submit" whenever form button
    #was clicked. So made it such that whenever form button is true, then print "st.success" message. else, make it false
    # if "FormSubmitter:addrecord-Submit" not in st.session_state:
    #     st.session_state["FormSubmitter:addrecord-Submit"]= False

    # # def create_session_dictionary():
    # #     if "add_records_dictionary" not in st.session_state:
    # #         st.session_state["add_records_dictionary"]={}
    # #     return 

    # #session states
    # st.write("first state")
    # st.write(st.session_state)


    # if st.button("Add new record") :
    #     st.write(st.session_state)

    #     with st.form("addrecord"):
    #         add_record_data = {}
    #         def addrecordfunc():
                
    #             # Create input fields for each column
    #             for column_name, options in filter_options_to_add_record.items():
    #                 if column_name == 'cleanliness_rating':
    #                     add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
    #                 elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'business']:
    #                     add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
    #                 else:
    #                     add_record_data[column_name] = st.text_input(f'Enter {column_name}')

    #             # Add input fields for additional columns
    #             add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
    #             add_record_data['realSum'] = st.text_input('Enter Price')
            
    #             return
            
    #         addrecordfunc()

            #forums which helped: https://docs.streamlit.io/knowledge-base/using-streamlit/widget-updating-session-state 
            #sessionstate: https://docs.streamlit.io/library/api-reference/session-state
            #form button code :https://discuss.streamlit.io/t/do-not-reload-st-button-when-manipulation-st-selectbox/48743/2

    #         def func():
    #             submitted=st.form_submit_button("Submit")
    #             # if not st.session_state["FormSubmitter:addrecord-Submit"]: # if button has not been clicked
    #             if submitted:
    #                 st.write('clicked')
    #                 st.session_state["FormSubmitter:addrecord-Submit"] = True #our button has been clicked now
    #                 st.session_state["add_records_dictionary"] = add_record_data
                        
    #             else:
    #                 st.write('button not yet clicked')
            
    #         # # Every form must have a submit button.
    #         func()
    #         # st.session_state["add_records_dictionary"] = add_record_data
                 

    # if st.session_state["FormSubmitter:addrecord-Submit"]== True:
    #     if "add_records_dictionary" in st.session_state:
    #         response = requests.post('http://localhost:5000/add_record', json=st.session_state["add_records_dictionary"])
    #         if response.status_code == 201:
    #             st.success('Record added successfully')
    #             st.write(st.session_state)
    #             del st.session_state["add_records_dictionary"]  # Delete after processing

    #         else:
    #             st.error('Failed to add record')  
    #     else:
    #         st.error("add_records_dictionary is not set in st.session_state")  
    
####################################### add record test2 #############################################
    
    # if "FormSubmitter:addrecord-Submit" not in st.session_state:
    #     st.session_state["FormSubmitter:addrecord-Submit"] = False

    # #session states
    # st.write("first state")
    # st.write(st.session_state)

    # if st.button("Add new record"):

    #     with st.form("addrecord"):
    #         add_record_data = {}
            
    #         # add_record_data = {}
    #         # Create input fields for each column
    #         for column_name, options in filter_options_to_add_record.items():
    #             if column_name == 'cleanliness_rating':
    #                 add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
    #             elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'business']:
    #                 add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
    #             else:
    #                 add_record_data[column_name] = st.text_input(f'Enter {column_name}')

    #         # Add input fields for additional columns
    #         add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
    #         add_record_data['realSum'] = st.text_input('Enter Price')
            
            

    #         #function to add records in session state. Used in on_click of form submit button
    #         def add_session():
    #             st.session_state["add_records_dictionary"] = add_record_data

    #         #PROBLEM
    #         ###################### not even clicked on form submit, still on_click is called. maybe on_click is true
    #         #for outside "add new record" button. How to solve this?
    #         #it currently adds placeholder values in add_record_data
                
    #         #forum: https://discuss.streamlit.io/t/form-submit-buttons-on-click-being-called-before-clicking/27767/2
    #         #pass the function name to the on_click parameter instead of a function call (with arguments if present)
    #         st.form_submit_button("Submit",on_click=add_session)
            
    # #PROBLEM: add_records_dictionary automatically called without clicking on form submit button        
    # st.write("second")    
    # st.write(st.session_state)

    # if st.session_state["FormSubmitter:addrecord-Submit"]:
    #     if "add_records_dictionary" in st.session_state:
    #         response = requests.post('http://localhost:5000/add_record', json=st.session_state["add_records_dictionary"])
    #         if response.status_code == 201:
    #             st.success('Record added successfully')
    #             del st.session_state["add_records_dictionary"]  # Delete after processing
    #         else:
    #             st.error('Failed to add record')  
    #     else:
    #         st.error("add_records_dictionary is not set in st.session_state")

############################################# add record test 3 #WORKS #########################################
 
            
# if "button_clicked" not in st.session_state:
#         st.session_state.button_clicked=False

#     def func():
#         st.session_state.button_clicked=True

#     if (st.button("Add new record",on_click=func) or st.session_state.button_clicked) :

#         with st.form("addrecord"):
#             # Create input fields for each column
#             add_record_data = {}
#             for column_name, options in filter_options_to_add_record.items():
#                 if column_name == 'cleanliness_rating':
#                     add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
#                 elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'business']:
#                     add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
#                 else:
#                     add_record_data[column_name] = st.text_input(f'Enter {column_name}')

#             # Add input fields for additional columns
#             add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
#             add_record_data['realSum'] = st.text_input('Enter Price')



#             # Add a button to submit the record
#             if (st.form_submit_button('Submit')):
#                 response = requests.post('http://localhost:5000/add_record', json=add_record_data)
#                 if response.status_code == 201:
#                     st.success('Record added successfully')
#                 else:
#                     st.error('Failed to add record')
            

# <!-- ###################### add record in stremalit - ST.SESSION DICTIONARY NOT UPDATING #################### -->

# <!-- # Display the "Add new record" button outside the form
            
# #fixed it using sessions. Found auto-add of session named: "FormSubmitter:addrecord-Submit" whenever form button
# #was clicked. So made it such that whenever form button is true, then print "st.success" message. else, make it false
# if "FormSubmitter:addrecord-Submit" not in st.session_state:
#     st.session_state["FormSubmitter:addrecord-Submit"]= False

# #session states
# st.write("first state")
# st.write(st.session_state)

# if st.button("Add new record") :
#     st.write(st.session_state)

#     with st.form("addrecord"):
#         add_record_data = {}
        
#         # Create input fields for each column
#         for column_name, options in filter_options_to_add_record.items():
#             if column_name == 'cleanliness_rating':
#                 add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
#             elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'business']:
#                 add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
#             else:
#                 add_record_data[column_name] = st.text_input(f'Enter {column_name}')

#         # Add input fields for additional columns
#         add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
#         add_record_data['realSum'] = st.text_input('Enter Price')
        
        
#         def func():
#             submitted=st.form_submit_button("Submit")
#             if not st.session_state["FormSubmitter:addrecord-Submit"]: # if button has not been clicked
#                 if submitted:
#                     st.write('clicked')
#                     st.session_state["FormSubmitter:addrecord-Submit"] = True #our button has been clicked now
                    
#             else:
#                 st.write('button not yet clicked')
    
#         # # Every form must have a submit button.
#         func()
#         st.session_state["add_records_dictionary"] = add_record_data
             

# if st.session_state["FormSubmitter:addrecord-Submit"]== True:
#     if "add_records_dictionary" in st.session_state:
#         response = requests.post('http://localhost:5000/add_record', json=st.session_state["add_records_dictionary"])
#         if response.status_code == 201:
#             st.success('Record added successfully')
#             st.write(st.session_state)
#             del st.session_state["add_records_dictionary"]  # Delete after processing

#         else:
#             st.error('Failed to add record')  
#     else:
#         st.error("add_records_dictionary is not set in st.session_state")   -->
    


    