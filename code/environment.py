import pickle, random


class Environment:
    def __init__(self, lexicon_fname):
        with open(lexicon_fname, 'rb') as f:
            self.lexicon = pickle.load(f)       # list of lists, each sub list being [word, positive_score, negative_score, objective_score]
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
                self.emotion_words.append(l[0])
            else:
                # self.neutral_words[l[0]] = l[1:]
                self.neutral_words.append(l[0])


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
            i += 1
            group_picker = random.random()
            if group_picker >= 0.5:
                emotion_word_index = random.randint(0,len(self.emotion_words))
                if self.emotion_words[emotion_word_index] in emotion_words_set:     # if randomly picked word being picked hasn't been picked in this round yet
                    emotion_words_set.remove(self.emotion_words[emotion_word_index])
                    font_colour_current_word = self.get_random_colour()
                    final_test_set.append((self.emotion_words[emotion_word_index], font_colour_current_word))
                elif len(emotion_words_set) is 0:           # exhausted all emotion words, reset the set so that words can be repeated
                    emotion_words_set = set(self.emotion_words)
                    i -= 1          # did not add a word to final test set, decrement counter i
                else:               # randomly picked word has already been picked before in this round 
                    i -= 1          # did not add a word to final test set, decrement counter i
            else:
                neutral_word_index = random.randint(0,len(self.neutral_words))
                if self.neutral_words[neutral_word_index] in neutral_words_set:     # if randomly picked word being picked hasn't been picked in this round yet
                    neutral_words_set.remove(self.neutral_words[neutral_word_index])
                    font_colour_current_word = self.get_random_colour()
                    final_test_set.append((self.neutral_words[neutral_word_index], font_colour_current_word))
                elif len(neutral_words_set) is 0:        # exhausted all neutral words, reset the set so that words can be repeated
                    emotion_words_set = set(self.emotion_words)
                    i -= 1      # did not add a word to final test set, decrement counter i
                else:           # randomly picked word has already been picked before in this round 
                    i -= 1      # did not add a word to final test set, decrement counter i
        return final_test_set
        

    def get_trial_set_bocked(self, num_of_words=30):
        '''
        Return a test set for Experiment Design - "blocked" (the stimuli are presented in separate blocks of trials defined by word valence)
        param num_of_words number of words to select for the test set
        '''

        pass


        
    def reset_sets(self):
        return set(self.emotion_words), set(self.neutral_words)

    
    def get_random_colour(self):
        return self.colours[random.randint(0,len(self.colours))]


    

