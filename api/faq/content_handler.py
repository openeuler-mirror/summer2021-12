import jieba

words_file_paths = ["words/ad.txt", "words/politics.txt", "words/sex.txt"]


def load_my_userdict():
    for path in words_file_paths:
        jieba.load_userdict(path)


load_my_userdict()


def get_filtered_words(filtered_words_txt_path):
    _filtered_words = []
    with open(filtered_words_txt_path, encoding='utf-8') as filtered_words_txt:
        lines = filtered_words_txt.readlines()
        for line in lines:
            _filtered_words.append(line.strip())
    return _filtered_words


filtered_words = set()
for path in words_file_paths:
    filtered_words.update(get_filtered_words(path))


def check_document(doc):
    """
    敏感词检查
    :param doc: 待检查的文档
    :return: bool值，包含敏感词时返回 false
    """
    tokens = jieba.cut(str(doc))
    _processed = ""
    for t in tokens:
        if t in filtered_words:
            return False
    return True


def process_document(doc):
    """
    将文档中的敏感词替换为等长度的 ‘*’
    :param doc: 待处理的文档
    :return: 处理过的文档
    """
    tokens = jieba.cut(str(doc))
    _processed = ""
    for t in tokens:
        _processed = _processed + (t if str(t) not in filtered_words else ("*" * len(t)))

    return _processed


if __name__ == "__main__":
    load_my_userdict()
    my_doc = "法轮功德无量"
    print(process_document(my_doc))
    my_doc = "法轮功和习近平"
    print(process_document(my_doc))
    my_doc = "原味内衣服搞gay片可不行"
    print(process_document(my_doc))
