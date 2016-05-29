import json
import re


def get_raw_text(path, output):
    with open(output, "w") as f:
        articles = json.load(open(path, "r"), encoding="utf-8")
        #print(articles[0]['text'], type(articles[0]['text']))
        f.writelines("\n".join(map(lambda a: strip(a['text'].lower()).encode('utf-8'), articles)))


def strip(s):
    return re.sub(u"[^\w\s]+", "", s, flags=re.UNICODE)


def find_all_nonalphanum_chars(path):
    articles = json.load(open(path, "r"), encoding="utf-8")
    matches = set()
    for art in articles:
        matches.update(set(re.findall(u"[^\w\s]+", art['text'], flags=re.UNICODE)))
    return matches


def read_lemma_dict(path):
    with open(path, "r") as f:
        d = {}
        lines = f.read().decode('utf-8').lower().split(u'\n')
        for line in lines:
            val, key = tuple(line.split(u'\t'))
            if key not in d:
                d[key] = val
        return d


def lemmatize_text(path, output, lemma_dict):
    with open(path, "r") as f:
        lines = f.read().decode('utf-8').split(u'\n')
        new_lines = []
        base_forms = set(lemma_dict.values())
        for line in lines:
            new_line = []
            for word in line.split():
                new_word = lemma_dict[word] if len(word) > 3 and word in lemma_dict and word not in base_forms else word
                new_line.append(new_word)
            new_lines.append(" ".join(new_line))
    with open(output, "w") as out:
        out.writelines("\n".join(new_lines).encode("utf-8"))


def read_word_set(path):
    with open(path, "r") as f:
        return set(f.read().decode('utf-8').split('\n'))


def tokenize(text, word_ref):
    words = text.split()
    tokens = []
    i, total = 0, len(words)
    while i < total:
        for j in range(min(2, total - i - 1), -1, -1):
            token = " ".join(words[i:i+j+1])
            if token in word_ref or j == 0:
                tokens.append(token)
                i += j + 1
                break
    return tokens

if __name__ == "__main__":
    #get_raw_text("nd_items.json", "nd_text.txt")
    #print(find_all_nonalphanum_chars("se_items.json"))
    ld = read_lemma_dict("lemmatization-pl.txt")
    lemmatize_text("nd_text.txt", "nd_lemma_text.txt", ld)
    lemmatize_text("gazeta_text.txt", "gazeta_lemma_text.txt", ld)
    lemmatize_text("se_text.txt", "se_lemma_text.txt", ld)
    #ws = read_word_set("wikiwords.txt")
    #with open("nd_text.txt", "r") as f:
    #    lines = f.read().decode('utf-8').split(u'\n')
    #    for l in lines[:5]:
    #        print(tokenize(l, ws))
