from flask import Flask,request
from youtube_transcript_api import YouTubeTranscriptApi as yta

import spacy
import pytextrank

app = Flask(__name__)

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

    finalsum = ""

    for sent in doc._.textrank.summary(limit_sentences=nosen):
        finalsum += sent.text

    return finalsum

if __name__ == '__main__':
    app.run()