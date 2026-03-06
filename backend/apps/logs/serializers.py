from rest_framework import serializers
from .models import LogFile


class LogUploadSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogFile
        fields = ["file"]

    def validate_file(self, file):

        allowed_extensions = [".log", ".txt"]

        if not any(file.name.endswith(ext) for ext in allowed_extensions):
            raise serializers.ValidationError(
                "Only .log and .txt files are allowed."
            )

        max_size = 50 * 1024 * 1024  # 50 MB

        if file.size > max_size:
            raise serializers.ValidationError(
                "File size must be under 50 MB."
            )

        return file