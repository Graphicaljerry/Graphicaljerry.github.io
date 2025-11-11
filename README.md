# AI Photo Summarizer

An AI-powered photo description app that uses OpenAI's Vision API to analyze and describe images.

## ✨ Features

- 📷 Drag & drop or click to upload photos
- 🤖 AI-powered image analysis using GPT-4o-mini
- 🎨 Modern graphite black design
- ⚡ Instant analysis - no button needed
- 🔒 Secure API key handling

## 🚀 Quick Start (Local Development)

### Requirements
- Python 3.7+
- OpenAI API Key ([Get one here](https://platform.openai.com/api-keys))

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Graphicaljerry/Graphicaljerry.github.io.git
   cd Graphicaljerry.github.io
   ```

2. **Configure your API key**
   ```bash
   cp config_local.example.py config_local.py
   ```

   Edit `config_local.py` and add your OpenAI API key:
   ```python
   OPENAI_API_KEY = 'sk-proj-YOUR-KEY-HERE'
   ```

3. **Start the server**
   ```bash
   python3 test_server.py
   ```

4. **Open in browser**
   ```
   http://localhost:8001/photo-summarizer.html
   ```

5. **Upload a photo and watch it get analyzed!** 🎉

## 📁 Files

- `photo-summarizer.html` - Frontend interface
- `test_server.py` - Local development server (Python)
- `server.py` - Alternative local server
- `analyze-photo.php` - PHP backend (for PHP hosting)
- `config.php` - PHP configuration (for PHP hosting)
- `config_local.py` - Your API key (gitignored - never committed)

## 🌐 Deploying to Production

### ⚠️ Important: GitHub Pages Limitation

**GitHub Pages only serves static files** - it cannot run backend code (Python/PHP).

To deploy this app online, you have two options:

### Option 1: Deploy with a Backend Server

Deploy the backend to a service that supports Python or PHP:

**Python Backend:**
- [Heroku](https://www.heroku.com/)
- [Railway](https://railway.app/)
- [PythonAnywhere](https://www.pythonanywhere.com/)
- [Vercel](https://vercel.com/) (with serverless functions)

**PHP Backend:**
- Any PHP hosting provider
- [Heroku](https://www.heroku.com/)
- Traditional web hosting with PHP support

### Option 2: Use Serverless Functions

Convert the backend to serverless functions:
- Vercel Functions
- Netlify Functions
- AWS Lambda
- Cloudflare Workers

## 🔒 Security Notes

- ✅ API keys are stored in gitignored files (`config_local.py`, `config.php`)
- ✅ `.htaccess` blocks direct access to `config.php`
- ✅ Never commit API keys to git
- ⚠️ Don't expose API keys in frontend code

## 🛠️ Troubleshooting

### "Failed to analyze photo"

**Local Development:**
1. Make sure `test_server.py` is running
2. Check that `config_local.py` exists and has your API key
3. Verify your OpenAI API key is valid
4. Check the terminal for error messages

**Deployed Version:**
1. Verify your backend server is running
2. Check that the frontend is pointing to the correct backend URL
3. Verify CORS headers are configured correctly
4. Check API key is configured on the server

### "Failed to fetch"

1. Make sure the server is running on port 8001
2. Open the browser console (F12) to see detailed errors
3. Check that the URL is correct: `http://localhost:8001/photo-summarizer.html`

## 📝 How It Works

1. **User uploads photo** → Frontend converts image to base64
2. **Frontend sends to backend** → POST request to `/analyze-photo.php`
3. **Backend calls OpenAI** → Using your API key stored server-side
4. **AI analyzes image** → GPT-4o-mini Vision API processes the image
5. **Result displayed** → Description shown below the photo

## 💡 Development

### Running Locally

```bash
# Option 1: Use test_server.py (recommended)
python3 test_server.py

# Option 2: Use server.py
python3 server.py

# Option 3: If you have PHP
php -S localhost:8000
```

### Testing

1. Start the server
2. Open http://localhost:8001/photo-summarizer.html
3. Upload a test image
4. Check server logs for any errors

## 📄 License

This project was created with Claude Code.

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 🔗 Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [GitHub Pages Documentation](https://docs.github.com/pages)

---

**Made with ❤️ and AI**
