#import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

#@st.cache_resource
#def load_summarizer():
    # """
    #Loads the Hugging Face summarization tokenizer and model explicitly.
    #We are using a smaller DistilBART model to save resources.
    #By loading the model directly instead of using `pipeline`, we bypass issues with missing pipeline tasks.
    #"""
    #model_name = "sshleifer/distilbart-cnn-12-6"
    #tokenizer = AutoTokenizer.from_pretrained(model_name)
    #model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    #return tokenizer, model
# Load model globally (only once)
#model_name = "sshleifer/distilbart-cnn-12-6"
#model_name = "facebook/bart-large-cnn"        # Best quality, slower
#model_name = "google/pegasus-xsum"             # Great for short summaries
model_name = "philschmid/bart-large-cnn-samsum" # Good for conversational text
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

"""def summarize_text(long_text: str) -> str:
    #put here three (")")
    #Generates a concise summary for the input text.
    #put here three (")")
    if not long_text or not long_text.strip():
        raise ValueError("Text to summarize cannot be empty.")
    
    input_length = len(long_text.split())
    if input_length < 20:
        return "Text is too short to summarize properly. Please provide a longer paragraph."
        
    max_len = min(130, max(20, input_length // 2))
    min_len = min(30, max(10, input_length // 4))

    #tokenizer, model = summarizer
    
    # Tokenize input
    inputs = tokenizer([long_text], max_length=1024, return_tensors="pt", truncation=True)
    
    # Generate summary tokens
    summary_ids = model.generate(
        inputs["input_ids"], 
        #num_beams=4, 
        #max_length=max_len, 
        #min_length=min_len, 
        #early_stopping=True
        max_length=100,       # Allow longer output
        min_length=40,        # Force more content
        num_beams=6,          # More beams = better search (was 4)
        length_penalty=1.0,   # Lower = shorter, Higher = longer (try 1.0)
        no_repeat_ngram_size=3,
        early_stopping=True,
        repetition_penalty=2.5  # ← ADD THIS: reduces repeated phrases
        )
    
    # Decode to text
    summary_text = tokenizer.decode(summary_ids[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)
    return summary_text.strip()"""
def chunk_text(text, max_words=200):
    words = text.split()
    return [" ".join(words[i:i+max_words]) 
            for i in range(0, len(words), max_words)]

def summarize_text(long_text: str) -> str:
    chunks = chunk_text(long_text)
    summaries = []
    
    for chunk in chunks:
        inputs = tokenizer([chunk], max_length=1024, 
                            return_tensors="pt", truncation=True)
        ids = model.generate(inputs["input_ids"],
                            max_length=100, min_length=30,
                            num_beams=4, early_stopping=True)
        summaries.append(tokenizer.decode(ids[0], 
                        skip_special_tokens=True))
    
    return " ".join(summaries)

if __name__ == "__main__":
    # Test block
    simulated_text = "Natural language processing (NLP) is an interdisciplinary subfield of computer science and linguistics. It is primarily concerned with giving computers the ability to support and manipulate human language. It involves processing natural language datasets, such as text corpora or speech corpora, using either rule-based or probabilistic (i.e. statistical and, most recently, neural network-based) machine learning approaches."
    try:
        #model_pack = load_summarizer()
        print(summarize_text(simulated_text)) #, #model_pack))
    except Exception as e:
        print(f"Error loading local model: {e}")
