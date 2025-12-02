from flask import Flask, request, jsonify
import requests
import json
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()



client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Load Bhagavad Gita chunks once at startup
def load_gita():
    with open("bhagavad_gita_new.json", "r", encoding="utf-8") as f:
        print("loaded")
        return json.load(f)

gita_chunks = load_gita()
   

app = Flask(__name__)
CORS(app)
# ---- LLM and Embedding Inference ----
def inference_final_llm(prompt):
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["TEXT"]
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.candidates and chunk.candidates[0].content:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    response_text += part.text

    return response_text



def inference_embeddings(text):
  
    
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text)

    # This returns the vector: response.embedding.values
    embedding_vector = result.embeddings[0].values
   
    return embedding_vector


    
    


  

def get_emotions_from_text(user_text):
    
    prompt = f"""
Take the text below and classify it into 1–3 emotions from this list:
["sadness", "fear", "peace", "happiness", "motivation", "anger", "wisdom"].

Text: "{user_text}"

Return JSON strictly in this format:
{{"tags": ["happiness", "peace"]}}
"""
    contents = [
        types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        )
    ]

    generate_content_config = types.GenerateContentConfig(
        response_modalities=["TEXT"]
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=contents,
        config=generate_content_config,
    ):
        if chunk.candidates and chunk.candidates[0].content:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    response_text += part.text

    

    try:
        
        return json.loads(response_text)
    except:
        return {"tags": ["wisdom"]}  # fallback


# ---- API Endpoint ----
@app.route("/get_gita_wisdom", methods=["POST"])
def get_gita_wisdom():
    try:
        data = request.json
        
        user_text = data.get("text", "")
        print(user_text)

        if not user_text:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        # Step 1: Get emotion tags
        user_tags = get_emotions_from_text(user_text)
        print(user_tags)
        
        # Step 2: Get embeddings
        user_embed = inference_embeddings(user_text)
        print(user_embed)
    
        # Step 3: Filter matching chunks
        matching_chunks = [
            c for c in gita_chunks if any(tag in c["emotions"] for tag in user_tags["tags"])
        ]

        if not matching_chunks:
            return jsonify({"error": "No matching shlokas found"}), 404

        df = pd.DataFrame.from_records(matching_chunks)
        print(df)

        # Step 4: Cosine similarity
        similarities = cosine_similarity(np.vstack(df["embeddings"]), [user_embed]).flatten()
        top_indices = similarities.argsort()[::-1][:3]
        retrieved_chunks = df.loc[top_indices]

        # Step 5: Final LLM prompt
        final_llm_prompt = f'''
You are a motivational and friendly guide who explains the wisdom of the Bhagavad Gita in a natural, simple way dont give a large text just 4-5 lines with highly motivation mention the chapter with shloka_iast.  

The user has shared their feelings or question:  
"{user_text}"  

Your task is to respond to the user with an uplifting explanation using the following retrieved shlokas:  
{retrieved_chunks.to_dict(orient="records")}  

Guidelines:  
- Speak in plain, easy-to-understand English.  
- Directly address the user’s question or feelings with care and empathy.  
- Be warm, friendly, and encouraging, like a personal mentor.  
- Use a motivational tone, reminding the user of hope, strength, and wisdom.  
- Add a few relevant emojis (✨🙏💪🌸😊🔥).  
- Never just repeat the shloka—explain its meaning in a practical, relatable way.  
- Keep the explanation short, clear, and impactful.  
- Always keep the explanation respectful because this is a devotional project.  
'''

        final_result = inference_final_llm(final_llm_prompt)
        

        return jsonify({
            "user_text": user_text,
            "tags": user_tags["tags"],
            "response": final_result
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/")
def live():
    return "app is live"    


if __name__ == "__main__":
    app.run(debug=True)
