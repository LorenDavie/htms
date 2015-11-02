""" 
Models for MakeSense.
"""

from django.db import models
from djax.content import ACEContent, ContentManager, M2MFieldConverter
from django.conf import settings

class Book(models.Model,ACEContent):
    """ 
    The book.
    """
    title = models.CharField(max_length=100,unique=True)
    dedication = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    class ACE:
        content_type = 'Book'
        field_map = {
            'title':'title',
            'dedication':'dedication',
        }

class Chapter(models.Model,ACEContent):
    """ 
    A chapter in the book.
    """
    book = models.ForeignKey(Book,related_name='chapters')
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name
    
    def main_pages(self):
        """ 
        Gets the non-supporting pages.
        """
        return self.pages.filter(is_supporting_material=False)
    
    def supporting_material(self):
        """ 
        Gets supporting material.
        """
        return self.pages.filter(is_supporting_material=True)
    
    def first_page(self):
        """
        Returns the first page of the chapter.
        """
        return self.pages.all()[0]
    
    def last_page(self):
        """
        Returns the last page of the chapter.
        """
        last_index = self.pages.count() - 1
        return self.pages.all()[last_index]
    
    def has_previous_chapter(self):
        """
        Returns True if the is a chapter prior to this one, False otherwise.
        """
        previous_order = self.order - 1
        return self.book.chapters.filter(order=previous_order).exists()
    
    def previous_chapter(self):
        """
        Returns the previous chapter, or None if there is no prior chapter.
        """
        previous_order = self.order - 1
        try:
            return self.book.chapters.get(order=previous_order)
        except Chapter.DoesNotExist:
            return None
    
    def has_next_chapter(self):
        """
        Returns True if the chapter has another chapter following this one, False otherwise.
        """
        next_order = self.order + 1
        return self.book.chapters.filter(order=next_order).exists()
    
    def next_chapter(self):
        """
        Gets the chapter following this one, if it exists, or None.
        """
        next_order = self.order + 1
        try:
            return self.book.chapters.get(order=next_order)
        except Chapter.DoesNotExist:
            return None
    
    def get_page_count_offset(self):
        """
        Returns the total number of pages of chapters preceding this one.
        """
        if self.has_previous_chapter():
            return self.previous_chapter().get_page_count_offset() + self.pages.count()
        else:
            return self.pages.count()
    
    class Meta:
        unique_together = (('book','order'),)
        ordering = ['order']
    
    class ACE:
        content_type = 'Chapter'
        field_map = {
            'book':'book',
            'order':'order',
            'name':'name',
            'slug':'slug',
        }

class Page(models.Model,ACEContent):
    """ 
    A page in the chapter (sort of a mini chapter).
    """
    chapter = models.ForeignKey(Chapter,related_name='pages')
    title = models.CharField(max_length=500)
    body = models.TextField()
    graphic = models.URLField(max_length=400,blank=True, null=True)
    slug = models.SlugField()
    ordering = models.IntegerField(default=0)
    is_supporting_material = models.BooleanField(default=False)
    supporting_material_type = models.CharField(null=True, max_length=100)
    download = models.URLField(null=True)
    
    objects = ContentManager()
    
    def __unicode__(self):
        return self.title
    
    def page_number(self):
        """ 
        Gets 1-indexed page number.
        """
        return self.ordering + 1
    
    def offset_page_number(self):
        """
        Gets 1-indexed page number, offset by chapter offset.
        """
        if self.chapter.has_previous_chapter():
            return self.page_number() + self.chapter.previous_chapter().get_page_count_offset()
        else:
            return self.page_number()
    
    def term_usage(self,term):
        """
        Counts incident of term usage in this page.
        """
        return self.body.count(term)
    
    def get_is_supporting_material(self):
        """ 
        Accessor for is_supporting_material
        """
        return 'True' if self.is_supporting_material else 'False'
    
    def set_is_supporting_material(self,value):
        """ 
        Mutator for is_supporting_material.
        """
        if value == 'True':
            self.is_supporting_material = True
        else:
            self.is_supporting_material = False
    
    supporting_material_prop = property(get_is_supporting_material,set_is_supporting_material)
    
    def next_page(self):
        """ 
        Gets the next page, or None if there is no next page.
        """
        try:
            next_page_order = self.ordering + 1
            return self.chapter.pages.get(ordering=next_page_order)
        except Page.DoesNotExist:
            return None
        
    def previous_page(self):
        """ 
        Gets the previous page, if it exists. Otherwise returns None.
        """
        try:
            previous_page_order = self.ordering - 1
            return self.chapter.pages.get(ordering=previous_page_order)
        except Page.DoesNotExist:
            return None
    
    def has_previous_page(self):
        """
        Returns True if there is a previous page, False otherwise.
        """
        previous_page_order = self.ordering - 1
        return self.chapter.pages.filter(ordering=previous_page_order).exists()
    
    def is_list_element(self):
        """ 
        Tests if this page is part of a list.
        """
        if '.' in self.title:
            title_elements = self.title.split('.')
            try:
                int(title_elements[0])
                return True # successful cast, title starts with in, indicating list element
            except ValueError:
                pass # unsuccessful cast
        
        return False # if we're here, this isn't a list element
    
    class Meta:
        ordering = ['ordering']
    
    class ACE:
        content_type = 'Page'
        field_map = {
            'chapter':'chapter',
            'title':'title',
            'body':'body',
            'graphic':'graphic',
            'slug':'slug',
            'ordering':'ordering',
            'is_supporting_material':'supporting_material_prop',
            'supporting_material_type':'supporting_material_type',
            'download':'download',
        }

class TermManager(models.Manager):
    """
    Manager class for term.
    """
    def get_alpha_groups(self,queryset=None):
        """
        Groups by alphabet.
        """
        if not queryset:
            queryset = self.all()
        
        blocks = []
        
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            block = {'key':letter}
            block['terms'] = queryset.filter(term__istartswith=letter)
            blocks.append(block)
        
        return blocks

class Term(models.Model,ACEContent):
    """ 
    A lexicon term.
    """
    term = models.CharField(max_length=100)
    term_slug = models.SlugField()
    word_type = models.CharField(max_length=100)
    word_type_slug = models.SlugField()
    description = models.TextField(blank=True)
    usage = models.ManyToManyField(Page,related_name='terms')
    related = models.ManyToManyField('self',related_name='related_to')
    total_usage = models.IntegerField(default=0)
    
    objects = TermManager()
    
    def __unicode__(self):
        return self.term
    
    def get_alternatives(self):
        """
        Alternative accessor.
        """
        return ['%s|%s' % (alt.alternative_term,alt.word_type) for alt in self.alternatives.all()]
    
    def set_alternatives(self,values):
        """
        Alternative mutator.
        """
        [alt.delete() for alt in self.alternatives.all()]
        
        for value in values:
            term_alt, word_type = value.split('|')
            TermAlternative.objects.create(term=self,
                                           alternative_term=term_alt,
                                           word_type=word_type)
    
    alt_prop = property(get_alternatives,set_alternatives)
    
    def usage_chapters(self):
        """
        Gets pages that use the term, organized into chapters.
        """
        chapter_list = []
        for chapter in Chapter.objects.all():
            chapter_rows = []
            column_index = 0
            current_row = []
            for page in chapter.pages.all():
                usage = self.usage.filter(pk=page.pk).exists()
                current_row.append({'page':page,'usage':usage})
                if column_index == 4:
                    # this is the end of the row
                    chapter_rows.append(current_row)
                    current_row = []
                    column_index = 0
                else:
                    column_index += 1
            
            chapter_list.append({'chapter':chapter,'chapter_rows':chapter_rows})
        
        return chapter_list
    
    class Meta:
        unique_together = (('term','word_type'),)
        ordering = ['term']
    
    class ACE:
        content_type = 'Term'
        field_map = {
            'term':'term',
            'term_slug':'term_slug',
            'word_type':'word_type',
            'word_type_slug':'word_type_slug',
            'description':'description',
            #'usage':M2MFieldConverter('usage'),
            #'alternatives':'alt_prop',
        }
        

class TermAlternative(models.Model):
    """ 
    An alternative to the term.
    """
    term = models.ForeignKey(Term,related_name='alternatives')
    alternative_term = models.CharField(max_length=100)
    word_type = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.alternative_term

