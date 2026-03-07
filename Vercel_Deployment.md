# Vercel Deployment Guide (Recommended for Python)

Netlify primarily supports JavaScript, TypeScript, and Go for serverless functions natively. It struggles with Python, which is why your deployment failed to find the Python functions despite the `serverless-wsgi` wrapper.

**Vercel** is highly recommended for Python Flask applications as it has **official, native Python support** with zero configurations required for `app.py`.

## Automated Deployment to Vercel

1. **Commit the Configuration**
   I've created a `vercel.json` file in your repository which tells Vercel how to serve your Flask app.
   Make sure to commit `vercel.json` to your GitHub repository.

2. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com/) and sign up or log in with GitHub.
   - Click **Add New...** -> **Project**.
   - Select the GitHub repository containing this Flask project.

3. **Deploy**
   - Vercel will automatically detect the settings from `vercel.json`.
   - Click the **Deploy** button.
   - Wait 1-2 minutes.

4. **Done!**
   Your site is now live on the Vercel edge network and correctly handles Python functions. Any future pushes to your `main` branch will deploy automatically.
