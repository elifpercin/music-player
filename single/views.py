from django.db.models import Q
from .forms import AlbumForm, SarkiForm, UserForm
from .models import Album, Sarki
from django.shortcuts import render, get_object_or_404,reverse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseRedirect

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']
AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']


def create_song(request, album_id):
    form = SarkiForm(request.POST or None, request.FILES or None)

    album = get_object_or_404(Album, pk=album_id)

    if form.is_valid():

        albums_songs = album.sarki_set.all()

        for s in albums_songs:

            if s.sarki_basligi == form.cleaned_data.get("sarki_basligi"):
                context = {'album': album, 'form': form, 'error_message': 'Var Olan Bir Şarkı'}

                return render(request, 'single/create_song.html', context)

        sarki = form.save(commit=False)

        sarki.album = album

        sarki.ses_dosyalari = request.FILES['ses_dosyalari']

        file_type = sarki.ses_dosyalari.url.split('.')[-1]

        file_type = file_type.lower()

        if file_type not in AUDIO_FILE_TYPES:
            context = {'album': album,'form': form,'error_message': 'Audio file must be WAV, MP3, or OGG'}

            return render(request, 'single/create_song.html', context)

        sarki.save()

        return render(request, 'single/detail.html', {'album': album})

    context = {'album': album, 'form': form}

    return render(request, 'single/create_song.html', context)


def sarkilar(request, filter_by):
    if not request.user.is_authenticated():

        return render(request, 'single/login.html')

    else:

        try:

            song_ids = []

            for album in Album.objects.filter(user=request.user):

                for song in album.sarki_set.all():
                    song_ids.append(song.pk)

            kullanici_muzik = Sarki.objects.filter(pk__in=song_ids)

            if filter_by == 'favoriler':
                kullanici_muzik = kullanici_muzik.filter(favoriler=True)

        except Album.DoesNotExist:
            kullanici_muzik = []

        return render(request, 'single/sarkilar.html', {'song_list': kullanici_muzik, 'filter_by': filter_by})


def create_album(request):
    if not request.user.is_authenticated():

        return render(request, 'single/login.html')

    else:

        form = AlbumForm(request.POST or None, request.FILES or None)

        if form.is_valid():

            album = form.save(commit=False)

            album.user = request.user

            album.album_logo = request.FILES['album_logo']

            file_type = album.album_logo.url.split('.')[-1]

            file_type = file_type.lower()

            if file_type not in IMAGE_FILE_TYPES:
                context = {'album': album, 'form': form, 'error_message': 'Image file must be PNG, JPG, or JPEG'}

                return render(request, 'single/create_album.html', context)

            album.save()

            return render(request, 'single/detail.html', {'album': album})

        context = {

            "form": form,

        }

    return render(request, 'single/create_album.html', context)


def register(request):

    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user:  # eğerki kullanıcı varsa
            if user.is_active:
                login(request, user)

                albums = Album.objects.filter(user=request.user)
                return render(request, 'single/index.html', {'albums': albums})

    context = {"form": form}

    return render(request, 'single/register.html', context)


def index(request):
    if not request.user.is_authenticated():  # eğerki kullanıcının kimlik doğrulanmadıysa

        return render(request, 'single/login.html')  # giriş yapsın
    else:
        albums = Album.objects.filter(user=request.user)  # kullanıcının filtrelediği album alanları

        sarki_sonucu = Sarki.objects.all()

        query = request.GET.get("q")  # sorgu

        if query:

            albums = albums.filter(
                Q(album_basligi__icontains=query) | Q(sarkici__icontains=query)).distinct()

            sarki_sonucu = sarki_sonucu.filter(Q(sarki_basligi__icontains=query)).distinct()

            return render(request, 'single/index.html', {'albums': albums, 'sarkilar': sarki_sonucu})

        else:
            print(albums)
            return render(request, 'single/index.html', {'albums': albums})


def kullanici_giris(request):
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                albums = Album.objects.filter(user=request.user)
                return render(request, 'single/index.html', {'albums': albums})

            else:
                return render(request, 'single/login.html', {'error_message': 'Hesabınız Buluanamadı'})

        else:
            return render(request, 'single/login.html', {'error_message': 'Geçersiz Giriş'})
    else:
        return render(request, 'single/login.html')


def kullanici_cikis(request):
    logout(request)

    form = UserForm(request.POST or None)

    context = {"form": form, }

    return render(request, 'single/login.html', context)


def detail(request, album_id):
    if not request.user.is_authenticated():

        return render(request, 'single/login.html')

    else:

        user = request.user

        album = get_object_or_404(Album, pk=album_id)

        return render(request, 'single/detail.html', {'album': album, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Sarki, pk=song_id)

    try:

        if song.favoriler:

            song.favoriler = False

        else:

            song.favoriler = True
        song.save()

    except (KeyError, Sarki.DoesNotExist):

        return JsonResponse({'success': False})

    else:
        #return render(request, 'single/sarkilar.html', {'song_list': kullanici_muzik, 'filter_by': filter_by})
        url = request.GET.get('sayfa')
        print(url)
        if not url:
            url = reverse('single:detail',kwargs={'album_id':song.album.id})
        return HttpResponseRedirect(url)


def album_sil(request, album_id):
    album = Album.objects.get(pk=album_id)

    album.delete()

    albums = Album.objects.filter(user=request.user)

    return render(request, 'single/index.html', {'albums': albums})


def sarki_sil(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)

    sarki = Sarki.objects.get(pk=song_id)


    sarki.delete()

    return render(request, 'single/detail.html', {'album': album})


def favori_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)

    try:

        if album.favoriler:

            album.favoriler = False

        else:

            album.favoriler = True

        album.save()

    except (KeyError, Album.DoesNotExist):

        return JsonResponse({'success': False})


    else:

        return HttpResponseRedirect(reverse('single:detail', kwargs={'album_id': album.album.id}))