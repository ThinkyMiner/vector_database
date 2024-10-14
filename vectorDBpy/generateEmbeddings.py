import PyPDF2
import google.generativeai as gemini
import json

# Replace with your Gemini API key
gemini.configure(api_key="AIzaSyC1xOKaJPP0p5Y493lIQ5HnKgfx93Y6bj0")

# Function to read PDF content, split into sentences, and generate embeddings
def process_pdf(pdf_path, output_file):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)

        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Split text into sentences
    sentences = text.split('.')

    # Generate embeddings
    results = []
    for sentence in sentences:
        stripped_sentence = sentence.strip()
        if stripped_sentence:  # Check if the sentence is not empty
            # Generate embeddings using the embeddings-004 model
            embedding_response = gemini.embed_content(
                model="models/text-embedding-004",
                content=stripped_sentence,
                task_type="retrieval_document",
                title="Embedding of single string"
            )
            
            # Prepare a dictionary with the sentence and its embedding
            result_entry = {
                "sentence": stripped_sentence,
                "embedding": embedding_response['embedding']
            }
            results.append(result_entry)

    # Save results to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(results, json_file, indent=4)  # Use indent for pretty printing

# Example usage
pdf_path = "/Users/kartik/Desktop/vector_database/Kartik_Sehgal_CV.pdf"
output_file = "embeddings.json"
process_pdf(pdf_path, output_file)