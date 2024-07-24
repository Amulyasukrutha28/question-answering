# question-answering
This project implements a system for extracting content from digital textbooks, indexing the content using a combination of BM25 and dense retrieval methods, and providing an interactive interface to query the content and receive relevant answers.  

Selected Textbooks
The following textbooks were used for content extraction:

The Constitution of Algorithms: Link
The Future is Present: Link
Assetization: Link

Setup Instructions
1. Clone the Repository
bash
Copy code
git clone https://github.com/yourusername/textbook-retrieval-system.git
cd textbook-retrieval-system
2. Create and Activate a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Download NLTK Data
python
Copy code
import nltk
nltk.download('punkt')
nltk.download('wordnet')
Dependencies
The project requires the following Python libraries:

fitz (PyMuPDF)
nltk
sentence-transformers
faiss
numpy
rank_bm25
transformers
To install these dependencies, use the following command:

bash
Copy code
pip install PyMuPDF nltk sentence-transformers faiss-cpu numpy rank_bm25 transformers
Running the System
1. Extract Text from Textbooks
Ensure the textbooks (PDF files) are available in the project directory with the names algorithms.pdf, assetization.pdf, and the_future.pdf.

2. Run the Main Script
bash
Copy code
python main.py
3. Interactive Querying
The system will prompt you to enter your query. Type your question and press Enter. The system will process the query and display the answer along with the top relevant chunks from the textbooks.

To exit the interactive querying, type exit.
