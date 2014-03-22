#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# # LING 572 HW3 Multinomial Learner
# Create a model file based on training data.
# Args: training file, P_delta, Cond_delta, model file

import sys
import re
import math

# Read file names from arguments.
training = open(sys.argv[1])
P_DELTA = float(sys.argv[2])
COND_DELTA = float(sys.argv[3])
model_file = open(sys.argv[4], 'w')


classes = {}
terms = {}
Z = {}
V = 0

# Convert training vector into vector list for ease of processing. Count terms and classes.
vector_list = []
for line in training.readlines():
    v = ['', {}]  # represents vector: ['class of vector', {terms in vector}]
    v[0] = re.match(r'^[\S]+ ([\S]+) ', line).group(1) # class name
    if v[0] not in classes:
        classes[v[0]] = 1
        Z[v[0]] = 0
    else:
        classes[v[0]] += 1
    features = re.findall(r'([A-Za-z]+) ([0-9]+)', line) # (term, count) in vector
    for f in features:
        terms[f[0]] = ''
        Z[v[0]] += int(f[1])
        v[1][f[0]] = int(f[1])
    vector_list.append(v)

vector_count = len(vector_list)
V = len(terms)

# Gather term counts per class.
term_class_count = {}
for v in vector_list:
    for term in terms:
        if term in v[1]:
            if (term, v[0]) in term_class_count:
                term_class_count[(term, v[0])] += v[1][term]
            else:
                term_class_count[(term, v[0])] = v[1][term]

# Calculate and store probabilities.
term_class_prob = {}
for t in terms:
    for c in classes:
        top = COND_DELTA + term_class_count.get((t, c), 0)
        bottom = (COND_DELTA * V) + Z[c]
        term_class_prob[(t, c)] = top / float(bottom)


# Output to model file.
for c in classes:
    top = P_DELTA + classes[c]
    bottom = float((P_DELTA*len(classes)) + vector_count)    
    prob = top / bottom
    logprob = 0.0
    if prob != 0:
        logprob = math.log10(prob)
    model_file.write(c + ' ' + str(prob) + ' ' + str(logprob) + '\n')
for c in classes:
    for t in terms:
        prob = term_class_prob[(t, c)]
        logprob = math.log10(prob)
        model_file.write(t+ ' ' + c + ' ' + str(prob) + ' ' + str(logprob) + '\n')


