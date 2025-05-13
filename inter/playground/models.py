from django.db import models

class PDFSummary(models.Model):
    user = models.CharField(max_length=100)
    full_text = models.TextField()
    summary = models.TextField()

    def __str__(self):
        return f"Summary by {self.user}"
