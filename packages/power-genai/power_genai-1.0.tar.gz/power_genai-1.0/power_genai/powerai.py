from nltk.corpus import wordnet
import re
import hnswlib
from thematch import match as powermatch

def lemma(sentence):
	sentence = sentence.split()
	final = []
	for word in sentence:
		if len(word) > 3 and word.isalpha():
			for tag in ['n','v','r']:
				word = wordnet.morphy(word,tag) or word 
		final.append(word)
	sentence = " ".join(final)
	return sentence	
	
def custom_cosine_similarity(loaders, query, query_embedding, top_n=25):	
	final = {}
	if len(preprocess(query)) == 0:
		return final	
	labels, distances = loaders.model_embeddings.knn_query(query_embedding, k = top_n)
	distances = [float(100-(d*100)) for d in distances[0]]
	results = dict(zip([loaders.model_labelmap[l] for l in labels[0]], distances))
	results = {q:round(score,2) for q,score in results.items() if score>85}		
	for msn,score in results.items():
		match_score = powermatch.token_set_ratio(query, loaders.msn_data[msn])
		if score <=98 and match_score > 90:
			final[msn] = score+1
		elif score>=98.5 and match_score==100:
			final[msn] = 100
		elif match_score>50:
			final[msn] = score
	final = dict(sorted(final.items(), key=lambda item: item[1], reverse=True))
	return final
	
def unspsc_code_name(loaders, code):
	unspsc_code = unspsc_name = ""
	code = re.sub(r'[^a-z0-9]', '', code)
	temp = [u for u in loaders.unspsc_tree if u in code]
	if len(temp) == 1:
		unspsc_code = temp[0]
		unspsc_name = loaders.unspsc_id_name[unspsc_code]
	return unspsc_code, unspsc_name 