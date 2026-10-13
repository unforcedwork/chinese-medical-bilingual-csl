"""Structural CSL checks + optional Pandoc single-layout rendering smoke test.

Pandoc does not support the CSL-M multi-layout extension in the shipped style.
The temporary copy exists only to test formatting of the Chinese+translation branch.
"""
import copy
import json
import re
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLE = ROOT / 'chinese-medical-bilingual.csl'
XMLNS = {'c': 'http://purl.org/net/xbiblio/csl'}


def main():
    tree = ET.parse(STYLE)
    root = tree.getroot()
    assert root.tag == '{http://purl.org/net/xbiblio/csl}style', 'Root must be a CSL style'
    assert root.attrib.get('class') == 'in-text', 'Style must use in-text citations'
    layouts = root.findall('.//c:bibliography/c:layout', XMLNS)
    assert len(layouts) == 2, 'Need English and Chinese CSL-M layouts'
    assert layouts[0].attrib.get('locale') == 'en', 'First layout must be English'
    assert 'locale' not in layouts[1].attrib, 'Second layout must be default Chinese'
    mirror = root.find('.//c:macro[@name="entry-translation"]', XMLNS)
    assert mirror is not None
    assert mirror.find('.//c:text[@macro="author-original"]', XMLNS) is not None
    assert mirror.find('.//c:text[@macro="title-translation"]', XMLNS) is not None
    assert layouts[1].find('.//c:group[@display="block"]', XMLNS) is not None
    condition = layouts[1].find('.//c:if[@variable="original-title original-author"]', XMLNS)
    assert condition is not None and condition.attrib.get('match') == 'all', (
        'Translation row must require both original title and original author'
    )
    fixture = json.loads((ROOT / 'tests/references.json').read_text(encoding='utf-8'))
    fixture_by_id = {item['id']: item for item in fixture}
    assert {'lin2020', 'english', 'no_translation', 'title_without_author', 'author_without_title'} <= fixture_by_id.keys()
    assert fixture_by_id['lin2020'].get('original-title') and fixture_by_id['lin2020'].get('original-author')
    assert fixture_by_id['title_without_author'].get('original-title') and not fixture_by_id['title_without_author'].get('original-author')
    assert fixture_by_id['author_without_title'].get('original-author') and not fixture_by_id['author_without_title'].get('original-title')
    print('PASS: XML, CSL layout selection, and translation-row requirements')

    if not shutil.which('pandoc'):
        print('SKIP: Pandoc not found; rendering smoke test omitted')
        return
    with tempfile.TemporaryDirectory() as td:
        temp = Path(td)
        working = copy.deepcopy(root)
        bib = working.find('c:bibliography', XMLNS)
        bib.remove(bib.findall('c:layout', XMLNS)[0])
        ET.ElementTree(working).write(temp / 'test.csl', encoding='utf-8', xml_declaration=True)
        (temp / 'test.md').write_text('---\nbibliography: refs.json\ncsl: test.csl\nnocite: |\n  @*\n---\n', encoding='utf-8')
        (temp / 'refs.json').write_bytes((ROOT / 'tests/references.json').read_bytes())
        proc = subprocess.run(['pandoc', '--citeproc', 'test.md', '-t', 'plain'], cwd=temp, capture_output=True, text=True)
        assert proc.returncode == 0, proc.stderr
        s = re.sub(r'\s+', ' ', proc.stdout)
        assert '[1] 林志强, 李小波, 黄顺祥, 等.' in s
        assert 'Lin ZQ, Li XB, Huang SX, et al.' in s
        assert 'Chinese population[J]. Chin J Neurol, 2020, 53(11): 882-887.' in s
        assert s.count('10.3760/cma.j.cn113694-20200511-00343') == 2
        assert '[3] 张三. 无英文对照的示例[J].' in s
        assert s.count('Genetic and clinical features') == 1
        assert s.count('[1]') == 1, 'Bilingual output must reuse one reference number'
        assert 'MUST NOT RENDER:' not in s
        assert 'MustNotRender' not in s
        assert s.count('A random English journal paper') == 1
        print('PASS: rendered bilingual output, one number, DOI duplication, English-only entry, and incomplete-translation fallback')
        print('NOTE: Zotero CSL-M language-based layout selection still requires Zotero/Word end-to-end verification')


if __name__ == '__main__':
    main()
