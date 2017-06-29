from django.db import models


class Country(models.Model):
    """Country where the data have been recorded"""

    name = models.CharField(
        max_length=100,
        unique=True
    )


class Record(models.Model):
    """Temperature record"""

    date = models.DateField()

    temperature = models.DecimalField(
        "Average temperature",
        help_text="In Celcius",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    uncertainty = models.DecimalField(
        "Average temperature uncertainty",
        help_text="The 95% confidence interval around the average",
        decimal_places=3,
        max_digits=6,
        null=True,
        blank=True,
    )

    country = models.ForeignKey(
        'Country',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('date', 'country')
