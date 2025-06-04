# Birthday Easter Egg Hunt

A Streamlit application for a fun Easter egg hunt game to celebrate a special birthday!

## Features

- 9 text input fields for Easter egg answers
- Fuzzy string matching for flexible answer checking
- Feedback on correct/incorrect answers
- Hints available when needed
- Colorful UI with success/error messages

## Setup and Installation

1. Make sure you have Python 3.7+ installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the application, run:

```
streamlit run app.py
```

The application will open in your default web browser. If it doesn't, you can access it at `http://localhost:8501`.

## How to Play

1. Enter your answers in the 9 text input fields
2. Click "Submit" to check your answers
3. Use the "Hint" button if you need help
4. Correct any wrong answers and try again!

## Requirements

- streamlit
- fuzzywuzzy
- python-Levenshtein (for faster fuzzy matching)

All requirements are listed in `requirements.txt`.
