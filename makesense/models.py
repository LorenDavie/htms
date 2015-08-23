""" 
Models for MakeSense.
"""

from django.db import models
from djax.content import ACEContent, ContentManager, M2MFieldConverter

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

class Example(models.Model,ACEContent):
    """ 
    An example for the chapter.
    """
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    class ACE:
        content_type = 'Example'
        field_map = {
            'title':'title',
            'body':'body',
        }

class Excercise(models.Model,ACEContent):
    """ 
    An excercise for the user.
    """
    title = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    
    def __unicode__(self):
        return self.title
    
    class ACE:
        content_type = 'Excercise'
        field_map = {
            'title':'title',
            'body':'body',
        }

class WorkSheet(models.Model,ACEContent):
    """ 
    A worksheet for the user.
    """
    title = models.CharField(max_length=100)
    downloadable = models.URLField(max_length=400,blank=True)
    image = models.URLField(max_length=400,blank=True)
    
    def __unicode__(self):
        return self.title
    
    class ACE:
        content_type = 'WorkSheet'
        field_map = {
            'title':'title',
            'downloadable':'downloadable',
            'image':'image',
        }

class Chapter(models.Model,ACEContent):
    """ 
    A chapter in the book.
    """
    book = models.ForeignKey(Book,related_name='chapters')
    order = models.IntegerField()
    name = models.CharField(max_length=100)
    example = models.ForeignKey(Example,unique=True,null=True)
    excercise = models.ForeignKey(Excercise,unique=True,null=True)
    worksheet = models.ForeignKey(WorkSheet,unique=True,null=True)
    slug = models.SlugField()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        unique_together = (('book','order'),)
        ordering = ['order']
    
    class ACE:
        content_type = 'Chapter'
        field_map = {
            'book':'book',
            'order':'order',
            'name':'name',
            #'example':'example',
            #'excercise':'excercise',
            #'worksheet':'worksheet',
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
    
    def __unicode__(self):
        return self.title
    
    def page_number(self):
        """ 
        Gets 1-indexed page number.
        """
        return self.order + 1
    
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
        }

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
            'alternatives':'alt_prop',
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

