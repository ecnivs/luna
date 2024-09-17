from googlesearch import search
from transformers import BartForConditionalGeneration, BartTokenizer

# Function to search Google and retrieve top results
def google_search(query, num_results=5):
    results = []
    for result in search(query, num_results=num_results):
        results.append(result)
    return results

# Function to summarize text using BART
def summarize_with_bart(text):
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(inputs['input_ids'], max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Example of combining search with summarization
if __name__ == "__main__":
    query = "Python programming tutorials"
    
    # Perform Google search
    results = google_search(query)

    # Summarize the search results
    for idx, result in enumerate(results):
        print(f"Result {idx + 1}: {result}")
        summary = summarize_with_bart(result)
        print(f"Summary: {summary}\n")


