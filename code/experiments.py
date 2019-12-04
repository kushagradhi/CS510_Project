from environment import Environment
from cognitive_process import Subject


def cal_response_mixed(word_count,word,prev_word,emotion_words,response_time):
         ###-- Calculating the scores to show effect of words
    if word in emotion_words:
        if prev_word in emotion_words:
            word_count['emo_emo'][0]+=1
            word_count['emo_emo'][1]+=response_time
        else:
            word_count['emo_neut'][0]+=1
            word_count['emo_neut'][1]+=response_time
    else:
        if prev_word in emotion_words:
            word_count['neut_emo'][0]+=1
            word_count['neut_emo'][1]+=response_time
        else:
            word_count['neut_neut'][0]+=1
            word_count['neut_neut'][1]+=response_time
    
    return word_count

def print_mixed(word_count):

    print("------------------------------------------------------------------")
    print("\n")
    print("Average response time (in seconds): ")
    print("------------------------------------------------------------------")
    print("Emotion word | Emotion word : " , word_count['emo_emo'][1]/word_count['emo_emo'][0])
    print("Neutral word | Emotion word : " , word_count['emo_neut'][1]/word_count['emo_neut'][0])
    print("Emotion word | Neutral word : " , word_count['neut_emo'][1]/word_count['neut_emo'][0])
    print("Neutral word | Neutral word : " , word_count['neut_neut'][1]/word_count['neut_neut'][0])

def print_block(word_count,block_pattern,block_size):
    print("------------------------------------------------------------------")
    print("\n")
    print("Average response time (in seconds): ")
    print("------------------------------------------------------------------")
    for i in range(0,len(block_pattern)):
        bname="Neutral"
        if block_pattern[i].lower()=='e':
            bname="Emotion"
        print("Block " , i , " : ", bname, word_count[i]/block_size)
        

def Experiment(type_of_test='mixed',  num_of_words=30, number_of_trials=7, block_pattern="nen", block_size=10):

    # Response time for mixed
    if type_of_test=='mixed':
        word_count={'emo_neut':[0,0.0],'neut_emo':[0,0.0],'emo_emo':[0,0.0],'neut_neut':[0,0.0]}
    else:
        #word_count=dict.fromkeys(range(num_of_words/block_size))
        word_count={i:0 for i in range(int(num_of_words/block_size))}

    # Generate test subject
    test_subject=Subject()
    # Create environment
    env=Environment()
    print("Test begins")
    # Running the trials:
    for trial_num in range(number_of_trials):
        test_subject.WM = [0] * test_subject.max_size_WM
        test_subject.WM_response = []
        test_subject.WM = [0] * test_subject.max_size_WM   # working memory with num_of_chunk chunks
        test_subject.emotion_scores = [0] * test_subject.max_size_WM   # to keep a track of decaying emotional effect from words seen prior
        test_subject.current_size_WM = 0        # to keep record of the current number of words in the WM 
        test_subject.current_colour_perceived = "blank"
    #Generate word list (will be different for every trial):
        if type_of_test=='mixed':
            word_list=env.get_trial_set_mixed()
        else: 
            word_list=env.get_trial_set_blocked()

        prev_word=None
        #Running the experiment:
        print("------------------------------------------------------------------")
        print("Trial: ",trial_num+1 )
        print("Total number of words: ", len(word_list))
        print("------------------------------------------------------------------")
        print("\n")
        block_num=0
        for i in range(0,len(word_list)):
            word_type='Neutral word'
            if i>0:
                prev_word=word_list[i-1][0]
            word=word_list[i][0]
            color=word_list[i][1]

            if word in env.emotion_words:
                word_type='Emotional word'
            print("Trial #" + str(trial_num+1) + " Word #" + str(i+1) + " : " + word[:-2]  + " in font color " + color  + " [ " + word_type + " ] ")
            #Test subject reads the word
            test_subject.read_display(word_list[i])
            #Time calculated for subject to respond
            response_time=test_subject.get_response_time(word)

            #Subject speaks out the color
            test_subject.speak_current_colour()
            print("Time taken (in seconds): " + str(response_time))
            ## Checking if the subject has recognized the font color correctly
            val=test_subject.is_colour_recognized(test_subject.current_colour_perceived)
            print("Answer is " + str(val))
            print("------------------------------------------------------------------")
        
            if type_of_test=='mixed':
                if i>0:
                    word_count=cal_response_mixed(word_count,word,prev_word,env.emotion_words,response_time)
            
            else:
                if (i)%(block_size)==0 and (i)>0:
                    print("Increment at ", i)
                    block_num+=1
                word_count[block_num]+=response_time
                #word_count[block_num].append(response_time)



    if type_of_test=='mixed':
        print_mixed(word_count)   
    else:
        print_block(word_count,block_pattern,block_size)

if __name__=='__main__':

    #default: num_of_words=30, block_pattern="nen", block_size=10

    Experiment(type_of_test='mixed',number_of_trials=1)
