#MAIN STREAMLIT 
import time
import streamlit as st
import requests
import pandas as pd

# Set page title and favicon
st.set_page_config(page_title="Airbnb Amsterdam Weekdays", page_icon=":house_with_garden:")

############################################background image #####################################################
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1505256465238-0c54e270b1b3?q=80&w=870&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
    
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)


######################################## Define custom CSS styles for the tabs###############################
custom_css = """
<style>
/* Remove the box background in Streamlit tabs */
.st-c0.st-ca.st-cb.st-cc.st-cd.st-ce.st-cf.st-cg.st-ae.st-ch.st-ag.st-ah.st-ai.st-aj.st-ci.st-cj.st-ck.st-cl.st-cm.st-cn {
    background-color: transparent !important;
    box-shadow: none !important;
}
</style>
"""

# Display the custom CSS styles
st.markdown(custom_css, unsafe_allow_html=True)


##################################### Session dictionary update test ####################################

# # st.session_state['trial']={"records":{}}
# # the callback function for the button will add 1 to the
# st.write(st.session_state)
# # slider value up to 10
# def plus_one():
#     if st.session_state["slider"] < 10:
#         st.session_state.slider += 1
#     else:
#         pass
#     return

# # when creating the button, assign the name of your callback
# # function to the on_click parameter
# add_one = st.button("Add one to the slider", on_click=plus_one, key="add_one")

# # create the slider
# slide_val = st.slider("Pick a number", 0, 10, key="slider")

####################################### each tab content ##################################

tab1, tab2= st.tabs(["Filter", "Visualize"])


with tab1:


    # Define header style
    st.markdown("<h3 style='text-align: center; color: #FFEDDE;'>AIRBNB: Amsterdam Bookings Analysis</h3>", unsafe_allow_html=True)



    # Make a request to the Flask API to get filter options
    filter_options_response = requests.get('http://localhost:5000/filter_options')

    if filter_options_response.status_code == 200:
        filter_options = filter_options_response.json()
        #creating a copy of filter options so it doesn't hamper the options while adding a new record
        filter_options_to_add_record = filter_options.copy() 
        # Insert 'All' as a default column at the beginning of the dictionary
        filter_options = {'All': ['All'], **filter_options}
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
            plot_data=response.json()
            plot_data=pd.DataFrame(plot_data)
            filtered_data = response.json()
            total_rows = len(filtered_data)

            # Apply CSS styles to center-align the container div
            st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="overflow-y: auto; height: 250px; width: 800px; background-color: white; color: black; border: 1px solid black; border-radius: 5px; padding: 10px;">
                            <table style="margin: 0 auto; text-align: center;">
                                <thead>
                                    <tr>
                                        <th>Sr.No.</th> {''.join(f'<th>{key}</th>' for key in filtered_data[0].keys())}
                                    </tr>
                                </thead>
                                <tbody>
                                    {''.join(f"<tr><td>{index+1}</td>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>" for index, row in enumerate(filtered_data))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <p style="text-align: center; color: #FFEDDE;">Total Rows: {total_rows}</p>
                    """,
                    unsafe_allow_html=True
                )

        else:
            st.error('Failed to fetch all records from API')
    else:
        # Depending on the selected column, display appropriate filter options and filter data
        if column_name == 'business':
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
        # response = requests.get('http://localhost:5000/filter_data', params={'column_name': column_name, 'selected_option': selected_option, 'radio_option': radio_option, 'selected_cleanliness_rating_level': selected_cleanliness_rating_level})
        if column_name == 'business':
            response = requests.get('http://localhost:5000/filter_data', params={'column_name': column_name, 'radio_option': radio_option})

        elif column_name=='cleanliness_rating':
            response = requests.get('http://localhost:5000/filter_data', params={'column_name': 'cleanliness_rating', 'selected_option': selected_cleanliness_rating_level})
        else:
            response = requests.get('http://localhost:5000/filter_data', params={'column_name': column_name, 'selected_option': selected_option})

        if response.status_code == 200:
            filtered_data = response.json()
            total_rows = len(filtered_data)

            if filtered_data:  #check if there exists data with given filters, else show 'no record'
                # Apply CSS styles to center-align the container div
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: center;">
                        <div style="overflow-y: auto; height: 250px; width: 800px; background-color: white; color: black; border: 1px solid black; border-radius: 5px; padding: 10px;">
                            <table style="margin: 0 auto; text-align: center;">
                                <thead>
                                    <tr>
                                        <th>Sr.No.</th> {''.join(f'<th>{key}</th>' for key in filtered_data[0].keys())}
                                    </tr>
                                </thead>
                                <tbody>
                                    {''.join(f"<tr><td>{index+1}</td>{''.join(f'<td>{value}</td>' for value in row.values())}</tr>" for index, row in enumerate(filtered_data))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <p style="text-align: center; color: #FFEDDE;">Total Rows: {total_rows}</p>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown("<p>No data available.</p>", unsafe_allow_html=True)

            
        else:
            st.error('Failed to fetch filtered data from API main')


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

############################################# add record test 3 #########################################
############ This works fine in terms of adding data into table. No default values taken in dictionary###################            
# ISSUE: form not closing after submission. Tried "clear_on_submit=True", but it doesn't send request api call.
#Tried session state for form submit, didnt work
            
    if "button_clicked" not in st.session_state:
        st.session_state.button_clicked=False

    def func():
        st.session_state.button_clicked=True

    if (st.button("Add new record",on_click=func) or st.session_state.button_clicked) :

        with st.form("addrecord"):
            # Create input fields for each column
            add_record_data = {}
            for column_name, options in filter_options_to_add_record.items():
                if column_name == 'cleanliness_rating':
                    add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
                elif column_name in ['bedrooms', 'person_capacity', 'room_type', 'business']:
                    add_record_data[column_name] = st.selectbox(f'Select {column_name}', options)
                else:
                    add_record_data[column_name] = st.text_input(f'Enter {column_name}')

            # Add input fields for additional columns
            add_record_data['guest_satisfaction_overall'] = st.text_input('Enter guest satisfaction overall(%)')
            add_record_data['realSum'] = st.text_input('Enter Price')



            # Add a button to submit the record
            if (st.form_submit_button('Submit')):
                response = requests.post('http://localhost:5000/add_record', json=add_record_data)
                if response.status_code == 201:
                    st.success('Record added successfully')
                else:
                    st.error('Failed to add record')
        
###############################################delete record button ###########################################
    if st.button("Delete Record"):
        st_del_button=True
    else:
        st_del_button=False

    if st_del_button:
        srno=st.number_input("Enter Sr.No.",value=0,step=1)
        response=requests.delete('http://localhost:5000/deleterecord',params={'srno':srno})

        if response.status_code == 201:
                st.success('Record deleted sucessfully')
        else:
                st.error(f'Failed to delete record. Error: {response.text}')

######################### plots #################################################################################
import matplotlib.pyplot as plt
import seaborn as sns

# Set the figure size for seaborn plots
sns.set_theme(rc={'figure.figsize': (8, 6)})  # Adjust the width and height as needed

with tab2:
    plot_type = st.selectbox(
    "Pick a plot type",
    ("Select","Count","Pie","Histogram","Box Plot",'Correlation Matrix')
    )

    columns=['room_type',
        'business',
        'bedrooms',
        'person_capacity',
        'cleanliness_rating',
        'realSum',
        'guest_satisfaction_overall'
    ]
    if plot_type=='Count':
        column_name=st.selectbox('Column',columns)
        if column_name=='guest_satisfaction_overall':
            plot_data['guest_satisfaction_overall'] = plot_data['guest_satisfaction_overall'].astype(int)
            plot=sns.countplot(data=plot_data, x=column_name)
            plt.xticks(rotation=60)
        else:
            plot=sns.countplot(data=plot_data, x=column_name)
            # Display the plot using Streamlit's layout features

        # Annotate each bar with its corresponding frequency
        for p in plot.patches:
            plot.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                        textcoords='offset points')

        col1, col2 = st.columns([0.6, 0.4])  # Adjust the width ratio as needed

        with col1:
            st.pyplot(plot.figure)

    if plot_type=='Pie':
        column_name=st.selectbox('Column',columns)

        # Calculate the counts of each category
        counts = plot_data[column_name].value_counts()
        labels=plot_data[column_name].unique()

        fig, ax = plt.subplots()
        ax.pie(counts, labels=labels, startangle=60)
        ax.axis('equal')
        ax.legend(labels, loc="best")
        plt.title(column_name)
        col1, col2 = st.columns([0.6, 0.4])  # Adjust the width ratio as needed

        with col1:
            st.pyplot(fig)
        
    if plot_type=='Box Plot':
        xcolumn_name=st.selectbox('X column',columns)

        # Allow users to select Y column if they want
        include_ycolumn = st.checkbox('Include Y column')
        if include_ycolumn:
            ycolumn_name = st.selectbox('Y column', columns)
        else:
            ycolumn_name = None
        # Allow users to select hue if they want
        include_hue = st.checkbox('Include Plot division basis (hue)')
        if include_hue:
            hue = st.selectbox('Plot division basis (hue)', columns)
        else:
            hue = None

        plot=sns.boxplot(data=plot_data,x=xcolumn_name,y=ycolumn_name,hue=hue,gap=.1)
        # Display the plot using Streamlit's layout features
        col1, col2 = st.columns([0.6, 0.4])  # Adjust the width ratio as needed

        with col1:
            st.pyplot(plot.figure)
        
    if plot_type == 'Correlation Matrix':
        # Drop string columns from the DataFrame
        numeric_data = plot_data.select_dtypes(include='number')

        # Compute the correlation matrix
        correlation_matrix = numeric_data.corr()

        # Create the heatmap
        fig, ax = plt.subplots()
        sns.heatmap(correlation_matrix, annot=True, cmap="YlGnBu", ax=ax)  # Adjust the color map as needed
        plt.title('Correlation Matrix Heatmap')  # Add a title to the heatmap
        plt.xticks(rotation=45)  # Rotate xticks for better visibility if needed

        col1, col2 = st.columns([0.6, 0.4])  # Adjust the width ratio as needed

        with col1:
            st.pyplot(fig)


    # # Create histogram
    if plot_type == 'Histogram':
        column_name = st.selectbox('Column', columns)
        if column_name == 'cleanliness_rating':
            # Define bin edges and labels
            bins = [0, 3, 7, 10]
            labels = ['Low', 'Medium', 'High']

            # Create a new column with bin labels
            plot_data['cleanliness_category'] = pd.cut(plot_data[column_name], bins=bins, labels=labels)

            # Plot the histogram
            fig, ax = plt.subplots()
            sns.histplot(data=plot_data, x='cleanliness_rating', bins=bins, ax=ax)
            ax.set_xlabel('Cleanliness Rating')
            ax.set_ylabel('Frequency')
            ax.set_title('Distribution of Cleanliness Ratings')

            # Annotate each bar with its corresponding frequency
            for p in ax.patches:
                ax.annotate(f'{p.get_height()}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha='center', va='center', fontsize=10, color='black', xytext=(0, 5),
                            textcoords='offset points')

            # Display the plot in Streamlit layout
            col1, col2 = st.columns([0.6, 0.4])  # Adjust the width ratio as needed
            with col1:
                st.pyplot(fig)



#############################################################################################################################################
# # Visualize the distribution of realSum values.
# real_sum_values = [entry['realSum'] for entry in filtered_data]

# fig, ax = plt.subplots(figsize=(12, 3))  # Adjust the figure size as needed
# ax.hist(real_sum_values, bins=20, color='skyblue', edgecolor='black')
# ax.set_title('Histogram of realSum')
# ax.set_xlabel('realSum')
# ax.set_ylabel('Frequency')

# # Display plot in Streamlit
# st.pyplot(fig)

# # Show the distribution and variability of person_capacity
# person_capacity_values = [entry['person_capacity'] for entry in filtered_data]
# fig, ax = plt.subplots(figsize=(12, 3))
# ax.boxplot(person_capacity_values)
# ax.set_title('Boxplot of person_capacity')
# ax.set_xlabel('person_capacity')


# st.pyplot(fig)


