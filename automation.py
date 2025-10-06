from dotenv import load_dotenv
import imaplib
import email
import os
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse, urlunparse

load_dotenv()
#get email and password from env
username = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
if not username or not password:
    raise ValueError("EMAIL and PASSWORD must be set in the .env file")


def parse_emails():
    #login
    mail = connect_to_email()

    #search_data gets msg numbers 
    _, search_data = mail.search(None, '(BODY "unsubscribe")')
    #split the message numbers 
    data = search_data[0].split()

    links = []

    #parse through numbers 
    for i, number in enumerate(data):

        # #only check 50 emails to keep run time fast for testing
        # if i >= 50: 
        #     break

        #get the specific number, for all email
        _, data = mail.fetch(number, "(RFC822)")

        #get the message 
        msg = email.message_from_bytes(data[0][1])

    
        if msg.is_multipart():

            #step through all parts and see if its text
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    payload = part.get_payload(decode=True)        
                    try:
                        html_content = payload.decode("utf-8")
                    except UnicodeDecodeError:
                        try:
                            html_content = payload.decode("ISO-8859-1")
                        except UnicodeDecodeError:
                            html_content = payload.decode("utf-8", errors="ignore")  
                    links.extend(extract_html_link(html_content))

 
        else:
            if msg.get_content_type() == "text/html":     
                payload = msg.get_payload(decode=True)        
                try:
                    html_content = payload.decode("utf-8")
                except UnicodeDecodeError:
                    try:
                        html_content = payload.decode("ISO-8859-1")
                    except UnicodeDecodeError:
                        html_content = payload.decode("utf-8", errors="ignore")  
                links.extend(extract_html_link(html_content))
        
    mail.logout()

    return links


    
def extract_html_link(html_content):
    #parse through html using soup
    soup = BeautifulSoup(html_content, "html.parser")

    #get the links which has the word "unsubsribe" in it 
    links = [link["href"] for link in soup.find_all("a", href=True) if "unsubscribe" in link["href"].lower()]

    #return those links 
    return links

def connect_to_email():
    #connect to server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    mail.select("inbox")
    return mail 


def click_link(link):
    try:
        resposne = requests.get(link, timeout=8)
        if resposne.status_code == 200:
            print(f"Successfully visited {link}")

        else:
            print(f"Failed to visit {link}")
    
    except requests.exceptions.Timeout:
        print(f"Timeout on: {link}")
    except Exception as e:
        print(f"Error on: {link} {e}")



def normalize_link(link):
    try:

        #break link into components (scheme, netloc, path, query, etc.)
        parsed = urlparse(link)  

        #Remove query params and fragments (like ?utm=, &trk=, #section)
        clean = parsed._replace(query="", fragment="")

        #rebuild a clean URL
        return urlunparse(clean)  
    
    except Exception:
        return None  #if parsing fails, return None (skip bad link)

def clean_links(links):
    #keep only http/https links and normalize them
    normalized = [normalize_link(l) for l in links if l and l.startswith("http")]

    #filter only those that have 'unsubscribe' in them
    normalized = [l for l in normalized if l and "unsubscribe" in l.lower()]

    #remove duplicates by converting to set, then back to list
    return list(set(normalized))


def save_links(links):
    with open("links.txt", "w") as file:
        file.write("\n".join(links))

    print("\n\n-------------Links saved in file called 'links.txt-------------'")


def main():
    print("Parsing email...")
    links = parse_emails()

    print("Cleaning parsed links...")
    #clean links up
    links = clean_links(links)

    print("Visiting links...")
    for link in links: 
        click_link(link)

    save_links(links)



if __name__ == "__main__":
    main()

 
