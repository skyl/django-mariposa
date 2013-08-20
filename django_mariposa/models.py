from django.db import models


class DBMigration(models.Model):
    filename = models.CharField(max_length=255, unique=True)
    sha1 = models.CharField(max_length=40, primary_key=True)
    executed_dt = models.DateField()

    def __unicode__(self):
        return "%s-%s %s" % (
            self.filename,
            self.sha1,
            self.timestamp,
        )

    class Meta:
        db_table = "dbmigration"
