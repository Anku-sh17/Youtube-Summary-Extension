from flask import Flask,request,jsonify,session
from youtube_transcript_api import YouTubeTranscriptApi as yta
from googletrans import Translator

import spacy
import pytextrank

app = Flask(__name__)
app.secret_key = 'scripter'

@app.route('/settings', methods=['POST'])
def handle_settings():
    data = request.get_json()
    summary_length = data.get('summaryLength')   
    language = data.get('selectedLanguage') 
    print(f"summary length : {summary_length}")
    session['final_length'] = summary_length  # Store summary_length in the session
    session['language'] = language
    print(f"final length : {session['final_length']}")
    return jsonify({"message": "Input received successfully!"}), 200

@app.get('/summary')
def summary_api():
    url = request.args.get('url','')
    video_id = url.split('=')[1]
    summary = get_summary(get_transcript(video_id))
    return summary, 200

def get_transcript(vid_id):
    lang_codes = ['en', 'en-US', 'fr', 'es']

    for lang_code in lang_codes:
        try:
            data = yta.get_transcript(vid_id, languages=[lang_code])
            transcript = ''
            for value in data:
                for key, val in value.items():
                    if key == 'text':
                        transcript += val

            l = transcript.splitlines()
            final_tra = " ".join(l)
            return final_tra
        
        except Exception:
            continue
    return None

def get_summary(final_tra):

    nlp = spacy.load("en_core_web_lg")
    nlp.add_pipe("textrank")
    doc = nlp(final_tra)

    num_sentences = sum(1 for _ in doc.sents)

    nosen = num_sentences//2
    print(f"nosen value at 56 :{nosen}")
    if 'final_length' in session:
        nosen = session['final_length']
        nosen = int(nosen)
        session.pop('final_length', None)
    print(f"nosen value at 59 :{nosen}")

    finalsum = ""

    for sent in doc._.textrank.summary(limit_sentences=nosen):
        finalsum += sent.text

    translated_text = finalsum
    
    if 'language' in session:
        translated_text = translate_text(finalsum,session['language'] )
        session.pop('language', None)

    return translated_text

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

if __name__ == '__main__':
    app.run()