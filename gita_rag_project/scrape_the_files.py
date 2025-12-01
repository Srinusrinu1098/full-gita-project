import requests
import os

# chapter → number of shlokas
shloka_counts = {
    1: 47,
    2: 72,
    3: 43,
    4: 42,
    5: 29,
    6: 47,
    7: 30,
    8: 28,
    9: 34,
    10: 42,
    11: 55,
    12: 20,
    13: 35,
    14: 27,
    15: 20,
    16: 24,
    17: 28,
    18: 78
}

base_dir = "bhagavad_gita"
os.makedirs(base_dir, exist_ok=True)


for chapter, count in shloka_counts.items():
    chapter_folder = os.path.join(base_dir, f"chapter_{chapter}")
    os.makedirs(chapter_folder, exist_ok=True)
    
    # create files or subfolders for shlokas
    for shloka in range(1, count + 1):
        
        base_url = f"https://www.gitasupersite.iitk.ac.in/srimad?language=dv&field_chapter_value={chapter}&field_nsutra_value={shloka}&etsiva=1&choose=1"
        with open(f"{base_dir}/chapter_{chapter}/shloka_{shloka}.html","w",encoding="utf-8") as f:
            data = requests.get(base_url)
            f.write(data.text)
            print(f"sucessfully created and added html chapter_{chapter}/shloka_{shloka}.html")
    print(f"completed bhagavad_gita {chapter}st chapter and {count} shlokas")
        

print("✅ Chapters and shloka files created successfully!")


       