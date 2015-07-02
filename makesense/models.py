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
    example = models.ForeignKey(Example,unique=True)
    excercise = models.ForeignKey(Excercise,unique=True)
    worksheet = models.ForeignKey(WorkSheet,unique=True)
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
            'example':'example',
            'excercise':'excercise',
            'worksheet':'worksheet',
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
    
    def __unicode__(self):
        return self.title
    
    class ACE:
        content_type = 'Page'
        field_map = {
            'chapter':'chapter',
            'title':'title',
            'body':'body',
            'graphic':'graphic',
            'slug':'slug',
        }

class TermAlternativesConverter(object):
    """ 
    Converter for alternatives field of Term model.
    """
    field = 'alternatives'
    deferred = True
    
    def to_local_model(self,ace_content,ace_field_value,local_model):
        """ 
        Creates TermAlternative objects.
        """
        [alt.delete() for alt in local_model.alternatives.all()]
        
        for alt_value in ace_field_value:
            TermAlternative.objects.create(term=local_model,
                                           alternative_term=alt_value)
    
    def to_ace(self,local_model):
        """ 
        Gets alternative term values.
        """
        return [alt.alternative_term for alt in local_model.alternatives.all()]

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
    
    def __unicode__(self):
        return self.term
    
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
            'usage':M2MFieldConverter('usage'),
            'alternatives':TermAlternativesConverter()
        }
        

class TermAlternative(models.Model):
    """ 
    An alternative to the term.
    """
    term = models.ForeignKey(Term,related_name='alternatives')
    alternative_term = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.alternative_term
    
    class Meta:
        unique_together = (('term','alternative_term'),)
