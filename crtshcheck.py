import requests  # Importieren des requests Moduls für HTTP-Anfragen
from bs4 import BeautifulSoup  # Importieren von BeautifulSoup aus bs4 für HTML Parsing
from datetime import datetime, timedelta # Datetime import für Ablaufdatums#vergleich


# Funktion zum Abrufen der Daten von crt.sh basierend auf dem Benutzereingabe
def fetch_data_from_crtsh(user_input):
    url = f"https://crt.sh/?q={user_input}"  # Erstellen der URL mit dem Benutzereingabe
    response = requests.get(url)  # HTTP GET-Anfrage an die erstellte URL

    if response.status_code == 200:  # Überprüfen, ob die Anfrage erfolgreich war (HTTP-Status 200)
        return response.text  # Rückgabe des HTML-Inhalts der Seite
    else:
        return None  # Rückgabe von None im Fehlerfall

# Funktion zum Formatieren des HTML-Inhalts und Extrahieren der relevanten Daten
def format_output(html_content):
    soup = BeautifulSoup(html_content, 'lxml')  # Erstellen eines BeautifulSoup-Objekts zum Parsen des HTML-Inhalts
  
    # Suchen Sie alle Tabellen im HTML-Inhalt
    tables = soup.find_all('table')
    # Überprüfen, ob es mindestens drei Tabellen im HTML-Inhalt gibt
    if len(tables) > 2:
        table = tables[2]  # Auswahl der dritten Tabelle (Index 3 entspricht der vierten Tabelle, da die Indizierung bei 0 beginnt)
        headers = [th.text.replace("\n", " ").strip() for th in table.find_all('th')] # Extrahieren der Überschriften der Tabelle
        rows = table.find_all('tr')  # Extrahieren aller Zeilen der Tabelle

        formatted_data = []  # Liste zur Speicherung der formatierten Daten
        expiring_certificates = []  # Liste für Zertifikate, die in den nächsten 30 Tagen ablaufen

        # Durchlaufen aller Zeilen der Tabelle
        for row in rows:
            columns = row.find_all('td')  # Extrahieren aller Spalten (Zellen) der aktuellen Zeile
            column_data = [td.text for td in columns]  # Extrahieren des Textinhalts jeder Zelle
            
            # Überprüfen, ob das Zertifikat in den nächsten 30 Tagen abläuft
            not_after_date_str = column_data[3] if len(column_data) > 3 else None
            if not_after_date_str:
                not_after_date = datetime.strptime(not_after_date_str, "%Y-%m-%d").date()  # Extrahieren Sie nur das Datum
                if datetime.now().date() <= not_after_date <= (datetime.now() + timedelta(days=30)).date():
                    expiring_certificates.append(column_data)

            formatted_data.append(column_data)  # Hinzufügen der extrahierten Daten zur formatted_data Liste

        return headers, formatted_data, expiring_certificates  # Rückgabe der Überschriften, der formatierten Daten und der bald ablaufenden Zertifikate
    else:
        return None, [], []  # Rückgabe von None und zwei leeren Listen, wenn weniger als drei Tabellen vorhanden sind

# Funktion zum Anzeigen der formatierten Daten im Konsolenfenster
def print_formatted_header(headers):
    print("\n")
    for header in headers:
        print(header, end='\t')  # Anzeigen der Überschriften
    print("\n" + "-" * 100)  # Anzeigen einer Trennlinie nach den Überschriften

def print_formatted_data(headers, data):
    counter = 0
    print_formatted_header(headers)
    # Durchlaufen aller Zeilen der formatierten Daten
    for row in data:
        for column in row:
            print(column, end='\t')  # Anzeigen der Zellendaten, getrennt durch Tabulatoren
        print("\n")  # Neue Zeile nach jeder Zeile der Daten
        counter += 1
        if counter % 10 == 0:
            print_formatted_header(headers)
                

# Überprüfen, ob dieses Skript direkt ausgeführt wird (nicht als Modul importiert)
if __name__ == "__main__":
    user_input = input("Bitte geben Sie den Suchbegriff ein: ")  # Aufforderung an den Benutzer zur Eingabe
    data = fetch_data_from_crtsh(user_input)  # Abrufen der Daten von crt.sh basierend auf dem Benutzereingabe

    if data:  # Überprüfen, ob Daten erfolgreich abgerufen wurden
        headers, formatted_data, expiring_certificates = format_output(data)  # Formatieren der abgerufenen Daten
        if headers and formatted_data:  # Überprüfen, ob Überschriften und Daten vorhanden sind
            print_formatted_data(headers, formatted_data)  # Anzeigen der formatierten Daten
            # Zertifikate anzeigen, die in den nächsten 30 Tagen ablaufen
            if expiring_certificates:
                print("\nZertifikate, die in den nächsten 30 Tagen ablaufen:")
                for certificate in expiring_certificates:
                    print(certificate)
            else:
                print("\nEs gibt keine Zertifikate, die in den nächsten 30 Tagen ablaufen.")
        else:
            print("Keine relevanten Daten gefunden.")  # Nachricht anzeigen, wenn keine relevanten Daten gefunden wurden
    else:
        print("Fehler beim Abrufen der Daten von crt.sh")  # Fehlermeldung anzeigen, wenn keine Daten von crt.sh abgerufen werden konnten
