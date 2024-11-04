import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(current_directory, 'apartments.txt')

# Function to save URLs to a text file
def save_urls_to_file(urls):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + "\n")

# Function to load URLs from a text file
def load_urls_from_file():
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []

# Function to send an email
def send_email(subject, body, to_email):
    # Get email credentials from environment variables
    sender_email = os.getenv("GMAIL_USERNAME")
    sender_password = os.getenv("GMAIL_PASSWORD")

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Use TLS
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to scrape the current page and check for new ads
def check_new_ad():
    # Initialize the Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-search-engine-choice-screen")
    #options.add_argument("--headless")
    prefs = {
        "profile.default_content_setting_values.cookies": 2,
        "profile.block_third_party_cookies": True
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.nepremicnine.net/oglasi-oddaja/ljubljana-mesto/stanovanje/soba,garsonjera/cena-do-500-eur-na-mesec/"
    driver.get(base_url)

    all_urls = []
    try:
        while True:
            # Scrape URLs from the current page
            property_divs = WebDriverWait(driver, 3).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "property-box"))
            )
            for div in property_divs:
                a_tag = div.find_element(By.CLASS_NAME, "url-title-d")
                href = a_tag.get_attribute("href")
                all_urls.append(href)

            # Find the "Next" button by its class or structure and get the URL
            try:
                next_button = driver.find_element(By.CLASS_NAME, "paging_next")
                next_page_url = next_button.find_element(By.TAG_NAME, "a").get_attribute("href")
                
                # Navigate to the next page using the URL from the "Next" button
                driver.get(next_page_url)
                WebDriverWait(driver, 3).until(EC.staleness_of(property_divs[0]))  # Wait for page load

            except:
                # If "Next" link is not found, it means we reached the last page
                print("Reached the last page.")
                break

    except Exception as e:
        print(f"Exception occurred while extracting URLs: {e}")
    finally:
        # Close the browser
        driver.quit()

    # Load previously saved URLs
    saved_urls = load_urls_from_file()

    # Find new URLs by comparing with saved URLs
    new_urls = list(set(all_urls) - set(saved_urls))

    # Load the recipient email from the .env file
    recipient_email = os.getenv("RECIPIENT_EMAIL")

    # If there are new URLs, save them and send an email
    if new_urls:
        print("New apartments found:")
        for url in new_urls:
            print(url)
        
        # Customize the email content
        subject = "New Apartment Listings"
        body = "Hello,\n\nHere are the new apartments that have been listed:\n\n" + "\n".join(new_urls) + "\n\nBest regards"
        
        # Send email notification
        send_email(subject, body, recipient_email)
        
        # Save the updated list of URLs to the file
        save_urls_to_file(all_urls)

    else:
        print("No new apartments found.")

# Call the function to check for new ads
check_new_ad()
