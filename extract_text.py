from lxml import etree
from lxml.etree import Element as E
import re
import conllu_path as cp

def strip_namespace(key : str) -> str:
    return re.sub(r'{.*}', '', key)

def strip_namespace_dict(d : dict) -> dict:
    return {strip_namespace(k):v for k,v in d.items()}

def correct_diactricics(text :str) -> str:
    bad_dia = {'ş':'ș', 'ţ':'ț', 'Ş':'Ș', 'Ţ':'Ț'}
    for k,v in bad_dia.items():
        text = text.replace(k, v)
    return text

def get_xml_sentence(sent_node : E) -> (str, str):
    attrib = strip_namespace_dict(sent_node.attrib)
    id = attrib.get('id')
    text = ''.join(sent_node.itertext())
    text = text.replace('\n', ' ').strip()
    text = correct_diactricics(text)
    return id, text

def conllu_sentence_dict(doc : cp.Doc) -> dict[str, cp.Sentence]:
    d = dict()
    for sentence in doc:
        projection = sentence.projection()
        projection.sort(key=lambda n : n.id())
        text = ' '.join([n.sdata('form') for n in projection])
        d[text] = sentence
    return d


if __name__ == "__main__":
    # xmlfile = './MTE1984-ana/oana-ro.xml'
    xmlfile = './MTE1984-ana/oalg-enro.xml'
    tree =etree.parse(xmlfile)
    root = tree.getroot()
    link_list = []
    for i, child in enumerate(root):
        attribs = child.attrib.get('targets')
        if not attribs:
            continue
        attribs = attribs.split(' ')
        sent_ids = [a.split('#')[1] for a in attribs]
        en = [a for a in sent_ids if 'en' in a]
        ro = [a for a in sent_ids if 'ro' in a]
        if len(en) + len(ro) != len(attribs):
            print('Incomplete attribs at ' + str(attribs))
        link_list.append((en, ro))


