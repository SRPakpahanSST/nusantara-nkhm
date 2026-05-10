import os
import json

# Path folder sumber JSON (soal mentah) dan file output
base_path = "/storage/emulated/0/PIDI/AppNkhm/soal_mentah"
output_file = "/storage/emulated/0/PIDI/AppNkhm/questions.py"

# Mapping folder ke nama file JSON (sesuai generate_soal.py)
file_mapping = {
    "IQ": "iq_1.json",
    "EQ": "eq_1.json",
    "SQ": "sq_1.json",
    "AQ": "aq_1.json",
    "Nasionalisme": "nasionalisme_1.json"
}

all_questions = []

# Baca semua file JSON
for folder, filename in file_mapping.items():
    filepath = os.path.join(base_path, folder, filename)
    if not os.path.exists(filepath):
        print(f"⚠️ File tidak ditemukan: {filepath}")
        continue
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if isinstance(data, list):
            all_questions.extend(data)
            print(f"✅ Membaca {len(data)} soal dari {folder}")
        else:
            print(f"❌ File {filepath} bukan list/array, diabaikan")
    except Exception as e:
        print(f"❌ Error baca {filepath}: {e}")

# Validasi dan konversi tiap soal
valid_questions = []
for q in all_questions:
    # Cek field wajib
    required = ["text", "options", "correct", "type", "national"]
    if not all(k in q for k in required):
        print(f"⚠️ Soal tidak lengkap: {q.get('text', '')[:50]}... diabaikan")
        continue

    # Konversi national ke boolean Python (True/False)
    if isinstance(q["national"], bool):
        pass  # sudah benar
    elif isinstance(q["national"], str):
        q["national"] = q["national"].lower() == "true"
    else:
        q["national"] = bool(q["national"])

    # Opsional: pastikan options adalah list
    if not isinstance(q["options"], list):
        print(f"⚠️ Options bukan list pada soal: {q['text'][:50]}, diabaikan")
        continue

    valid_questions.append(q)

# Tulis ke questions.py dengan format aman
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("# -*- coding: utf-8 -*-\n")
    f.write("# Auto-generated question bank. Do not edit manually.\n")
    f.write("# Dibuat oleh gabung_soal.py\n\n")
    f.write("QUESTION_BANK = [\n")
    for q in valid_questions:
        f.write("    {\n")
        f.write(f'        "text": {json.dumps(q["text"])},\n')
        f.write(f'        "options": {json.dumps(q["options"])},\n')
        f.write(f'        "correct": {json.dumps(q["correct"])},\n')
        f.write(f'        "type": "{q["type"]}",\n')
        # Boolean Python ditulis tanpa tanda kutip
        f.write(f'        "national": {q["national"]}\n')
        f.write("    },\n")
    f.write("]\n")

print(f"\n✅ SELESAI: {len(valid_questions)} soal valid digabung ke {output_file}")
