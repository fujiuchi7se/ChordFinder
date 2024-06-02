from django.shortcuts import render, get_object_or_404
from .models import ChordProgression

def key_list(request):
    keys = ChordProgression.objects.values_list('key', flat=True).distinct()
    return render(request, 'chords/key_list.html', {'keys': keys})

def song_list(request, key):
    songs = ChordProgression.objects.filter(key=key)
    return render(request, 'chords/song_list.html', {'songs': songs, 'key': key})

def song_detail(request, song_id):
    song = get_object_or_404(ChordProgression, id=song_id)
    return render(request, 'chords/song_detail.html', {'song': song})