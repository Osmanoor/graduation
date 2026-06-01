import pickle
import os
import glob
import sys
import io
import unicodedata

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target_queries = [
    'ما هو الرباط المنصوري؟',
    'من هو مؤسس الفلسفة البراغماتية؟',
    'من هو نيكولا بوالو؟',
]

def norm(s):
    return unicodedata.normalize('NFKC', s).strip()

pkl_dir = 'results/enhanced_queries'
files = sorted(glob.glob(os.path.join(pkl_dir, '*.pkl')))

for target in target_queries:
    target_n = norm(target)
    print('\n' + '#' * 80)
    print(f'# QUERY: {target}')
    print('#' * 80)

    for fp in files:
        name = os.path.basename(fp)
        try:
            with open(fp, 'rb') as f:
                data = pickle.load(f)
        except Exception as e:
            print(f'\n[{name}] FAILED to load: {e}')
            continue

        if not isinstance(data, dict):
            continue

        originals = (data.get('original') or data.get('originals')
                     or data.get('original_queries') or data.get('queries'))
        enhanced = data.get('enhanced') or data.get('enhanced_queries')
        qids = data.get('query_ids') or data.get('qids')

        if originals is None or enhanced is None:
            print(f'\n[{name}] Unexpected structure. Keys: {list(data.keys())}')
            continue

        found_idx = None
        for i, q in enumerate(originals):
            if norm(q) == target_n:
                found_idx = i
                break

        if found_idx is None:
            # Try a fuzzy keyword fallback (any salient word in target)
            kw_candidates = [w for w in target_n.replace('؟', '').split() if len(w) > 3]
            for i, q in enumerate(originals):
                qn = norm(q)
                if all(kw in qn for kw in kw_candidates):
                    found_idx = i
                    print(f'\n[{name}] (fuzzy match: "{q}")')
                    break

        print(f'\n[{name}]')
        if found_idx is None:
            print('  Query not found.')
            continue

        qid = qids[found_idx] if qids else 'N/A'
        enh = enhanced[found_idx]
        print(f'  query_id: {qid}')
        print(f'  original ({len(originals[found_idx])} chars): {originals[found_idx]}')
        print(f'  enhanced ({len(enh)} chars):')
        print(f'  {enh}')
        print('-' * 80)
