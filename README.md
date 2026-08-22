# virtual-stylist

A personalized virtual styling web application that recommends complete outfits based on user preferences, outfit requirements, fashion attributes, and product compatibility.

The system combines user profiling, clothing metadata, rule-based recommendation and ranking, explainable recommendations, recommendation history, favorites, and live e-commerce product retrieval.


#  Prerequisites

Before running the project, install:

* Python 3.12+
* PostgreSQL
* Git
* A modern web browser

The backend requires Python packages listed in:

backend/requirements.txt



#  Clone the Repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Then:

```bash
cd virtual-stylist
```



#  PostgreSQL Setup

Create the project database.

Using PostgreSQL:

```bash
createdb virtual_stylist_db
```

Alternatively:

```bash
psql postgres
```

Then:

```sql
CREATE DATABASE virtual_stylist_db;
```

Verify:

```bash
psql -l
```

You should see:

```text
virtual_stylist_db
```



#  Backend Setup

Move into the backend:

```bash
cd backend
```

Create a Python virtual environment:

### macOS / Linux

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
```

Activate:

```powershell
venv\Scripts\activate
```



#  Install Python Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

The project provides pinned dependency versions in `backend/requirements.txt`.



#  Configure Environment Variables

Copy the example environment file.

From inside `backend`:

```bash
cp .env.example .env
```

Open:

```text
backend/.env
```

Set your PostgreSQL credentials:

```env
DATABASE_URL=postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/virtual_stylist_db
```

For example:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/virtual_stylist_db
```




#  Initialize the Database

The project contains:

```text
backend/app/database/init_db.py
```

This creates the SQLAlchemy database tables used by the application.

From the `backend` directory:

```bash
python3 -m app.database.init_db
```

Expected output:

```text
Tables created successfully.
```



#  Import the Clothing Dataset

The dataset importer is located at:

```text
dataset/import_dataset.py
```

The importer expects `clothing_dataset.csv` to be in its current working directory.

From the project root:

```bash
cd dataset
```

Make sure the backend virtual environment is still activated.

Then run:

```bash
python3 import_dataset.py
```

The script skips clothing items that already exist and imports new items into the database.

Expected output will include:

```text
Imported X clothing items successfully.
```

After importing:

```bash
cd ..
```



#  Start the Backend

Move into the backend:

```bash
cd backend
```

Activate the virtual environment if necessary:

```bash
source venv/bin/activate
```

Start FastAPI:

```bash
uvicorn main:app --reload --port 8001
```

The API will be available at:


http://127.0.0.1:8001


The API documentation is available at:


http://127.0.0.1:8001/docs


The root endpoint should return:


{
  "message": "Virtual Stylist API Running"
}



#  Start the Frontend

The frontend is a static HTML/CSS/JavaScript application.

Open a second terminal.

From the project root:

```bash
cd frontend
```

Start a local web server:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

The frontend communicates with the backend running on:

```text
http://127.0.0.1:8001
```



#  Running the Complete Application

You should have two terminals running.

 Terminal 1 — Backend

```bash
cd virtual-stylist/backend
source venv/bin/activate
uvicorn main:app --reload --port 8001
```

### Terminal 2 — Frontend

```bash
cd virtual-stylist/frontend
python3 -m http.server 8000
```

Open:


http://localhost:8000




1. Project Overview

The application allows users to:

* Create an account
* Log in securely
* Create and manage a fashion profile
* Enter outfit requirements
* Receive personalized outfit recommendations
* View recommendation explanations
* Save favourite outfits
* Retrieve products from supported online retailers

The recommendation system analyses factors such as:

* Gender
* Body type
* Skin tone
* Style preference
* Favourite colours
* Occasion
* Temperature
* Season
* Clothing category
* Clothing colour
* Clothing style
* Clothing compatibility



##  Main Features

### User Authentication

* User registration
* User login
* Password hashing
* JWT-based authentication
* Protected user endpoints

### User Profile

Users can maintain information including:

* Gender
* Body type
* Skin tone
* Style preference
* Favourite colours

### Clothing Dataset

The application contains a structured clothing dataset with attributes including:

* Name
* Category
* Gender
* Colour
* Style
* Occasion
* Fit
* Season
* Skin-tone suitability
* Body-type suitability
* Temperature
* Material
* Tags
* Image

### Personalized Recommendations

The recommendation engine evaluates clothing items against the user's profile and requested context.

It considers:

1. Occasion compatibility
2. Style compatibility
3. Skin-tone compatibility
4. Body-type compatibility
5. Favourite colours
6. Gender compatibility
7. Temperature
8. Season

The system then ranks clothing items and builds complete outfits containing:

* Top
* Bottom
* Shoes

### Explainable Recommendations

Recommendations include reasons explaining why an outfit or product was selected.

Examples include:

* Matches requested occasion
* Matches requested style
* Suitable for the user's skin tone
* Suitable for the user's body type
* Matches a favourite colour
* Suitable for the requested temperature

### Recommendation History

Previous user requests and recommendation responses can be stored and retrieved.

### Favourite Outfits

Users can save recommended outfits as favourites.

### E-Commerce Product Retrieval

The application contains retailer/product retrieval services that can retrieve product information from supported external retailers.

Retrieved product information can include:

* Product name
* Brand
* Retailer/source
* Price
* Currency
* Product image
* Product URL
* Category
* Colour
* Style
* Occasion
* Availability
* Sizes
* Other product metadata

Product links can direct users to the original retailer website.



## 3. System Architecture


                    User
                     │
                     ▼
          HTML / CSS / JavaScript
                 Frontend
                     │
                     ▼
               FastAPI API
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
 Authentication   Profile    Recommendations
                              │
                              ▼
                    Recommendation Engine
                              │
                ┌─────────────┴─────────────┐
                │                           │
                ▼                           ▼
        Local Clothing Dataset       E-Commerce Retrieval
                │                           │
                └─────────────┬─────────────┘
                              ▼
                       Outfit Ranking
                              │
                              ▼
                   Recommended Outfits
                              │
                              ▼
                    PostgreSQL Database




##  Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* FastAPI
* Uvicorn

### Database

* PostgreSQL
* SQLAlchemy

### Authentication

* JWT
* bcrypt
* Passlib

### Data Processing

* Pandas
* NumPy

### Product Retrieval

* Python HTTP requests
* BeautifulSoup
* Retailer-specific retrieval services

### Version Control

* Git
* GitHub

---

## 5. Project Structure

```text
virtual-stylist/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routes/
│   │   ├── services/
│   │   └── recommendation/
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── test_ecommerce.py
│
├── dataset/
│   ├── clothing_dataset.csv
│   ├── clothing_dataset_v2new.csv
│   ├── import_dataset.py
│   ├── generate_dataset.py
│   ├── generators/
│   ├── images/
│   └── v2_fashion_dataset/
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│   └── images/
│
└── docs/
```



#  Basic User Flow

After starting the application:

```text
Open Website
      ↓
Register
      ↓
Login
      ↓
Create / Update Profile
      ↓
Enter Outfit Request
      ↓
Recommendation Processing
      ↓
View Recommended Outfits
      ↓
View Reasons
      ↓
Save Favourite Outfit
      ↓
View History
```



#  API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8001/docs
```

This can be used to inspect and test the backend endpoints.

Main functional areas include:

* Authentication
* Profile management
* Clothing management
* Recommendations
* Favourite outfits
* Chat history



#  Recommendation Method

The recommendation engine uses structured clothing metadata and user information.

The system evaluates factors such as:

```text
User Profile
     +
Requested Occasion
     +
Requested Style
     +
Colour Preferences
     +
Skin Tone
     +
Body Type
     +
Temperature
     +
Season
          ↓
     Item Scoring
          ↓
 Category Ranking
          ↓
 Outfit Generation
          ↓
 Outfit Compatibility
          ↓
 Final Ranking
```

The recommendation process is designed to provide explainable results rather than simply returning an unexplained prediction.



#  E-Commerce Integration

The project contains retailer-specific services for retrieving live product information.

Supported/configured retailer services may include:

* GFLOCK
* Cool Planet
* Kapruka
* Neverbe
* Signature

The availability of products depends on the accessibility and current structure of the external retailer websites.

External websites may change their:

* URLs
* HTML structure
* Product pages
* Product availability
* Prices
* Images

Therefore, live retailer retrieval may occasionally fail even when the core Virtual Stylist application is functioning correctly.

The local clothing dataset provides an independent source for the recommendation system.



#  Testing E-Commerce Retrieval

The repository contains:

```text
backend/test_ecommerce.py
```

From the backend directory, run:

```bash
python3 test_ecommerce.py
```

This tests retrieval of live e-commerce products from the configured retrieval service.

An internet connection is required.



#  Clothing Images

The backend serves clothing images through:

```text
/images
```

The image directory is:

```text
dataset/images/
```

The FastAPI application mounts this directory so that clothing images can be accessed by the frontend.



#  Database Tables

The application currently contains database models for:

```text
users
profiles
clothing_items
ecommerce_products
favorites
chat_history
```

The database tables are created through:

```text
backend/app/database/init_db.py
```



#  Troubleshooting

## PostgreSQL connection error

Check that PostgreSQL is running:

```bash
pg_isready
```

Check that the database exists:

```bash
psql -l
```

Check your:

```text
backend/.env
```

and verify:

```env
DATABASE_URL=...
```



## Port 8001 already in use

Check the process:

```bash
lsof -i :8001
```

Stop the old process if necessary, or run the backend using another port.

If you change the backend port, also update:

```text
frontend/app.js
```

because the frontend currently uses:

```text
http://127.0.0.1:8001
```



## `ModuleNotFoundError`

Make sure the backend virtual environment is activated:

```bash
source venv/bin/activate
```

Then reinstall dependencies:

```bash
pip install -r requirements.txt
```



## No clothing recommendations

Check:

1. PostgreSQL is running.
2. `virtual_stylist_db` exists.
3. Database tables have been created.
4. The clothing dataset has been imported.
5. A user profile has been created.
6. The required clothing categories contain data.



## Live retailer products are unavailable

Check:

* Internet connection
* Retailer website availability
* Retailer page structure

External retailer integrations are independent third-party services and may change without notice.




#  Project Limitations

* Live retailer data depends on external websites.
* Retailer page structures may change.
* Product availability and prices may change.
* Recommendation quality depends on the available clothing metadata.
* The system is an academic prototype and is not intended to operate as a large-scale commercial platform.



#  Future Improvements

Potential future improvements include:

* More retailer integrations
* More comprehensive fashion datasets
* Improved natural-language understanding
* More advanced learning from user feedback
* More sophisticated outfit compatibility modelling
* Improved recommendation evaluation
* Deployment to a cloud environment
* Automated monitoring of retailer integrations



#  Academic Context

The project focuses on:

* Personalized recommendation systems
* Fashion recommendation
* User preference modelling
* Rule-based and hybrid recommendation
* Outfit compatibility
* Explainable recommendations
* Natural-language outfit requests
* E-commerce product retrieval
* Web application development


