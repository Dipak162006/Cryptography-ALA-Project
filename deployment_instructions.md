# Netlify Deployment Guide

This project is now fully configured for Netlify using serverless Python functions without disrupting local testing.

## Local Testing Setup

To test the site entirely as it would run on Netlify, you can use the Netlify CLI.
*Note: Make sure you have NodeJS installed in order to run `npm` commands.*

1. **Install Netlify CLI** command globally:
   ```powershell
   npm install -g netlify-cli
   ```
2. **Run Netlify Dev Server** locally:
   Make sure your virtual environment is activated (`.\venv\Scripts\activate`), then run:
   ```powershell
   netlify dev
   ```
   This command reads `netlify.toml`, starts the serverless function, and provides a localhost URL where the site is served.

## Automated Deployment to Netlify

To deploy the site to production:

1. **Push your code to GitHub** 
   Make sure all files (except the `venv/` folder and `__pycache__/`) are committed to a GitHub repository.
   
2. **Connect to Netlify**
   - Go to [app.netlify.com](https://app.netlify.com/) and log in.
   - Click "Add new site" -> "Import an existing project".
   - Select GitHub and choose your repository.

3. **Configure Build Settings**
   Netlify should automatically detect the `netlify.toml` file in your repository. 
   Verify the build settings are:
   - **Base directory**: (Leave empty)
   - **Build command**: (Leave empty, we don't need a build script for this python serverless app)
   - **Publish directory**: `.`
   - **Functions directory**: `netlify/functions`

4. **Deploy Site**
   Click the "Deploy site" button. Wait a minute or two for the deployment to finish building.

5. **Done!**
   Your site is now live via the Netlify serverless edge! Any future commits to your GitHub `main` branch will deploy automatically.
