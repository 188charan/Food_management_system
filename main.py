import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd

def validate_alpha(input_str):
    # Loop through each character in the input string
    for char in input_str:
        # Check if the character is not an alphabet and not a space
        if not (char.isalpha() or char.isspace()):
            return False
    return True

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
                fname VARCHAR(35) NOT NULL,
                lname VARCHAR(35),
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
                fname VARCHAR(35) NOT NULL,
                lname VARCHAR(25) ,
                food_type VARCHAR(20) NOT NULL,
                food_name VARCHAR(20) NOT NULL,
                quantity INT NOT NULL,
                door_no VARCHAR(20) NOT NULL,
                street VARCHAR(20) NOT NULL,
                area VARCHAR(20) NOT NULL,
                city VARCHAR(20) NOT NULL,
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
                o_door_no VARCHAR(20) NOT NULL,
                o_street VARCHAR(20) NOT NULL,
                o_area VARCHAR(20) NOT NULL,
                o_city VARCHAR(20) NOT NULL,
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
                email VARCHAR(255) PRIMARY KEY,
                rating INT NOT NULL,
                experience TEXT NOT NULL
            )
        """)
        connection.commit()
    except Error as e:
        st.error(f"Error creating feedback table: {e}")

# Function to simulate user signup and store in the login table
def signup(fname,lname, email, password, connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO login (fname, lname, email, password) VALUES (%s, %s, %s, %s)
        """, (fname, lname, email, password))
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
    st.title(":orange[You are stepping towards a good cause]")
    #st.title(":blue[Donate Food]")
    st.write("Please fill out the form below to donate food.")
    
    col1,col2 = st.columns(2)
    # Form inputs with validation
    with col1:
        fname = st.text_input("First name:")
        door_no = st.text_input("Door number/House name:")
        street = st.text_input("Street:")
    with col2:
        lname = st.text_input("Last name:")
        area = st.text_input("Area:")
        city = st.text_input("City:")
    food_type = st.selectbox("Food Type:", ["Veg", "Non Veg"])
    food_name=st.text_input("Food name:")
    quantity = st.number_input("Quantity of Food (sufficient for the number of people):", min_value=1, step=1)
    phone_number = st.text_input("Phone Number:")
    
    if st.button("Submit Donation"):
        # Form validation
        if not validate_alpha(fname):
            st.error("Please enter a valid First name with only alphabetic characters.")
            return
        if not validate_alpha(lname):
            st.error("Please enter a valid Last name with only alphabetic characters.")
            return
        if not validate_alpha(food_name):
            st.error("Please enter a valid food name with only alphabetic characters.")
            return
        if not validate_alpha(area):
            st.error("Please enter a valid Area with only alphabetic characters.")
            return
        if not validate_alpha(city):
            st.error("Please enter a valid food name with only alphabetic characters.")
            return
        if not is_positive_integer(quantity):
            st.error("Please enter a valid quantity.")
            return
        if not is_valid_phone_number(phone_number):
            st.error("Please enter a valid phone number.")
            return

        # Store donation details in the donate table
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO donate (fname, lname, food_type,food_name, quantity, door_no, street, area, city, phone_number) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, lname, food_type,food_name, quantity, door_no, street, area, city, phone_number))
            connection.commit()
            st.success("Donation submitted successfully!")
            st.snow()
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
            SELECT id, food_type,food_name, quantity, CONCAT_WS(' , ',area,city) AS Address, phone_number FROM donate
        """)
        donate_data = cursor.fetchall()
        df=pd.DataFrame(donate_data,columns=cursor.column_names)
    except Error as e:
        st.error(f"Error retrieving donate data: {e}")
        donate_data = []

    # Display table of available food items
    st.table(df)
    
    col1,col2=st.columns(2)
    # Form to place an order
    with col1:
        selected_id = st.text_input("Enter Donate ID:")
        order_door_no = st.text_input("Enter Door number/House name:")
        order_area = st.text_input("Enter Area:")
    with col2:
        order_quantity = st.number_input("Enter Quantity:", min_value=1, step=1)
        order_street = st.text_input("Enter Street:")
        order_city = st.text_input("Enter City:")
    phone_number = st.text_input("Enter Phone Number:")

    if st.button("Place Order"):
        # Form validation
        if not validate_alpha(order_area):
            st.error("Please enter a valid Area with only alphabetic characters.")
            return
        if not validate_alpha(order_city):
            st.error("Please enter a valid City with only alphabetic characters.")
            return
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
                    INSERT INTO orders (donate_id, quantity, o_door_no, o_street, o_area, o_city, phone_number) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (selected_id, order_quantity,order_door_no, order_street, order_area, order_city , phone_number))
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
            SELECT o.id AS order_id, CONCAT_WS(' , ',d.door_no,d.street,d.area,d.city) AS Donor_address,d.phone_number AS Donor_phone,
                   CONCAT_WS(' , ',o.o_door_no,o.o_street,o.o_area,o.o_city) AS Recipient_address, o.phone_number AS Recipient_phone, o.status as Delivery_status
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

# Recipt generating page
def generate_receipt(connection):
    st.title("Generate your receipt here")
    st.subheader("Please enter your delivery ID to generate your Delivery receipt")

    number = st.text_input("Delivery id:")
    if st.button("Generate"):
        #if not is_positive_integer(number):
        #    st.error("Please enter a valid delivery id.")
        #    return
        try:
            cursor = connection.cursor()
            cursor.execute("""
                SELECT fname, lname, food_name, food_type,door_no,street,area,city FROM donate WHERE id = %s
            """, (number,))
            receipt_data = cursor.fetchone()
            cursor.execute("""
                SELECT o_door_no,o_street,o_area,o_city,id, quantity FROM orders WHERE  donate_id= %s
            """, (number,))
            order_data = cursor.fetchone()
            if receipt_data:
                o_door_no,o_street,o_area,o_city,id, quantity= order_data
                o_address = o_door_no+" , "+o_street+" , "+o_area+" , "+o_city
                fname, lname, food_name, food_type, door_no,street,area,city= receipt_data
                address = door_no+" , "+street+" , "+area+" , "+city
                # HTML code for the receipt with custom styling
                receipt_html = f"""
                <div style="background-color: #f2f2f2;color:black; border: 2px solid #333; padding: 20px;">
                    <h2 style="text-align: center; color: #333;">Delivery Receipt</h2>
                    <p><strong>Delivery id:</strong> {id}</p>
                    <p><strong>Donar Name:</strong> {fname} {lname}</p>
                    <p><strong>Food Type:</strong> {food_type}</p>
                    <p><strong>Food Name:</strong> {food_name}</p>
                    <p><strong>Quantity:</strong> {quantity}</p>
                    <p><strong>Donar Address:</strong> {address}</p>
                    <p><strong>Recipient Address:</strong> {o_address}</p>
                </div>
                """

                # Display the receipt using the st.markdown function
                st.markdown(receipt_html, unsafe_allow_html=True)
            else:
                st.error("No donation record found for the provided phone number.")
                
        except Error as e:
            st.error(f"Error generating the receipt: {e}")


# Feedback Page
def feedback_page(connection):
    st.title("Feedback")
    st.write("Please provide your feedback below.")

    email = st.text_input("Email:")
    rating = st.slider("Rating (1-10):", min_value=1, max_value=10)
    experience = st.text_area("Your Experience:")

    if st.button("Submit Feedback"):
        # Form validation
        if not is_valid_email(email):
            st.error("Please enter a valid name with only alphabetic characters.")
            return

        # Store feedback in the feedback table
        try:
            cursor = connection.cursor()
            cursor.execute("""
                INSERT INTO feedback (email, rating, experience) 
                VALUES (%s, %s, %s)
            """, (email, rating, experience))
            connection.commit()
            st.success("Feedback submitted successfully!")
        except Error as e:
            st.error(f"Error submitting feedback: {e}")


# Login Page
def login_page(connection):
    st.title("Login")

    email = st.text_input("Enter the email:")
    password = st.text_input("Enter the Password:", type="password")

    if st.button("Login"):
        if login(email, password, connection):
            st.session_state.logged_in = True

# Signup Page
def signup_page(connection):
    st.title("Sign Up")

    fname = st.text_input("First name:")
    lname = st.text_input("Last name:")
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    if st.button("Sign Up"):
        # Form validation for signup fields
        if not is_alpha(fname):
            st.error("Please enter a valid First name with only alphabetic characters.")
            return
        if not validate_alpha(lname):
            st.error("Please enter a valid Last name with only alphabetic characters and spaces.")
            return
        if not is_valid_email(email):
            st.error("Please enter a valid email address.")
            return
        if not is_valid_password(password):
            st.error("Please enter a valid password with at least 6 characters.")
            return

        # Call signup function to simulate user signup
        signup(fname,lname, email, password, connection)

def logout():
    st.session_state.logged_in = False
    st.session_state.user_data = {}

def front_page():
    st.title("Welcome to :violet[Annamrutha] Food Management System")
    #st.title(":orange[FEED THE HUNGER]")
    st.header(":green[Let's pitch in and help out by giving to hunger relief!!]")
    st.write("\n")
    st.write("\n")
    st.image("img1.jpg",width= 600,caption="Children across India are facing a threat of undernourishment. Your donation helps us nourish millions of children with mid-day meals across thousands of schools all over India")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    st.write("\n")
    #st.image("col1.jpg", width=520,)
    st.image("col2.webp",width=600,caption="The COVID-19 pandemic has left our senior citizens without any basic support. Your generous donations can contribute to keep them safe.")
    st.write("\n")
    st.write("\n")
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
            st.sidebar.title(':violet[Annamrutha]')
            pages = ["Home","Login","Sign Up","Reset Password"]
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
            st.sidebar.title(':violet[Annamrutha]')
            pages = [ "Donate", "Order", "Delivery","Generate recipt", "Feedback", "Logout"]
            selection = st.sidebar.radio("Go to", pages)
            if selection == "Donate":
                donate_page(connection)
            elif selection == "Order":
                order_page(connection)
            elif selection == "Delivery":
                delivery_page(connection)
            elif selection == "Generate recipt":
                generate_receipt(connection)
            elif selection == "Feedback":
                feedback_page(connection)
            elif selection == "Logout":
                logout()
                st.success("Logged out successfully. Redirecting to login page...")
                st.session_state.logged_in = False
                front_page()

if __name__ == "__main__":
    main()

