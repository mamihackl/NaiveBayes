#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# # LING 572 HW3 Multi-variate Bernoulli Learner
# Create a model file based on training data.
# Args: training file, P_delta, Cond_delta, model file

 
# Imports

import sys
import re
import math

# Classes

class Vector:
    ''' an object representing a single document or instance '''
    name = '' # instance name
    true_class = '' # gold standard class label
    sys_class = '' # system assigned class label
    features = False # data structure containing the vector's features
    
    def __init__(self, name, clss, features):
        self.name = name
        self.true_class = clss
        self.features = features
        
class Vector_List:
    ''' An object containing Vector objects and associated info.
        This object is customized according to task (e.g. binary or not). 
        MB learner is binary, so features is a set rather than dictionary of
        counts per feature.'''
    vlist = []
    classes = {} # dictionary containing class counts
    term_set = set() # set containing all terms/features from vectors in list
    term_per_class = {} # dictionary of counts using (feature, class) as key
    
    def add_vectors(self, data_file):
        ''' take an open data file, create a vector per line, add it to list '''
        for line in data_file.readlines():
            feature_set = set()
            n, c = re.match(r'(^[\S]+) ([\S]+) ', line).group(1,2)
            features = re.findall(r'([A-Za-z]+) [0-9]+', line) 
            for f in features:
                feature_set.add(f)
                self.term_set.add(f)
                if (f, c) in self.term_per_class:
                    self.term_per_class[(f,c)] += 1
                else:
                    self.term_per_class[(f,c)] = 1
            vector = Vector(n, c, feature_set)
            if c in self.classes:
                self.classes[c] += 1
            else:
                self.classes[c] = 1
            self.vlist.append(vector)
     
    def output_to_model(self, p_delta, cond_delta, model_file):
        ''' Output probabilities to model file using deltas for smoothing. '''
        # prior prob
        for c in self.classes:
            top = p_delta + self.classes[c] 
            bottom = (p_delta * len(self.classes)) + len(self.vlist)
            prob = top / float(bottom)
            logprob = 0.0
            if prob != 0:
                logprob = math.log10(prob)
            model_file.write(c + ' ' + str(prob) + ' ' + str(logprob) + '\n')
        # cond prob
        for c in self.classes:
            for t in self.term_set:
                top = cond_delta + self.term_per_class.get((t,c), 0)
                bottom = (2 * cond_delta) + self.classes[c]
                prob = top / float(bottom)
                logprob = 0.0
                if prob != 0:
                    logprob = math.log10(prob)
                model_file.write(t+' '+c+' '+ str(prob)+' '+str(logprob)+'\n')
        

# Main

training = open(sys.argv[1])
P_DELTA = float(sys.argv[2])
COND_DELTA = float(sys.argv[3])
model_file = open(sys.argv[4], 'w')

training_vectors = Vector_List()
training_vectors.add_vectors(training)
training_vectors.output_to_model(P_DELTA, COND_DELTA, model_file)

