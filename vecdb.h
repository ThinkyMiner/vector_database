#include <stdio.h>
#include <string.h>
#include <math.h>

struct node{
    int id;
    float embedding[1024];
    char word[256];
};

typedef struct node vecEmbedding;

vecEmbedding *createVecEmbedding(int id, float *embedding, char *word){
    vecEmbedding *newVec = (vecEmbedding *)malloc(sizeof(vecEmbedding));
    newVec->id = id;
    memcpy(newVec->embedding, embedding, 1024 * sizeof(float));
    strcpy(newVec->word, word);
    return newVec;
}

float cosine_similarity(vecEmbedding emb1, vecEmbedding emb2)
{
    float dot_product = 0.0;
    float norm_vec1 = 0.0;
    float norm_vec2 = 0.0;
    int size = sizeof(emb1.embedding);

    for (int i = 0; i < size; i++)
    {
        float res = emb1.embedding[i] * emb2.embedding[i];
        dot_product += res;
        norm_vec1 += res;
        norm_vec2 += res;
    }

    norm_vec1 = sqrt(norm_vec1);
    norm_vec2 = sqrt(norm_vec2);

    if (norm_vec1 == 0.0 || norm_vec2 == 0.0)
    {
        return 0.0;
    }

    return dot_product / (norm_vec1 * norm_vec2);
}
