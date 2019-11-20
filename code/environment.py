import pickle, random
from lexicon import read_data


class Environment:
    def __init__(self, lexicon_fname='Micro-WNOp-data.txt'):
        self.lexicon=read_data(lexicon_fname)   # list of lists, each sub list being [word, positive_score, negative_score, objective_score]
        self.emotion_words, self.neutral_words = [], []            
        self.colours = ["red", "blue", "yellow", "green", "orange", 
                        "brown", "cyan", "pink", "grey", "purple"]  # font colour that will be randomly assigned to each word in the test set

        self.classify_words_in_lexicon()   
    
    def classify_words_in_lexicon(self, class_threshold=0.5):
        '''
        Groups the words in the WN-Micro-Op lexicon to emotion and neutral words
        '''
        for l in self.lexicon:
            if l[1] >= class_threshold or l[2] >= class_threshold:
                # self.emotion_words[l[0]] = l[1:]
                words=l[0].split(" ")
                for w in words:
                    self.emotion_words.append(w)
            else:
                # self.neutral_words[l[0]] = l[1:]
                words=l[0].split(" ")
                for w in words:
                    self.neutral_words.append(w)
                #self.neutral_words.append(l[0])


    def get_trial_set_mixed(self, num_of_words=30):
        '''
        Return a test set for Experiment Design - "mixed" (the stimuli are presented in one block in which emotion and neutral words 
                    are intermixed in the same list)
        param num_of_words number of words to select for the test set
        '''
        final_test_set = []
        emotion_words_set, neutral_words_set = set(self.emotion_words), set(self.neutral_words)  
        i = 0    
        while i < num_of_words:
            group_picker = random.random()
            if group_picker >= 0.5:
                emotion_word_index = random.randint(0,len(self.emotion_words)-1)
                if self.emotion_words[emotion_word_index] in emotion_words_set:     # if randomly picked word being picked hasn't been picked in this round yet
                    emotion_words_set.remove(self.emotion_words[emotion_word_index])
                    font_colour_current_word = self.get_random_colour()
                    final_test_set.append((self.emotion_words[emotion_word_index], font_colour_current_word))
                    i += 1                                  # added a word to the final_list, increment counter
                elif len(emotion_words_set) is 0:           # exhausted all emotion words, reset the set so that words can be repeated
                    emotion_words_set = set(self.emotion_words)
                else:                                       # randomly picked word has already been picked before in this round 
                    continue                                
            else:
                neutral_word_index = random.randint(0,len(self.neutral_words)-1)
                if self.neutral_words[neutral_word_index] in neutral_words_set:     # if randomly picked word being picked hasn't been picked in this round yet
                    neutral_words_set.remove(self.neutral_words[neutral_word_index])
                    font_colour_current_word = self.get_random_colour()
                    final_test_set.append((self.neutral_words[neutral_word_index], font_colour_current_word))
                    i += 1                                  # added a word to the final_list, increment counter
                elif len(neutral_words_set) is 0:           # exhausted all neutral words, reset the set so that words can be repeated
                    emotion_words_set = set(self.emotion_words)
                else:                                       # randomly picked word has already been picked before in this round 
                    continue                                
        return final_test_set
        

    def get_trial_set_blocked(self, num_of_words=30, block_pattern="nen", block_size=10):
        '''
        Return a test set for Experiment Design - "blocked" (the stimuli are presented in separate blocks of trials defined by word valence)
        param num_of_words number of words to select for the test set
        param num_of_words number of words in the test set
        param block_pattern string consisting of characters n/e, meaning neutral/emotional; blocks will be generated following this pattern
        param block_size size of each neutral/emotion block of words
        '''
        final_test_set =[]
        if set(block_pattern) != {'e', 'n'}:
            print(f'invalid block pattern requested {block_pattern}, must contain only {"e", "n"}')
            return final_test_set
        while block_pattern is not '':
            if block_pattern[0] == 'n':
                word_set = self.neutral_words
            elif block_pattern[0] == 'e':
                word_set = self.emotion_words
            
            current_word_set = set(word_set)      # set to maintain which words has not been seen yet
            max_index = len(word_set)
            i = 0
            while i < block_size:
                word_index = random.randint(0,max_index-1)
                if word_set[word_index] in current_word_set:
                    current_word_set.remove(word_set[word_index])
                    font_colour_current_word = self.get_random_colour()
                    final_test_set.append((word_set[word_index], font_colour_current_word))
                    i += 1                          # added a word to the final_list, increment counter
                elif len(current_word_set) is 0:    # exhausted all neutral words, reset the set so that words can be repeated
                    current_word_set = set(word_set)
                else:                               # randomly picked word has already been picked before in this round 
                    continue
                
            block_pattern = block_pattern[1:]
        return final_test_set

    
    def get_random_colour(self):
        return self.colours[random.randint(0,len(self.colours)-1)]


    

