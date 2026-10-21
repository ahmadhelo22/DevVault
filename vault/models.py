from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models


class Status(models.TextChoices):
    DRAFT = "draft", "Draft"
    ACTIVE = "active", "Active"
    ARCHIVED = "archived", "Archived"


ALLOWED_TRANSITIONS = {
    "draft": {"active"},
    "active": {"draft", "archived"},
    "archived": {"active"},
}


class Tag(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tags",
    )
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["owner", "name"],
                name="unique_user_tag",
            )
        ]

    def __str__(self):
        return self.name


class Snippet(models.Model):
    class Language(models.TextChoices):
        PYTHON = "python", "Python"
        JAVASCRIPT = "javascript", "JavaScript"
        SQL = "sql", "SQL"
        HTML = "html", "HTML"
        CSS = "css", "CSS"
        BASH = "bash", "Bash"
        OTHER = "other", "Other"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="snippets",
    )
    title = models.CharField(max_length=200)
    language = models.CharField(
        max_length=30,
        choices=Language.choices,
    )
    code = models.TextField()
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="snippets",
    )

    class Meta:
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["owner", "status"]),
            models.Index(fields=["owner", "-updated_at"]),
        ]

    def __str__(self):
        return self.title
