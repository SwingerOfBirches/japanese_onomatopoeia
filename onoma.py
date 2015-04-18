# 1. Decide what to do with final diphthongs.
#    For now keeping them in root.
# 2. Do all the removal at once or step by step.
#    Step by step
# 3. Find inner geminates
#    !!!! When looking for inner geminates: make lowercase
# 4. Find inner nasals (n+ consonant, n')
# 5. Find inner long vowels
# 6. Mixed roots
# 7. Exceptions like　こけこっこ

import romkan


b = ['じゃんじゃん','じゃじゃん','じゅん','じゃーんじゃーん',\
     'じゃじゃーん','ぴったっと','きらきらり','がっちゃっ',"しゃーしゃー",\
     'きらきら','ごろごろ','ぽいぽい','きゃー']

# Onomatopoeia strings
raw = ''
hiragana = ''
katakana = ''
hepburn = ''
kunrei = ''
onoma = ''
root = ''

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





# Find word ending (vowel -short, long, diphthong-, "-n", "ri", stop)
# and check for base repetition

descriptors = {}
  

def ending(input=onoma, base=root):
    
    global root
    root = onoma
    global descriptors
    descriptors = {}
    vowels = ['a','e','i', 'o','u']

    if onoma.endswith('n') or onoma.endswith('Q'):
        descriptors['ending']= onoma[-1]
        if root[:len(root)//2] == root[len(root)//2:]:
            descriptors['base repetition']=True
            root = root[:len(root)//2-1]           
        else:
            root = root[:-1]
            if root[len(root)//2:] == root[:len(root)//2]:
                descriptors['base repetition']=True
                root = root[len(root)//2:]
            else:
                root = root[:len(onoma)-1]
        print('Onomatopoeia: ' + raw)
        print('Base: ' + root)
        print('Info')
        for i in descriptors: print(i + ': ' + str(descriptors[i]))
        
    elif onoma.endswith('ri'):
        descriptors['ending']= 'ri'
        root = root[:-2]
        # for a hypothetical /kirakirari/. Check if this pattern exists
        if root[len(root)//2:] == root[:len(root)//2]:
            descriptors['base repetition']=True
            root = root[len(root)//2:]
        print('Onomatopoeia: ' + raw)
        print('Base: ' + root)
        print('Info')
        for i in descriptors: print(i + ': ' + str(descriptors[i]))
    
    elif onoma.endswith('-'):
        descriptors['ending']= 'vowel, long'
        if root[len(root)//2:] == root[:len(root)//2]:
            descriptors['base repetition']=True
            root = root[:len(root)//2-1]
        else:
            root = root[:-1]
        print('Onomatopoeia: ' + raw)
        print('Base: ' + root)
        print('Info')
        for i in descriptors: print(i + ': ' + str(descriptors[i]))

    elif onoma[-1] in vowels:
        if onoma[-2] in vowels:
            descriptors['ending']= 'vowel, diphthong'
            if root[len(root)//2:] == root[:len(root)//2]:
                descriptors['base repetition']=True
                root = root[:len(root)//2]
        else:
            descriptors['ending']= 'vowel, short'
            if root[len(root)//2:] == root[:len(root)//2]:
                descriptors['base repetition']=True
                root = root[:len(root)//2]
        print('Onomatopoeia: ' + raw)
        print('Base: ' + root)
        print('Info')
        for i in descriptors: print(i + ': ' + str(descriptors[i]))
    else:
        print('This does not seem to be an onomatopoeia.')

   
def analyzer(input):
    strings(input)
    ending()


