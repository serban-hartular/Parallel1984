import stanza
from stanza.utils.conll import CoNLL
import conllu_path as cp


_nlp = stanza.Pipeline(lang='ro') #, download_method=None)


def parse_to_doc(input : str, parser = None) -> cp.Doc:
    if not parser:
        parser = _nlp
    TEMPFILE = 'temp.conllu'
    stanza_doc = parser(input)
    CoNLL.write_doc2conll(stanza_doc, TEMPFILE)
    cp_doc = cp.Doc.from_conllu(TEMPFILE)
    return cp_doc

