import random

# Reading the data file line by line and formatting it as per its reference paper to load the data correctly
def  read_data(filename):
    f=open(filename,'r')
    data=[]
    
    for line in f:
        d=[]
        if line.startswith('#'):
            continue
        cols=line.split("\t")
        #Common words: Given in the form: pos_score , neg_score, words
        if len(cols)==3:
            words=cols[2].strip().replace('#','')
            pos_score=float(cols[0])
            neg_score=float(cols[1])
            
        #Group 1 Words: given by 3 evaluators in the form of pos_score1, neg_score1, pos_score2, neg_score2, pos_score3, neg_score3, words
        elif len(cols)==7:
            pos_score=round((float(cols[0])+float(cols[2])+float(cols[4]))/3.0,6)
            neg_score=round((float(cols[1])+float(cols[3])+float(cols[5]))/3.0,6)
            words=cols[6].strip().replace('#','')
             
        #Groups 2 words: given by 2 evaluators in the form of pos_score1, neg_score1, pos_score2, neg_score2, words
        else:
            pos_score=round((float(cols[0])+float(cols[2]))/2.0,6)
            neg_score=round((float(cols[1])+float(cols[3]))/2.0,6)
            words=cols[4].strip().replace('#','')
        obj_score=round(1-pos_score-neg_score,6)
        d=[words,pos_score,neg_score,obj_score]
        data.append(d)
    return data
    #print(data)

'''
---- Function to generate lexicon for different subjects (people). The random factor this change does can be considered as an 
effect of the prior experiences of people. This manipulation is done to show the effect that a word can have a different level of 
emotional response (or lack of) based on their experience/genetics. For ex: someone could be more emotional towards the word 'cancer'
 as compared to another person.
'''
def test_subjects(sub_data):
    # Generating a random number called bias by which the experiences of people varies
    bias=round(random.uniform(0,0.3),6)
    n=len(sub_data)
    #print(bias)
    for i in range(0,n):
        '''
        Generating a random factor by which the bias is split among the other two factors, i.e. If we are reducing the positive score 
        of a word for a subject by 0.3, we want to add the 0.3 to the negative and neutral score. Instead of doing that split equally, 
        we are using more randomization, that means the word could have a 0.25 effect added to the negative score and 0.05 effect to 
        the neutral score for one person.
        '''
        s=random.randint(2,7)

        ##-- Subtracting the score from the positive and assigning to the neutral and negative split by a random factor
        if sub_data[i][1]>=bias:
            sub_data[i][1]=round(sub_data[i][1]-bias,6)
            sub_data[i][2]=round(sub_data[i][2]+(bias/s),6)
            sub_data[i][3]=round(sub_data[i][3]+(bias*(1 - (1/s))),6)
        ##-- Subtracting the score from the negative and assigning to the neutral and positive split by a random factor
        elif sub_data[i][2]>=bias:
            sub_data[i][2]=round(sub_data[i][2]-bias,6)
            sub_data[i][1]=round(sub_data[i][1]+(bias/s),6)
            sub_data[i][3]=round(sub_data[i][3]+(bias*(1 - (1/s))),6)
        ##-- Subtracting the score from the neutral and assigning to the negative and positive split by a random factor
        else:
            sub_data[i][3]=round(sub_data[i][3]-bias,6)
            sub_data[i][1]=round(sub_data[i][1]+(bias/s),6)
            sub_data[i][2]=round(sub_data[i][2]+(bias*(1 - (1/s))),6)
    return sub_data


if __name__=='__main__':
    data=read_data('Micro-WNOp-data.txt')
    for i in range(0,20):
        print(data[i])
    
    