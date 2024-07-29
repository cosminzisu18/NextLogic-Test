import json
import re
import tkinter as tk
from tkinter import filedialog
from collections import Counter, defaultdict

def clean_text_value(value):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        return value
    return '"' + value.replace('"', '') + '"'

def convert_tags_to_json(text):
    text = re.sub(r'(?<!")(\w+)(?=:)', r'"\1"', text)
    text = re.sub(r'"text":\s*([^,}]+?)(?=,\s*"boundingBox")', lambda match: f'"text": {clean_text_value(match.group(1))}', text)
    return text

def validate_json(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        error_pos = e.pos
        snippet_start = max(0, error_pos - 20)
        snippet_end = min(len(text), error_pos + 20)
        error_snippet = text[snippet_start:snippet_end]
        return {
            "error": f"JSONDecodeError: {e}",
            "snippet": error_snippet,
            "message": str(e),
            "position": error_pos
        }

def extract_text(json_data):
    return [item['text'] for item in json_data if 'text' in item]

def extract_card_number(texts):
    pattern = r'\b(\d{4} \d{5} \d)\b'
    card_numbers = [match for text in texts for match in re.findall(pattern, text)]
    return "\n".join(card_numbers) if card_numbers else None

def clean_text(text):
    return re.sub(r'[a-z]', '', text)

def most_common_word(texts):
    combined_text = ' '.join(texts)
    words = re.findall(r'\b[A-Z0-9]{4,}\b', combined_text)
    return Counter(words).most_common(1)[0][0] if words else None

def extract_citizen_data(texts, common_word):
    data_with_regex = []
    pattern = re.compile(r'^(\d+)\s+([A-Z]+)\s+([A-Z])\s+{}\s*$'.format(re.escape(common_word)))
    pattern_lipsit = re.compile(r'^(\d+)([A-Z]+)\s+([A-Z])\s+{}\s*$'.format(re.escape(common_word)))

    for text in texts:
        cleaned_text = clean_text(text)
        match = pattern.match(cleaned_text)
        if match:
            data_with_regex.append(match.groups())
        else:
            match_lipsit = pattern_lipsit.match(cleaned_text)
            if match_lipsit:
                num, firstname_initial, initial = match_lipsit.groups()
                firstname = ''.join(re.findall(r'[A-Z]+', firstname_initial))
                data_with_regex.append((num, firstname, initial))

    formatted_data = set(f"{num} {firstname} {initial} {common_word}" for num, firstname, initial in data_with_regex)
    return list(formatted_data)

def most_common_per_number(texts, common_word):
    grouped_data = defaultdict(list)
    pattern = re.compile(rf'^(\d+)\s+([A-Z ]+)\s+([A-Z])\s+{re.escape(common_word)}$')

    for text in texts:
        cleaned_text = clean_text(text)
        match = pattern.match(cleaned_text)
        if match:
            num, name, initial = match.groups()
            grouped_data[num].append(f"{name.strip()} {initial} {common_word}")

    common_names = {num: Counter(names).most_common(1)[0][0] for num, names in grouped_data.items()}
    return common_names

def clean_user_name(user_name):
    return user_name.rstrip()

def extract_names(texts):
    common_word = most_common_word(texts)
    citizen_data = extract_citizen_data(texts, common_word)
    most_common_names = most_common_per_number(citizen_data, common_word)
    sorted_results = sorted(most_common_names.items(), key=lambda x: int(x[0]))
    formatted_result = [f"{num} {name}" for num, name in sorted_results]
    cleaned_result = [clean_user_name(name) for name in formatted_result]
    return cleaned_result if cleaned_result else None

def extract_valid_to(texts):
    pattern = r'\b(\d{2}/\d{4})\b'
    valid_to_dates = [match for text in texts for match in re.findall(pattern, text)]
    return valid_to_dates[0] if valid_to_dates else None

def upload_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                text = file.read()
                fixed_text = convert_tags_to_json(text)
                json_result = validate_json(fixed_text)
                if isinstance(json_result, dict) and "error" in json_result:
                    print("Error in JSON:", json_result["message"])
                    display_result("", [], "No VALID TO date found")
                    return

                filtered_texts = extract_text(json_result)
                card_numbers = extract_card_number(filtered_texts)
                users = extract_names(filtered_texts)
                valid_to_date = extract_valid_to(filtered_texts)
                
                result = {
                    "cardNumber": card_numbers,
                    "users": users,
                    "validTo": valid_to_date,
                }

                print("Extracted Data:")
                print(json.dumps(result, indent=4))
                
                display_result(card_numbers, users, valid_to_date)
                
        except UnicodeDecodeError as e:
            display_result("", [], "No VALID TO date found")
        except Exception as e:
            display_result("", [], "No VALID TO date found")

def display_result(card_number, names, valid_to_date):
    global result_frame
    
    upload_button.pack_forget()
    file_type_info.pack_forget()
    
    result_frame = tk.Frame(root, bg='#f0f8ff', bd=0)
    result_frame.pack(expand=True, fill=tk.BOTH, pady=20)
    
    inner_frame = tk.Frame(result_frame, bg='#e0ffe0', bd=10, relief=tk.RAISED)
    inner_frame.pack(expand=True, fill=tk.BOTH, padx=30, pady=30)
    
    card_number_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    card_number_frame.pack(anchor='center', pady=20)
    
    card_number_text = tk.Label(card_number_frame, text=card_number or "No card number found", bg='#e0ffe0', font=('Courier New', 40, 'bold'), fg='#333333')
    card_number_text.pack()
    
    users_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    users_frame.pack(anchor='w', padx=10, pady=10)
    
    if names:
        user_font = ('Courier New', 16)
        for name in names:
            parts = name.split()
            row_text = f"{parts[0].ljust(5)} {parts[1].ljust(15)} {parts[2].ljust(5)} {parts[3].ljust(10)}"
            row_label = tk.Label(users_frame, text=row_text, bg='#e0ffe0', font=user_font, anchor='w', fg='#333333')
            row_label.pack(anchor='w')
    else:
        no_names_text = tk.Label(users_frame, text="No names found", bg='#e0ffe0', font=('Courier New', 16), fg='#333333')
        no_names_text.pack()
    
    valid_to_frame = tk.Frame(inner_frame, bg='#e0ffe0')
    valid_to_frame.pack(anchor='e', pady=10, padx=10, side=tk.BOTTOM, fill=tk.X)
    
    valid_to_text = tk.Label(valid_to_frame, text=f"VALID TO {valid_to_date}" if valid_to_date else "No date found", bg='#e0ffe0', font=('Courier New', 16), fg='#333333')
    valid_to_text.pack(anchor='e', padx=(0, 15))

root = tk.Tk()
root.title("Proiect Zisu Cosmin")
root.geometry("800x600")
root.configure(bg='#f0f8ff')

frame = tk.Frame(root, bg='#f0f8ff')
frame.pack(expand=True, fill=tk.BOTH)

upload_button = tk.Button(frame, text="Upload", command=upload_file,
                          bg='#4CAF50', fg='white', font=('Helvetica', 16, 'bold'),
                          relief=tk.RAISED, bd=5, padx=20, pady=10, cursor="hand2")
upload_button.pack(expand=True)

file_type_info = tk.Label(frame, text="Only .txt files are accepted", bg='#f0f8ff', font=('Helvetica', 12))
file_type_info.pack()

result_frame = tk.Frame(root, bg='#f0f8ff')

root.mainloop()
