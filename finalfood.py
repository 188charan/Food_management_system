import streamlit as st
import mysql.connector
from mysql.connector import Error
#import random
import pandas as pd

# Function to check if a string contains only alphabetic characters
def is_alpha(s):
    return s.isalpha()

# Function to check if a string is a valid email address
def is_valid_email(s):
    # Basic email format validation
    return "@" in s and "." in s

# Function to check if a string is a valid phone number
def is_valid_phone_number(s):
    # Assuming a valid phone number has only numeric characters and a certain length
    return s.isdigit() and len(s) == 10

# Function to check if a value is a positive integer
def is_positive_integer(value):
    return isinstance(value, int) and value >= 1

# Function to check if a string is a valid password
def is_valid_password(s):
    # For simplicity, just checking if the password is at least 6 characters long
    return len(s) >= 6

# Function to generate a unique ID (integer within 5 digits)
#def generate_unique_id():
#    return random.randint(10000, 99999)

# Function to create a MySQL connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="bmgiwu7opiyq7grqp43g-mysql.services.clever-cloud.com",
            user="u9vthbpksygk4fsf",
            password="1xt1TYlaGbyzDkVGDoa4",
            database="bmgiwu7opiyq7grqp43g"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error: {e}")
        return None

# Function to create login table
def create_login_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating login table: {e}")

# Function to create donate table
def create_donate_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS donate (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                food_type VARCHAR(20) NOT NULL,
                food_name VARCHAR(20) NOT NULL,
                quantity INT NOT NULL,
                address VARCHAR(255) NOT NULL,
                phone_number VARCHAR(10) NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating donate table: {e}")

# Function to create orders table
def create_orders_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INT AUTO_INCREMENT PRIMARY KEY,
                donate_id INT,
                quantity INT NOT NULL,
                delivery_address VARCHAR(255) NOT NULL,
                phone_number VARCHAR(10) NOT NULL,
                status VARCHAR(20) DEFAULT 'Not Delivered',
                FOREIGN KEY (donate_id) REFERENCES donate(id)
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating orders table: {e}")

# Function to create feedback table
def create_feedback_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                rating INT NOT NULL,
                experience TEXT NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating feedback table: {e}")

# Function to simulate user signup and store in the login table
def signup(name, email, password, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO login (name, email, password) VALUES (%s, %s, %s)
        """, (name, email, password))
        connection.commit()
        st.success("Account created successfully! Please log in.")
        st.balloons()
    except Error as e:
        st.error(f"Error signing up: {e}")

# Function to simulate user login
def login(email, password, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM login WHERE email = %s AND password = %s
        """, (email, password))
        user = cursor.fetchone()
        if user:
            st.success(f"Logged in as {user[1]}")
            st.balloons()
            return True
        else:
            st.error("Invalid email or password. Please try again.")
            return False
    except Error as e:
        st.error(f"Error logging in: {e}")
        return False

# Function to reset password
def reset_password(connection):
    st.title("Reset Password")
    st.write("Please enter your email and new password.")

    email = st.text_input("Email:")
    new_password = st.text_input("New Password:", type="password")
    confirm_password = st.text_input("Confirm Password:", type="password")

    if st.button("Reset Password"):
        # Form validation
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if not is_valid_password(new_password):
            st.error("Please enter a valid password with at least 6 characters.")
            return
        if new_password != confirm_password:
            st.error("New password and confirm password do not match.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE login SET password = %s WHERE email = %s
            """, (new_password, email))
            connection.commit()
            st.success("Password reset successfully! Please log in with your new password.")
        except Error as e:
            st.error(f"Error resetting password: {e}")

# Donate Page
def donate_page(connection):
    st.title(":green[You are stepping towards a good cause]")
    st.title(":rainbow[Donate Food]")
    st.write("Please fill out the form below to donate food.")
    
    # Form inputs with validation
    name = st.text_input("Name:")
    food_type = st.selectbox("Food Type:", ["Veg", "Non Veg"])
    food_name=st.text_input("Food name:")
    quantity = st.number_input("Quantity of Food:", min_value=1, step=1)
    address = st.text_input("Address:")
    phone_number = st.text_input("Phone Number:")
    
    if st.button("Submit Donation"):
        # Form validation
        if not is_alpha(name):
            st.error("Please enter a valid name with only alphabetic characters.")
            return
        if not is_alpha(food_name):
            st.error("Please enter a valid food name with only alphabetic characters.")
            return
        if not is_positive_integer(quantity):
            st.error("Please enter a valid quantity.")
            return
        if not is_alpha(address):
            st.error("Please enter a valid address.")
            return
        if not is_valid_phone_number(phone_number):
            st.error("Please enter a valid phone number.")
            return

        # Store donation details in the donate table
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO donate (name, food_type,food_name, quantity, address, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (name, food_type,food_name, quantity, address, phone_number))
            connection.commit()
            st.success("Donation submitted successfully!")
        except Error as e:
            st.error(f"Error submitting donation: {e}")

# Order Page
def order_page(connection):
    st.title("Order Food")
    st.write("Browse the available food items and fill out the form to place an order.")
    
    # Retrieve donate table data
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, name, food_type, quantity, address, phone_number FROM donate
        """)
        donate_data = cursor.fetchall()
        df=pd.DataFrame(donate_data,columns=cursor.column_names)
    except Error as e:
        st.error(f"Error retrieving donate data: {e}")
        donate_data = []

    # Display table of available food items
    st.table(df)

    # Form to place an order
    selected_id = st.text_input("Enter Donate ID:")
    order_quantity = st.number_input("Enter Quantity:", min_value=1, step=1)
    delivery_address = st.text_input("Enter Delivery Address:")
    phone_number = st.text_input("Enter Phone Number:")

    if st.button("Place Order"):
        # Form validation
        if not is_positive_integer(order_quantity):
            st.error("Please enter a valid order quantity.")
            return
        if not is_valid_phone_number(phone_number):
            st.error("Enter a valid phone number.")
            return
        # Check if order quantity is available in donate table
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT quantity FROM donate WHERE id = %s
            """, (selected_id,))
            available_quantity = cursor.fetchone()[0]
            
            if order_quantity <= available_quantity:
                # Store order details in the orders table
                cursor.execute("""
                    INSERT INTO orders (donate_id, quantity, delivery_address, phone_number) 
                    VALUES (%s, %s, %s, %s)
                """, (selected_id, order_quantity, delivery_address, phone_number))
                connection.commit()
                
                # Update donate table with new available quantity
                new_quantity = available_quantity - order_quantity
                cursor.execute("""
                    UPDATE donate SET quantity = %s WHERE id = %s
                """, (new_quantity, selected_id))
                connection.commit()
                
                st.success("Order placed successfully!")
            else:
                st.error("Ordered quantity exceeds available quantity!")
                
        except Error as e:
            st.error(f"Error placing order: {e}")

# Delivery Page
def delivery_page(connection):
    st.title("Delivery Status")
    st.write("Track the delivery status of your food donations and orders.")
    
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT o.id AS order_id, d.name AS donor_name, d.address AS donor_address, 
                   o.delivery_address AS recipient_address, o.status as delivery_status
            FROM orders o
            INNER JOIN donate d ON o.donate_id = d.id
        """)
        delivery_data = cursor.fetchall()
        df=pd.DataFrame(delivery_data,columns=cursor.column_names)
    except Error as e:
        st.error(f"Error retrieving delivery data: {e}")
        delivery_data = []

    # Display table of delivery details
    st.table(df)
    # Form to update delivery status
    st.subheader("Update Delivery Status")
    delivery_id = st.text_input("Enter ID:")
    email = st.text_input("Enter Email:")
    password = st.text_input("Enter Password:", type="password")

    if st.button("Delivered"):
        # Form validation
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if not is_valid_password(password):
            st.error("Please enter a valid password.")
            return

        # Check if ID exists and status is "Not Delivered"
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT status FROM orders WHERE id = %s
            """, (delivery_id,))
            status = cursor.fetchone()
            
            if status and status[0] == "Not Delivered":
                # Update status to "Delivered"
                cursor.execute("""
                    UPDATE orders SET status = 'Delivered' WHERE id = %s
                """, (delivery_id,))
                connection.commit()
                st.success("Delivery status updated successfully!")
            else:
                st.error("Invalid ID or delivery is already marked as delivered!")
                
        except Error as e:
            st.error(f"Error updating delivery status: {e}")

# Feedback Page
def feedback_page(connection):
    st.title("Feedback")
    st.write("Please provide your feedback below.")

    name = st.text_input("Name:")
    rating = st.slider("Rating (1-10):", min_value=1, max_value=10)
    experience = st.text_area("Your Experience:")

    if st.button("Submit Feedback"):
        # Form validation
        if not is_alpha(name):
            st.error("Please enter a valid name with only alphabetic characters.")
            return

        # Store feedback in the feedback table
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO feedback (name, rating, experience) 
                VALUES (%s, %s, %s)
            """, (name, rating, experience))
            connection.commit()
            st.success("Feedback submitted successfully!")
        except Error as e:
            st.error(f"Error submitting feedback: {e}")

# Login Page
def login_page(connection):
    st.title("Login")

    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Login"):
        if login(email, password, connection):
            st.session_state.logged_in = True

# Signup Page
def signup_page(connection):
    st.title("Sign Up")

    name = st.text_input("Name:")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Sign Up"):
        # Form validation for signup fields
        if not is_alpha(name):
            st.error("Please enter a valid name with only alphabetic characters.")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if not is_valid_password(password):
            st.error("Please enter a valid password with at least 6 characters.")
            return

        # Call signup function to simulate user signup
        signup(name, email, password, connection)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_data = {}

def front_page():
    st.title("Welcome to :violet[Annamrutha] Food Management System")
    #st.title(":green[FEED THE HUNGER]")
    st.header(":green[Let's pitch in and help out by giving to hunger relief!!]")
    #st.image("col1.jpg", width=520,)
    st.image("col1.jpg",width= 600,caption="Children across India are facing a threat of undernourishment. Your donation helps us nourish millions of children with mid-day meals across thousands of schools all over India")
    st.image("col2.webp",width=600,caption="The COVID-19 pandemic has left our senior citizens without any basic support. Your generous donations can contribute to keep them safe.")
    st.image("col3.jpg",width=600,caption="The COVID-19 pandemic has left thousands of people without access to food and at an imminent risk of hunger and infection. Your donations can help us provide food relief to the ones in need")
    st.header(":violet[Please login to donate food....]")

# Main App
def main():
    #page configuration.
    st.set_page_config(page_title='Annamrutha', page_icon='🍽️')
    # Create a connection to the MySQL database
    connection = create_connection()
    if connection:
        # Create tables if they don't exist
        create_login_table(connection)
        create_donate_table(connection)
        create_orders_table(connection)
        create_feedback_table(connection)

        if "reset_password" not in st.session_state:
            st.session_state.reset_password = False

        # Check if the user is logged in, if not, show the login/signup pages
        if "logged_in" not in st.session_state or not st.session_state.logged_in:
            st.sidebar.title(':rainbow[Annamrutha]')
            pages = ["Home","Login","Sign Up"]
            if st.session_state.reset_password:
                pages.append("Reset Password")
            selection = st.sidebar.radio("Go to", pages)
            if selection == "Home":
                front_page()
            if selection == "Login":
                login_page(connection)
            elif selection == "Sign Up":
                signup_page(connection)
            elif selection == "Reset Password":
                reset_password(connection)

        else:
            # If the user is logged in, show the multipage app
            st.sidebar.title(':rainbow[Annamrutha]')
            pages = [ "Donate", "Order", "Delivery", "Feedback", "Logout"]
            selection = st.sidebar.radio("Go to", pages)
            if selection == "Donate":
                donate_page(connection)
            elif selection == "Order":
                order_page(connection)
            elif selection == "Delivery":
                delivery_page(connection)
            elif selection == "Feedback":
                feedback_page(connection)
            elif selection == "Logout":
                logout()
                st.success("Logged out successfully. Redirecting to login page...")
                st.session_state.logged_in = False
                front_page()

if __name__ == "__main__":
    main()

