from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Verbindung zur Datenbank herstellen
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn





# Hauptseite
@app.route('/')
def index():
    data = get_data()
    return render_template('main.html', data = data)

# Daten aus der Datenbank abrufen Hauptseite
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Kalender")
    data = cursor.fetchall()
    conn.close()
    return data





# Newsletter/Anmeldung
@app.route('/newsletter')
def newsletter():
    data = get_data()
    return render_template('Newsletter.html', data = data)

# Forms für Datenbank Anmeldung/ Newsletter
@app.route('/submit', methods=['POST','GET'])
def submit():
        if request.method == 'POST':
            title = request.form['name']
            content = request.form['email']

            # Datenbankverbindung herstellen
            conn = connect_db()
            cursor = conn.cursor()

            # SQL-Befehl zum Einfügen von Daten
            cursor.execute("INSERT INTO newsletter (Name, email) VALUES (?, ?)", (name, email))

            # Änderungen in der Datenbank speichern
            conn.commit()

            # Datenbankverbindung schließen
            conn.close()
            print(title, content, 'wurden in der Datenbank gespeichert')
            return redirect('/newsletter')







if __name__ == '__main__':
    app.run(debug=True)