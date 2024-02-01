# KIRANA - Online Grocery Store Web Application
This project is a web application that leverages Flask for building APIs and VueJS for the user interface. The chosen technologies ensure flexibility, scalability, and ease of development. There is smart login and signup for single admin, store managers and users. The user can buy products from multiple sections and will be sent daily reminders and monthly reports each month. There can be multiple store managers who can add products and delete them, download reports of products and add coupons. The can also propose to add sections after getting approval from admin's end. The store manager can only login after being approved from the admin. There is only one admin who can add sections, approve store managers and approve, and delete sections.

# Getting Started

# Installation


# open first terminal window
## Create a virtual environment activate it and install requirements :
cd backend

virtualenv venv

source venv/bin/activate 

 On Windows, use venv\Scripts\activate

pip install -r requirements.txt

brew install redis  (only if using first time)

# open 2nd terminal window
## install redis

cd backend

bash local_workers.sh 

# open 3d terminal window
## install redis

cd backend

bash flower.sh 

# open 4th terminal window
## Start the Flask app:
python app.py

# open 5th terminal window
## install npm and run the app

npm install

npm run serve



# Login details
## admin login
Username: admin

password: admin


# Technologies Used
Flask

SQLite

HTML/CSS

Vue.js

Celery

Redis

flask_jwt_extended

sqlalchemy

# Project Structure
The project follows this directory structure:

backend/: backend part

frontend/: frontend part



# Features
User Registration and Authentication: Enabling users to create accounts and securely log in.

Store Manager Registration and Authentication: Allowing store managers to register and authenticate for managing their stores.

Product Browsing and Searching: Providing an interface for customers to browse and search for products.

Category Display: Organizing products into categories for easier navigation.

Cart Management: Enabling customers to add products to a cart and manage their selections.

Order Placement: Facilitating the process for customers to place orders.

Administrator Functionalities for Managing Products and Categories: Giving administrators control over product listings and category organization.

Administration of Authorizations: Allowing administrators to manage user permissions and access.

Management of Section Addition Requests: Enabling administrators to handle requests for adding new sections or categories.

Provision of Reminder and Reporting Services: Implementing features to send reminders and generate reports for users and managers.

Downloading of .CSV Reports: Offering functionality for users to download detailed reports in .CSV format.
