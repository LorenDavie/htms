"""
Loads the pages into ACE.
"""
from makesense.models import Book, Chapter, Page
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from bs4 import BeautifulSoup

class Command(BaseCommand):
    """
    Command class.
    """
    def add_arguments(self,parser):
        parser.add_argument('filename')
    
    def execute(self,*args,**kwargs):
        """
        Main exec method.
        """
        filename = kwargs['filename']
        book, book_created = Book.objects.get_or_create(title='How To Make Sense of Any Mess',dedication='')
        
        if book_created:
            book.push_to_library()
            print 'pushed book into ACE library'
        
        with open(filename,'rb') as html_file:
            soup = BeautifulSoup(html_file,'html.parser')
            
            # create chapters
            chapter_count = 1
            for chapter_title in soup.find_all('h1'):
                if chapter_title.string:
                    chapter_no, chapter_title_name = chapter_title.string.split('.',1)
                    print 'creating chapter',chapter_title_name
                    chapter = Chapter.objects.create(book=book,
                                                     order=chapter_count,
                                                     name=chapter_title_name,
                                                     slug=slugify(chapter_title_name))
                    chapter.push_to_library()
                    self.build_chapter(chapter,chapter_title)
                    chapter_count += 1
    
    def build_chapter(self,chapter,chapter_title_element):
        """
        Builds out the chapter.
        """
        for sibling in chapter_title_element.next_siblings:
            print 'found sibling',sibling.name
            if sibling.name == 'h2' and sibling.string:
                slug = slugify(sibling.string)
                if len(slug) > 50:
                    slug = slug[:50]
                page = Page.objects.create(chapter=chapter,
                                           title=sibling.string,
                                           slug=slug)
                print 'created page',page.title
                self.build_page(page,sibling)
    
    def build_page(self,page,page_title_element):
        """
        Builds out the page.
        """
        page_body = ''
        for sibling in page_title_element.next_siblings:
            if sibling.name == 'h2':
                # reached the end
                page.body = page_body
                page.save()
                page.push_to_library()
                return
            elif sibling.name == 'img':
                page.graphic = sibling['src']
            else:
                page_body += unicode(sibling)
