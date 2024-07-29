# FastAPI PDF Form Filling

This project demonstrates how to create a FastAPI application that accepts form data, fills out fields in a PDF form, and returns a read-only modified PDF using `fillpdf`.

## Features

- Accepts form data using FastAPI.
- Handles multiple selection inputs.
- Fills out fields in a PDF form.
- Returns a read-only modified PDF.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/roopeshkp34/Fill-Pdf-Form.git
    cd Fill-Pdf-Form
    ```

2. **Create a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Start the FastAPI application**:
    ```sh
    python main.py
    ```

## API Endpoints

### POST /fill-pdf/

Accepts form data, validates it, fills out a PDF form, and returns the modified PDF.

- **Request Parameters**:
    - `name` (str): A required text field.
    - `date` (datetime.date): A required date field.
    - `address` (str): A required text field.
    - `favorite_activities_checkbox` (List[str]):  A list of favorite activities (Reading, Walking, Music, Other).
    - `favorite_activity_radio` (FavoriteActivity): A required `FavoriteActivity` enum field 

- **Response**:
    - `200 OK`: Returns the modified PDF file.
    - `400 Bad Request`: Returns an error if any invalid activities are submitted.
