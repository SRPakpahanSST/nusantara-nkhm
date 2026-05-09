import os
import json

base_path = "/storage/emulated/0/PIDI/AppNkhm/soal_mentah"
output_file = "/storage/emulated/0/PIDI/AppNkhm/questions.py"

all_questions = []

# Mapping folder ke nama file JSON yang dihasilkan (satu file per folder)
file_mapping = {
    "IQ": "iq_1.json",
    "EQ": "eq_1.json",
    "SQ": "sq_1.json",
    "AQ": "aq_1.json",
    "Nasionalisme": "nasional_1.json"
}

for folder, filename in file_mapping.items():
    filepath = os.path.join(base_path, folder, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File tidak ditemukan: {filepath}")
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            print(f"❌ Skip {filepath}: bukan array/list")
            continue
        # Validasi setiap soal minimal punya field yang diperlukan
        for soal in data:
            if not all(k in soal for k in ["text", "options", "correct", "type", "national"]):
                print(f"⚠️ Soal dalam {filepath} tidak lengkap, diskip")
                continue
            all_questions.append(soal)
        print(f"✅ Membaca {len(data)} soal dari {folder}")
    except Exception as e:
        print(f"❌ Error membaca {filepath}: {e}")

# Tulis ke questions.py
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("QUESTION_BANK = [\n")
    for q in all_questions:
        f.write("    {\n")
        f.write(f'        "text": {json.dumps(q["text"])},\n')
        f.write(f'        "options": {json.dumps(q["options"])},\n')
        f.write(f'        "correct": {json.dumps(q["correct"])},\n')
        f.write(f'        "type": "{q["type"]}",\n')
        national_str = "True" if q["national"] else "False"
        f.write(f'        "national": {national_str}\n')
        f.write("    },\n")
    f.write("]\n")

print(f"\n✅ SELESAI: {len(all_questions)} soal total digabung ke {output_file}")
