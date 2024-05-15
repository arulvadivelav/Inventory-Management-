# Inventory-Management
The goal is to create a web application using Flask framework to manage inventory of a 
list of products in respective warehouses. Imaging this application will be used in a 
shop or a warehouse that needs to keep track of various products and various locations

## Installation
### Clone the repository
```https://github.com/arulvadivelav/Inventory-Management-```

### Create a virtual environment
```python3 -m venv inventory_env```

### Activate virtual environment
```inventory_env/Scipts/activate.bat```

### Navigate to the project directory
```cd Inventory-Management-/my_flask_project```

### Install dependencies
```pip install -r requirements.txt```

### Database connection
Update database connection in the top of the app.py file

### Apply migrations
```flask db migrate```
```flask db upgrade```

### Run application
```flask run``` to run the appication

### Swagger UI
Using ```http://127.0.0.1:5000/api/docs``` to test the APIs