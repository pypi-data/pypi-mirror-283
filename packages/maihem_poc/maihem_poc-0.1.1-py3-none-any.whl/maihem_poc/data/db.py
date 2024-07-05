import pandas as pd


def get_vector_db(filename: str) -> pd.DataFrame:
	try:
		df = pd.read_csv(f"{filename}_vectordb.csv")
	except FileNotFoundError:
		return None


def get_chunks(filename: str):
	vector_db = get_vector_db(filename)
	if vector_db is not None:
		return list(vector_db['chunks'])
