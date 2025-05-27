from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Configuração - substitua pela sua chave GIPHY
GIPHY_API_KEY = os.getenv('GIPHY_API_KEY', 'N6mi7CKzGBSqbG9Q2qZrJJHOJRxsAfwQ')  # Obtenha em https://developers.giphy.com/


@app.route('/', methods=['GET', 'POST'])
def index():
    gifs = []
    search_term = ''

    if request.method == 'POST':
        search_term = request.form.get('search_term', '').strip()
        if search_term:
            # Buscar GIFs na API do Giphy
            url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={search_term}&limit=5"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                gifs = [{
                    'title': gif.get('title', 'Sem título'),
                    'url': gif['images']['original']['url'],
                    'webp_url': gif['images']['original'].get('webp', gif['images']['original']['url']),
                    'whatsapp_url': f"https://wa.me/?text={gif['images']['original']['url']}"
                } for gif in data['data']]

    return render_template('index.html', gifs=gifs, search_term=search_term)


if __name__ == '__main__':
    app.run(debug=True)
