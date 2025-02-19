import enum

import conllu_path as cp

import utils


class Definiteness(enum.Enum):
    DEF = 'DEF'
    INDEF = 'INDEF'
    BARE = 'BARE'

def what_determiner_ro(node : cp.Tree) -> Definiteness:
    if node.sdata('feats.Definite') == 'Def' or\
            cp.Search('<[feats.Definite=Def | feats.PronType=Dem]').match(node):
        return Definiteness.DEF
    if cp.Search('<[upos=DET | deprel=nummod]').match(node):
        return Definiteness.INDEF
    return Definiteness.BARE

def what_determiner_en(node : cp.Tree) -> Definiteness:
    if cp.Search('.[<[feats.Definite=Def | feats.PronType=Dem | deprel=nummod] | /[deprel=nmod:poss]]').match(node):
        return Definiteness.DEF
    if cp.Search('<[upos=DET | lemma=many]').match(node):
        return Definiteness.INDEF
    return Definiteness.BARE

def get_noun_left_perifiery(noun : cp.Tree) -> list[cp.Tree]:
    left_perifery = cp.Search('<[upos=DET,PRON,ADJ,ADP | deprel=det,case,cop]').match(noun)
    fixed = [cp.Search('/[deprel=fixed,flat]').match(child) for child in left_perifery]
    for f in fixed:
        left_perifery.extend(f)
    left_perifery.sort(key=lambda n : n.id())
    return left_perifery

if __name__ == "__main__":
    print('Loading...')
    noun_pairs = utils.p_load('./noun_equivalents_list.p')
    roDoc = cp.Doc.from_conllu('./ro1984-v1.conllu')
    enDoc = cp.Doc.from_conllu('./en1984-v1.conllu')

    limit = 1000
    count = 0

    for np in noun_pairs:
        if count > limit:
            break
        i = np['chunk_index']
        en_tok = np['src_data']['index']
        en_uid = np['src_data']['uid']
        en_node = enDoc.get_node(en_uid)
        en_perifery = get_noun_left_perifiery(en_node)
        en_string = ' '.join([n.sdata('form') for n in en_perifery + [en_node]])
        en_def = what_determiner_en(en_node).value
        en_deprel = en_node.sdata('deprel')
        if 'index' in np['trgt_data']:
            ro_tok = np['trgt_data']['index']
            ro_uid = np['trgt_data']['uid']
            ro_node = roDoc.get_node(ro_uid)
            ro_perifery = get_noun_left_perifiery(ro_node)
            ro_string = ' '.join([n.sdata('form') for n in ro_perifery + [ro_node]])
            ro_def = what_determiner_ro(ro_node).value
            ro_deprel = ro_node.sdata('deprel')
        else:
            ro_tok = ro_uid = ro_node = ro_def = ro_string = ro_deprel = None
        if ro_def == en_def:
            continue
        data = [i, en_string, en_tok, en_def, en_deprel,
                ro_string, ro_tok, ro_def, ro_deprel, '\t',
                "'" + str(en_node.sentence()), "'" + str(ro_node.sentence()) if ro_node else None]
        print('\t'.join([str(s) for s in data]))
        count += 1



