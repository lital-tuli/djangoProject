from rest_framework import serializers
from .models import Comment

class RecursiveCommentSerializer(serializers.Serializer):
    """
    A serializer that recursively serializes replies to comments.
    """
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    
    Includes additional fields:
    - author_username: The username of the comment author
    - replies: Nested serialization of replies to this comment
    """
    author_username = serializers.ReadOnlyField(source='author.username')
    replies = RecursiveCommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Comment
        fields = ('id', 'article', 'content', 'author', 'author_username', 
                  'created_at', 'reply_to', 'replies')
        read_only_fields = ('author', 'created_at')
    
    def validate_content(self, value):
        """
        Validates that the comment content doesn't contain inappropriate words.
        """
        inappropriate_words = ['spam', 'inappropriate', 'offensive']
        for word in inappropriate_words:
            if word in value.lower():
                raise serializers.ValidationError(
                    f"Comment contains inappropriate word: '{word}'"
                )
        return value
    
    def validate_reply_to(self, value):
        """
        Validates that the reply_to comment belongs to the same article.
        """
        if value and 'article' in self.initial_data:
            article_id = self.initial_data.get('article')
            if value.article.id != int(article_id):
                raise serializers.ValidationError(
                    "Reply must be to a comment on the same article"
                )
        return value

