# GitHub Setup Instructions

## How to Get This Project on GitHub

This Vehicle Registration Analytics Dashboard is currently running on Replit. Here's how to transfer it to GitHub:

### Option 1: Download and Upload to GitHub (Recommended)

1. **Download the project files from Replit:**
   - In your Replit workspace, click the three dots menu (⋯) 
   - Select "Download as zip"
   - Extract the downloaded zip file

2. **Create a new GitHub repository:**
   - Go to [GitHub.com](https://github.com)
   - Click "New repository" (green button)
   - Name it: `vehicle-registration-dashboard`
   - Make it public or private as preferred
   - Don't initialize with README (since we have one)

3. **Upload the files:**
   - Click "uploading an existing file"
   - Drag and drop all the project files:
     - `app.py`
     - `data_collector.py`
     - `data_processor.py`
     - `utils.py`
     - `README.md`
     - `github_requirements.txt` (rename to `requirements.txt`)
     - `.gitignore`
     - `LICENSE`
     - `.streamlit/config.toml`

4. **Commit the files:**
   - Add commit message: "Initial commit: Vehicle Registration Analytics Dashboard"
   - Click "Commit new files"

### Option 2: Use Git Commands (Advanced)

If you're familiar with Git:

```bash
# In your local machine
git clone <your-new-github-repo-url>
cd vehicle-registration-dashboard

# Copy all files from your downloaded Replit project
# Then:
git add .
git commit -m "Initial commit: Vehicle Registration Analytics Dashboard"
git push origin main
```

### Option 3: GitHub Import (If Replit supports it)

1. Check if your Replit has GitHub integration enabled
2. Use Replit's "Export to GitHub" feature if available
3. Follow the prompts to create a new repository

## Running on Your Local Machine

After getting the code on GitHub:

1. **Clone the repository:**
   ```bash
   git clone <your-github-repo-url>
   cd vehicle-registration-dashboard
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard:**
   ```bash
   streamlit run app.py --server.port 8501
   ```

4. **Access the dashboard:**
   Open your browser to `http://localhost:8501`

## Important Notes

- **Dependencies**: Use the `github_requirements.txt` file (rename it to `requirements.txt` when uploading)
- **Configuration**: The `.streamlit/config.toml` file contains the server settings
- **Data Source**: The app fetches data from Vahan Dashboard (vahan.parivahan.gov.in)
- **Port**: Default Streamlit port is 8501, but you can change it

## Deployment Options

Once on GitHub, you can deploy to:

- **Streamlit Cloud**: Connect your GitHub repo directly
- **Heroku**: Use the provided files for deployment
- **Railway**: Easy deployment with GitHub integration
- **Vercel**: For serverless deployment

## File Structure After Upload

```
vehicle-registration-dashboard/
├── app.py                    # Main Streamlit application
├── data_collector.py         # Data collection from Vahan Dashboard  
├── data_processor.py         # Analytics and data processing
├── utils.py                 # Utility functions
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore rules
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── SETUP_INSTRUCTIONS.md  # This file
```

Your project is now ready for GitHub! 🚀