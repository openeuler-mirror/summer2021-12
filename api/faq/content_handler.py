import jieba

words_file_paths = ["words/ad.txt", "words/politics.txt", "words/sex.txt"]

for path in words_file_paths:
    jieba.load_userdict(path)


def get_filtered_words(filtered_words_txt_path):
    _filtered_words = []
    with open(filtered_words_txt_path,encoding='utf-8') as filtered_words_txt:
        lines = filtered_words_txt.readlines()
        for line in lines:
            _filtered_words.append(line.strip())
    return _filtered_words


filtered_words = set()
for path in words_file_paths:
    filtered_words.update(get_filtered_words(path))


def process_document(doc):
    tokens = jieba.cut(str(doc))
    _processed = ""
    for t in tokens:
        _processed = _processed + (t if str(t) not in filtered_words else ("*"*len(t)))

    return _processed


if __name__ == "__main__":
    my_doc = "法轮功德无量"
    print(process_document(my_doc))
    my_doc = "法轮功和习近平"
    print(process_document(my_doc))
    my_doc = "原味内衣服搞gay片可不行"
    print(process_document(my_doc))

