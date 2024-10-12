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
    embeddings = []
    for sentence in sentences:
        # Generate embeddings using the embeddings-004 model
        print(sentence)
        embedding_response = gemini.embed_content(
            model="models/text-embedding-004",
            content=sentence.strip(),
            task_type="retrieval_document",
            title="Embedding of single string"
        )
        
        # Access the embedding correctly from the response dictionary
        embeddings.append(embedding_response['embedding'])

    # Save embeddings to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(embeddings, json_file)

# Example usage
pdf_path = "/Users/kartik/Desktop/vector_database/EA1.pdf"
output_file = "/Users/kartik/Desktop/vector_database/vectorDB/src/embedding.json"
process_pdf(pdf_path, output_file)