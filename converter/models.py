from django.db import models


class Conversion(models.Model):
    input_file_name = models.CharField(max_length=255)
    output_file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.input_file_name} to {self.output_file_name} on {self.created_at}"
