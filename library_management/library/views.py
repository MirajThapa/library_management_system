from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Book, BookDetails, BorrowedBooks
from .serializers import UserSerializer, BookSerializer, BookDetailsSerializer, BorrowedBooksSerializer


# function based views 
# User APIs
@api_view(['POST'])
def create_user(request):
    # gets the serilized data and save it in postgresql database
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# list down all the users details
@api_view(['GET'])
def list_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(UserID=user_id)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = UserSerializer(user)
    return Response(serializer.data)

# can add new books
@api_view(['POST'])
def add_new_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# gets all the books
@api_view(['GET'])
def list_all_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_book_by_id(request, book_id):
    # exception handle if the books is not availan=e
    try:
        book = Book.objects.get(BookID=book_id)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)

@api_view(['PUT'])
def assign_update_book_details(request, book_id):
    try:
        book = Book.objects.get(BookID=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    book_serializer = BookSerializer(instance=book, data=request.data)
    if book_serializer.is_valid():
        # update book fields
        book_serializer.save()

        # check if the book has associated details
        details_data = request.data.get('details')
        details_instance = book.details

        if details_instance is not None:
            # update existing details
            details_serializer = BookDetailsSerializer(instance=details_instance, data=details_data)
        else:
            # creating new details if none exist
            details_serializer = BookDetailsSerializer(data=details_data)

        if details_serializer.is_valid():
            details_serializer.save()
            book.details = details_serializer.instance
            return Response(book_serializer.data)
        else:
            return Response(details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# borrow books
@api_view(['POST'])
def borrow_book(request):
    serializer = BorrowedBooksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def return_book(request, borrowed_book_id):
    # check if the book is borrowed or not
    try:
        borrowed_book = BorrowedBooks.objects.get(id=borrowed_book_id)
    except BorrowedBooks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

# update the return_date 
    serializer = BorrowedBooksSerializer(instance=borrowed_book, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# gets all the books
@api_view(['GET'])
def list_all_borrowed_books(request):
    borrowed_books = BorrowedBooks.objects.all()
    serializer = BorrowedBooksSerializer(borrowed_books, many=True)
    return Response(serializer.data)

