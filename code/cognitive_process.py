from lexicon import read_data,test_subjects
import time

class Subject:
    def __init__(self, num_of_chunks=7, decay_factor=2):
        '''
        param num_of_chunks number of chunks is working memory
        param decay_factor rate at which the effect of previous words decay in the subject's memory
        '''
        # Subject specific characteristics
        self.decay_factor = decay_factor
        self.max_size_WM = num_of_chunks 
        self.filename='Micro-WNOp-data.txt'

        ## Short-term/Working memory parameters
        self.WM_response = []
        self.WM = [0] * self.max_size_WM   # working memory with num_of_chunk chunks
        self.emotion_scores = [0] * self.max_size_WM   # to keep a track of decaying emotional effect from words seen prior
        self.current_size_WM = 0        # to keep record of the current number of words in the WM 
        self.current_colour_perceived = "blank"     # represents the current visual perception
        self.lexicon=read_data(self.filename)
        
        ## Long-term memory parameters
        self.mental_lexicon=test_subjects(self.lexicon)     # individual lexicon with small alterations in scores to reflect personal experiences etc.
        self.LTM_known_colours = ["red", "blue", "yellow", "green", "orange", "brown", "cyan", "pink", "grey", "purple", 
                                "ivory", "magenta", "fuscia", "hazel", "gold", "amber", 
                                "cherry", "mahogany", "crimson", "scarlet", "mauve"]    
                                # colours that the subject can recognize by matching perception to that stored in long term memory
        

    def get_response_time(self, word):
        '''
        Calculate the response time based on effect of previously seen words
        '''
        res_time=self.get_weighted_word_score(word)
        time.sleep(res_time)
        return res_time

    def get_raw_word_score(self, word):
        '''
        Returns the emotion score associated with the word from the lexicon
        '''
        raw_word_score = 0
        # lookup associated score from lexicon (for now, later will incorporate polarity score of related words from SentiWordNet 3.0)
        for i in range(0,len(self.mental_lexicon)):
            if word in self.mental_lexicon[i][0]:
                raw_word_score= self.mental_lexicon[i][1] + self.mental_lexicon[i][2]
                break
        return raw_word_score

    def get_weighted_word_score(self, word):
        emotion_score = self.get_raw_word_score(word)
        for i in range(self.max_size_WM-1):
            emotion_score += self.emotion_scores[i] / ( (self.max_size_WM - i) * self.decay_factor)
        return emotion_score


    def read_display(self, stimulus):
        '''
        param stimulus <tuple> the word and associated colour, passed here as a tuple
        '''
        if self.current_size_WM >= self.max_size_WM:
            self.WM=self.WM[1:]
            self.emotion_scores=self.emotion_scores[1:]
            #self.current_size_WM -=1
        else:
            self.current_size_WM += 1

        self.WM.append(stimulus[0])
        self.emotion_scores.append(self.get_weighted_word_score(stimulus[0]))
        self.current_colour_perceived = stimulus[1]


    def is_colour_recognized(self, perceived_colour):
        return perceived_colour in self.LTM_known_colours


    def speak_current_colour(self):
        print(f'Subject response: {self.current_colour_perceived} \n\n')



    

    