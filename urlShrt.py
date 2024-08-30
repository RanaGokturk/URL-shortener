import random
import string
from flask import Flask, render_template, request, redirect, url_for
import psycopg2



conn = psycopg2.connect(
    dbname="urlShortenerTest",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS urls (
        id SERIAL PRIMARY KEY,
        original_url TEXT NOT NULL,
        short_url TEXT NOT NULL UNIQUE
    )
''')

conn.commit()

app = Flask(__name__)

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(1))
    return short_url

def generate_unique_short_url(cursor):   #Veritabanında zaten var olmayan benzersiz bir kısa URL oluşturur.???

    while True:
        short_url = generate_short_url()
        cursor.execute('SELECT short_url FROM urls WHERE short_url = %s', (short_url,))
        result = cursor.fetchone()
        if not result:
            return short_url

@app.route('/shortUrl', methods=['POST']) #POST HTTP metodu ile çalışır. Bu da, form verilerinin gönderilmesi gibi durumlarda kullanılır
def short_url():
    long_url = request.form['url']  #request: Flask tarafından sağlanan, gelen HTTP isteğini temsil eden bir nesnedir.
    short_url = generate_unique_short_url(c)

    # Kısaltılmış URL'yi veritabanına kaydet
    c.execute('''
        INSERT INTO urls (original_url, short_url)
        VALUES (%s, %s)
    ''', (long_url, short_url))
    conn.commit()

    shortened_url = f"http://localhost:5001/{short_url}"

   

    return render_template("shortUrl.html", short_url=shortened_url)  #render_template fonksiyonu, belirtilen şablon dosyasını işleyip kullanıcıya döndüren bir Flask fonksiyonudur.


@app.route('/')
def html():
    return render_template("index.html") 

@app.route('/<short_url>')
def redirect_short_url(short_url):
    # Veritabanından kısa URL'nin karşılık geldiği uzun URL'yi alın
    c.execute('SELECT original_url FROM urls WHERE short_url = %s', (short_url,))
    result = c.fetchone()

    if result:
        original_url = result[0]
        return redirect(original_url)
    else:
        return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)








