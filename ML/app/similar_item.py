from sklearn.metrics.pairwise import cosine_similarity


class SimilarItemRetriever(object):
    def __init__(self, matrix, product_ids):
        self.matrix = matrix
        self.product_ids = product_ids

    def get_product_vector(self, product_id):
        # Get product index
        product_index = self.product_ids.index(product_id)
        # Get product vector
        product_vector = self.matrix.iloc[product_index].values.reshape(1, -1)
        return product_vector

    def get_similar_products_by_vector(self, product_vector, top_n=5):
        similarities = cosine_similarity(product_vector, self.matrix)
        # Get top_n product indices
        top_indices = similarities[0].argsort()[-top_n:][::-1]
        # Get product IDs for the top indices
        similar_products = [self.product_ids[idx] for idx in top_indices]
        return similar_products

    def get_similar_products_by_id(self, product_id, top_n=5):
        product_vector = self.get_product_vector(product_id)
        similar_products = self.get_similar_products_by_vector(product_vector, top_n)
        return similar_products
