from collections import defaultdict
from nltk.util import ngrams
from nltk.corpus import wordnet
import re
def tfidf(id_terms, cat_product_count_filtered):	
	term_max_freq = defaultdict(int)
	for terms_count in id_terms.values():
		for term, frequency in terms_count.items():
				term_max_freq[term] = max(term_max_freq[term],frequency)
	tf = {}
	idf = {}
	for cat_id, terms_count in id_terms.items():
		tf[cat_id] = {term:frequency/cat_product_count_filtered[cat_id] for term,frequency in terms_count.items()}
		idf[cat_id] = {term:frequency/term_max_freq[term] for term,frequency in terms_count.items()}
	del term_max_freq
	tf = {cat_id : tf_within_cat for cat_id,tf_within_cat in tf.items() if tf_within_cat}
	idf = {cat_id : idf_cat for cat_id,idf_cat in idf.items() if idf_cat}	
	tf_idf = {cat_id: {term:(tf[cat_id][term] + idf[cat_id][term]) for term in terms_count} for cat_id,terms_count in id_terms.items()}
	del tf
	del idf
	tf_idf = {cat_id : term_freq for cat_id,term_freq in tf_idf.items() if term_freq}	
	del id_terms
	term_max_tfidf = defaultdict(int)
	for terms_count in tf_idf.values():
		for term, frequency in terms_count.items():
				term_max_tfidf[term] = max(term_max_tfidf[term],frequency)
	tf_idf = {cat_id : {term:round(100*term_freq/term_max_tfidf[term],2) for term , term_freq in term_freq.items()} for cat_id,term_freq in tf_idf.items()}	
	tf_idf = {cat_id : {term:score for term , score in term_freq.items() if score>1} for cat_id,term_freq in tf_idf.items()}	
	return(tf_idf)

def create_cbow(docs):
	indexes = defaultdict(set)
	dlist = list(docs.items())
	for _id, doc in dlist:
		for word in doc:
			indexes[word].add(_id)	
	return indexes
	
def similarity_knn(combs, loaders):
	matched = {}
	ordered = {}
	if len(combs[0])>1:
		for combination in combs:			
			lst = [get_cbow(c) for c in combination]
			lst.sort(key = len, reverse=True)
			smallest_set = lst.pop()
			combinations_matched_temp = len(smallest_set.intersection(*lst))
			if combinations_matched_temp > 0:
				pairs = [" ".join(sorted(n)) for n in ngrams(combination, 2)]		
				matched[tuple(combination)] = combinations_matched_temp
				ordered[tuple(combination)] = sum([loaders.bigrams_ordered[n] for n in pairs if n in loaders.bigrams_ordered])	
		if len(matched)>0 and len(ordered)>0:
			matched_max = max(matched.values())
			ordered_max = max(ordered.values())
			if matched_max > 0 and ordered_max > 0: 
				matched = {comb:round(50*score/matched_max,2) for comb,score in matched.items()}
				ordered = {comb:round(50*score/ordered_max,2) for comb,score in ordered.items()}		
				matched = {comb:score+ordered[comb] for comb,score in matched.items()}
	else:
		matched = {tuple(combination):len(get_cbow(combination[0])) for combination in combs}
	if matched:
		most_frequent = max(matched, key= lambda x: matched[x])
		return list(most_frequent)	   
	else:
		return list()
		
def lemma_excluding_brand(word, loaders):
	original_word = word	
	if len(word) > 3 and word not in loaders.brand_mapping:
		number = ""
		seg = re.compile("(^\d+\.*\d*)([a-z]+$)").match(word)
		if seg:
			number = seg.groups()[0]
			word = seg.groups()[1]
		for tag in loaders.morphy_pos_tags:
			word = wordnet.morphy(word,tag) or word
		temp = re.sub('s$', '', word)
		if len(word)>2 and temp[-1]!="s":
			word = temp
		word = number+word
		if word in loaders.brand_mapping:
			word = original_word
	return word
def lemma(word, loaders):
	original_word = word	
	if len(word) > 3:
		number = ""
		seg = re.compile("(^\d+\.*\d*)([a-z]+$)").match(word)
		if seg:
			number = seg.groups()[0]
			word = seg.groups()[1]
		for tag in loaders.morphy_pos_tags:
			word = wordnet.morphy(word,tag) or word
		temp = re.sub('s$', '', word)
		if len(word)>2 and temp[-1]!="s":
			word = temp
		word = number+word
	return word
def lemma_excluding_brandcategory(word, loaders):
	original_word = word
	if len(word) > 3 and word not in loaders.category_brand_words_list:
		number = ""
		seg = re.compile("(^\d+\.*\d*)([a-z]+$)").match(word)
		if seg:
			number = seg.groups()[0]
			word = seg.groups()[1]
		for tag in loaders.morphy_pos_tags:
			word = wordnet.morphy(word,tag) or word
		temp = re.sub('s$', '', word)
		if len(word)>2 and temp[-1]!="s":
			word = temp
		word = number+word
		if word in loaders.category_brand_words_list:
			word = original_word
	return word
	
def clean_text(input_text, loaders):
	text = input_text.lower() 
	text = re.sub(r'\n', ' ', text) 
	text = text.replace('..','.').replace('. ', ' ').replace("- "," ").replace(" -"," ")
	text = re.sub(r'[,:;{}?!/_\$@<>()\\#%+=\[\]\']',' ', text)
	text = re.sub(r'\d+\.*\d*\w*x\d+\.*\d*\w*', ' ', text, flags=re.IGNORECASE)		
	text = re.sub(r'[^a-z0-9.*\- ]', '', text)
	text = text.rstrip('.') 
	text = " ".join([t.replace("."," ") if t.replace(".","").isalpha() else t for t in text.split()])
	text = " ".join([t.replace("-"," ") if t.replace("-","").isalnum() else t for t in text.split()])
	text = " ".join([t.replace("*","x") if t.replace(".","").replace("*","").isnumeric() else t.replace("*","") for t in text.split()])
	text = ' '.join([t for t in text.split() if t not in loaders.stopwords])
	return text
	
def clean_input(input_text):
	text = " ".join(input_text)
	text = text.replace('..','.').replace('. ', ' ').replace("- "," ").replace(" -"," ")
	text = re.sub(r"\s+"," ", text, flags = re.I)
	text = re.sub(r'([a-z])\1+', r'\1\1', text)
	text = re.sub(r'[,:;{}?!/_\$@<>()\\#%+=\[\]\']', ' ',text)
	text = " ".join([t.replace('"',' inch') if t.replace(".","").replace('"','').isnumeric() else t for t in text.split()])		
	text = re.sub(r'[^a-z0-9.*\- ]', '', text)	
	text = text.rstrip('.')	
	text = " ".join([t.replace("."," ") if t.replace(".","").isalpha() else t for t in text.split()])
	text = " ".join([t.replace("-"," ") if t.replace("-","").isalnum() else t for t in text.split()])
	text = " ".join([t.replace("*","x") if t.replace(".","").replace("*","").isnumeric() else t.replace("*","") for t in text.split()])
	text = text.split()
	return text	