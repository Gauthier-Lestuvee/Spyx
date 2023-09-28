from urllib import parse

TOKEN = "MTE1MzIzMjM3Njc0NzUzNjQ1NA.GKFpOc.HHNthhugd9lPGWPd3moyoP3IQq6Spe0xs6xvEA"
CLIENT_SECRET = "XuigKafmFb1byk9ZNgzmrRNeAPdOaVbS"
REDIRECT_URL = "http://localhost:5000/oauth/callback"
OAUTH_URL = f"https://discord.com/api/oauth2/authorize?client_id=1153232376747536454&redirect_uri={parse.quote(REDIRECT_URL)}&response_type=code&scope=identify"