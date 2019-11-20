from environment import Environment
from cognitive_process import Subject

def Experiment(type_of_test='mixed', number_of_trials=7):

    word_count={'emo_neut':[0,0.0],'neut_emo':[0,0.0],'emo_emo':[0,0.0],'neut_neut':[0,0.0]}

    # Generate test subject
    test_subject=Subject()
    # Create environment
    env=Environment()
    print("Test begins")
    # Running the trials:
    for trial_num in range(number_of_trials):
    
    #Generate word list (will be different for every trial):
        if type_of_test=='mixed':
            word_list=env.get_trial_set_mixed()
        else:
            word_list=env.get_trial_set_bocked()

        prev_word=None
        #Running the experiment:
        print("------------------------------------------------------------------")
        print("Trial: ",trial_num )
        print("Total number of words: ", len(word_list))
        print("------------------------------------------------------------------")
        print("\n")
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
        

            ###-- Calculating the scores to show effect of words
            if i>0:  #Calculated only after the subject has read two words
                if word in env.emotion_words:
                    if prev_word in env.emotion_words:
                        word_count['emo_emo'][0]+=1
                        word_count['emo_emo'][1]+=response_time
                    else:
                        word_count['emo_neut'][0]+=1
                        word_count['emo_neut'][1]+=response_time
                else:
                    if prev_word in env.emotion_words:
                        word_count['neut_emo'][0]+=1
                        word_count['neut_emo'][1]+=response_time
                    else:
                        word_count['neut_neut'][0]+=1
                        word_count['neut_neut'][1]+=response_time
    print("------------------------------------------------------------------")
    print("\n")
    print("Average response time (in seconds): ")
    print("------------------------------------------------------------------")
    print("Emotion word | Emotion word : " , word_count['emo_emo'][1]/word_count['emo_emo'][0])
    print("Neutral word | Emotion word : " , word_count['emo_neut'][1]/word_count['emo_neut'][0])
    print("Emotion word | Neutral word : " , word_count['neut_emo'][1]/word_count['neut_emo'][0])
    print("Neutral word | Neutral word : " , word_count['neut_neut'][1]/word_count['neut_neut'][0])
    


if __name__=='__main__':
    Experiment()
