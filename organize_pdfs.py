import os
import shutil
import fitz # PyMuPDF
import re
import unicodedata

INPUT_DIR = 'manuais_otimizados'
OUTPUT_DIR = 'organize_by_subject'
UNKNOWN_SUBJECT_DIR_NAME = 'Disciplina-não-identificada'
UNKNOWN_SUBJECT_DIR = os.path.join(OUTPUT_DIR, UNKNOWN_SUBJECT_DIR_NAME)

# Helper function to normalize text (remove accents)
def normalize_text(text):
    if not isinstance(text, str):
        return text
    normalized = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    return normalized

# Keywords to match subjects from the content of the PDF
SUBJECT_KEYWORDS = {
    "Matemática": ["matematica", "algebra", "geometria", "calculo"],
    "Português": ["portugues", "gramatica", "literatura", "redacao", "producao de texto", "generos leitura e analise"],
    "Geografia": ["geografia", "mapa", "paises", "ambiente", "atlas geografico"],
    "História": ["historia", "fatos historicos", "idade media", "cultura", "povos da antiguidade"],
    "Ciências Naturais": ["ciencias", "biologia", "quimica", "fisica"], 
    "Língua Estrangeira": ["ingles", "espanhol", "frances", "lingua estrangeira", "english"],
    "Artes": ["arte", "desenho", "pintura", "musica"],
    "Educação Física": ["educacao fisica", "esporte"],
    "Cidadania": ["cidadania", "moral e etica"],
    "Empreendedorismo": ["empreendedorismo", "negocios", "financas"],
    "Caligrafia": ["caligrafia"],
    "Atividades de Reforço": ["atividades de reforco"],
    "Tabuada": ["tabuada"]
}

# Keywords to match subjects directly from the filename (higher priority)
FILENAME_SUBJECT_KEYWORDS = {
    "Matemática": ["matematica"],
    "Português": ["portugues", "gramatica", "literatura", "producao de texto", "generos leitura e analise"],
    "Geografia": ["geografia", "atlas geografico", "megacartografia"],
    "História": ["historia", "fatos historicos", "povos da antiguidade", "escravidao moderna", "movimentos contestatorios"],
    "Ciências Naturais": ["ciencias", "biologia", "quimica", "fisica"],
    "Língua Estrangeira": ["ingles", "english"],
    "Artes": ["arte"],
    "Educação Física": ["educacao fisica"],
    "Cidadania": ["cidadania", "moral e etica"],
    "Empreendedorismo": ["empreendedorismo", "negocios", "financas"],
    "Caligrafia": ["caligrafia"],
    "Atividades de Reforço": ["atividades de reforco"],
    "Tabuada": ["tabuada"]
}

def extract_text_from_pdf(pdf_path, num_pages=3):
    """
    Extracts text from the first `num_pages` of a PDF file.
    """
    text = ""
    try:
        with fitz.open(pdf_path) as doc:
            for i in range(min(num_pages, doc.page_count)):
                text += doc.load_page(i).get_text()
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return text

def identify_subject(filename, extracted_text):
    """
    Identifies the subject of a PDF based on keywords in the filename first,
    then in the extracted text. Returns the subject in Title Case or None if not identified.
    """
    normalized_filename_lower = normalize_text(filename).lower()

    # Prioritize filename keywords - sort by length descending for more specific matches first
    for subject, keywords_list in sorted(FILENAME_SUBJECT_KEYWORDS.items(), key=lambda item: max(len(k) for k in item[1]) if item[1] else 0, reverse=True):
        for keyword in sorted(keywords_list, key=len, reverse=True):
            normalized_keyword = normalize_text(keyword).lower()
            if re.search(r'\b' + re.escape(normalized_keyword) + r'\b', normalized_filename_lower):
                return subject
    
    # If not found in filename, try extracted text - sort by length descending for more specific matches first
    normalized_text_lower = normalize_text(extracted_text).lower()
    for subject, keywords_list in sorted(SUBJECT_KEYWORDS.items(), key=lambda item: max(len(k) for k in item[1]) if item[1] else 0, reverse=True):
        for keyword in sorted(keywords_list, key=len, reverse=True):
            normalized_keyword = normalize_text(keyword).lower()
            if re.search(r'\b' + re.escape(normalized_keyword) + r'\b', normalized_text_lower):
                return subject
    
    return None

def organize_pdfs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(UNKNOWN_SUBJECT_DIR, exist_ok=True)

    pdf_files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(INPUT_DIR, pdf_file)
        print(f"Processing {pdf_file}...")
        extracted_text = extract_text_from_pdf(pdf_path, num_pages=5) # Extract from first 5 pages

        # Pass both filename and extracted_text to identify_subject
        subject = identify_subject(pdf_file, extracted_text)
        
        if subject:
            target_dir = os.path.join(OUTPUT_DIR, subject)
        else:
            target_dir = UNKNOWN_SUBJECT_DIR
        
        os.makedirs(target_dir, exist_ok=True)
        shutil.copy(pdf_path, os.path.join(target_dir, pdf_file))
        print(f"Copied {pdf_file} to {target_dir} (Identified as: {subject if subject else 'Unknown'})")

if __name__ == "__main__":
    organize_pdfs()