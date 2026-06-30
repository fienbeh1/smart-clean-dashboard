mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = \$PORT\n\
enableCORS = false\n\
\n\
[theme]\n\
primaryColor = '#00897B'\n\
backgroundColor = '#F8FAFA'\n\
secondaryBackgroundColor = '#E0F2F1'\n\
textColor = '#1A202C'\n\
font = 'sans serif'\n\
" > ~/.streamlit/config.toml
