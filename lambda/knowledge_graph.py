import pandas as pd
import spacy
import itertools
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

import warnings
warnings.filterwarnings("ignore", message=r"\[W007\]", category=UserWarning)

#pd.set_option('display.max_colwidth', 200)

#nltk.download('stopwords')
#nltk.download('punkt')

def read_load_file(file_name):
    text = pd.read_json(file_name)
    
    load_file(text) # Parameter used to be 'text'

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

def perform_nlp(data):
    nlp_model = spacy.load("en_core_web_md")
    nlp_results = []

    for vals in data:
        nlp_results.append([vals[0], nlp_model(vals[1]), nlp_model(vals[2])])

    return nlp_results

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
'''