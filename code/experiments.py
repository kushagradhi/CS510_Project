from environment import Environment
from cognitive_process import Subject
from lexicon import read_data
import matplotlib.pyplot as plt
import time

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

def plot_mixed(metrics):
    num_rows = int(len(metrics)/2) + len(metrics)%2
    num_cols = 2 if len(metrics) >= 2 else 1
    fig, axes = plt.subplots(figsize=(8*num_cols,8*num_rows), nrows=num_rows, ncols=num_cols, squeeze=False)
    # fig.tight_layout()
    trial = 0
    for row in range(num_rows):    
        for col in range(num_cols): 
            axes[row][col].plot([i+1 for i in range(len(metrics[trial]["stock_score"]))], metrics[trial]["stock_score"], color="#66c2a5")
            axes[row][col].plot([i+1 for i in range(len(metrics[trial]["subject_score"]))], metrics[trial]["subject_score"], color="#fc8d62")
            axes[row][col].plot([i+1 for i in range(len(metrics[trial]["response_time"]))], metrics[trial]["response_time"], color="#8da0cb")
            axes[row][col].set_xticks([i+1 for i in range(len(metrics[trial]["stock_score"]))])
            axes[row][col].set_xticklabels(['N' if metrics[trial]["type"][w]==0 else 'E' for w in range(len(metrics[trial]["type"]))], fontsize=8)
            axes[row][col].set_xlabel('word type')
            axes[row][col].set_ylabel('Scores and Response time')
            axes[row][col].set_title('Trial' + str(trial+1))
            axes[row][col].legend(['stock_score', 'subject_score', 'response_time'], loc='upper left')
            trial += 1
            if trial >= len(metrics):
                break

    plt.savefig(str(time.time()) + ".png")  
    plt.show()
       

def Experiment(type_of_test='mixed',  num_of_words=30, number_of_trials=7, block_pattern="nen", block_size=10):

    # Response time for mixed
    if type_of_test=='mixed':
        word_count = {'emo_neut':[0,0.0],'neut_emo':[0,0.0],'emo_emo':[0,0.0],'neut_neut':[0,0.0]}
        metrics_record = [{"type":[], "stock_score":[], "subject_score":[], "response_time":[]} for n in range(number_of_trials)]   
                            # type_of_word(0=neut, 1=emo), stock_word_score, subject_word_score, response_time
    else:
        #word_count=dict.fromkeys(range(num_of_words/block_size))
        word_count = {i:0 for i in range(int(num_of_words/block_size))}

    # Generate test subject
    test_subject = Subject()
    # Create environment
    env = Environment()
    print("Test begins")

    # Running the trials:
    for trial_num in range(number_of_trials):
        # test_subject.WM = [0 for i in range(test_subject.max_size_WM)]
        # test_subject.WM_response = []
        test_subject.WM = [0 for i in range(test_subject.max_size_WM)]   # working memory with num_of_chunk chunks
        test_subject.emotion_scores = [0 for i in range(test_subject.max_size_WM)]   # to keep a track of decaying emotional effect from words seen prior
        test_subject.current_size_WM = 0        # to keep record of the current number of words in the WM 
        test_subject.current_colour_perceived = "blank"
    #Generate word list (will be different for every trial):
        if type_of_test=='mixed':
            word_list = env.get_trial_set_mixed(num_of_words)
        else: 
            word_list = env.get_trial_set_blocked()

        prev_word = None
        #Running the experiment:
        print("------------------------------------------------------------------")
        print("Trial: ",trial_num+1 )
        print("Total number of words: ", len(word_list))
        print("------------------------------------------------------------------")
        print("\n")
        block_num = 0
        for i in range(0,len(word_list)):
            word_type = 'Neutral word'
            if i>0:
                prev_word = word_list[i-1][0]
            word = word_list[i][0]
            color = word_list[i][1]

            if word in env.emotion_words:
                word_type='Emotion word'
            print("Trial #" + str(trial_num+1) + " Word #" + str(i+1) + " : " + word[:-2]  + " in font color " + color  + " [ " + word_type + " ] ")
            #Test subject reads the word
            test_subject.read_display(word_list[i])
            #Time calculated for subject to respond
            response_time = test_subject.get_response_time(word)
            # print(test_subject.WM)
            # print(test_subject.emotion_scores)
            #Subject speaks out the color
            test_subject.speak_current_colour()
            print("Time taken (in seconds): " + str(response_time))
            ## Checking if the subject has recognized the font color correctly
            val = test_subject.is_colour_recognized(test_subject.current_colour_perceived)
            print("Answer is " + str(val))
            print("------------------------------------------------------------------")
        
            if type_of_test=='mixed':
                if i>0:
                    word_count = cal_response_mixed(word_count,word,prev_word,env.emotion_words,response_time)
                metrics_record[trial_num]["type"].append(1 if word_type == "Emotion word" else 0)
                metrics_record[trial_num]["stock_score"].append(env.get_raw_word_score(word))
                metrics_record[trial_num]["subject_score"].append(test_subject.get_raw_word_score(word))
                metrics_record[trial_num]["response_time"].append(response_time)
            
            else:
                if (i)%(block_size)==0 and (i)>0:
                    print("Increment at ", i)
                    block_num += 1
                word_count[block_num] += response_time
                #word_count[block_num].append(response_time)

    if type_of_test=="mixed":
        # print(metrics_record)
        plot_mixed(metrics_record)


    if type_of_test=='mixed':
        print_mixed(word_count)   
    else:
        print_block(word_count,block_pattern,block_size)

if __name__=='__main__':

    #default: num_of_words=30, block_pattern="nen", block_size=10

    Experiment(type_of_test='mixed', num_of_words=30, number_of_trials=8)
