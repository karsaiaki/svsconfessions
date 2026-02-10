from flask import Flask, render_template, request, flash, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import textwrap
import io
import ssl

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here-change-this')

# Email configuration - Gmail SMTP
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465  # SSL port (more reliable than 587)
SENDER_EMAIL = os.getenv('SENDER_EMAIL')  # Your Gmail address
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')  # Your Gmail app password
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')  # Email where you want to receive submissions

# Rate limiting: max 3 confessions per device (tracked by IP)
MAX_CONFESSIONS_PER_DEVICE = 3
RESET_PERIOD_DAYS = 60  # Reset after 2 months
submission_records = {}  # { ip_address: { 'count': int, 'first_submission': datetime } }


def get_submission_count(ip):
    """Get the current submission count for an IP, resetting if 2 months have passed."""
    record = submission_records.get(ip)
    if not record:
        return 0
    # Silently reset if 2 months have passed since first submission
    if datetime.now() - record['first_submission'] > timedelta(days=RESET_PERIOD_DAYS):
        del submission_records[ip]
        return 0
    return record['count']


def generate_confession_image(confession_text, timestamp):
    """
    Generate a beautiful image from confession text
    Returns image bytes
    """
    try:
        # Image settings
        img_width = 1200
        padding = 60
        line_spacing = 15
        max_chars_per_line = 80
        
        # Colors (matching the white & blue website theme)
        bg_gradient_start = (224, 237, 255)  # Light blue
        bg_gradient_end = (192, 216, 255)    # Slightly deeper blue
        card_bg = (255, 255, 255)
        text_color = (15, 23, 42)            # Dark slate
        accent_color = (37, 99, 235)         # Blue primary
        subtitle_color = (107, 114, 128)     # Medium gray
        
        # Wrap text
        wrapped_lines = []
        for paragraph in confession_text.split('\n'):
            if paragraph.strip():
                wrapped_lines.extend(textwrap.wrap(paragraph, width=max_chars_per_line))
                wrapped_lines.append('')  # Add spacing between paragraphs
            else:
                wrapped_lines.append('')
        
        # Calculate image height
        title_height = 120
        timestamp_height = 60
        text_height = len(wrapped_lines) * (30 + line_spacing)
        total_height = title_height + timestamp_height + text_height + padding * 4
        
        # Create image with gradient background
        img = Image.new('RGB', (img_width, total_height), color=bg_gradient_start)
        draw = ImageDraw.Draw(img)
        
        # Draw gradient background
        for y in range(total_height):
            ratio = y / total_height
            r = int(bg_gradient_start[0] + (bg_gradient_end[0] - bg_gradient_start[0]) * ratio)
            g = int(bg_gradient_start[1] + (bg_gradient_end[1] - bg_gradient_start[1]) * ratio)
            b = int(bg_gradient_start[2] + (bg_gradient_end[2] - bg_gradient_start[2]) * ratio)
            draw.rectangle([(0, y), (img_width, y + 1)], fill=(r, g, b))
        
        # Draw white card with shadow
        card_padding = 40
        card_left = card_padding
        card_top = card_padding
        card_right = img_width - card_padding
        card_bottom = total_height - card_padding
        
        # Shadow effect
        shadow_offset = 8
        draw.rounded_rectangle(
            [(card_left + shadow_offset, card_top + shadow_offset), 
             (card_right + shadow_offset, card_bottom + shadow_offset)],
            radius=20,
            fill=(0, 0, 0, 30)
        )
        
        # White card
        draw.rounded_rectangle(
            [(card_left, card_top), (card_right, card_bottom)],
            radius=20,
            fill=card_bg
        )
        
        # Accent bar at top
        draw.rounded_rectangle(
            [(card_left, card_top), (card_right, card_top + 6)],
            radius=20,
            fill=accent_color
        )
        
        # Try to use custom fonts, fallback to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 48)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
            text_font = ImageFont.truetype("arial.ttf", 26)
            timestamp_font = ImageFont.truetype("arial.ttf", 22)
        except:
            # Fallback to default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            timestamp_font = ImageFont.load_default()
        
        current_y = card_top + padding
        
        # Draw title
        title = "Anonymous Confession"
        draw.text(
            (card_left + padding, current_y),
            title,
            font=title_font,
            fill=text_color
        )
        current_y += title_height
        
        # Draw timestamp
        timestamp_text = f"Received: {timestamp}"
        draw.text(
            (card_left + padding, current_y),
            timestamp_text,
            font=timestamp_font,
            fill=subtitle_color
        )
        current_y += timestamp_height
        
        # Draw separator line
        draw.line(
            [(card_left + padding, current_y), (card_right - padding, current_y)],
            fill=accent_color,
            width=3
        )
        current_y += padding
        
        # Draw problem description
        for line in wrapped_lines:
            draw.text(
                (card_left + padding, current_y),
                line,
                font=text_font,
                fill=text_color
            )
            current_y += 30 + line_spacing
        
        # Convert image to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG', quality=95)
        img_byte_arr.seek(0)
        
        return img_byte_arr.getvalue()
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        return None


def send_email(confession_text):
    """
    Send an email with the confession as both text and image using Gmail SMTP
    Returns True if successful, False otherwise
    """
    try:
        # Validate email configuration
        if not SENDER_EMAIL or not SENDER_PASSWORD or not RECEIVER_EMAIL:
            print("Error: Email configuration is missing!")
            print(f"SENDER_EMAIL: {'✓' if SENDER_EMAIL else '✗'}")
            print(f"SENDER_PASSWORD: {'✓' if SENDER_PASSWORD else '✗'}")
            print(f"RECEIVER_EMAIL: {'✓' if RECEIVER_EMAIL else '✗'}")
            return False
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create message
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = f'New Anonymous Confession - {timestamp}'
        
        # Email body
        body = f"""
New Anonymous Confession Received
==================================

Received At: {timestamp}

Confession:
-----------
{confession_text}

==================================
This is an automated message from Anonymous Confessions.

NOTE: The confession is also attached as an image below for easy viewing.
        """
        
        message.attach(MIMEText(body, 'plain'))
        
        # Generate and attach image
        print("Generating confession image...")
        confession_image = generate_confession_image(confession_text, timestamp)
        
        if confession_image:
            image_part = MIMEImage(confession_image, name=f'confession_{timestamp.replace(":", "-").replace(" ", "_")}.png')
            image_part.add_header('Content-Disposition', 'attachment', filename=f'confession_{timestamp.replace(":", "-").replace(" ", "_")}.png')
            message.attach(image_part)
            print("Image attached successfully!")
        else:
            print("Warning: Could not generate image, sending text only.")
        
        # Create secure SSL context
        context = ssl.create_default_context()
        
        # Connect to Gmail SMTP server using SSL (port 465)
        print("Connecting to Gmail SMTP server...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=60) as server:
            print("Logging in...")
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            
            print("Sending email...")
            text = message.as_string()
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        
        print(f"Email sent successfully to {RECEIVER_EMAIL}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


@app.route('/')
def index():
    """Display the confession form"""
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    used = get_submission_count(user_ip)
    remaining = max(0, MAX_CONFESSIONS_PER_DEVICE - used)
    return render_template('index.html', remaining=remaining, max_allowed=MAX_CONFESSIONS_PER_DEVICE)


@app.route('/submit', methods=['POST'])
def submit_problem():
    """Handle form submission"""
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    used = get_submission_count(user_ip)
    
    # Check if limit reached
    if used >= MAX_CONFESSIONS_PER_DEVICE:
        flash(f'You have reached the maximum limit of {MAX_CONFESSIONS_PER_DEVICE} confessions.', 'error')
        return redirect(url_for('index'))
    
    confession_text = request.form.get('problem_description', '').strip()
    
    # Validate input
    if not confession_text:
        flash('Please write your confession before submitting.', 'error')
        return redirect(url_for('index'))
    
    if len(confession_text) < 10:
        flash('Your confession is too short. Please write a bit more.', 'error')
        return redirect(url_for('index'))
    
    # Send email
    if send_email(confession_text):
        # Track submission with timestamp
        record = submission_records.get(user_ip)
        if record:
            record['count'] = used + 1
        else:
            submission_records[user_ip] = {'count': 1, 'first_submission': datetime.now()}
        remaining = MAX_CONFESSIONS_PER_DEVICE - (used + 1)
        flash(f'Your confession has been sent anonymously! ({remaining} remaining)', 'success')
        return redirect(url_for('success'))
    else:
        flash('Sorry, there was an error sending your confession. Please try again later.', 'error')
        return redirect(url_for('index'))


@app.route('/success')
def success():
    """Display success page"""
    return render_template('success.html')


if __name__ == '__main__':
    # Check if email configuration is set
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("\n⚠️  WARNING: Email configuration not found!")
        print("Please set environment variables for Gmail:")
        print("  - SENDER_EMAIL")
        print("  - SENDER_PASSWORD (Gmail App Password)")
        print("  - RECEIVER_EMAIL\n")
    
    # Use environment variable for port (required for Render.com)
    port = int(os.getenv('PORT', 5000))
    # Disable debug mode in production
    debug_mode = os.getenv('FLASK_ENV', 'production') != 'production'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
