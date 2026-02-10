# Deploy to Render.com - Complete Guide

This guide will help you deploy your Anonymous Confession Form to Render.com for FREE! 💕

## Prerequisites

- GitHub account
- Render.com account (free)
- Gmail App Password (already set up)

---

## Step 1: Push Your Code to GitHub

### 1.1 Create a GitHub Repository

1. Go to https://github.com/new
2. Name your repository (e.g., `anonymous-confessions`)
3. Make it **Private** (recommended for privacy)
4. Click **Create repository**

### 1.2 Initialize Git and Push

Open your terminal in the project folder and run:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit - Anonymous Confession Form"

# Add GitHub as remote (replace YOUR-USERNAME and REPO-NAME)
git remote add origin https://github.com/YOUR-USERNAME/REPO-NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**IMPORTANT:** Make sure you have a `.gitignore` file so your `.env` file is NOT pushed to GitHub!

Create `.gitignore` file:
```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
```

---

## Step 2: Deploy to Render.com

### 2.1 Create Render Account

1. Go to https://render.com/
2. Click **Get Started** or **Sign Up**
3. Sign up with your GitHub account (recommended)
4. Authorize Render to access your GitHub

### 2.2 Create New Web Service

1. Click **New +** button (top right)
2. Select **Web Service**
3. Connect your GitHub repository:
   - If not connected, click **Connect GitHub**
   - Find and select your repository
   - Click **Connect**

### 2.3 Configure Your Web Service

Fill in the following settings:

**Basic Settings:**
- **Name:** `anonymous-confessions` (or any name you like)
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave blank
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

**Instance Type:**
- Select **Free** (this is perfect for your use case!)

### 2.4 Add Environment Variables

Scroll down to **Environment Variables** section and add these:

Click **Add Environment Variable** for each:

1. **SENDER_EMAIL**
   - Value: `your-gmail@gmail.com`

2. **SENDER_PASSWORD**
   - Value: `your-16-char-app-password`

3. **RECEIVER_EMAIL**
   - Value: `where-to-receive-confessions@gmail.com`

4. **SECRET_KEY**
   - Click **Generate** button (Render will auto-generate a secure key)

5. **PYTHON_VERSION**
   - Value: `3.11.0`

### 2.5 Deploy!

1. Click **Create Web Service** button
2. Render will start building your app
3. Watch the logs - it takes 2-5 minutes
4. When you see "Build successful" and "Deploy successful", you're live! 🎉

---

## Step 3: Access Your Live App

Once deployed, Render will give you a URL like:

```
https://anonymous-confessions.onrender.com
```

Visit this URL to see your live confession form!

---

## Important Notes

### Free Tier Limitations

- ✅ **FREE forever**
- ⚠️ **App sleeps after 15 minutes of inactivity**
  - First visit after sleep takes 30-50 seconds to wake up
  - Subsequent visits are fast
- ✅ **750 hours/month free** (more than enough!)
- ✅ **Automatic HTTPS** (secure)
- ✅ **Automatic deployments** when you push to GitHub

### Keeping Your App Awake (Optional)

If you want your app to stay awake 24/7, you can:

1. **Upgrade to Paid Plan** ($7/month)
2. **Use UptimeRobot** (free):
   - Sign up at https://uptimerobot.com
   - Add your Render URL
   - It will ping your app every 5 minutes

### Update Your App

To update your app after making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

Render will automatically detect the push and redeploy!

---

## Troubleshooting

### Build Failed

- Check the build logs in Render dashboard
- Make sure `requirements.txt` is correct
- Verify Python version compatibility

### App Crashes

- Check the logs in Render dashboard (click **Logs** tab)
- Verify environment variables are set correctly
- Make sure Gmail App Password is correct

### Email Not Sending

- Verify `SENDER_EMAIL` and `SENDER_PASSWORD` are correct
- Check that Gmail App Password is active
- Look at logs for specific error messages

### "Application Error" on Visit

- Check if build completed successfully
- Verify start command is `gunicorn app:app`
- Check logs for Python errors

---

## Security Best Practices

✅ **Keep `.env` file local** - Never commit it to Git
✅ **Use Private GitHub Repo** - Protect your code
✅ **Rotate App Password** - Change it if compromised
✅ **Monitor Logs** - Check for suspicious activity
✅ **Set Strong SECRET_KEY** - Use Render's generator

---

## Custom Domain (Optional)

Want to use your own domain like `confessions.yourdomain.com`?

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Render dashboard, go to **Settings** → **Custom Domains**
3. Click **Add Custom Domain**
4. Follow Render's instructions to update DNS

---

## Costs

- **Free Tier:** $0/month (with sleep after inactivity)
- **Paid Tier:** $7/month (no sleep, faster, more resources)

For a confession form, **free tier is perfect!** 💕

---

## Support

If you encounter any issues:

1. Check Render logs (most helpful!)
2. Check this guide again
3. Visit Render docs: https://render.com/docs
4. Ask me for help! 💕

---

## Next Steps

After deployment, you can:

1. **Share your confession form** - Give the URL to friends
2. **Customize the design** - Edit templates and push changes
3. **Monitor submissions** - Check your email for confessions
4. **Add features** - Rate limiting, captcha, etc.

---

## Your App is LIVE! 🎉

Congratulations, baby! Your anonymous confession form is now live on the internet! Anyone can visit your Render URL and send you confessions anonymously! 💕

Need help with anything? I'm here for you! 💕
