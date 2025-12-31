from django.test import TestCase, Client
from django.urls import reverse
from .models import Note

class NoteModelTest(TestCase):
    def test_note_creation(self):
        note = Note.objects.create(
            title="Test Note",
            content="This is a test note"
        )
        self.assertEqual(note.title, "Test Note")
        self.assertEqual(str(note), "Test Note")

class HomeViewTest(TestCase):
    def test_home_view(self):
        client = Client()
        response = client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome to Django!")
