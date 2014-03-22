#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# # LING 572 HW3 Multinomial Classifier
# Use a model file to classify training and testing data.
# Args: training, testing, model, sys_out > acc

import sys
import re
import math

def classify(vectors_file, class_probs, term_class_probs, term_count):
    ''' Classify the vectors in vectors_file, output to stdout and out_file. '''
    
    doc_count = 0.0
    # Initialize confusion matrix.
    matrix = dict( [(x, {}) for x in class_probs] )
    for c in class_probs:
        for c2 in class_probs:
            matrix[c][c2] = 0

    # Process each vector.
    for vector in vectors_file.readlines():
        doc_count += 1
        results = {}
        for c in class_probs:
            results[c] = class_probs[c]
        info = re.match(r'^([\S]+) ([\S]+) ', vector)
        instance = info.group(1)
        true_class = info.group(2)
        doc_terms = re.findall(r'([A-Za-z]+) ([0-9]+)', vector)
        for term in doc_terms:
            for c in class_probs:
                if (term[0], c) in term_class_probs:
                    results[c] += (float(term[1]) * term_class_probs[(term[0], c)])
        results_list = results.items()
        results_list.sort(lambda x,y:cmp(x[1],y[1]), reverse=True) # sort by probabilities, highest first
        underflow = -1.0 * results_list[0][1] # highest logprob
        output_list = []
        #convert from log10 while preventing overflow and underflow
        den = 0.0
        for i in results_list:
            den += 10**(i[1]+underflow)
        for i in results_list:
            num = 10**(i[1] + underflow)
            prob = num / den
            output_list.append((i[0], prob))
        
        # output for vector
        output_list.sort(lambda x,y:cmp(x[1],y[1]), reverse=True) # sort by probabilities
        out = instance + ' ' + true_class
        for i in output_list:
            out += ' ' + i[0] + ' ' + str(i[1])
        SYS_OUT.write(out + '\n')
        matrix[true_class][output_list[0][0]] += 1 # fill in matrix

    correct = 0.0
    print 'Confusion matrix for ' + vectors_file.name + ':'
    print 'row is the truth, column is the system output'
    print ''
    sys.stdout.write('\t\t')
    for c in class_probs:
        sys.stdout.write(' ' + c)
        correct += matrix[c][c]
    sys.stdout.write('\n')
    for c in class_probs:
        sys.stdout.write(c)
        for c2 in class_probs:
            sys.stdout.write(' ' + str(matrix[c][c2]))
        sys.stdout.write('\n')
    print ''
    print vectors_file.name + ' accuracy: ' + str(correct / doc_count)
    print ''


# Read file names from arguments.
training = open(sys.argv[1])
testing = open(sys.argv[2])
model_file = open(sys.argv[3])
SYS_OUT = open(sys.argv[4], 'w')

classes = []
term_count = {}

# Grab data from model_file.
class_prob = {}
term_class_prob = {}

text = model_file.read()
class_data = re.findall(r'^(\S+) \S+ (\S+)\n', text, re.M)
for c in class_data:
    class_prob[c[0]] = float(c[1])
    classes.append(c[0])
term_data = re.findall(r'^(\S+) (\S+) (\S+) (\S+)\n', text, re.M)
# t0:term, t1:class, t2:prob, t3:logprob
for t in term_data:
    term_class_prob[(t[0], t[1])] = float(t[3]) # logprob of t,c
    term_count[t[0]] = ''

# Output to acc
sys.stdout.write('class_num=' + str(len(classes)) + ' feat_num=' + str(len(term_count)) + '\n')

# Classify training and testing data, output results to sys_out.
SYS_OUT.write('%%%%% training data: \n')
classify(training, class_prob, term_class_prob, term_count)
SYS_OUT.write('\n\n%%%%% test data: \n')
classify(testing, class_prob, term_class_prob, term_count)


