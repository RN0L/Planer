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
    return render_template('main.html', data = data, name = benutzername )
 
def benutzername():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM login")
    data = cursor.fetchall()
    conn.close()
    return data


# Daten aus der Datenbank abrufen Hauptseite Kalender tabelle
def get_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kalender ORDER BY priorisiert DESC")
    data = cursor.fetchall()
    conn.close()
    return data
 
 
def connect_db():
    return sqlite3.connect('database.db')
 
 
# Verändern main seite für Checkboxes Kalender
@app.route('/submit1', methods=['POST'])
def submit1():
    conn = connect_db()
    cursor = conn.cursor()
 
    for key in request.form:
        if key.startswith('fertig-') or key.startswith('priorisiert-'):
            item_id = key.split('-')[1]
            if 'fertig' in key:
                fertig_value = 1
            else:
                fertig_value = 0
            if 'priorisiert' in key:
                priorisiert_value = 1
            else:
                priorisiert_value = 0
           
#SQL befehl
            cursor.execute("UPDATE kalender SET Priorisiert = ?, Fertig = ? WHERE ID = ?", (priorisiert_value, fertig_value, item_id))
 
    conn.commit()
    conn.close()
    return redirect('/')
 
# Löschen von Datensätzen hauptseite
 
@app.route('/delete', methods=['POST'])
def delete_entry():
    delete_id = request.form.get('delete_id')
    if delete_id:
        conn = connect_db()
        cursor = conn.cursor()
       
        # SQL-Befehl zum Löschen des Datensatzes
        cursor.execute("DELETE FROM kalender WHERE ID = ?", (delete_id,))
       
        # Änderungen in der Datenbank speichern
        conn.commit()
       
        # Datenbankverbindung schließen
        conn.close()
       
        print('Datensatz gelöscht')
   
    return redirect('/')
 
 
 
# login
@app.route('/login')
def newsletter():
    data = get_data()
    return render_template('login.html', data = data)
 
 
@app.route('/navbar')
def navbar():
    data = get_data()
    return render_template('navbar.html', data = data)
 
 
 
@app.route('/about')
def about():
    data = get_data()
    return render_template('about.html', data = data)
 
@app.route('/registrieren')
def registrieren():
    data = get_data()
    return render_template('registrieren.html', data = data)
 
 
@app.route('/hinzufügen')
def hinzufügen():
    data = get_data()
    return render_template('hinzufügen.html', data = data)
 
 
# Forms für Datenbank hinzufügen
@app.route('/submit2', methods=['POST'])
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