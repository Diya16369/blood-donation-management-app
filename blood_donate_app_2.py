import streamlit as st
import pandas as pd

# Function to add donor to DataFrame
def add_donor(name, contact, blood_group):
    new_donor = pd.DataFrame({'Name': [name], 'Contact': [contact], 'Blood Group': [blood_group]})
    return new_donor

# Function to search donors by blood group
def search_donor_by_blood_group(df, blood_group):
    return df[df['Blood Group'] == blood_group]

# Function to edit donor details
def edit_donor(df, index, name, contact, blood_group):
    df.at[index, 'Name'] = name
    df.at[index, 'Contact'] = contact
    df.at[index, 'Blood Group'] = blood_group
    return df

# Function to delete donor
def delete_donor(df, index):
    df.drop(index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

# Main function
def main():
    st.title('Blood Donor Management System')

    # Create or load DataFrame
    if 'donors_df' not in st.session_state:
        st.session_state.donors_df = pd.DataFrame(columns=['Name', 'Contact', 'Blood Group'])

    # Sidebar for adding/editing/deleting donors
    st.sidebar.header('Manage Donors')
    option = st.sidebar.radio('Select Action', ['Add Donor', 'Edit Donor', 'Delete Donor'])

    if option == 'Add Donor':
        st.sidebar.subheader('Add New Donor')
        donor_name = st.sidebar.text_input('Name')
        donor_contact = st.sidebar.text_input('Contact Number')
        donor_blood_group = st.sidebar.selectbox('Blood Group', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
        if st.sidebar.button('Add Donor'):
            new_donor = add_donor(donor_name, donor_contact, donor_blood_group)
            if not isinstance(st.session_state.donors_df, pd.DataFrame):  # Check if donors_df is not DataFrame
                st.session_state.donors_df = pd.DataFrame(columns=['Name', 'Contact', 'Blood Group'])
            st.session_state.donors_df = pd.concat([st.session_state.donors_df, new_donor], ignore_index=True)
            st.success('New donor added successfully!')

    elif option == 'Edit Donor':
        st.sidebar.subheader('Edit Existing Donor')
        if not st.session_state.donors_df.empty:
            index_to_edit = st.sidebar.number_input('Enter Index of Donor to Edit', min_value=0, max_value=len(st.session_state.donors_df)-1, value=0)
            donor_name = st.sidebar.text_input('Name', value=st.session_state.donors_df.at[index_to_edit, 'Name'])
            donor_contact = st.sidebar.text_input('Contact Number', value=st.session_state.donors_df.at[index_to_edit, 'Contact'])
            donor_blood_group = st.sidebar.selectbox('Blood Group', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'], index=['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'].index(st.session_state.donors_df.at[index_to_edit, 'Blood Group']))
            if st.sidebar.button('Save Changes'):
                st.session_state.donors_df = edit_donor(st.session_state.donors_df, index_to_edit, donor_name, donor_contact, donor_blood_group)
                st.success('Donor details updated successfully!')
        else:
            st.sidebar.warning('No donors available for editing.')

    elif option == 'Delete Donor':
        st.sidebar.subheader('Delete Existing Donor')
        if not st.session_state.donors_df.empty:
            index_to_delete = st.sidebar.number_input('Enter Index of Donor to Delete', min_value=0, max_value=len(st.session_state.donors_df)-1, value=0)
            if st.sidebar.button('Delete Donor'):
                st.session_state.donors_df = delete_donor(st.session_state.donors_df, index_to_delete)
                st.success('Donor deleted successfully!')
        else:
            st.sidebar.warning('No donors available for deletion.')

    # Search donors by blood group
    st.header('Search Donors by Blood Group')
    search_blood_group = st.selectbox('Select Blood Group', ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    if st.button('Search'):
        donors_found = search_donor_by_blood_group(st.session_state.donors_df, search_blood_group)
        if donors_found.empty:
            st.warning('No donors found for selected blood group.')
        else:
            st.write('Donors found:')
            st.write(donors_found)
    
    # Button to display list of donors added
    if st.button("Show List of Donors"):
        st.write("List of Donors:")
        st.write(st.session_state.donors_df)

# Run the app
if __name__ == '__main__':
    main()
