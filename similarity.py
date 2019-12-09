
parent_link = []
child_link = []
child_blog_content = []
for i in range(10,20):
    links = " "
    url = blog_link[i]
    urlopen = urllib.request.urlopen(url)
    soup =BeautifulSoup(urlopen,'html.parser')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        content = link.get('href')
        parent_link.append(blog_link[i])
        child_link.append(content)

child_blog_content.append("permission denied")
for i in range(41,46):
    url = child_link[i]
    res = requests.get(url)
    html_page = res.content


    soup = BeautifulSoup(html_page, 'html.parser')

    text = soup.find_all(text=True)
    set([t.parent.name for t in text])

    output = ''
    blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
    'style',
	'script',
    '[document]',
 
	# there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    child_blog_content.append(output)
    
parent_blog_content = []
for i in range(0,46):
    url = parent_link[i]
    res = requests.get(url)
    html_page = res.content


    soup = BeautifulSoup(html_page, 'html.parser')

    text = soup.find_all(text=True)
    set([t.parent.name for t in text])

    output = ''
    blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
    'style',
	'script',
    '[document]',
 
	# there may be more elements you don't want, such as "style", etc.
    ]

    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    parent_blog_content.append(output)

import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt') # if necessary...


stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]
percent_similarity = []
for i in range(0,46):
    percent_similarity.append(cosine_sim(parent_blog_content[i],child_blog_content[i])*100)

common_words = []
for i in range(0,46):
    common = " "
    for ch in parent_blog_content[i].split():
        for ch2 in child_blog_content[i].split(): 
            if ch == ch2:
                common = common + ch + "  "
    common_words.append(common)
common_text = []
from collections import Counter 
  
def remov_duplicates(input): 
  
    input = input.split(" ") 
  
    for i in range(0, len(input)): 
        input[i] = "".join(input[i]) 
    UniqW = Counter(input) 
  
    s = " ,".join(UniqW.keys()) 
    common_text.append(s)
  
for i in range(0,46):
    input = common_words[i]
    remov_duplicates(input) 
    
    
#convert the lists into a dataframe merging them together
df = pd.DataFrame({'Parent Link':parent_link,'Child_link':child_link,'Common Words':common_text,'Percentage Similarity':percent_similarity}) 

#dataframe to csv
df.to_csv('D:\web-scraping\Similarity.csv',index = False)





