# StockAnalyzerApi
This API is used for gathering stock data and returning analyses on different asset types and how they can be compared.

# Virtual Environments
This API is written in Python, and so a virtual environment has been set up to isolate the packges installed for this project
from the base Python system.

To activate the virtual environment: env\Scripts\activate
  You should then see the prompt preceeded by the virtual environment name ((env) $)
To deactivate the virtual environment: deactivate

To learn more about virtual environments, see https://realpython.com/python-virtual-environments-a-primer/

# Dependencies Installations

We'll use pip freeze to put all of our dependencies in a requirements.txt and install from that file when setting up the dependencies for the project.
This requirements.txt will be tracked in git for the dependencies required for the environment. Whenever dependencies are updated, make sure to update
the requirements.txt file so that it is always up to date.

To use: pip freeze > requirements.txt

See https://pip.pypa.io/en/stable/cli/pip_freeze/ for the documentation

# Running the server
python manage.py runserver

# Setting up SSH for interacting with this repo for a Windows Computer:

### **1. Check for Existing SSH Keys**
Open **PowerShell** and run:
```powershell
ls ~/.ssh/id_*
```
If you see `id_rsa.pub` or `id_ed25519.pub`, you may already have an SSH key.

### **2. Generate a New SSH Key**
Run this command in **PowerShell**:
```powershell
ssh-keygen -t ed25519 -C "your-email@example.com"
```
- If `ed25519` is unsupported, try:
  ```powershell
  ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
  ```
- When prompted, press **Enter** to save it in the default location (`C:\Users\<YourUsername>\.ssh\id_ed25519`).
- Optionally, enter a **passphrase** for security.

### **3. Add the SSH Key to GitHub**
1. Retrieve your public key:
   ```powershell
   Get-Content ~/.ssh/id_ed25519.pub
   ```
   Copy the output.
2. Go to [GitHub SSH Settings](https://github.com/settings/keys).
3. Click **New SSH Key**, paste your key, and **save**.

### **4. Add the SSH Key to Your SSH Agent**
Run these commands in **PowerShell**:
```powershell
Start-Service ssh-agent
ssh-add ~/.ssh/id_ed25519
```
This ensures the key is used for authentication.

### **5. Test Your Connection**
Check if GitHub recognizes your SSH key:
```powershell
ssh -T git@github.com
```
You should see:
```
Hi your-username! You've successfully authenticated, but GitHub does not provide shell access.
```

### **6. Use SSH URLs for Git Operations**
Instead of HTTPS, clone repositories using SSH:
```powershell
git clone git@github.com:your-username/repository-name.git
```
This allows you to authenticate **without entering a password** every time.

Let me know if you need troubleshooting help! 🚀
