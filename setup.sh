mkdir -p ~/.streamlit/
cat > ~/.streamlit/config.toml << 'CONF'
[server]
headless = true
port = "${PORT}"
enableCORS = false
enableXsrfProtection = false

[theme]
primaryColor = "#00897B"
backgroundColor = "#F5FBF9"
secondaryBackgroundColor = "#FFFFFF"
textColor = "#1A202C"
font = "sans serif"
CONF
