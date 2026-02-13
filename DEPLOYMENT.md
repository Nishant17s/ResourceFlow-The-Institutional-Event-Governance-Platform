# Deployment Guide

Since this is a **Streamlit** application, the best and easiest way to deploy it is using **Streamlit Community Cloud**. It is free, supports the app's real-time features (websockets), and connects directly to your GitHub repository.

## 🚀 Option 1: Streamlit Community Cloud (Recommended)

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"Sign in with GitHub"**.
3.  Click **"New app"**.
4.  Select your repository: `Nishant17s/ResourceFlow-The-Institutional-Event-Governance-Platform`.
5.  **Main file path**: Enter `app.py`.
6.  Click **"Deploy!"**.

Your app will be live in minutes! 🎈

---

## ⚠️ Option 2: Vercel (Not Recommended)

**Why?** Streamlit relies on **Websockets** to maintain the connection between the server and your browser. Vercel is a **Serverless** platform designed for static sites and short-lived functions.
- Deploying Streamlit on Vercel often results in "Please wait..." connection loops or timeouts because Vercel kills the connection after a few seconds.
- You would need to use complex workarounds or Docker, which defeats the purpose of a quick prototype.

**Verdict**: Stick to Option 1 for a hassle-free experience.
