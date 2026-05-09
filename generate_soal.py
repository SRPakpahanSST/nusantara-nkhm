import os
import json
import random

BASE = "/storage/emulated/0/PIDI/AppNkhm/soal_mentah"

# ---------- Data untuk variasi soal ----------
# IQ (fokus pengetahuan umum & nasional)
iq_questions = [
    ("Siapa presiden pertama Indonesia?", "Soekarno", ["Soekarno", "Soeharto", "Habibie", "Megawati"]),
    ("Apa ibu kota Jawa Barat?", "Bandung", ["Bandung", "Surabaya", "Semarang", "Medan"]),
    ("Siapa pencipta lagu Indonesia Raya?", "WR Supratman", ["WR Supratman", "Ibu Sud", "Ismail Marzuki", "AT Mahmud"]),
    ("Apa lambang negara Indonesia?", "Garuda Pancasila", ["Garuda Pancasila", "Banteng", "Padi Kapas", "Bintang"]),
    ("Gunung tertinggi di Indonesia?", "Puncak Jaya", ["Puncak Jaya", "Kerinci", "Rinjani", "Semeru"]),
]
# EQ
eq_questions = [
    ("Temanmu gagal ujian dan menangis. Apa yang kamu lakukan?", "Menghibur dan memberi semangat", ["Biarkan saja", "Menghibur dan memberi semangat", "Membandingkan nilaimu", "Tegur dia"]),
    ("Kamu tidak sengaja menyinggung perasaan teman. Tindakan terbaik?", "Meminta maaf", ["Diam saja", "Meminta maaf", "Berpura-pura tidak tahu", "Menyalahkan dia"]),
    ("Melihat orang tua kesulitan menyeberang, sebaiknya?", "Membantunya", ["Pura tidak lihat", "Membantunya", "Merekam video", "Tertawa"]),
    ("Temanmu sedang berduka karena orang tua meninggal. Sikapmu?", "Ikut berduka dan mendampingi", ["Ikut berduka", "Bilang 'ikhlas'", "Bilang 'sudah takdir'", "Diam saja"]),
]
# SQ
sq_questions = [
    ("Sila pertama Pancasila adalah?", "Ketuhanan Yang Maha Esa", ["Ketuhanan", "Kemanusiaan", "Persatuan", "Kerakyatan"]),
    ("Bhinneka Tunggal Ika berarti?", "Berbeda-beda tetap satu", ["Berbeda-beda tetap satu", "Satu untuk semua", "Bersatu kita teguh", "Damai sejahtera"]),
    ("Sikap terhadap teman yang berbeda agama adalah?", "Menghormati", ["Menghormati", "Memaksa", "Menghina", "Menjauhi"]),
]
# AQ
aq_questions = [
    ("Kamu gagal dalam ujian. Sikap terbaik?", "Belajar lebih giat", ["Menyerah", "Belajar lebih giat", "Menyalahkan guru", "Tidak mau ujian lagi"]),
    ("Proyek kelompok macet, sebaiknya?", "Diskusi cari solusi", ["Keluar kelompok", "Diskusi cari solusi", "Diam saja", "Menyalahkan teman"]),
    ("Kamu ditolak dalam seleksi organisasi. Sikapmu?", "Mencoba lagi", ["Menyerah", "Mencoba lagi", "Menyalahkan panitia", "Iri pada yang lolos"]),
]

def generate_category(folder_name, questions_list, target_count, default_type, is_national=False):
    folder_path = os.path.join(BASE, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    all_soal = []
    for i in range(target_count):
        # Pilih template secara acak (bisa berulang)
        template = random.choice(questions_list)
        text, correct, options = template[0], template[1], template[2]
        soal = {
            "text": text,
            "options": options,
            "correct": correct,
            "type": default_type,
            "national": is_national
        }
        all_soal.append(soal)
    
    # Simpan dalam satu file JSON
    file_name = f"{folder_name.lower()}_1.json"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(all_soal, f, indent=2, ensure_ascii=False)
    print(f"✅ {target_count} soal {folder_name} -> {file_path}")

# Generate masing-masing kategori
generate_category("IQ", iq_questions, 160, "IQ", is_national=False)
generate_category("EQ", eq_questions, 195, "EQ", is_national=False)
generate_category("SQ", sq_questions, 70, "SQ", is_national=False)
generate_category("AQ", aq_questions, 70, "AQ", is_national=False)

# Untuk Nasionalisme: kita gunakan soal dari IQ/EQ/SQ/AQ yang bertema nasional (tapi kita buat sendiri)
nasional_questions = [
    ("Siapa yang membacakan teks proklamasi?", "Soekarno-Hatta", ["Soekarno", "Moh Hatta", "Soekarno-Hatta", "Ahmad Soebarjo"]),
    ("Hari Pahlawan diperingati setiap?", "10 November", ["10 November", "17 Agustus", "28 Oktober", "1 Juni"]),
    ("Sumpah Pemuda diikrarkan pada tahun?", "1928", ["1928", "1945", "1908", "1930"]),
    ("Lagu 'Indonesia Raya' pertama kali dikumandangkan pada?", "28 Oktober 1928", ["28 Oktober 1928", "17 Agustus 1945", "1 Juni 1945", "10 November 1945"]),
    ("Pahlawan yang dijuluk 'Singa dari Timur'?", "Pattimura", ["Pattimura", "Diponegoro", "Imam Bonjol", "Hasanuddin"]),
]
# Nasionalisme: campur tipe (IQ/EQ/SQ/AQ)
folder_nas = os.path.join(BASE, "Nasionalisme")
os.makedirs(folder_nas, exist_ok=True)
nasional_soal_list = []
for i in range(100):
    template = random.choice(nasional_questions)
    text, correct, options = template[0], template[1], template[2]
    # Tipe dipilih acak antara IQ, EQ, SQ, AQ
    tipe = random.choice(["IQ", "EQ", "SQ", "AQ"])
    soal = {
        "text": text,
        "options": options,
        "correct": correct,
        "type": tipe,
        "national": True
    }
    nasional_soal_list.append(soal)

file_nas = os.path.join(folder_nas, "nasionalisme_1.json")
with open(file_nas, 'w', encoding='utf-8') as f:
    json.dump(nasional_soal_list, f, indent=2, ensure_ascii=False)
print(f"✅ 100 soal Nasionalisme -> {file_nas}")

print("\n🎉 SEMUA FILE JSON BERHASIL DIBUAT!")
