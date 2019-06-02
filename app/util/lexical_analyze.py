import os
import re
if os.name is 'nt':
    from eunjeon import Mecab
else:
    from konlpy.tag import Mecab


rep = {
    "커피숍": "카페",
    "caffe": "카페",
    "커피샵": "카페",
    "커피전문점": "카페",
    "주방 보조": "주방보조",
    "ㅜㅜ": "도움말",
    "ㅠㅠ": "도움말",
    "HELP": "도움말",
    "가이드": "도움말",
    "도와줘": "도움말",
    "아니요": "아니",
    "아니오": "아니",
    "아냐": "아니",
    "아니야": "아니",
    "아닝": "아니",
    "하지마": "아니",
    "안할래": "아니",
    "안해": "아니",
    "취소": "아니",
    "ㄴㄴ": "아니",
    "ㅇㅇ": "그래",
    "ㅇㅋ": "그래",
} # define desired replacements here

# use these three lines to do the replacement
rep = dict((re.escape(k), v) for k, v in rep.items())
pattern = re.compile("|".join(rep.keys()))

mecab = Mecab()


def morphs(text):
    text = error_keyword_fix(text)
    morphs = []

    for pos in mecab.pos(''.join(text)):
        if pos[1] in ['SF', 'SE', 'SSO', 'SSC', 'SP', 'SO', 'SC', 'SW', 'SL', 'SY']:
            continue
        elif pos[1] in ['SN']:
            morphs.append('NUM')
        else:
            morphs.append(pos[0])
    return morphs


def error_keyword_fix(text):
    text = text.upper()
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    return text


if __name__ == '__main__':
    print(morphs('주말 알바가 관뒀어, 긴급하게 알바 구할 수 있을까?'))

