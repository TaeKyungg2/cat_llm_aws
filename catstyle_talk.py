from random import randint
from kiwipiepy import Kiwi
kiwi=Kiwi()
def make_cat_style_by_pos(sentence):
    kiwi_tag=kiwi.tokenize(sentence)
    result=''
    before_startnum=0
    isJump=False
    for i,token in enumerate(kiwi_tag):
        if isJump:
            isJump=False
            continue
        if i<len(kiwi_tag)-1 and 4520 <= ord(kiwi_tag[i+1].form[0]) <= 4546 and kiwi_tag[i+1].tag!='SW':
            result+=sentence[token.start:kiwi_tag[i+1].start+kiwi_tag[i+1].len]
            isJump=True
            continue
        if before_startnum != token.start:
            result+=' '
        if token.tag=='NP':
            if token.form=='내' or token.form=='나' or token.form=='제' or token.form=='저':
                result+='고냥이'
            else :result+=token.form
        elif token.tag=='EF':
            if token.form[-1]=='다':
                result+=token.form+'냥'
            else :result+=token.form+',냥.'
        else : result+=token.form
        before_startnum=token.start+token.len
    for i in range(len(result)-1):
        if result[i+1]==' ' and randint(0,9)>=9:
            result=result[:i]+", 냥, "+result[i:]
    return result
