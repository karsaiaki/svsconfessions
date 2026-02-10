# Problem Submission Form

A simple Flask web application that allows users to submit problems through a form. When submitted, the problem description is sent to your email via Gmail SMTP.

## Features

- Clean, modern, and responsive UI
- Simple one-field form (problem description only)
- Email notifications sent to your Gmail
- Success/error flash messages
- Character counter with auto-resizing textarea
- No user email required

## Prerequisites

- Python 3.7 or higher
- Gmail account with App Password enabled

## Setup Instructions

### 1. Clone or Download the Project

Place all files in a directory of your choice.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Gmail App Password

For security reasons, Gmail requires an App Password for third-party applications.

**Steps to create a Gmail App Password:**

1. Go to your Google Account: https://myaccount.google.com/
2. Navigate to **Security** in the left sidebar
3. Under "How you sign in to Google", enable **2-Step Verification** (if not already enabled)
4. After enabling 2-Step Verification, return to **Security**
5. Under "How you sign in to Google", click on **App passwords**
6. Select app: Choose **Mail**
7. Select device: Choose **Other (Custom name)** and enter "Problem Submission Form"
8. Click **Generate**
9. Copy the 16-character password (remove spaces)

**Important:** Keep this password secure! You'll use it in the next step.

### 4. Configure Environment Variables

1. Copy the `.env.example` file to create a new `.env` file:

```bash
cp .env.example .env
```

2. Open the `.env` file and fill in your details:

```env
# Email Configuration
SENDER_EMAIL=your-gmail@gmail.com
SENDER_PASSWORD=your-16-char-app-password
RECEIVER_EMAIL=where-to-receive-problems@gmail.com

# Flask Secret Key (change this to a random string)
SECRET_KEY=some-random-secret-key-here
```

**Configuration Details:**
- `SENDER_EMAIL`: Your Gmail address (the one that will send emails)
- `SENDER_PASSWORD`: The 16-character App Password you generated
- `RECEIVER_EMAIL`: Email address where you want to receive problem submissions (can be the same as SENDER_EMAIL)
- `SECRET_KEY`: A random string for Flask sessions (change the default value)

### 5. Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

Visit http://localhost:5000 in your browser to see the form.

## Project Structure

```
min_heart/
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html         # Problem submission form
│   └── success.html       # Success confirmation page
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your actual credentials (DO NOT COMMIT!)
└── README.md             # This file
```

## Usage

1. User opens the form at `http://localhost:5000`
2. User enters their problem description (minimum 10 characters)
3. User clicks "Submit Problem"
4. System sends email to your configured email address
5. User sees success confirmation page

## Email Format

You'll receive emails with this format:

```
Subject: New Problem Submission - 2026-02-10 15:30:45

New Problem Submission Received
================================

Submission Time: 2026-02-10 15:30:45

Problem Description:
-------------------
[User's problem description here]

================================
This is an automated message from your Problem Submission Form.
```

## Error Handling

The application includes error handling for:
- Empty submissions
- Too short descriptions (< 10 characters)
- SMTP connection errors
- Missing environment variables
- Email sending failures

## Security Notes

- **Never commit your `.env` file** to version control
- The `.env` file is already in `.gitignore` (if using Git)
- Keep your Gmail App Password secure
- Consider using environment-specific configurations for production
- For production, use a proper WSGI server like Gunicorn instead of Flask's development server

## Troubleshooting

### Email not sending?

1. **Check your credentials** in the `.env` file
2. **Verify 2-Step Verification** is enabled on your Google account
3. **Confirm App Password** is correct (16 characters, no spaces)
4. **Check console output** for error messages
5. **Verify Gmail SMTP** is not blocked by your firewall

### Common Errors:

**"Authentication failed"**
- Your App Password is incorrect
- 2-Step Verification is not enabled

**"Connection refused"**
- Check your internet connection
- Verify SMTP port 587 is not blocked

**"Email configuration not found"**
- Your `.env` file is missing or incomplete
- Environment variables are not loaded properly

## Customization

### Change Email Template

Edit the `body` variable in the `send_email()` function in `app.py` (lines 36-48).

### Change Form Validation

Modify the validation in the `submit_problem()` route in `app.py` (lines 84-91).

### Customize UI

Edit the HTML and CSS in `templates/index.html` and `templates/success.html`.

### Change Character Limit

Update the `maxlength` attribute in `templates/index.html` (line 72).

## Production Deployment

For production use:

1. Set `debug=False` in `app.py`
2. Use a production-grade WSGI server (Gunicorn, uWSGI)
3. Use environment variables from your hosting platform
4. Consider using a dedicated email service (SendGrid, Mailgun)
5. Add rate limiting to prevent spam
6. Implement CAPTCHA for bot protection

## License

This project is free to use and modify for your needs.

## Support

If you encounter any issues, check the troubleshooting section above or review the error messages in the console output.
