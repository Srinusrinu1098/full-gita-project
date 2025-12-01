import requests
import json
import pandas as pd
import joblib



def inference(promt):
    embedding = requests.post("http://localhost:11434/api/generate"
,json={
        "model" : "llama3.2",
        "prompt" : promt,
        "stream":False
    })
    result = embedding.json()
    res_len = len(json.loads(result["response"])["tags"])
    
    if(res_len < 1):
        print(f"it returned length {res_len}")
        return inference(promt)
    return result["response"]

chunked = []




# result = inference(text)
# parsed = json.loads(result)
# print(parsed["tags"])
count = 500
with open(f"gita.json","r",encoding="utf-8") as f:
        original = json.load(f)[500:]
        

        
            
        for chunk in original:
                 
            
            text = f"""
                    
    You are an assistant that classifies a Bhagavad Gita sloka into one or more emotional/mood categories.

    Sloka: {chunk["shloka"]}

    Choose all relevant tags from this list: ["sadness", "fear", "peace", "happiness", "motivation", "anger", "wisdom"].  

    Return strictly in JSON format like: {{"tags": ["motivation", "peace","wisdom"]}}.
    """
            result = inference(text)
            parsed = json.loads(result)
                
                
            chunked.append({**chunk,"emotions":parsed["tags"],"embeddings":chunk["embeddings"]})
            with open("gita2.json","w",encoding="utf-8") as out:
                json.dump( chunked,out, ensure_ascii=False, indent=4)
            print(count)
            count+=1

            
                    
                    
                
            

                
    #             # df = pd.DataFrame.from_records(content)
                
            