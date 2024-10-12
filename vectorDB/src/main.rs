use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use ndarray::Array1;
// use serde_json::Result;
use std::fs::File;
// use std::io::Read;
use ndarray::array;
// use std::io::{self};
use std::error::Error;
use std::io::BufReader;
// use ask_gemini::Gemini;


#[derive(Debug, Serialize, Deserialize)]
struct Embedding{
    sentence: String,
    embedding: Vec<f64>,
}

struct VectorStore{
    vector_data: HashMap<String, Array1<f64>>,
}


// async fn get_embedding_response(prompt: &str) -> Result<Vec<String>, Box<dyn std::error::Error>> {
//     let gemini = Gemini::new(None, Some("models/text-embedding-004"));
//     let response = gemini.ask(prompt).await?;
//     Ok(response)
// }


impl Embedding {
    fn read_json(file_path: &str) -> Result<Vec<(String, Vec<f64>)>, Box<dyn Error>> {
        // Open the JSON file
        let file = File::open(file_path)?;
        let reader = BufReader::new(file);
    
        // Deserialize the JSON into a Vec<Entry>
        let entries: Vec<Embedding> = serde_json::from_reader(reader)?;
    
        // Map the entries into a vector of (sentence, embedding) tuples
        let result: Vec<(String, Vec<f64>)> = entries.into_iter()
            .map(|entry| (entry.sentence, entry.embedding))
            .collect();
    
        Ok(result)
    }
}

impl VectorStore{

    fn new() -> Self {
        VectorStore {
            vector_data: HashMap::new(),
        }
    }

    fn add_vector(&mut self, data: Array1<f64>, vector_id: String){
        self.vector_data.insert(vector_id, data);
    }

    fn _get_vector(&mut self,vector_id: String) -> Array1<f64>{
        self.vector_data.get(&vector_id).unwrap().clone()
    }

    fn find_similar_vectors(&self, query_vector: &Array1<f64>, num_results: usize) -> Vec<(String, f64)> {
        let mut results = Vec::new();

        for (vector_id, vector) in &self.vector_data {
            let similarity = self.cosine_similarity(query_vector, vector);
            results.push((vector_id.clone(), similarity));
        }

        results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        results.into_iter().take(num_results).collect()
    }

    fn cosine_similarity(&self, vec1: &Array1<f64>, vec2: &Array1<f64>) -> f64 {
        let dot_product = vec1.dot(vec2);
        
        let norm1 = vec1.mapv(|x| x * x).sum().sqrt();  // L2 norm of vec1
        let norm2 = vec2.mapv(|x| x * x).sum().sqrt();  // L2 norm of vec2
    
        dot_product / (norm1 * norm2)
    }

    fn vec_to_array(vec: Vec<f64>) -> Array1<f64> {
        Array1::from_vec(vec)
    }
    
}

#[tokio::main]
async fn main() -> std::result::Result<(), Box<dyn Error>> {
    // Example usage:
    let mut store = VectorStore::new();
    let path_to_embedding_file = "/Users/kartik/Desktop/vector_database/vectorDB/src/embeddings.json";
    let res = Embedding::read_json(&path_to_embedding_file)?;
    
    // Now you can use sentence and embeddings here
    for (sentence, embedding) in res {
        store.add_vector( VectorStore::vec_to_array(embedding), sentence);
    }

    let query_vector = array![1.0, 0.0, 0.0];
    let similar_vectors = store.find_similar_vectors(&query_vector, 5);

    println!("Most similar vectors: {:?}", similar_vectors);
    Ok(())
}