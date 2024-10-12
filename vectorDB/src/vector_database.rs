// use std::collections::HashMap;
// use ndarray::{Array1, linalg::Dot};
// use ndarray::prelude::*;
// use ndarray::array;

// struct mem{
//     vector_data: HashMap<String, Array1<f64>>,
// }

// impl mem{

//     fn new() -> Self {
//         VectorStore {
//             vector_data: HashMap::new(),
//         }
//     }

//     fn add_vector(&mut self,data: String, vector_id: u32){
//         let mut m = mem{vector_data: HashMap::new()};
//         self.vector_data.insert(vector_id, vector);
//     }

//     fn get_vector(&mut self,vector_id: String) -> Vec<f32>{
//         if let Some(vector_embedding) = self.vector_data.get(vector_id) {
//             vector_embedding
//         } else {
//             println!("Vector not found");
//         }
//     }

//     fn find_similar_vectors(&self, query_vector: &Array1<f64>, num_results: usize) -> Vec<(String, f64)> {
//         let mut results = Vec::new();

//         for (vector_id, vector) in &self.vector_data {
//             let similarity = self.cosine_similarity(query_vector, vector);
//             results.push((vector_id.clone(), similarity));
//         }

//         results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
//         results.into_iter().take(num_results).collect()
//     }

//     fn cosine_similarity(&self, vec1: &Array1<f64>, vec2: &Array1<f64>) -> f64 {
//         let dot_product = vec1.dot(vec2);
//         let norm1 = vec1.norm_l2();
//         let norm2 = vec2.norm_l2();
//         dot_product / (norm1 * norm2)
//     }

// }


// fn main() {
//     // Example usage:
//     let mut store = VectorStore::new();

//     let vector1 = array![1.0, 2.0, 3.0];
//     let vector2 = array![4.0, 5.0, 6.0];

//     store.add_vector("vector1".to_string(), vector1.clone());
//     store.add_vector("vector2".to_string(), vector2.clone());

//     let query_vector = array![1.0, 0.0, 0.0];
//     let similar_vectors = store.find_similar_vectors(&query_vector, 5);

//     println!("Most similar vectors: {:?}", similar_vectors);
// }