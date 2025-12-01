from bs4 import BeautifulSoup
import json
import requests
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
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


chunked = []



def inference_embeddings(promt):
    embedding = requests.post("http://localhost:11434/api/embed"
,json={
        "model" : "llama3.2",
        "input" : promt,
        
    })
    result = embedding.json()
    return result["embeddings"][0]


for chapter, count in shloka_counts.items():
      for shloka_num in range(1, count + 1):
        with open(f"bhagavad_gita/chapter_{chapter}/shloka_{shloka_num}.html",encoding="utf-8") as f:

                content = f.read()
                soup = BeautifulSoup(content,"html.parser")
                shloka = soup.select_one("div.view-content").select_one("p").text[:-9].replace("\n\n"," ")
                translutation = soup.select_one("div.attachment").select_one("p").text[5:].replace("\n\n"," ")   
                sloka_iast = transliterate(shloka, sanscript.DEVANAGARI, sanscript.IAST)
                with open(f"gita.json","r",encoding="utf-8") as f:
                        content = json.load(f)
        
                        embeddings = inference_embeddings([chunk["translutation"] for chunk in content])
                        for i,chunk in enumerate(content):
                               chunked.append({"chapter_number":chapter,"shloka_number":shloka_num,"shloka":shloka,"translutation":translutation,"sloka_iast":sloka_iast,"embeddings":embeddings[i]})
                               with open(f"gita.json", "w", encoding="utf-8") as f:
                                        
                                        json.dump(chunked, f, indent=4, ensure_ascii=False)
                                        print(f"my job is done with chapter_{chapter},shloka_{shloka_num}")


        

        
        



        