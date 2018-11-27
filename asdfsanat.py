import tqdm
import argparse
import multiprocessing
from Levenshtein import distance

words = set()
with open("kotus.txt", "r") as infp:
    for line in infp:
        line = line.strip()
        if line and not (line.startswith("-") or line.endswith("-")):
            words.add(line.lower())
words = list(sorted(words))


def check_distance1(w):
    lw = len(w)
    matches = []
    shortlist = [
        mw
        for mw in words
        if mw != w and len(mw) > len(w)
        # and abs(len(mw) - lw) <= 2
    ]
    for mw in shortlist:
        if distance(w, mw) == 1:
            matches.append((w, mw))
    return matches


def check_suffix(w):
    lw = len(w)
    matches = []
    return [(w, mw) for mw in words if len(mw) == lw + 1 and mw.endswith(w)]


def check_prefix(w):
    lw = len(w)
    matches = []
    return [(w, mw) for mw in words if len(mw) == lw + 1 and mw.startswith(w)]


methods = {'distance1': check_distance1, 'suffix': check_suffix, 'prefix': check_prefix}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--method', choices=list(methods.keys()), required=True)
    args = ap.parse_args()
    method = methods[args.method]

    outf = open(f"out-{args.method}.txt", "a")
    with multiprocessing.Pool() as pool:
        with tqdm.tqdm(pool.imap_unordered(method, words, chunksize=50), total=len(words)) as prog:
            for result in prog:
                for w, mw in result:
                    l = f"{w} {mw}"
                    prog.set_description(l)
                    print(w, mw, file=outf)
            outf.flush()


if __name__ == "__main__":
    main()
