import stanza

import utils

if __name__ == '__main__':
    nlp = stanza.Pipeline("ro")
    doc_ro = stanza.Document([])
    texts = utils.p_load('./en_ro_texts.p')
    for i, (en_text, ro_text) in enumerate(texts):
        print(f'Doing chunck {i+1} of {len(texts)}.')
        _doc : stanza.Document = nlp(ro_text)
        _doc.sentences[0].comments.append(f"# newpar id = f{i}")
        doc_ro.sentences.extend(_doc.sentences)
    for i, sentence in enumerate(doc_ro.sentences):
        sentence.sent_id = str(i)



