# Gmail-Unsubscribe-Scraper
This project automatically finds, cleans, and visits unsubscribe links from your email inbox. It extracts links from emails and saves them for easy subscription management.

---

## Overview
The scraper connects securely to your Gmail account via IMAP and searches for emails containing the word "unsubscribe". It can handle both simple and multipart emails with HTML content.  

Using BeautifulSoup, the script extracts all HTML links containing "unsubscribe". Each link is normalized by removing query parameters and fragments to eliminate tracking data and ensure a clean URL. Duplicates and invalid links are filtered out automatically.

Once cleaned, the script attempts to visit each unsubscribe link to initiate unsubscription. All unique links are saved to a file called `links.txt` for record-keeping or manual review.

The workflow is fully automated, from connecting to your inbox to producing a final list of unsubscribe links, making it easier to manage unwanted subscriptions without manually opening emails.

---

## Technologies Used
- Python 3.10+
- dotenv
- imaplib
- email
- BeautifulSoup4
- requests
- urllib.parse

---

## How to Run

1. **Install dependencies:**
   - Run:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set up environment variables:**
- Add the `EMAIL` and `PASSWORD` fields in a `.env` file. **Must be a Gmail account**:
     ```env
     EMAIL=your_email@gmail.com
     PASSWORD=YOUR_APP_PASSWORD_KEY_FOR_THAT_GMAIL
     ```

3. **Run the scraper:**
   - Run:
     ```bash
     python src/unsubscribe_scraper.py
     ```

- The script will parse your inbox, extract and clean unsubscribe links, visit them, and save the unique links in `links.txt`.
