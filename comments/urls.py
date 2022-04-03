from django.urls import path

from comments.views import SaveCommentView, AddReplyComment

app_name = 'comments'

urlpatterns = [
    path('save_comment',SaveCommentView.as_view(),name='save_comment'),
    path('add_reply/<int:comment_id>',AddReplyComment.as_view(),name='add_reply'),
]