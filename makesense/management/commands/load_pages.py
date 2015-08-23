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
            #book.push_to_library()
            print 'pushed book into ACE library'
        
        with open(filename,'rb') as html_file:
            soup = BeautifulSoup(html_file,'html.parser')
            
            # create chapters
            chapter_count = 1
            for chapter_title in soup.find_all('h1'):
                chapter_no, chapter_title_name = chapter_title.get_text().split('.',1)
                print 'creating chapter',chapter_title_name
                chapter = Chapter.objects.create(book=book,
                                                 order=chapter_count,
                                                 name=chapter_title_name.strip(),
                                                 slug=slugify(chapter_title_name))
                #chapter.push_to_library()
                self.build_chapter(chapter,chapter_title)
                chapter_count += 1
    
    def build_chapter(self,chapter,chapter_title_element):
        """
        Builds out the chapter.
        """
        page_num = 0
        for sibling in chapter_title_element.next_siblings:
            if sibling.name == 'h1':
                return # you hit the beginning of the next chapter
            
            if sibling.name == 'h2':
                print 'found sibling:',sibling
                print 'get_text() yields:',sibling.get_text()
            
            if sibling.name == 'h2' and sibling.get_text():
                slug = slugify(sibling.get_text())
                if len(slug) > 50:
                    slug = slug[:50]
                
                if not Page.objects.filter(slug=slug).exists():
                    page = Page.objects.create(chapter=chapter,
                                               title=sibling.get_text().strip(),
                                               slug=slug,
                                               ordering=page_num)
                    page_num += 1
                    print 'created page',page.title
                    self.build_page(page,sibling)
                else:
                    print slug,'already exists.'
    
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
                #page.push_to_library()
                return
            elif sibling.name == 'img':
                page.graphic = sibling['src']
            else:
                page_body += unicode(sibling)
