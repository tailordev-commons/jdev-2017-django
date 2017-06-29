from django.db import models


class Country(models.Model):
    """Country where the data have been recorded"""

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ('name', )

    def __str__(self):
        return self.name


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
        verbose_name = "Record"
        verbose_name_plural = "Records"
        ordering = ('country', 'date')
        unique_together = ('date', 'country')

    def __str__(self):
        return '{} - {}'.format(self.country, self.date)
