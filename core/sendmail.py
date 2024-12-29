from datetime import datetime
from functools import lru_cache
import os
from pydantic import EmailStr
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition, From

def get_content(recipient_name, subject, link, unsubscribe_link, content):
    content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <title>{subject}</title>
        <style>
            /* General styles */
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
                background-color: #f6f6f6;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
            }}
            .header {{
                background-color: #4CAF50;
                color: white;
                text-align: center;
                padding: 10px 0;
            }}
            .content {{
                padding: 20px;
                font-size: 16px;
                line-height: 1.6;
                color: #333333;
            }}
            .content h1 {{
                font-size: 24px;
                color: #4CAF50;
            }}
            .button {{
                display: inline-block;
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                background-color: #f6f6f6;
                text-align: center;
                font-size: 12px;
                color: #888888;
                padding: 10px;
            }}
            .footer a {{
                color: #888888;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <table role="presentation" cellspacing="0" cellpadding="0">
            <tr>
                <td>
                    <div class="container">
                        <!-- Header Section -->
                        <div class="header">
                            <h1>AI Financial News Analysis</h1>
                        </div>

                        <!-- Content Section -->
                        <div class="content">
                            {content}
                        </div>

                        <!-- Footer Section -->
                        <div class="footer">
                            <p>&copy; 2024 Financial Solutions All rights reserved.</p>
                            <p>If you wish to unsubscribe, <a href="{unsubscribe_link}">click here</a>.</p>
                        </div>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """.format(recipient_name=recipient_name, link=link, unsubscribe_link=unsubscribe_link, subject=subject, content=content)

    return content

@lru_cache()
def send_email_with_html(email_address: EmailStr, content: str):

    content = get_content("Hasan Naseem", f"Financial News Analysis for {datetime.now().strftime('%Y-%m-%d')}", "https://enaar.solutions", "https://enaar.solutions/unsubscribe", content)

    message = Mail(
        from_email=From("info@enaar.solutions", "Enaar Solutions"),
        to_emails=email_address,
        subject=f"AI Financial News Analysis for {datetime.now().strftime('%Y-%m-%d')}",
        html_content=content,
    )

    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)