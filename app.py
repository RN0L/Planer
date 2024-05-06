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
    global benutzername
    if request.method == 'POST':
         prio=request.form['priorisiert']
    data = get_data(benutzername)
    return render_template('main.html', data = data)
 
# Daten aus der Datenbank abrufen Hauptseite Kalender tabelle
def get_data(benutzername):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM kalender WHERE Benutzername='{benutzername}' ORDER BY priorisiert DESC;")
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
@app.route('/login', methods=['GET','POST'])
def login():
    global benutzername
    if request.method == 'POST':
        benutzername = request.form['Benutzername']
        passwort = request.form['Passwort']

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login")
        data = cursor.fetchall()

        for user in data:
            if benutzername == user[1]:
                print(benutzername)
                print(passwort)
                print(user[2])
                if passwort == user[2]:
                    return redirect('/')
                    
                else:  
                     print("Passwort falsch")
        conn.close()
    return render_template('login.html')
 
 
@app.route('/navbar')
def navbar():
    return render_template('navbar.html')
 
 
 
@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/registrieren')
def registrieren():
    return render_template('registrieren.html')
 
 
@app.route('/hinzufügen')
def hinzufügen():
    return render_template('hinzufügen.html')
 
 
# Forms für Datenbank hinzufügen
@app.route('/submit2', methods=['POST'])
def submit2():
    if request.method == 'POST':
        titel = request.form['titel']
        datum = request.form['datum']
 
        # Datenbankverbindung herstellen
        conn = connect_db()
        cursor = conn.cursor()
 
        # SQL-Befehl zum Einfügen von Daten
        cursor.execute("INSERT INTO kalender (Ereignis, Beschreibung, Priorisiert, Fertig, Datum) VALUES (?, ?, ?, ?, ?)", (titel, "Nicht vorhanden", 0, 0, datum))
 
        # Änderungen in der Datenbank speichern
        conn.commit()
 
        # Datenbankverbindung schließen
        conn.close()
 
        print(f"{titel} wurde in der Datenbank gespeichert")
        return redirect('/hinzufügen')
 
 
 
 
 
 
if __name__ == '__main__':
    app.run(debug=True)