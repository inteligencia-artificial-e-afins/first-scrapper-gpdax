import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def scrape_content(url, div_class):
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        divs = soup.find_all('div', class_=div_class)

        content = ""
        for div in divs:
            lis = div.find_all('li')
            for li in lis:
                content += li.text.strip() + "\n"

            paragraphs = div.find_all('p')
            for paragraph in paragraphs:
                content += paragraph.text.strip() + "\n"

        print(content)  # Print extracted content
        return content
    else:
        return "Failed to access the page"

# Set up SMTP server details
smtp_server = 'smtp.gmail.com'
smtp_port = 587

# Create email message
msg = MIMEMultipart()
msg['From'] = 'math@edu.unifil.br'
msg['To'] = 'mario.adaniya@unifil.br'
msg['Subject'] = '[DS101]'

# Email body with scraped content
url = 'https://pt.wikipedia.org'
div_class = 'main-page-block-contents'
content = scrape_content(url, div_class)
body = f'Dados de Extração.\n\n{content}'
msg.attach(MIMEText(body, 'plain'))

 #Authenticate and send email
username = 'math@edu.unifil.br'
password = 'Mathpdalmeida2001'

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(username, password)
    text = msg.as_string()
    server.sendmail(username, msg['To'], text)
    print('Email sent successfully!')
except Exception as e:
    print(f'Error: {e}')
finally:
    server.quit()
