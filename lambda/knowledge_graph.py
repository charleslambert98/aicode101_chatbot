import pandas as pd
import spacy
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

# Blocks console warning regarding vectors in a smaller library
import warnings
warnings.filterwarnings("ignore", message=r"\[W007\]", category=UserWarning)

#pd.set_option('display.max_colwidth', 200)

# Only one run required of the below code, if already run on EC2 instance, not required
#nltk.download('stopwords')
#nltk.download('punkt')

# Handles reading file from EFS
def read_load_file(file_name):
    text = pd.read_json(file_name)
    
    load_file(text) 

'''
Description: Gathers only necessary data for the NLP process, commented section handles stopword 
removal. WARNING: Stopword removal takes a large amount of time, but only slightly improves 
accuracy

Parmeters: file_content - Loaded in JSON file
Returns: data - important data from 'file_content'
'''
def load_file(file_content):
    data = []

    for i in file_content:
        '''
        description_tokens = word_tokenize(file_content[i]['description'])
        filtered_desc_tokens = [word for word in description_tokens if not word in stopwords.words()]
        filtered_description = (" ").join(filtered_desc_tokens)

        title_tokens = word_tokenize(file_content[i]['title'])
        filtered_title_tokens = [word for word in title_tokens if not word in stopwords.words()]
        filtered_title = (" ").join(filtered_title_tokens)

        data.append([i, filtered_description, filtered_title])
        '''
        data.append([i, file_content[i]['description'], file_content[i]['title']])

    return data

'''
Description: Breaks down each word in the data into appropriate tokenized/vectored forms

Parameters: data - JSON/Dictionary containing step number, description, and title
Returns: nlp_results - tokenized/vectored 'data'
'''
def perform_nlp(data):
    nlp_model = spacy.load("en_core_web_md")
    nlp_results = []

    for vals in data:
        nlp_results.append([vals[0], nlp_model(vals[1]), nlp_model(vals[2])])

    return nlp_results

'''
Description: Gathers a similarity value between each description/title of each step and provides 
and appropriate weight based off of the average value of the similarity for the description and 
the title. Each step will have a similarity factor with another step. The top 2 results will be 
selected and added to the resultant dictionary. Note: This can be modified to return more results
by changing the 'while i < 2' section.

Parameters: nlp_data - tokenized/vectored data 
Returns: results_dict - dictionary containing the step number and it's most similar steps
'''
def gather_similarity(nlp_data):
    similar_dict = {}
    avg_desc_similarity = 0
    avg_title_similarity = 0
    count = 0

    for step_1, step_2 in itertools.combinations(nlp_data, 2):
        curr_desc_similarity = step_1[1].similarity(step_2[1])
        curr_title_similarity = step_1[2].similarity(step_2[2])

        avg_desc_similarity = ((avg_desc_similarity * count) + curr_desc_similarity) / (count + 1)
        avg_title_similarity = ((avg_title_similarity * count) + curr_title_similarity) / (count + 1)
        count += 1

        similarity_factor = ((avg_desc_similarity * curr_desc_similarity) + (avg_title_similarity * curr_title_similarity))
        if step_1[0] in similar_dict:
            similar_dict[step_1[0]].append([step_2[0], similarity_factor, step_2[2].text])
        else:
            similar_dict[step_1[0]] = [[step_2[0], similarity_factor, step_2[2].text]]

    results_dict = {}
    for key in similar_dict:
        i = 0
        while i < 2:
            if len(similar_dict[key]) < 2:
                break
            temp_best = [0, 0]
            for similarity in similar_dict[key]:
                if similarity[1] > temp_best[1]:
                    temp_best = similarity
            
            if key in results_dict:
                results_dict[key].append(temp_best)
            else:
                results_dict[key] = [temp_best]

            similar_dict[key].remove(temp_best)
            i += 1
    
    return results_dict
"""

'''
Description: Used to generate a visual of the knowledge graph created from the above processes.
It is NOT recommended this be used in Lambda. If you wish to use this function, make a copy of this
code and run it on a local machine.

Parameter: results - dictionary of steps and similarities
Returns: N/A - displays a plot containing the knowledge graph of the lesson
'''

def generate_visual(results):
    G = nx.Graph()

    for key in results:
        for val in results[key]:
            G.add_edge(key, val[0], weight=1/val[1])

    edges = G.edges()
    weights = [G[u][v] for u,v in edges]

    plt.figure(figsize=(10,10))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=800, edge_cmap=plt.cm.Blues, pos=pos, width=weights)
    plt.show()       
"""