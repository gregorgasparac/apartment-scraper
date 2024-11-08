# Apartment Scraper

### Overview
This project is a Python-based web scraping tool that collects apartment listings from **nepremicnine.net**. Users can specify filters like price, location, and amenities to narrow down their search results. The program retrieves the relevant data and presents it in a structured format, simplifying the apartment hunting process. The results can also be emailed to a specified recipient.

In the variable `base_url`, you can specify any link from **nepremicnine.net** that matches your search criteria.


### Prerequisites
Before you start, make sure you have the following installed:

- **Python 3.8+**: The program requires Python to run. [Download Python here](https://www.python.org/downloads/).
- **ChromeDriver**: Required for interacting with web pages using Selenium. [Download ChromeDriver here](https://chromedriver.chromium.org/), and ensure it matches your installed Chrome version. Place `chromedriver` in your system path or project directory.

### Required Python Libraries
Install the required libraries using:
```bash
pip install -r requirements.txt
```

## Environment Setup
To enable email notifications, set up the following environment variables:

### Step 1: Create a `.env` file
Create a `.env` file in the project directory (or set these variables directly in your environment).

### Step 2: Add the following lines to your `.env` file
Replace the placeholders with your actual credentials:

Note: For Gmail, you'll need an App Password if two-factor authentication is enabled on your account.

   ```plaintext
   GMAIL_USERNAME=your_email@gmail.com
   GMAIL_PASSWORD=your_app_password
   RECIPIENT_EMAIL=recipient_email@gmail.com
   ```

## How to run

```bash
python scraper.py
```

##

