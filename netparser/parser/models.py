from itertools import chain

from django.db import models


class PrintableModel(models.Model):
    def __repr__(self):
        return str(self.to_dict())

    def to_dict(instance):
        opts = instance._meta
        data = {}
        for f in chain(opts.concrete_fields, opts.private_fields):
            data[f.name] = f.value_from_object(instance)
        for f in opts.many_to_many:
            data[f.name] = [i.id for i in f.value_from_object(instance)]
        return data

    class Meta:
        abstract = True


class AsInfo(PrintableModel):
    created = models.DateTimeField(auto_now_add=True)
    jobid = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    provider = models.TextField()

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['jobid']),]
        verbose_name = 'asinfo'
        verbose_name_plural = 'asinfos'
        managed = False
        db_table = 'as_info'


class Network(PrintableModel):
    network = models.CharField(max_length=128)
    provider = models.TextField()
    country = models.TextField()
    ip_version = models.PositiveSmallIntegerField()
    as_info = models.ForeignKey(
        AsInfo, related_name='networks', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'network'
        verbose_name_plural = 'networks'
        managed = False
        db_table = 'network'
