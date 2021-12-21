import math
import numpy as np
import numpy.linalg as la
from sklearn.cluster import DBSCAN

from find_papers_by_keyword.trie.utils import construct_trie, construct_re, get_matches
from find_papers_by_keyword.utils import get_top_k, concat_paper_info, standardize_non_ascii

class PaperKeywordAssigner():
    """ Computes similarity scores between papers and keywords and assigns relevant keywords to papers
    
    See README Step 2 for implementation details
    """

    def assign_paper_keywords(self, paper_data, keyword_data, golden_keywords, 
            paper_embeddings, keyword_embeddings, paper_id_to_emb_ind, 
            word_to_other_freq):
        """ Assigns relevant keywords to publications
        
        For every paper in paper_data, assigns a set of keywords from golden_keywords that best
        match the paper content. Every assignment is described by the match score between the paper
        and the keyword. Semantically similar keywords are dropped using clustering

        Args:
            paper_data: A list of dictionaries containing paper data, using the following schema:
                [
                    {
                        "id": str,
                        "title": str,
                        "abstract": str
                    },
                    ...
                ]
            keyword_data: A list of dictionaries containing keyword data, using the following schema:
                [
                    {
                        "id": int,
                        "keyword": str
                    },
                    ...
                ]
                For simplicity, the "id" field must represent the row index of the keyword's embedding 
                in keyword_embeddings
            golden_keywords: A list of keywords that will be searched and assigned to the papers. This represents
                the set of all possible keywords that this module can take as its search input.
                Ideally, golden_keywords should be a subset of the keywords from keyword_data, however, the function
                is built to handle any exceptions. If golden_keywords contains a word not found in keyword_data, the
                keyword will be skipped from assignment
            paper_embeddings: A np.ndarray representing vector embeddings for every papers in paper_data
            keyword_embeddings: A np.ndarray representing vector embeddings for every keyword in keyword_data
            paper_id_to_emb_ind: A dictionary mapping papers to embeddings, where keys are strings reprsenting paper id's
                and values are ints representing the row of corresponding embedding in paper_embeddings
            word_to_other_freq: A dictionary describing how often keywords appear in non-CS publications. Every entry maps
                a keyword string to an int representing the frequency in non-CS papers.
        Returns:
            A list of tuples representing paper-keyword assignments and their corresponding match score. Every tuple uses the 
            format (paper_id: str, keyword_id: int, match_score: float)
        """     

        keyword_to_id = {k["keyword"]: k["id"] for k in keyword_data}
        keyword_embeddings = self._normalize_embs(keyword_embeddings)
        word_id_to_other_freq = self._get_word_id_to_other_freq(
            word_to_other_freq, keyword_to_id)

        """
        Keyword set formed from the set intersection of
        - Springer set: parse papers for author-labeled keywords and keep those
        with freq >= 5
        - EmbedRank set: Use EmbedRank to extract keywords from entire cs corpus.
        """
        keyword_search_set = set(golden_keywords)
        keywords_trie = construct_trie(keyword_search_set)
        keywords_re = construct_re(keywords_trie)

        # For every paper, finds top keyword matches. Stores matches in database
        # Every row in database has paper, keyword, and match score
        # For every paper, removes duplicate keywords using clustering
        assignments = []
        print("Starting paper keyword extraction: ")
        for p_i, paper in enumerate(paper_data):
            paper_id = paper['id']
            raw_text = concat_paper_info(paper['title'], paper['abstract'])

            paper_embedding_ind = paper_id_to_emb_ind[paper_id]
            paper_embedding = paper_embeddings[paper_embedding_ind]
            paper_embedding = self._normalize_vec(paper_embedding)

            match_ids = self._get_keyword_match_ids(
                raw_text, keywords_re, keyword_to_id)
            
            if len(match_ids) == 0:
                # No matches to assign
                continue

            # Uses assmuption that ids are the indices of the embedding
            match_embs = keyword_embeddings[match_ids]
            # Compute dot of every match embedding with this paper's embedding
            sim_scores = np.dot(match_embs, paper_embedding)

            keyword_scores = self._get_penalized_keyword_scores(zip(match_ids, sim_scores), word_id_to_other_freq)

            # Select top-k-scoring keywords
            query_keywords = 17
            top_keywords = get_top_k(keyword_scores, min(
                query_keywords, len(keyword_scores) - 1), lambda t: t[1])

            selected_keyword_ids = [t[0] for t in top_keywords]
            selected_keyword_embs = keyword_embeddings[selected_keyword_ids]

            max_keywords = 9
            unique_top_keywords = self._get_unique_keywords(top_keywords, selected_keyword_embs, max_keywords)

            # self._add_paper_assignments_to_database(cursor, paper_id, unique_top_keywords)
            for keyword_id, keyword_score in unique_top_keywords:
                assignments.append((paper_id, str(keyword_id), str(keyword_score)))

            if p_i % 1000 == 0:
                print("On " + str(p_i) + "th paper")

        print(f"{p_i} papers analyzed")
        return assignments

    def _get_unique_keywords(self, keywords, embeddings, max_keywords):
        """
        Retruns a list of keywords that are mathematically unique using DBSCAN clustering.
        The input embedding vectors will be grouped into clusters using DBSCAN. Out of every cluster,
        only one representative keyword will be retreieved and returned from this method, up to a total
        of "max_keywords" returned.

        Args:
            keywords: A list of keywords
            embeddings: A list of keyword embeddings. This list should be parallel to keywords.
            max_keywords: The maximum unique keywords to retrieve. The length of the returned list
                will be no greater than max keywords

        Returns:
            A list of keywords that is a subset of the input, "keywords." These keywords are each unique
            from each other, based on DBSCAN clustering. 
        """
        db = DBSCAN(eps=0.47815, min_samples=2).fit(embeddings)
        labels = db.labels_

        curr_groups = set()
        unique_top_keywords = []

        for i, keyword in enumerate(keywords):
            if len(unique_top_keywords) >= max_keywords:
                break

            group_idx = labels[i]

            if group_idx == -1:
                unique_top_keywords.append(keyword)
            elif group_idx not in curr_groups:
                curr_groups.add(group_idx)
                unique_top_keywords.append(keyword)

        return unique_top_keywords

    def _get_penalized_keyword_scores(self, matches, word_id_to_other_freq):
        """
        Returns a tuple of keyword/score pairs, but penalizes keyword matches that appear frequently (more than 1000 times) in non-CS papers.
        For such keywords, the keyword score is divided by its square root

        Args:
            matches: A list of tuples representing matches. Every tuple should be in the format (keyword_id, match_score), where match_score is the
                similarity score betwen keyword_id and a paper.
                The i'th element of match_scores should be the score corresponding to the i'th element of keyword_ids
            word_id_to_other__freq: a dictionary mapping a keyword to its frequency in non-CS papers. The keys of this dictionary are keyword ids

        Returns:
            A list of tuples in the same format as the input argument "matches". However, the return list contains penalized match scores based on
            the specification above
        """
        # Keyword scores will be stored as: (<keyword_id, match_score>, ...)
        keyword_scores = []
        for match_id, kw_score in matches:
            # Checking if current keyword appears in non-cs papers in arxiv corpus
            if match_id in word_id_to_other_freq:
                other_freq = word_id_to_other_freq[match_id]

                # Penalize general words
                if other_freq >= 1000:
                    kw_score /= math.sqrt(other_freq)

            kw_t = (match_id, kw_score)
            keyword_scores.append(kw_t)

        return keyword_scores

    def _get_keyword_match_ids(self, raw_text, keywords_re, keyword_to_id):
        """
        Finds all keywords that appear in raw_text and returns the ids of the matched keywords

        Args:
            raw_text: the string that will be search for keywords
            keyword_re: a regex pattern that will be searched on raw_text
            keyword_to_id: a dictionary mapping keyword strings to keyword id's

        Returns:
            A list of keyword id's corresponding to all keywords that were found in raw_text
        """
        # Get candidate keywords by checking occurrence
        keyword_matches = get_matches(raw_text, keywords_re, True)
        match_ids = []
        for keyword, match_freq in keyword_matches:
            try:
                match_ids.append(keyword_to_id[keyword])
            except KeyError:
                # If match is not in keyword_to_id, then match doesn't exist in our original keyword dataset
                # so we skip the corresponding matched keyword
                continue
            except Exception as e:
                print("Exception", type(e), e)
                match_ids.append(keyword_to_id[standardize_non_ascii(keyword)])
                
        return match_ids

    def _get_word_id_to_other_freq(self, word_to_other_freqs, word_to_id):
        """
        Converts a map from words to frequencies into a map of word ids to other frequencies

        Args:
            word_to_other_freqs: a dictionary mapping keyword strings to ints
            word_to_id: a dictinoary mapping keyword strings to the corresponding keyword id's

        Returns:
            A dictionary mapping keyword id's to ints
        """
        word_id_to_other_freq = {}
        for word, freq in word_to_other_freqs.items():
            if word in word_to_id:
                word_id_to_other_freq[word_to_id[word]] = freq

            # If word is not in word_to_id, then word doesn't exist in our keyword dataset and will never
            # be matched with a paper. We can skip adding this word to the dictionary

        return word_id_to_other_freq

    def _normalize_embs(self, emb_arr):
        """
        Normalizes columns of a matrix by 2-norm
        """
        emb_norms = la.norm(emb_arr, axis=1)
        return emb_arr / emb_norms[:, None]

    def _normalize_vec(self, vec):
        """
        Normalizes vectors by 2-norm
        """
        return vec / la.norm(vec)

