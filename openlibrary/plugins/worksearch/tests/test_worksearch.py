import web
from openlibrary.plugins.worksearch.code import (
    process_facet,
    get_doc,
)


def test_process_facet():
    facets = [('false', 46), ('true', 2)]
    assert list(process_facet('has_fulltext', facets)) == [
        ('true', 'yes', 2),
        ('false', 'no', 46),
    ]


def test_get_doc():
    doc = get_doc(
        {
            'author_key': ['OL218224A'],
            'author_name': ['Alan Freedman'],
            'cover_edition_key': 'OL1111795M',
            'edition_count': 14,
            'first_publish_year': 1981,
            'has_fulltext': True,
            'ia': ['computerglossary00free'],
            'key': '/works/OL1820355W',
            'lending_edition_s': 'OL1111795M',
            'public_scan_b': False,
            'title': 'The computer glossary',
        }
    )
    assert doc == web.storage(
        {
            'key': '/works/OL1820355W',
            'title': 'The computer glossary',
            'url': '/works/OL1820355W/The_computer_glossary',
            'edition_count': 14,
            'ia': ['computerglossary00free'],
            'collections': set(),
            'has_fulltext': True,
            'public_scan': False,
            'lending_edition': 'OL1111795M',
            'lending_identifier': None,
            'authors': [
                web.storage(
                    {
                        'key': 'OL218224A',
                        'name': 'Alan Freedman',
                        'url': '/authors/OL218224A/Alan_Freedman',
                    }
                )
            ],
            'first_publish_year': 1981,
            'first_edition': None,
            'subtitle': None,
            'cover_edition_key': 'OL1111795M',
            'languages': [],
            'id_project_gutenberg': [],
            'id_librivox': [],
            'id_standard_ebooks': [],
            'id_openstax': [],
            'editions': [],
        }
    )


import unittest
from FuncionalidadeOculta import OpenlibrarySearch

class TestOpenlibrarySearch(unittest.TestCase):
    
    def setUp(self):
        # Configura o ambiente de teste com alguns livros
        self.search_service = OpenlibrarySearch()
        self.search_service.add_book("Diário de uma Paixão", "Nicholas Sparks", ["Romance", "Drama"])
        self.search_service.add_book("It", "Stephen King", ["Terror", "Suspense"])
        self.search_service.add_book("O Iluminado", "Stephen King", ["Terror", "Suspense"])
        self.search_service.add_book("A Coisa", "Stephen King", ["Terror", "Suspense"])
    
    def test_hide_specific_subject(self):
        self.search_service.hide_subject('Romance')
        results = self.search_service.search('Diário de uma Paixão')
        for book in results:
            self.assertNotIn('Romance', book['subjects'])
    
    def test_hide_specific_author(self):
        self.search_service.hide_author('Stephen King')
        results = self.search_service.search('It')
        for book in results:
            self.assertNotEqual(book['author'], 'Stephen King')

    def test_hide_multiple_filters(self):
        self.search_service.hide_subject('Terror')
        self.search_service.hide_author('Stephen King')
        results = self.search_service.search('It')
        self.assertNotIn({'title': 'It', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        results = self.search_service.search('O Iluminado')
        self.assertNotIn({'title': 'O Iluminado', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)

    def test_filters_persistence(self):
        self.search_service.hide_subject('Terror')
        results = self.search_service.search('It')
        self.assertNotIn({'title': 'It', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        results = self.search_service.search('O Iluminado')
        self.assertNotIn({'title': 'O Iluminado', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        self.search_service.add_book("A Coisa", "Stephen King", ["Terror", "Suspense"])
        results = self.search_service.search('A Coisa')
        self.assertNotIn({'title': 'A Coisa', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
    
    def test_conflicting_filters(self):
        self.search_service.hide_subject('Terror')
        self.search_service.hide_author('Stephen King')
        results = self.search_service.search('It')
        self.assertNotIn({'title': 'It', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        results = self.search_service.search('O Iluminado')
        self.assertNotIn({'title': 'O Iluminado', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        self.search_service.add_book("A Coisa", "Stephen King", ["Terror", "Suspense"])
        results = self.search_service.search('A Coisa')
        self.assertNotIn({'title': 'A Coisa', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)

    def test_remove_subject_filter(self):
        self.search_service.hide_subject('Terror')
        self.search_service.remove_subject('Terror')
        results = self.search_service.search('It')
        self.assertIn({'title': 'It', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        results = self.search_service.search('O Iluminado')
        self.assertIn({'title': 'O Iluminado', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)

    def test_remove_author_filter(self):
        self.search_service.hide_author('Stephen King')
        self.search_service.remove_author('Stephen King')
        results = self.search_service.search('It')
        self.assertIn({'title': 'It', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)
        results = self.search_service.search('O Iluminado')
        self.assertIn({'title': 'O Iluminado', 'author': 'Stephen King', 'subjects': ['Terror', 'Suspense']}, results)


    def test_invalid_subject_filter(self):
        # Teste para garantir que filtros inválidos não causam problemas
        self.search_service.hide_subject('Inexistente')  # Filtro inválido
        results = self.search_service.search('Diário de uma Paixão')
        # Inicialmente, o filtro inválido não deve impactar os resultados
        self.assertIn({'title': 'Diário de uma Paixão', 'author': 'Nicholas Sparks', 'subjects': ['Romance', 'Drama']}, results)

    def test_invalid_author_filter(self):
        # Teste para garantir que filtros inválidos não causam problemas
        self.search_service.hide_author('Inexistente')  # Filtro inválido
        results = self.search_service.search('Diário de uma Paixão')
        # Inicialmente, o filtro inválido não deve impactar os resultados
        self.assertIn({'title': 'Diário de uma Paixão', 'author': 'Nicholas Sparks', 'subjects': ['Romance', 'Drama']}, results)

    def test_log_error_on_invalid_filter(self, mock_logging_warning):
        # Testar logging para filtros inválidos
        self.search_service.validate_subject_filter = lambda x: False
        self.search_service.validate_author_filter = lambda x: False
        
        self.search_service.hide_subject('Inexistente')
        self.search_service.hide_author('Inexistente')
        
        mock_logging_warning.assert_any_call('Invalid subject filter applied: Inexistente')
        mock_logging_warning.assert_any_call('Invalid author filter applied: Inexistente')




if __name__ == '__main__':
    unittest.main()
