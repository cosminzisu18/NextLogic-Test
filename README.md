# NextLogic-Test

A Python tool for parsing and validating text files into JSON format.

Bună ziua, sunt Cosmin. Aici voi scrie pașii pe care i-am parcurs pentru a finaliza testul.

## 1. Alegerea Limbajului și a Bibliotecilor

Am ales ca limbaj de programare Python și am folosit Tkinter pentru a crea interfața grafică:
- Tkinter este o bibliotecă standard în Python, care permite crearea de interfețe grafice ușor și rapid.
- JSON este o bibliotecă standard în Python pentru manipularea datelor în format JSON.

## 2. Instalarea Bibliotecilor

- Tkinter vine preinstalat cu majoritatea distribuțiilor de Python, dar poate fi instalat cu comanda `pip install tk`.
- JSON este o bibliotecă standard și nu necesită instalare separată.

## 3. Crearea Fișierului Python de Bază (main.py)

Am început prin importarea bibliotecilor necesare și definirea funcțiilor utile pentru manipularea și procesarea textului și a datelor JSON:
- `import json`: Pentru a lucra cu datele în format JSON.
- `import re`: Pentru a utiliza expresii regulate în vederea extragerii și manipulării textului.
- `import tkinter as tk`: Pentru a crea interfața grafică.
- `from tkinter import filedialog`: Pentru a deschide un dialog de selectare a fișierelor.
- `from collections import Counter, defaultdict`: Pentru a utiliza structuri de date specializate, cum ar fi numărătoarele și dicționarele implicite.

## 4. Conversia Fișierului `.txt` într-un JSON Valid

### 4.1. **Eliminarea Spațiilor Inutile**

- Funcția `clean_text_value` elimină spațiile de la începutul și sfârșitul textului și adaugă ghilimele în jurul valorilor, dacă acestea nu sunt deja acoperite de ghilimele.

### 4.2. **Adăugarea Ghilimelelor la Chei**

- Funcția `convert_tags_to_json` adaugă ghilimele în jurul cheilor care nu au deja ghilimele, folosind expresii regulate pentru a modifica textul JSON.

### 4.3. Prelucrarea Valorilor Între `"text"` și `"boundingBox"`

- Funcția `convert_tags_to_json` aplică `clean_text_value` pentru a adăuga ghilimele valorilor între `"text":` și `"boundingBox"`.

### 4.4. **Validarea JSON-ului**

- Funcția `validate_json` încearcă să parseze textul JSON și, în caz de eroare, returnează detalii despre eroare, inclusiv poziția și un fragment al textului din jurul erorii.


## 5. Extracția și Curățarea Datelor

Am folosit patternuri pentru a extrage datele din datele JSON și am aplicat ideologii de colectare date, curățarea acestora, eliminând date lipsă sau date irelevante, transformarea datelor, analiza lor pentru a descoperi un tipar:

5.1. **Extracția Numărului Cardului**:
- Am folosit formatul de xxxx xxxxx x.

5.2. **Extracția Numărului, Numele, Inițiala și Prenumele**:
- **5.2.a.** Curățarea Datelor pentru a Păstra Doar Cifrele și Majusculele:
  - Am curățat datele și am afișat inițial numai cifrele și majusculele (mai exact, am înlocuit literele mici cu un șir gol).
  - Funcția folosită: `remove_lowercase`.

- **5.2.b.** Păstrarea Doar a Majusculelor și Cifrelor:
  - Am păstrat doar majusculele, cifrele și spațiile, eliminând orice altceva.
  - Funcția folosită: `keep_uppercase_and_numbers`.

- **5.2.c.** Identificarea Celui Mai Repetitiv Cuvânt:
  - Am căutat cel mai repetitiv cuvânt și l-am considerat nume de familie (am combinat textele într-un șir de caractere, am găsit toate cuvintele de cel puțin 4 caractere, am contorizat aparițiile fiecărui cuvânt și l-am returnat).
  - Funcția folosită: `most_common_word`.

- **5.2.d.** Separarea și Repoziționarea Numele de Familie:
  - Am separat numele de familie de restul caracterelor și l-am poziționat la sfârșit (împărțind textul în părți bazate pe cel mai comun cuvânt, apoi recompunând textul și afișând numele de familie la final).
  - Funcția folosită: `separate_common_word`.

- **5.2.e.** Crearea unui Pattern Regex pentru Extracția Datelor într-un Format Specific:
  - Am creat un pattern regex pentru a extrage datele într-un format specific: nr firstname initial lastname.
  - Funcția folosită: `extract_citizen_data`.

- **5.2.f.** Preluarea Celui Mai Frecvent Nume pentru Fiecare Număr:
  - Am preluat după fiecare număr (index) cel mai frecvent nume, pentru a nu afișa și anumite derivate ale datelor care ar respecta într-un fel condiția de mai sus.
  - Funcția folosită: `most_common_per_number`.

- **5.2.g.** Ștergerea Spațiilor Goale de După Sfârșitul Numele Utilizatorului:
  - Am utilizat o funcție pentru a șterge spațiile goale de după sfârșitul numelui utilizatorului.
  - Funcția folosită: `clean_user_name`.

- **5.2.h.** Extracția și Păstrarea Textelor care Conțin Cel Mai Frecvent Nume pentru Fiecare Număr:
  - Am utilizat funcțiile de mai sus pentru a extrage și păstra doar textele care conțin cel mai frecvent nume pentru fiecare număr.
  - Funcția folosită: `extract_names`.

5.3. **Extracția Datei de Expirare**:
- Am folosit formatul care caută o dată în formatul "mm/yyyy".

## 6. Crearea și Afișarea Interfeței Grafice

- Am creat o interfață grafică folosind Tkinter pentru a permite utilizatorului să încarce un fișier .txt și să vizualizeze datele extrase.
- Am creat un buton pentru încărcarea fișierului și etichete pentru a afișa informațiile relevante.
- Am utilizat un cadru pentru a afișa datele într-un mod structurat și estetic plăcut.

Prin acești pași, am reușit să extrag și să afișez corect datele din fișierul .txt într-un format JSON valid și să le prezint într-o interfață grafică ușor de utilizat.
