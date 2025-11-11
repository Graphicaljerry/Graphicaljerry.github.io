# AI Photo Summarizer - Setup Instructions

## Important: Configure Your API Key

Before the photo summarizer will work, you need to add your OpenAI API key to the configuration file.

### Step 1: Get Your OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Generate a new API key
4. Copy the key (it will look like: `sk-...`)

### Step 2: Configure the Application

1. Open the file `config.php` in a text editor
2. Find this line:
   ```php
   define('OPENAI_API_KEY', 'your-api-key-here');
   ```
3. Replace `'your-api-key-here'` with your actual API key:
   ```php
   define('OPENAI_API_KEY', 'sk-proj-...');
   ```
4. Save the file

### Step 3: Test the Application

1. Open `photo-summarizer.html` in your web browser
2. Upload a photo
3. The AI will automatically analyze it and show you a description!

## Security Notes

- ✅ Your API key is stored on the server (in `config.php`)
- ✅ The key is protected from web access (via `.htaccess`)
- ✅ The key is NOT committed to git (via `.gitignore`)
- ✅ Users cannot see your API key in the browser
- ⚠️ Never commit `config.php` to a public repository

## How It Works

1. **Frontend** (`photo-summarizer.html`):
   - User uploads a photo
   - Photo is converted to base64
   - Sent to your PHP backend

2. **Backend** (`analyze-photo.php`):
   - Receives the photo
   - Uses YOUR API key (from `config.php`)
   - Calls OpenAI Vision API
   - Returns the result to the frontend

3. **Result**:
   - AI description is displayed below the photo
   - Your API key stays secure on the server

## Troubleshooting

### "API key not configured" error
- Make sure you've edited `config.php` with your real API key
- Make sure `config.php` is in the same directory as `analyze-photo.php`

### Photos won't analyze
- Check that your server has PHP with cURL support
- Check that your API key is valid
- Check browser console for error messages

### Need help?
- Visit [OpenAI API Documentation](https://platform.openai.com/docs)
- Check that you have credits available in your OpenAI account
