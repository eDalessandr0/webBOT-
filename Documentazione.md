# Documentazione del Bot

## Introduzione
Questo bot è progettato per consentire a un Raspberry Pi di tradurre un messaggio di testo in codice Morse e inviarlo a una stanza specifica su WebEX utilizzando le API

## Librerie
Il programma richiede l'installazione delle seguenti librerie Python:
- `requests`: Utilizzata per effettuare richieste HTTP alle API di WebEX.
- `RPi.GPIO`: Necessaria per controllare i pin GPIO su Raspberry Pi.
- `unicodedata`: Utilizzata per la rimozione degli accenti dai caratteri Unicode.

## Configurazione Hardware
È necessario collegare un LED al pin GPIO del Raspberry Pi per visualizzare il codice Morse trasmesso.

## Funzioni Principali
- `text_to_morse(text)`: Questa funzione accetta una stringa di testo come input e la converte in codice Morse utilizzando un dizionario predefinito. Gli spazi tra le parole vengono rappresentati da `/`.
- `rimuovi_accenti(input_string)`: Questa funzione accetta una stringa di testo Unicode come input e restituisce la stessa stringa senza accenti.
- `light_morse_code(text)`: Questa funzione accetta una stringa in codice Morse e utilizza un LED collegato al pin GPIO per trasmettere il codice Morse. Punti (`.`) vengono rappresentati da un breve impulso di accensione, trattini (`-`) da un impulso più lungo, e `/` indica uno spazio tra le parole.
- `morse_to_text(morse_code)`: Questa funzione converte una stringa in codice Morse in testo leggibile.

## API WebEX
Il programma utilizza le API di Webex per interagire con le stanze. È necessario fornire un token di autorizzazione valido (`APIAuthorizationKey`) per accedere alle API. Il programma recupera l'ID della stanza in base al nome specificato (`roomNameToSearch`) e invia il messaggio di codice Morse a quella stanza.

## Utilizzo
1. Collega un LED al pin GPIO 17 del Raspberry Pi.
2. Configura correttamente il token di autorizzazione API (`APIAuthorizationKey`) con un valore valido.
3. Specifica il nome della stanza Cisco Spark da utilizzare (`roomNameToSearch`).
4. Esegui il programma.


