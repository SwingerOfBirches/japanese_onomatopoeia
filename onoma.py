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
# 8. Triple base repetition like ははは -> (..)\1{2,}
#　 はっはっは　lo mismo después de quitar Q
#    あははは　lo mismo?
# 9. What if they end in 'to' (not 'tto') 
#    Does this possibility exist?


import romkan
import re

# I'm using this to test
b = ['ははは','あははは','はっはっは','はっはっはっ','じゃんじゃん','じゃじゃん','じゅん',\
     'じゃーん  じゃーん', 'じゃじゃーん','ぴったっと','きらきらり','がっちゃっ',\
     "しゃーしゃー", 'きらきら','ごろごろ','ぽいぽい','きゃー','ぽん','ぱっ',\
     'ぼっさぼっさ', 'ひんやり','ふんわり'] 

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


# check for triple repetition at the beginning
#  not happy with this

def triple_rep():
    global onoma
    global descriptors
    pattern = r'(..)\1{2,}$' # searching from the beginning, just in case there's prefixation
    pattern2 = r'^(..)\1{2,}'
    if re.search(pattern, onoma):
        descriptors['base repetition'] = True
        rep = re.search(pattern,onoma)
        pos = rep.span()
        base = rep.group(1)
        if not base[0] == onoma[0]:
            descriptors['prefix'] = onoma[:pos[0]]
        onoma = base
    elif re.search(pattern2, onoma):
        descriptors['base repetition'] = True
        rep = re.search(pattern2,onoma)
        onoma = rep.group(1)

# final check
def f_triple():
    global onoma
    global descriptors
    if not len(onoma)%3: # checking if length of onoma is divisible by 3
       l = len(onoma)//3
       if onoma[:l] == onoma[l:l*2] == onoma[l*2:]:
           descriptors['base repetition'] = True
           onoma = onoma[:l]     
            

# Find word ending (vowel -short, long, diphthong-, "-n", "ri", stop)
# and check for base repetition

def ending():
    
    global onoma
    global descriptors
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
        descriptors['base split by Q'] = True
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
         descriptors['base split by n'] = True
         x = re.finditer(n, onoma, re.I)
         for match in x:
             pos = match.span()
             onoma = onoma[:pos[0]] + onoma[pos[1]-1:]
    
         repetition()
    
    elif re.search(m, onoma, re.I):
         descriptors['base split by n'] = True
         x = re.finditer(m, onoma, re.I)
         for match in x:
             pos = match.span()
             onoma = onoma[:pos[0]] + onoma[pos[1]:]
    
         repetition()

def long_vowel():
    global onoma
    global descriptors
    if '-' in onoma:
        descriptors['inner long vowel'] = True
        onoma = onoma.replace('-','')

        repetition()


def analyzer(input):
    global descriptors
    descriptors = {'base repetition': False, 'ending':'','base split by Q': False, 'base split by n':False, 'inner long vowel':False, 'prefix':False}
    strings(input)
    triple_rep()
    repetition()
    ending()
    geminates()
    syllabic_n()
    long_vowel()
    f_triple()
    print('Onomatopoeia: ' + raw)
    print('Base: ' + onoma)
    print('INFO')
    for i in descriptors: 
        print(i + ': ' + str(descriptors[i]))
    print('********')
