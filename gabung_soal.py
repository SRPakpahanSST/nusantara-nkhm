import os
import json

base_path = "/storage/emulated/0/PIDI/AppNkhm/soal_mentah"
output_file = "/storage/emulated/0/PIDI/AppNkhm/questions.py"

all_questions = []

if not os.path.exists(base_path):
    print(f"ERROR: Folder {base_path} tidak ditemukan.")
else:
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                print(f"Memproses: {filepath}")
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    parent_folder = os.path.basename(root)
                    if 'type' not in data or not data['type']:
                        if parent_folder in ['IQ','EQ','SQ','AQ']:
                            data['type'] = parent_folder
                        else:
                            data['type'] = 'IQ'
                    if parent_folder == 'Nasionalisme':
                        data['national'] = True
                    elif 'national' not in data:
                        data['national'] = False
                    required = ["text", "options", "correct"]
                    if not all(k in data for k in required):
                        print(f"  ❌ Skip {file}: field tidak lengkap")
                        continue
                    all_questions.append(data)
                    print(f"  ✅ Loaded: {file} (type={data['type']}, national={data['national']})")
                except Exception as e:
                    print(f"  ❌ Error {file}: {e}")

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

print(f"\n✅ SELESAI: {len(all_questions)} soal digabung ke {output_file}")
