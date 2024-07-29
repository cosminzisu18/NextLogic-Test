# NextLogic-Test

A Python tool for parsing and validating text files into JSON format.

Bună ziua, sunt Cosmin. Aici voi scrie pașii pe care i-am parcurs pentru a finaliza testul.

## 1. Alegerea Limbajului și a Bibliotecilor

Am ales ca limbaj de programare Python și am folosit Tkinter pentru a crea interfața grafică:
- Tkinter este o bibliotecă standard în Python, care permite crearea de interfețe grafice ușor și rapid.
- JSON este o bibliotecă standard în Python pentru manipularea datelor în format JSON.

## 2. Instalarea Bibliotecilor

- Tkinter vine preinstalat cu majoritatea distribuțiilor de Python, dar poate fi instalat cu comanda pip install tk.
- JSON este o bibliotecă standard și nu necesită instalare separată.

## 3. Crearea Fișierului Python de Bază (main.py)

Am început prin importarea bibliotecilor necesare și definirea funcțiilor utile pentru manipularea și procesarea textului și a datelor JSON:
- import json: Pentru a lucra cu datele în format JSON.
- import re: Pentru a utiliza expresii regulate în vederea extragerii și manipulării textului.
- import tkinter as tk: Pentru a crea interfața grafică.
- from tkinter import filedialog: Pentru a deschide un dialog de selectare a fișierelor.
- from collections import Counter, defaultdict: Pentru a utiliza structuri de date specializate, cum ar fi numărătoarele și dicționarele implicite.

## 4. Conversia Fișierului .txt într-un JSON Valid

### 4.1. **Eliminarea Spațiilor Inutile**

- Funcția clean_text_value elimină spațiile de la începutul și sfârșitul textului și adaugă ghilimele în jurul valorilor, dacă acestea nu sunt deja acoperite de ghilimele.

### 4.2. **Adăugarea Ghilimelelor la Chei**

- Funcția convert_tags_to_json adaugă ghilimele în jurul cheilor care nu au deja ghilimele, folosind expresii regulate pentru a modifica textul JSON.

### 4.3. Prelucrarea Valorilor Între "text" și "boundingBox"

- Funcția convert_tags_to_json aplică clean_text_value pentru a adăuga ghilimele valorilor între "text": și "boundingBox".

### 4.4. **Validarea JSON-ului**

- Funcția validate_json încearcă să parseze textul JSON și, în caz de eroare, returnează detalii despre eroare, inclusiv poziția și un fragment al textului din jurul erorii.


## 5. Extracția și Curățarea Datelor

Am folosit diverse funcții pentru a extrage și curăța datele din textul JSON, asigurându-ne că datele sunt relevante și corect formatate.

### 5.1. **Extracția Numărului Cardului**

- Funcția extract_card_number utilizează o expresie regulată pentru a extrage numerele de card în formatul xxxx xxxxx x din textul JSON.

### 5.2. **Extracția Numărului, Numele, Inițiala și Prenumele**

- **5.2.a.** **Curățarea Datelor pentru a Păstra Doar Cifrele și Majusculele**:
  - Funcția clean_text elimină literele mici, păstrând doar majusculele și cifrele.

- **5.2.b.** **Identificarea Celui Mai Repetitiv Cuvânt**:
  - Funcția most_common_word caută și returnează cuvântul cel mai frecvent din text, considerat a fi numele de familie.

- **5.2.c.** **Separarea și Repoziționarea Numele de Familie**:
  - Funcția extract_citizen_data separă numele de familie de restul datelor și îl poziționează la sfârșit, folosind cel mai comun cuvânt identificat anterior.

- **5.2.d.** **Crearea unui Pattern Regex pentru Extracția Datelor într-un Format Specific**:
  - Funcția extract_citizen_data creează un pattern regex pentru a extrage datele într-un format specific, cum ar fi nr firstname initial lastname.

- **5.2.e.** **Preluarea Celui Mai Frecvent Nume pentru Fiecare Număr**:
  - Funcția most_common_per_number grupează și identifică cel mai frecvent nume pentru fiecare număr de card, evitând derivatele necorespunzătoare.

- **5.2.f.** **Ștergerea Spațiilor Goale de După Sfârșitul Numele Utilizatorului**:
  - Funcția clean_user_name elimină spațiile goale de la sfârșitul numelui utilizatorului.

- **5.2.g.** **Extracția și Păstrarea Textelor care Conțin Cel Mai Frecvent Nume pentru Fiecare Număr**:
  - Funcția extract_names combină funcțiile anterioare pentru a extrage și păstra doar textele care conțin cel mai frecvent nume pentru fiecare număr de card.


### 5.3. **Extracția Datei de Expirare**:
- Am folosit formatul care caută o dată în formatul "mm/yyyy".

  

## 6. Încărcarea și Procesarea Fișierului

Am implementat funcționalități pentru încărcarea, procesarea și extragerea datelor din fișierul .txt, asigurându-ne că datele sunt corect formatate și prezentate.

### 6.1. Încărcarea Fișierului

- **Funcția upload_file**:
  - Deschide un dialog pentru selectarea fișierului .txt.
  - Citește conținutul fișierului folosind encodarea utf-8-sig.

### 6.2. Conversia și Validarea JSON-ului

- **Conversie**:
  - Funcția convert_tags_to_json transformă textul în format JSON valid.
- **Validare**:
  - Funcția validate_json verifică validitatea JSON-ului și returnează eventualele erori.

### 6.3. Extracția Datelor

- **Funcția extract_text**:
  - Extrage textul din JSON.
- **Funcția extract_card_number**:
  - Utilizează o expresie regulată pentru a extrage numerele de card în formatul xxxx xxxxx x.
- **Funcția extract_names**:
  - Extrage și formatează numele utilizatorilor folosind funcții de curățare și identificare a celor mai frecvente nume.
- **Funcția extract_valid_to**:
  - Extrage data de validitate folosind o expresie regulată.

### 6.4. Formatul Rezultatelor

- Rezultatul final este structurat în formatul JSON, dupa cerință:
  
json
  {
    "cardNumber": "0000 00000 0",
    "users": ["1 FirstName MiddleNameInitial LastName", ...],
    "validTo": "00/0000"
  }


## 7. Afișarea Rezultatelor

Am implementat funcția `display_result` pentru a prezenta datele extrase într-o interfață grafică, folosind Tkinter pentru a crea un layout estetic și informativ.

### 7.1. **Funcția `display_result`**

- **Scop**:
  - Afișează numărul de card, numele utilizatorilor și data de validitate într-un format structurat.

- **Funcționalitate**:
  - **Ascunde Elementele Anterioare**:
    - Funcția ascunde butonul de încărcare a fișierului și informațiile despre tipul de fișier.
  - **Creare Cadru Rezultate**:
    - Creează un cadru principal (`result_frame`) pentru afișarea rezultatelor.
  - **Creare Cadru Interior**:
    - Adaugă un cadru interior (`inner_frame`) cu un fundal diferit și bordură ridicată.
  - **Afișare Număr Card**:
    - Creează un cadru pentru numărul cardului (`card_number_frame`) și adaugă textul numărului de card sau un mesaj alternativ dacă nu a fost găsit niciun număr.
  - **Afișare Nume Utilizatori**:
    - Creează un cadru pentru numele utilizatorilor (`users_frame`).
    - Dacă există nume, le afișează într-un format tabelar. Dacă nu sunt nume, afișează un mesaj alternativ.
  - **Afișare Data de Validitate**:
    - Creează un cadru pentru data de validitate (`valid_to_frame`) și adaugă textul datei de validitate sau un mesaj alternativ dacă nu a fost găsită nicio dată.

Prin acești pași, am reușit să extrag și să afișez corect datele din fișierul .txt într-un format JSON valid și să le prezint într-o interfață grafică ușor de utilizat.
