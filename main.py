import json
import re
import tkinter as tk
from tkinter import filedialog
from collections import Counter, defaultdict

# functiile pentru a face jsonul valid
    #prin value.strip() am eliminat spatiile de la inceputul si sfarsitul textului
def clean_text_value(value):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value
    return '"' + value.replace('"', '') + '"'

def convert_tags_to_json(text):
    text = re.sub(r'(?<!")(\w+)(?=:)', r'"\1"', text)
    
        # am folosit o functie pentru a adauga ghilimele
    def add_quotes_to_text_value(match):
        value = match.group(1).strip()
        return f'"text": {clean_text_value(value)}'
    
        # am pus intre ghilimele tot ce se afla intra "text": si , "boundingBox"  
    text = re.sub(r'"text":\s*([^,}]+?)(?=,\s*"boundingBox")', add_quotes_to_text_value, text)

        # am folosit o functie pentru a elimina ghilimelele extra, daca exista intre cuvinte
    # def remove_extra_quotes(text):
    #     text = re.sub(r'(?<!")"([^"]*)"(?!")', r'"\1"', text)
    #     return text
    
    # text = remove_extra_quotes(text)
    return text

    # verificam mereu daca apar erori, unde apar acele erori si ce erori sunt
def validate_json(text):
    try:
        json_data = json.loads(text)
        return json_data
    except json.JSONDecodeError as e:
        error_pos = e.pos
        snippet_start = max(0, error_pos - 50)
        snippet_end = min(len(text), error_pos + 50)
        error_snippet = text[snippet_start:snippet_end]

        return {
            "error": f"JSONDecodeError: {e}",
            "snippet": error_snippet,
            "message": str(e),
            "position": error_pos
        }

# pentru a fi mai fiabil si mai optimizat programul, vom prelua numai partea care ne intereseaza, anume "text":
def extract_text(json_data):
    texts = []
    for item in json_data:
        if 'text' in item:
            texts.append(item['text'])
    return texts

# expresie regulata pentru extragere cardNumber (am folosit ca pattern: xxxx xxxxx x)
def extract_card_number(texts):
    pattern = r'\b(\d{4} \d{5} \d)\b'
    card_numbers = []
    for text in texts:
        card_numbers.extend(re.findall(pattern, text))
    if card_numbers:
        return "\n".join(card_numbers)  
    else:
        return "No Card Number date found"

# inceput expresie regulata pentru extragere nume
    # am indepartat caracterele cu lowercase, deoarece am observat ca numele sunt cu uppercase
def remove_lowercase(text):
    return re.sub(r'[a-z]', '', text)

    # am pastrat caracterele cu uppercase
def keep_uppercase_and_numbers(text):
    return re.sub(r'[^A-Z0-9 ]', '', text)

    # am cautat cel mai comun si lung cuvant de minim 4 litere pentru a-l considera numele de familie (lastName)
def most_common_word(texts):
    combined_text = ' '.join(texts)
    words = re.findall(r'\b[A-Z0-9]{4,}\b', combined_text)
    word_counts = Counter(words)
    most_common = word_counts.most_common(1)
    return most_common[0][0] if most_common else None

    # am separat numele de familie (cel mai comun cuvant) de restul caracterelor si l-am pozitionat la sfarsit
def separate_common_word(texts, common_word):
    separated_texts = []
    for text in texts:
        processed_text = keep_uppercase_and_numbers(remove_lowercase(text))
        if common_word in processed_text:
            parts = processed_text.split(common_word)
            separated_text = parts + [common_word]
            separated_texts.append(' '.join(separated_text))
    return separated_texts

    # acum facem o filtrare pentru a extrage datele intr-un format de genul: nr firstname initial lastname (pentru lastname ne folosim de cel mai comun cuvant)
def extract_citizen_data(texts, common_word):
    data_with_regex = []
    pattern = re.compile(r'^(\d+)\s+([A-Z]+)\s+([A-Z])\s+{}\s*$'.format(re.escape(common_word)))
    pattern_lipsit = re.compile(r'^(\d+)([A-Z]+)\s+([A-Z])\s+{}\s*$'.format(re.escape(common_word)))

    for text in texts:
        cleaned_text = keep_uppercase_and_numbers(remove_lowercase(text))
        
        match = pattern.match(cleaned_text)
        if match:
            data_with_regex.append(match.groups())
        else:
            match_lipsit = pattern_lipsit.match(cleaned_text)
            if match_lipsit:
                num, firstname_initial, initial = match_lipsit.groups()
                num = num
                firstname = ''.join(re.findall(r'[A-Z]+', firstname_initial))
                data_with_regex.append((num, firstname, initial))
    
    formatted_data = set(f"{num} {firstname} {initial} {common_word}" for num, firstname, initial in data_with_regex)
    
    return list(formatted_data)

    # acum am preluat dupa fiecare nr (index) cel mai frecvent nume, pentru a nu afisa si anumite derivate ale datelor care ar respecta intr-un fel conditia de mai sus
def most_common_per_number(texts, common_word):
    grouped_data = defaultdict(list)
    
    for text in texts:
        cleaned_text = keep_uppercase_and_numbers(remove_lowercase(text))
        pattern = rf'^(\d+)\s+([A-Z ]+)\s+([A-Z])\s+{re.escape(common_word)}$'
        match = re.match(pattern, cleaned_text)
        if match:
            num, name, initial = match.groups()
            grouped_data[num].append(f"{name.strip()} {initial} {common_word}")
    
    common_names = {}
    for num, names in grouped_data.items():
        name_counts = Counter(names)
        most_common_name = name_counts.most_common(1)[0][0]
        common_names[num] = most_common_name
    
    return common_names

    # am utilizat o functie pentru a sterge spatiile goale de dupa sfarsitul numelui utilizatorului
def clean_user_name(user_name):
    return re.sub(r'\s+$', '', user_name)

    # am utilizat functiile de mai sus pentru a extrage si pastra doar textele care contin cel mai frecvent nume pentru fiecare numar
def extract_names(texts):
    common_word = most_common_word(texts)
    citizen_data = extract_citizen_data(texts, common_word)
    
    most_common_names = most_common_per_number(citizen_data, common_word)
    
    sorted_results = sorted(most_common_names.items(), key=lambda x: int(x[0]))
    
    max_length = max(len(f"{num} {name}") for num, name in sorted_results)
    
    formatted_result = [f"{num} {name}".ljust(max_length) for num, name in sorted_results]

    cleaned_result = [clean_user_name(name) for name in formatted_result]
    
    return cleaned_result

# expresie regulata pentru a prelua data de validitate din text(am cautat ca pattern: dd/yyyy)
def extract_valid_to(texts):
    pattern = r'\b(\d{2}/\d{4})\b'
    valid_to_dates = []
    for text in texts:
        valid_to_dates.extend(re.findall(pattern, text))
    if valid_to_dates:
         return valid_to_dates[0]
    else:
        return "No VALID TO date found"


# GUI Functions
def upload_file():
    # Deschide un dialog de fisiere pentru a selecta un fisier text
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    
    # Verifica daca a fost selectat un fisier
    if file_path:
        try:
            # Deschide fisierul selectat si citeste continutul sau
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                text = file.read()
                
                # Conversia textului într-un format JSON valid dupa functiile create mai sus
                fixed_text = convert_tags_to_json(text)
                
                # Validarea textului JSON dupa functia creata mai sus 
                json_result = validate_json(fixed_text)
                
                # Daca exista o eroare în JSON, afiseaza mesajul de eroare si opreste functia
                if isinstance(json_result, dict) and "error" in json_result:
                    print("Error in JSON:", json_result["message"])
                    display_result("", [], "No VALID TO date found")
                    return
                
                # Extrage textele din JSON
                filtered_texts = extract_text(json_result)

                # Extrage numerele de card din textele filtrate
                card_numbers = extract_card_number(filtered_texts)
                
                # Extrage numele din textele filtrate
                users = extract_names(filtered_texts)
                
                # Extrage data de validitate din textele filtrate
                valid_to_date = extract_valid_to(filtered_texts)
                
                # Creeaza un dictionar cu rezultatele extrase conform modelului din cerinta: {cardNumber: 0000 00000 0, users: [1 FirstName MiddleNameInitial LastName...], validTo: 00/0000},
                result = {
                    "cardNumber": card_numbers,
                    "users": users,
                    "validTo": valid_to_date,
                }
                
                # Afiseaza datele extrase în consola în format JSON
                print("Extracted Data:")
                print(json.dumps(result, indent=4))
                
                # Afiseaza rezultatele în interfata grafica
                display_result(card_numbers, users, valid_to_date)
                
        except UnicodeDecodeError as e:
            # În cazul unei erori de decodare a caracterelor, afiseaza un mesaj de eroare si opreste functia
            display_result("", [], "No VALID TO date found")
        except Exception as e:
            # În cazul oricarei alte erori, afiseaza un mesaj de eroare generic si opreste functia
            display_result("", [], "No VALID TO date found")

def display_result(card_number, names, valid_to_date):
    global result_frame
    
    upload_button.pack_forget()
    file_type_info.pack_forget()
    
    # Creeaza un cadru principal pentru rezultate
    result_frame = tk.Frame(root, bg='#f0f8ff', bd=0)
    result_frame.pack(expand=True, fill=tk.BOTH, pady=20)
    
    # Creeaza un cadru secundar pentru rezultate, cu fundal verde deschis si margini
    inner_frame = tk.Frame(result_frame, bg='#e0ffe0', bd=10, relief=tk.RAISED)
    inner_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
    
    # Creeaza un cadru pentru numarul de card
    card_number_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    card_number_frame.pack(anchor='center', pady=20)
    
    # Creeaza un label pentru afisarea numarului de card
    card_number_text = tk.Label(card_number_frame, text=card_number, bg='#e0ffe0', font=('Courier New', 40, 'bold'), fg='#333333')
    card_number_text.pack()
    
    # Creeaza un cadru pentru utilizatori 
    users_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    users_frame.pack(anchor='w', padx=10, pady=10)
    
    if names:
        # Foloseste font cu latimi fixe pentru aliniere uniforma
        user_font = ('Courier New', 16)
        
        # Formatam si aliniem fiecare rând în mod uniform
        for name in names:
            parts = name.split()
            num = parts[0] if len(parts) > 0 else ""
            firstname = parts[1] if len(parts) > 1 else ""
            initial = parts[2] if len(parts) > 2 else ""
            citizen = parts[3] if len(parts) > 3 else ""
            
            # Asigura alinierea uniforma a fiecarei coloane
            row_text = f"{num.ljust(5)} {firstname.ljust(15)} {initial.ljust(5)} {citizen.ljust(10)}"
            
            row_label = tk.Label(users_frame, text=row_text, bg='#e0ffe0', font=user_font, anchor='w', fg='#333333')
            row_label.pack(anchor='w')
    else:
        no_names_text = tk.Label(users_frame, text="No names found", bg='#e0ffe0', font=('Courier New', 16), fg='#333333')
        no_names_text.pack()
    
    # Creeaza un cadru pentru data de validitate
    valid_to_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    valid_to_frame.pack(anchor='e', pady=10, padx=10, side=tk.BOTTOM, fill=tk.X)
    
    if valid_to_date:
        valid_to_text = tk.Label(valid_to_frame, text=f"VALID TO {valid_to_date}", bg='#e0ffe0', font=('Courier New', 16), fg='#333333')
    else:
        valid_to_text = tk.Label(valid_to_frame, text="No date found", bg='#e0ffe0', font=('Courier New', 16), fg='#333333')
    
    valid_to_text.pack(anchor='e', padx=(0, 15))

# Initializarea GUI
root = tk.Tk()
root.title("Proiect Zisu Cosmin")
root.geometry("800x600")
root.configure(bg='#f0f8ff')

# Creeaza un cadru principal pentru interfata grafica
frame = tk.Frame(root, bg='#f0f8ff')
frame.pack(expand=True, fill=tk.BOTH)

# Creeaza un buton pentru încarcarea fisierului
upload_button = tk.Button(frame, text="Upload", command=upload_file,
                          bg='#4CAF50', fg='white', font=('Helvetica', 16, 'bold'),
                          relief=tk.RAISED, bd=5, padx=20, pady=10, cursor="hand2")
upload_button.pack(expand=True)

# Creeaza un label pentru a informa utilizatorii despre tipul de fisier acceptat
file_type_info = tk.Label(frame, text="Only .txt files are accepted", bg='#f0f8ff', font=('Helvetica', 12))
file_type_info.pack()

result_frame = tk.Frame(root, bg='#f0f8ff')

root.mainloop()