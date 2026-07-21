# How to run & restart the Financial Assistant

A short guide for starting, stopping, and restarting the Streamlit app.

---

## 1. First-time setup (only once)

Open **PowerShell** in the project folder (`C:\Financial Assisstant`) and install
the dependencies:

```powershell
pip install -r requirements.txt
```

Then create your `.env` file from the example and add your API key:

```powershell
Copy-Item .env.example .env
notepad .env
```

In `.env`, set your key:

```
OPENAI_API_KEY=sk-...your-key-here...
```

Save and close the file.

---

## 2. Start the application

From the project folder, run:

```powershell
python -m streamlit run .\finance_assistant.py
```

Wait a few seconds until you see this line in the terminal:

```
  Local URL: http://localhost:8501
```

Then open **http://localhost:8501** in your browser.

> **Important:** keep this terminal window **open and running**. The app is only
> live while this command is running. If you close the window or press
> `Ctrl + C`, the app stops and the browser page will no longer load.

---

## 3. Stop the application

Click on the terminal window that is running the app and press:

```
Ctrl + C
```

The server shuts down. The browser page at `http://localhost:8501` will stop
loading — that is expected.

---

## 4. Restart the application

1. **Stop** the running app with `Ctrl + C` (see step 3).
2. **Start** it again with the run command:

   ```powershell
   python -m streamlit run .\finance_assistant.py
   ```

3. Wait for the `Local URL: http://localhost:8501` line, then **refresh** the
   browser tab (`Ctrl + F5` for a hard refresh).

> **Tip:** You usually do **not** need to restart just to see edits. Streamlit
> auto-reloads when you save a `.py` file — click **"Rerun"** (or **"Always
> rerun"**) in the top-right of the app. A full restart is only needed when you
> change `.env`, install new packages, or the app gets into a bad state.

---

## 5. Troubleshooting

| Problem | Fix |
|---------|-----|
| **Page won't load / "can't reach this site"** | Make sure the `python -m streamlit run ...` command is still running in a terminal. If it isn't, start it again (step 2). |
| **Blank or stuck page** | Hard-refresh the browser with `Ctrl + F5`. |
| **"Port 8501 is already in use"** | An old instance is still running. Either use the URL it prints (e.g. `8502`), or stop the old one. To free the port: `Get-Process python \| Stop-Process` (this stops *all* Python processes). |
| **"No OPENAI_API_KEY found"** | Your `.env` file is missing or the key isn't set. See step 1. |
| **`streamlit` not recognized** | Always launch with `python -m streamlit run ...` (not just `streamlit run ...`). |

---

## Quick reference

| Action | Command |
|--------|---------|
| Start | `python -m streamlit run .\finance_assistant.py` |
| Stop | `Ctrl + C` in the app's terminal |
| Restart | `Ctrl + C`, then run the start command again |
| Open in browser | http://localhost:8501 |
