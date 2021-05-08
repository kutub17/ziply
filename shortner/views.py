from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import shortUrl
import random, string


# Create your views here.
@login_required(login_url='/login')
def dashboard(req):
    usr = req.user
    urls = shortUrl.objects.filter(user=usr)

    return render(req, 'dashboard.html', {'urls': urls})


def random_generate():
    return ''.join(random.choice(string.ascii_lowercase+string.digits) for _ in range(6))


@login_required(login_url='/login')
def generate(req):
    if req.method == 'POST':
        if req.POST['original']:
            usr = req.user
            original = req.POST['original']
            generated = False
            while not generated:
                short = random_generate()
                newurl = shortUrl(
                    user=usr,
                    original_url=original,
                    short_url=short,

                )
                newurl.save()
                return redirect(dashboard)

        else:
            messages.error(req, "Empty Fields")
            return redirect(dashboard)

    else:
        return redirect(dashboard)


def home(req, query=None):
    if not query or query is None:
        return render(req, 'home.html')
    else:
        try:
            check = shortUrl.objects.get(short_url=query)
            check.visits = check.visits + 1
            check.save()
            url_to_redirect = check.original_url
            return redirect(url_to_redirect)
        except shortUrl.DoesNotExists:
            return render(req, 'home.html', {"error": "error"})
