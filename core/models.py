from django.db import models


class Contact(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField()
    service = models.CharField(max_length=100)
    message = models.TextField(max_length=2000)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def __str__(self):
        return f"{self.fname} {self.lname} — {self.email} ({self.submitted_at:%Y-%m-%d})"
