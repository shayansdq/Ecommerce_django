from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
# Create your views here.
from comments.forms import CommentCreateForm
from comments.models import Comment
from products.models import Product


class SaveCommentView(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm

    def post(self, request, *args, **kwargs):
        print('c', request.session['product_cm'])
        product_instance = get_object_or_404(Product, pk=int(request.session['product_cm']))
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.customer = request.user.customer
            new_comment.product = product_instance
            new_comment.save()
            messages.success(request, 'Your comment submitted successfully', 'success')
            return redirect('products:product_detail', product_instance.id)


class AddReplyComment(LoginRequiredMixin, CreateView):
    form_class = CommentCreateForm

    def post(self, request, *args, **kwargs):
        print('sss', kwargs['comment_id'])
        form = self.form_class(request.POST)
        product_instance = get_object_or_404(Product, pk=int(request.session['product_cm']))
        if form.is_valid():
            new_comment: Comment = form.save(commit=False)
            parent_comment: Comment = Comment.objects.get(pk=int(kwargs['comment_id']))
            new_comment.customer = request.user.customer
            new_comment.product = product_instance
            new_comment.reply = parent_comment
            new_comment.is_reply = True
            new_comment.save()
            messages.success(request, 'Your comment submitted successfully', 'success')
            return redirect('products:product_detail', product_instance.id)
