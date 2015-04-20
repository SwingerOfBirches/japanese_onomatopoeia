# 1. Decide what to do with final diphthongs.
#    For now keeping them in root.
# 2. Do all the removal at once or step by step.
#    Step by step
# 3. Find inner geminates
#    DONE
# 4. Find inner nasals (n+ consonant, n')
#    DONE
# 5. Find inner long vowels
# 6. Mixed roots
# 7. Exceptions like　こけこっこ
# 8. Triple base repetition like ははは　or はっはっは
# 9. What if they end in 'to' (not 'tto') 
#    Regex if to x 2 ?

import romkan
import re


b = ['じゃんじゃん','じゃじゃん','じゅん','じゃーんじゃーん',\
     'じゃじゃーん','ぴったっと','きらきらり','がっちゃっ',"しゃーしゃー",\
     'きらきら','ごろごろ','ぽいぽい','きゃー','ぽん','ぱっ','ぼっさぼっさ',\
'ひんやり','ふんわり'] 

# Onomatopoeia strings
raw = ''
hiragana = ''
katakana = ''
hepburn = ''
kunrei = ''
onoma = ''


# create the necessary strings
def strings(input):
    global raw
    raw = input
    global kunrei
    kunrei = romkan.to_kunrei(input)
    # Using "kunrei" because hiragana <> katakana conversion doesn't work
    global hiragana
    hiragana = romkan.to_hiragana(kunrei) 
    global katakana
    katakana = romkan.to_katakana(kunrei)
    global hepburn
    hepburn = romkan.to_hepburn(hiragana)
    global onoma
    onoma = kunrei
    changes_dict = {'ch': 'C', 'ty':'T', 'sy':'S', 'ny': 'N', 'zy':'Z', \
                    'dj':'D', 'l':'r','xtu':'Q', 'aa':'a-','ee':'e-','ii':'i-', \
                    'oo':'o-','uu':'u-'}
    for key in changes_dict:
        onoma = onoma.replace(key, changes_dict[key])
    if onoma.endswith('tto'):
        onoma = onoma[:-3] + 'Q'
    return(hiragana + ' ' + katakana + ' ' + hepburn + ' ' + onoma)


# looking for base repetition


descriptors = {}


def repetition():
    global onoma
    global descriptors
    if onoma[len(onoma)//2:] == onoma[:len(onoma)//2]:
             descriptors['base repetition']=True
             onoma = onoma[:len(onoma)//2]
             return True

    

# Find word ending (vowel -short, long, diphthong-, "-n", "ri", stop)
# and check for base repetition

def ending():
    
    global onoma
    onoma = onoma
    global descriptors
    descriptors = {}
    vowels = ['a','e','i', 'o','u']

    if onoma.endswith('n') or onoma.endswith('Q'):
        descriptors['ending']= onoma[-1]
        repetition()
        onoma = onoma[:-1]          
        repetition()

    elif onoma.endswith('ri'):
        descriptors['ending']= 'ri'
        repetition()
        onoma = onoma[:-2]
        repetition()
    
    elif onoma.endswith('-'):
        descriptors['ending']= 'vowel, long'
        if repetition() is True:
            pass
        else:
            onoma = onoma[:-1]

    elif onoma[-1] in vowels:
        if onoma[-2] in vowels:
            descriptors['ending']= 'vowel, diphthong'
            repetition()
        else:
            descriptors['ending']= 'vowel, short'
            repetition()

def geminates():
    rep = r'(.)\1{1,}'
    global onoma
    global descriptors
    if re.search(rep,onoma,re.I):
        descriptors['inner Q'] = True
        geminates = ['kk','tt', 'pp','mm', 'nn', \
'ss', 'bb', 'dd', 'ff', 'gg', 'hh', 'jj','zz','rr']
        for gem in geminates:
            x = re.finditer(gem, onoma, re.I)
            for match in x:
                pos = match.span()
                onoma = onoma[:pos[0]] + onoma[pos[1]-1:]
                  
        repetition()
        

def syllabic_n():
    global onoma
    global descriptors
    n = r'n[^a,e,i,o,u,\']'
    m = r'n\''

    if re.search(n, onoma, re.I):
         descriptors['syllabic n'] = True
         x = re.finditer(n, onoma, re.I)
         for match in x:
             pos = match.span()
             onoma = onoma[:pos[0]] + onoma[pos[1]-1:]
    
         repetition()

         print('AFTER SYLLABIC NASAL')
         print('Base: ' + onoma)
         print('INFO')
         for i in descriptors: print(i + ': ' + str(descriptors[i]))
    
    elif re.search(m, onoma, re.I):
         descriptors['syllabic n'] = True
         x = re.finditer(m, onoma, re.I)
         for match in x:
             pos = match.span()
             onoma = onoma[:pos[0]] + onoma[pos[1]:]
    
         repetition()



    
def analyzer(input):
    strings(input)
    repetition()
    ending()
    geminates()
    syllabic_n()
    print('Onomatopoeia: ' + raw)
    print('Base: ' + onoma)
    print('INFO')
    for i in descriptors: 
        print(i + ': ' + str(descriptors[i]))
    print('********')
        

        repetition()
