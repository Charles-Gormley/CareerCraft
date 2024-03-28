################# LIBRARIES #################
# Internal Repository Libraries
from src.parsers import Embeddings, KeytermExtractor
import numpy as np



class ATS:

    def __init__(self, resume: str, job_description: str):
        self.resume = resume
        self.job_description = job_description

    ######### Embeddings #########
    def initialize_embedding_model(self, embedding_model_str: str):
        """
        Initialize the embedding model.
        """
        self.model = Embeddings(embedding_model_str)
        self.model.initialize_embedding_model()
        return True

    def calculate_embedding_vector(self, text: str, embedding_model: str):
        """
        Calculate the vectors for the resume and job description.
        """
        embedding = self.model.calculate_embedding(text)
        return embedding

    def cosine_similarity(self, vector1: np.array, vector2: np.array) -> float:
        """
        Calculate the cosine similarity between two vectors.
        """
        similarity = np.dot(vector1, vector2) / (np.linalg.norm(vector1) * np.linalg.norm(vector2))
        return similarity

    def calculate_embedding_similarity_score(self, embedding_model: str) -> float:
        """
        Calculate the similarity score between the resume and job description.
        """
        # Initialize the embedding model

        # Calculate the vectors

        # Calculate the cosine similarity

        # Return the similarity score

        pass

    ######### Key Words #########
    def extract_keywords_from_job_description(self, extractor: str):
        """
        Extract keywords from the resume.
        """
        # Extract keywords

        # Return the keywords
        pass
        
    def count_keywords_in_resume(self, extractor: str):
        """
        Count the number of keywords in the resume.
        """
        # Count the keywords

        # Return the count
        pass

    def assign_score_to_keyword_count(self, count: int):
        """
        The count of each keyword should appear 2 --> 4 times in the resume.
        """
        # Assign a score for each count. 

        # Calculate the Average Score. 

        # Return the individual scores and the average score.

        pass

    ######### Education #########
    def get_gpa_from_resume():
        pass

    def get_education_level_from_resume():
        pass

    ######### Company Experience #########
    def calculate_company_prestige_level():
        '''
        Calculate the prestige level of the company. e.g. Google would be like 10, while Boeing would be 4. 
        This is to be done in the future when we could have a database on this kind of stuff.
        '''
        pass


    ######### Years of Experience #########
    def calculate_exp_resume(self):
        """
        Calculate the years of experience from the resume.
        """
        # TODO: 
        # Calculate the years of experience

        # Return the years of experience
        pass


    ######### Main Functions #########
    def calculate_ats_weighted_average(self, scores: list[float], weights=None) -> float:
        """
        Calculate the weighted average of the scores.

        Args:
            scores (list): A list of scores. 
            weights (list): A list of weights.

        Returns:
            float: The weighted average of the scores.
        """
        if not weights: # Default weights if not provided where each score has equal weight
            weights = [ round(1/len(scores), 2) ] * len(scores)

        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        return weighted_sum
    
    def threhsold_check(self, score: float, threshold: float):
        """
        Check if the score is above the threshold.

        Args:
            score (float): The score to check.
            threshold (float): The threshold value.

        Returns:
            bool: True if the score is above the threshold, False otherwise.
        """
        return score > threshold