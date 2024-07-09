from django.db import models
from django.contrib.contenttypes.fields import GenericRelation

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name

class TestSuite(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=1)  # Пример: default=1
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.name

class TestCase(models.Model):
    name = models.CharField(max_length=255)
    suite = models.ForeignKey(TestSuite, on_delete=models.CASCADE, related_name='test_cases')
    setup = models.TextField(blank=True)
    scenario = models.TextField(blank=True)
    expected = models.TextField(blank=True)
    description = models.TextField(blank=True)
    is_steps = models.BooleanField(default=False)
    is_archive = models.BooleanField(default=False)
    attributes = models.JSONField(default=dict, blank=True)
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.name

class TestCaseStep(models.Model):
    name = models.CharField(max_length=255)
    scenario = models.TextField()
    expected = models.TextField(blank=True)
    test_case = models.ForeignKey(TestCase, on_delete=models.CASCADE, related_name='steps')
    sort_order = models.PositiveIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

class Comment(models.Model):
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[:20]
