from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django import IntegrityError

from .models import Post, Comment, Like


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pass12345")

    def test_post_str_returns_title(self):
        post = Post.objects.create(
            title="Hello",
            content="World",
            author=self.user,
        )
        self.assertEqual(str(post), "Hello")

    def test_get_absolute_url(self):
        post = Post.objects.create(
            title="A",
            content="B",
            author=self.user,
        )
        self.assertEqual(post.get_absolute_url(), reverse("post-detail", kwargs={"pk": post.pk}))


class CommentModelTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.commenter = User.objects.create_user(username="bob", password="pass12345")
        self.post = Post.objects.create(title="T", content="C", author=self.author)

    def test_comment_str_contains_username(self):
        c = Comment.objects.create(post=self.post, user=self.commenter, content="Nice")
        self.assertIn("bob", str(c).lower())

    def test_comment_likes_many_to_many(self):
        c = Comment.objects.create(post=self.post, user=self.commenter, content="Nice")
        c.likes.add(self.author)
        self.assertEqual(c.likes.count(), 1)
        self.assertTrue(c.likes.filter(username="author").exists())


class LikeModelTests(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.user = User.objects.create_user(username="charlie", password="pass12345")
        self.post = Post.objects.create(title="T", content="C", author=self.author)

    def test_like_str(self):
        like = Like.objects.create(post=self.post, user=self.user)
        self.assertIn("charlie", str(like).lower())

    def test_unique_like_per_user_per_post(self):
        Like.objects.create(post=self.post, user=self.user)
        with self.assertRaises(IntegrityError):
            Like.objects.create(post=self.post, user=self.user)


