from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Verbindung zur Datenbank herstellen
def connect_db():
    conn = sqlite3.connect('database.db')
    return conn





# Hauptseite Kalender
@app.route('/',methods=['POST','GET'])
def index():
    if request.method == 'POST':
         prio=request.form['priorisiert']
    data = get_data()
    return render_template('main.html', data = data)

# Daten aus der Datenbank abrufen Hauptseite
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kalender")
    data = cursor.fetchall()
    conn.close()
    return data





    # Verändern main seite 
@app.route('/submit1', methods=['POST'])
def submit1():
    if request.method == 'POST':
        fertig = request.form.get('fertig') == 'on'  # Wenn das Kontrollkästchen ausgewählt wurde, wird 'on' gesendet
        priorisiert = request.form.get('priorisiert') == 'on'

        # Datenbankverbindung herstellen
        conn = connect_db()
        cursor = conn.cursor()

        # SQL-Befehl zum Aktualisieren der Daten
        cursor.execute("UPDATE kalender SET Priorisiert = ?, Fertig = ? WHERE ID = ?", (priorisiert, fertig, id))

        # Änderungen in der Datenbank speichern
        conn.commit()

        # Datenbankverbindung schließen
        conn.close()
        
        print('Änderungen in der Datenbank gespeichert')
        return redirect('/')






# login
@app.route('/navbar')
def navbar():
    data = get_data()
    return render_template('navbar.html', data = data)


@app.route('/hinzufügen')
def hinzufügen():
    data = get_data()
    return render_template('hinzufügen.html', data = data)






# login
@app.route('/login')
def newsletter():
    data = get_data()
    return render_template('login.html', data = data)

# Forms für Datenbank Anmeldung/ Newsletter
@app.route('/submit2', methods=['POST','GET'])
def submit2():
            if request.method == 'POST':
                title = request.form['name']
                content = request.form['email']

                # Datenbankverbindung herstellen
                conn = connect_db()
                cursor = conn.cursor()

                # SQL-Befehl zum Einfügen von Daten
                cursor.execute("INSERT INTO login (name, passwort) VALUES (?, ?)", ("name", "pAssword"))

                # Änderungen in der Datenbank speichern
                conn.commit()

                # Datenbankverbindung schließen
                conn.close()
                print(title, content, 'wurden in der Datenbank gespeichert')
                return redirect('/login')







if __name__ == '__main__':
    app.run(debug=True)