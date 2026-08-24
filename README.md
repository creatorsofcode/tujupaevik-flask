# Tujupäevik (Flask)

Veebipõhine Python/Flask versioon algsest Android rakendusest [Tujupäevik](https://github.com/markorillo/mobiilirakendusteare),
mille autorid on Caupo Helvik, Marko Rillo, Peeter Roop, Priit Laupa ja Tatjana Kuznetsova.

Rakendus on üleval ja töötab aadressil **[https://tujud.runmyapi.com/](https://tujud.runmyapi.com/)** — proovi kohe järele!

Rakendus lubab kasutajal iga päev salvestada oma tuju, tuju põhjuse, tempo ja energiataseme
ning näha nende kohta lihtsat statistikat.

## Vaated

1. Avaleht
2. Mis tunne on? — tuju valik (8 tuju)
3. Miks ma nii tunnen? — põhjuse valik või vaba tekst
4. Mis tempoga ma sõidan? — 0-100 liugur
5. Kui palju energiat mul on? — 0-100 liugur
6. Kuidas mul läinud on? — üldine statistika (tulp-diagramm)
7. Tujude statistika
8. Tempode statistika (arendamisel)

## Andmete salvestamine

Andmed salvestatakse kohalikku `data/tujuStorage.json` faili, kuupäeva kaupa:

```json
{
  "24-Aug-2026": {
    "mood": ["happy"],
    "reason": ["Saavutus"],
    "tempo": ["70"],
    "fuel": ["55"]
  }
}
```

## Käivitamine

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Rakendus käivitub aadressil http://127.0.0.1:5000
