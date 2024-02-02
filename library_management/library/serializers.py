from rest_framework import serializers
from .models import User, Book, BookDetails, BorrowedBooks

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class BookDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = ['DetailsID', 'NumberOfPages', 'Publisher', 'Language']

class BookSerializer(serializers.ModelSerializer):
    details = BookDetailsSerializer(required=False, allow_null=True)

    class Meta:
        model = Book
        fields = ['BookID', 'Title', 'ISBN', 'PublishedDate', 'Genre', 'details']

# custom update function for the book
    def update(self, instance, validated_data):
        # update Book model fields
        instance.Title = validated_data.get('Title', instance.Title)
        instance.ISBN = validated_data.get('ISBN', instance.ISBN)
        instance.PublishedDate = validated_data.get('PublishedDate', instance.PublishedDate)
        instance.Genre = validated_data.get('Genre', instance.Genre)
        instance.save()

        # update or create BookDetails
        details_data = validated_data.get('details', {})
        details_instance, created = BookDetails.objects.get_or_create(BookID=instance, defaults=details_data)
        
        if not created:
            details_serializer = BookDetailsSerializer(instance=details_instance, data=details_data)
            if details_serializer.is_valid():
                details_serializer.save()
            else:
                raise serializers.ValidationError(details_serializer.errors)

        return instance

# serilizer for borrowed books data
class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = ['UserID', 'BookID', 'BorrowDate', 'ReturnDate']
