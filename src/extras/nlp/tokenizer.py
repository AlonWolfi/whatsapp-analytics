from extras.nlp.hebtokenizer import tokenize as nlp_tokenize

START_TOKEN = '###'
END_TOKEN = '$$$'

def tokenize_text(txt, max_len = 100):
    tok = [word for lng, word in nlp_tokenize(txt)]
    tok = [START_TOKEN] + tok[:(max_len - 2)] + [END_TOKEN]
    return tok