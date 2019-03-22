from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class BaseModel(SafeDeleteModel):
    """
    Base model. Other models will inherit from this
    """
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        abstract = True


# Create your models here.
class Complaints(BaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    owner = models.ForeignKey(User, related_name='complaints', null=True, on_delete=models.SET_NULL)
    description = models.TextField('description', null=False)
    status = models.CharField('status', default='open', max_length=50)
    resolved_at = models.DateTimeField('date resolved', null=True)
    resolver = models.ForeignKey(User, null=True, related_name="resolved_complaints", on_delete=models.SET_NULL)


class ComplaintComments(BaseModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    owner = models.ForeignKey(User, null=True, related_name='complaint_comments', on_delete=models.SET_NULL)
    comment = models.TextField('comment', null=False)
    complaint = models.ForeignKey(Complaints, related_name="comments", on_delete=models.CASCADE)

