#!/usr/bin/env python3

import itertools

class scale(object):
    def __init__(self,keymode):
        '''specify keymode as [A-G][#bn]?[Mmhl]'''
        try:
            key,accidental,mode=list(keymode)
        except ValueError as e:
            try:
                key,mode=list(keymode)
                accidental=''
            except ValueError as e:
                key=key
                accidental=''
                mode='M'
        modes={
            'M':[2, 2, 1, 2, 2, 2, 1, 2],#ionian
            'm':[2, 1, 2, 2, 1, 2, 2, 2],#aeolian
            'h':[2, 1, 2, 2, 1, 3, 0, 3],#harmonic end=3?
            'l':[2, 1, 2, 2, 2, 2, 1, 2],#melodic
            }
        fromdegree=lambda k:dict([(i,sum(k[0:j[0]])) for i,j in enumerate(enumerate(k))])
        wanted=[chr(k) for k in itertools.chain(range(ord(key),ord('H')),range(ord('A'),ord(key)))]
        target=dict((r,fromdegree(modes[mode])[p]) for p,r in enumerate(wanted))
        kb=[chr(k) for k in itertools.chain(range(ord('C'),ord('H')),range(ord('A'),ord('C')))]
        Cmajor=dict((r,fromdegree(modes['M'])[p]) for p,r in enumerate(kb))
        Cmajor.update(dict((fromdegree(modes['M'])[p],r) for p,r in enumerate(kb)))
        Cmajorfull=dict(map(lambda i:(i[0],Cmajor[i[0]-1]+'#')
            if i[1]==None else (i[0],i[1]),
            [(k,Cmajor.get(k)) for k in range(0,12)]))
        Cmajorfull.update({v:k for k,v in Cmajorfull.items()})
        transpose=lambda k:((Cmajorfull[key]+k)%12)
        raw=dict(
                (Cmajorfull[transpose(k)+1]+'b',k)
                if wanted[i][0]!=Cmajorfull[transpose(k)][0]
                else (Cmajorfull[transpose(k)],k) 
                for i,(j,k) in enumerate(target.items())
                )
        rawbase=dict((k[0],v-1) if 'b' in k else (k,v) for k,v in raw.items())
        self.normal,self.raw=target,rawbase
    def acc(self,note,step):
        kb=list(map(chr,itertools.chain(range(ord('C'),ord('H')),range(ord('A'),ord('C')))))
        return kb[note]
    def note(self,n):
        try:
            note,acc=list(n)
        except ValueError as e:
            note=n
            acc=''
        if not acc or acc in ('n','N'):
            return self.normal[note]
        else:
            if acc in ('b','@'):
                return self.raw[note]-1
            if acc=='#':
                return self.raw[note]+1
        
def main():
    for accidental in ('','n','#','b'):
        for mode in ('M','m','h','l'):
            for key in map(chr,itertools.chain(range(ord('C'),ord('H')),range(ord('A'),ord('C')))):
                signature=key+accidental+mode
                s=scale(signature)
                print(signature,'\t',s.normal)
                print('\t',s.raw)
            print('')

if __name__=='__main__':
    main()
