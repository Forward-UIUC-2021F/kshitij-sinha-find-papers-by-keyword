from src.find_papers_by_keyword.embeddings_generator import EmbeddingsGenerator
from src.file_readers.paper_file_reader import PaperFileReader
from src.find_papers_by_keyword.utils import write_pickle_data, write_json_data

paper_file = "data/mag_papers.json"
reader = PaperFileReader("id", "title", "abstract", "n_citation")
papers = reader.read_file(paper_file)

print(papers[0])

generator = EmbeddingsGenerator()
embs, id_to_ind = generator.generate_paper_embeddings(papers)

write_pickle_data(embs, "data/mag_embs.pickle")
write_json_data(id_to_ind, "data/mag_id_to_ind.json")

