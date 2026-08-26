# -*- coding: utf-8 -*-
import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from gtts import gTTS

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "audio", "phrases")
os.makedirs(OUT, exist_ok=True)

LANG_MAP = {"EN": "en", "FR": "fr", "ES": "es", "DE": "de"}

phrases = {
    "room": {
        "EN": ["This is a pen.", "It is blue.", "I write with it."],
        "FR": [u"C'est un stylo.", u"Il est bleu.", u"J'\u00e9cris avec."],
        "ES": [u"Es un bol\u00edgrafo.", u"Es azul.", u"Escribo con \u00e9l."],
        "DE": [u"Das ist ein Stift.", u"Er ist blau.", u"Ich schreibe damit."],
    },
    "kitchen": {
        "EN": ["This is an apple.", "It is sweet.", "I can make juice."],
        "FR": [u"C'est une pomme.", u"Elle est douce.", u"Je peux faire du jus."],
        "ES": [u"Es una manzana.", u"Es dulce.", u"Puedo hacer jugo."],
        "DE": [u"Das ist ein Apfel.", u"Er ist s\u00fc\u00df.", u"Ich kann Saft machen."],
    },
    "disaster": {
        "EN": ["Earthquake! Drop, cover, and hold on!", "Fire! Stop, drop, and roll!", "Help! I need help!"],
        "FR": [u"Tremblement de terre! Couvrez-vous!", u"Au feu! Couchez-vous et roulez!", u"Au secours! J'ai besoin d'aide!"],
        "ES": [u"\u00a1Terremoto! \u00a1Ag\u00e1chate, c\u00fabrete y ag\u00e1rrate!", u"\u00a1Fuego! \u00a1Para, t\u00edrate y rueda!", u"\u00a1Ayuda! \u00a1Necesito ayuda!"],
        "DE": [u"Erdbeben! Ducken, sch\u00fctzen und festhalten!", u"Feuer! Stopp, hinlegen und rollen!", u"Hilfe! Ich brauche Hilfe!"],
    },
    "karaoke": {
        "EN": ["Hello, my name is...", "Four languages, one big world.", "We learn together day by day."],
        "FR": [u"Bonjour, je m'appelle...", u"Quatre langues, un grand monde.", u"Nous apprenons ensemble jour apr\u00e8s jour."],
        "ES": [u"Hola, me llamo...", u"Cuatro idiomas, un gran mundo.", u"Aprendemos juntos d\u00eda tras d\u00eda."],
        "DE": [u"Hallo, ich hei\u00dfe...", u"Vier Sprachen, eine gro\u00dfe Welt.", u"Wir lernen Tag f\u00fcr Tag zusammen."],
    },
}

total = sum(len(texts) for group in phrases.values() for texts in group.values())
done = 0
failed = []

for group, langs in phrases.items():
    for lang, texts in langs.items():
        for i, text in enumerate(texts, 1):
            filename = f"{group}-{lang.lower()}-{i}.mp3"
            filepath = os.path.join(OUT, filename)
            if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
                done += 1
                print(f"[{done}/{total}] SKIP: {filename}")
                continue
            try:
                tts = gTTS(text=text, lang=LANG_MAP[lang])
                tts.save(filepath)
                done += 1
                print(f"[{done}/{total}] OK: {filename}")
            except Exception as e:
                done += 1
                failed.append(filename)
                print(f"[{done}/{total}] FAIL: {filename} -> {e}")

print(f"\nDone! {total - len(failed)}/{total} files generated.")
if failed:
    print("Failed:", ", ".join(failed))
