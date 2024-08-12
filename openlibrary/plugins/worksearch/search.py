"""Search utilities.
"""

from openlibrary.utils.solr import Solr
from infogami import config

_ACTIVE_SOLR: Solr | None = None


def get_solr():
    global _ACTIVE_SOLR
    if not _ACTIVE_SOLR:
        base_url = config.plugin_worksearch.get('solr_base_url')
        _ACTIVE_SOLR = Solr(base_url)
    return _ACTIVE_SOLR


class OpenlibrarySearch:
    def __init__(self):
        # Inicializa a lista de livros, o conjunto de temas ocultos e autores ocultos
        self.books = []
        self.hidden_subjects = set()
        self.hidden_authors = set()

    def add_book(self, title, author, subjects):
        # Adiciona um livro à lista de livros
        self.books.append({
            "title": title,
            "author": author,
            "subjects": subjects
        })

    def hide_subject(self, subject):
        # Adiciona um tema ao conjunto de temas a serem ocultados
        self.hidden_subjects.add(subject)

    def hide_author(self, author):
        # Adiciona um autor ao conjunto de autores a serem ocultados
        self.hidden_authors.add(author)

    def remove_subject(self, subject):
        # Remove um tema do conjunto de temas a serem ocultados
        self.hidden_subjects.discard(subject)

    def remove_author(self, author):
        # Remove um autor do conjunto de autores a serem ocultados
        self.hidden_authors.discard(author)

    def validate_subject_filter(self, subject):
        # Verifica se o tema é válido (existe em algum livro)
        return any(subject in book['subjects'] for book in self.books)

    def validate_author_filter(self, author):
        # Verifica se o autor é válido (existe em algum livro)
        return any(author == book['author'] for book in self.books)
    
    

    def search(self, query):
        results = []
        for book in self.books:
            # Verifica se o livro contém algum tema ou autor oculto
            if any(subj in self.hidden_subjects for subj in book['subjects']) or book['author'] in self.hidden_authors:
                continue
            # Adiciona o livro aos resultados se o título corresponder à consulta
            if query.lower() in book["title"].lower():
                results.append(book)
        return results

