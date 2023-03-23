import paramiko, os
from flask import Flask, render_template, request, redirect
import wikipedia
import sys


app = Flask(__name__)
app.secret_key = 'my_secret_key'

@app.route('/')
def hello_world():
    return 'hello test'

@app.route('/cars')
def cars():
    cars = ['BMW', 'VW', 'Nissan']
    return render_template('home.html', cars_html=cars)

@app.route('/wiki/search')
def wiki_cars():
    search_term = request.args.get('search_term')
    results = searchWikipedia(search_term)
    return render_template('results.html', results=results)

@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        search_term = request.form['search_term']
        print(search_term)
        results = searchWikipedia(search_term)
        return render_template('results.html', results=results)
    

@app.route('/search_screen')
def search_screen():
    return render_template('search.html')
    
    # cars = searchWikipedia('cars')
    # return render_template('results.html', cars=cars)
    

def searchWikipedia(term):
    results = []
    pageIds = wikipedia.search(term)
    # print(page)
    pages = []
    for pageId in pageIds:
        try:
            page = wikipedia.page(pageId)
            pages.append(page)
        except:
            print("Oups: could not parse the page:", pageId)
            pass
    if len(pages) >= 0:
        for page in pages:
            page_dict = {}
            page_dict['title'] = page.title
            page_dict['url'] = page.url
            results.append(page_dict)

            print("title: " + page.title + " URL: " + page.url + " Content: " + page.content)
    else:
        return "No results!"
    return results

# arguments = "".join(sys.argv[1:]) ## read the arguments (i.e., the search term)
# searchWikipedia("car")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8001))
    app.run(debug=True, host='0.0.0.0', port=port)
