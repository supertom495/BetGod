import re
from django.http import HttpResponse, JsonResponse
from .models import Bet, Profile, Wallet, Card, User, Event, Team
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from datetime import datetime
from django.db.models import Q
# Create your views here.
from dashboard.models import Author, Post
from .forms import UserForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render


# logic for profile page
def profile(request):
    # retrieve information from database
    u = Profile.objects.get(user_id=request.user.id)
    user = request.user
    wallet = Wallet.objects.get(wallet_id=u.user_wallet_id)
    c = Card.objects.get(card_number=wallet.wallet_card_id)
    be = Bet.objects.filter(bet_user_id=user.id)

    # add funds or withdraw
    if request.method == 'POST':

        type = request.POST['type']
        amount = request.POST['amount']

        if type == 'add':
            if amount.isdigit() and int(amount) > 0:
                wallet.wallet_points += int(amount)
            else:
                return HttpResponse('Invalid argument!')
        if type == 'withdraw' and int(amount) < wallet.wallet_points:
            if amount.isdigit():
                wallet.wallet_points -= int(amount)
            else:
                return HttpResponse('Invalid argument!')
        wallet.save()

    context = {
        "user": user,
        "profile": u,
        "card": c,
        "bet": be,
    }
    return render(request, "profile.html", context)


# homepage logic
def homepage(request):
    # redirect to search page
    if request.method == 'POST':
        keyword = request.POST['keyword']
        return redirect('search', keyword)

    # display lasted 8 matches
    events = Event.objects.all().order_by('-event_id')[:7]

    context = {'events': events}

    return render(request, "HomePage.html", context)


def gameList(request, game):
    # redirect to searching page
    if request.method == 'POST':
        keyword = request.POST['keyword']
        return redirect('search', keyword)

    # query matches with given game type
    event_list = Event.objects.filter(event_name=game)
    page = request.GET.get('page', 1)

    # separate result to different pages
    paginator = Paginator(event_list, 8)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'gameList.html', {'events': events})


# search matches with keyword
def search(request, keyword):
    # redirect to searching result
    if request.method == 'POST':
        keyword = request.POST['keyword']
        return redirect('search', keyword)

    # query from database if the team name contains keyword
    event_list = Event.objects.filter(Q(event_team_a__team_name__contains=keyword) | Q(event_team_b__team_name__contains=keyword))
    page = request.GET.get('page', 1)

    # separate results into pages
    paginator = Paginator(event_list, 8)
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    return render(request, 'gameList.html', {'events': events})


def register(request):
    context = {}
    # context to display error information
    context['err'] = ''
    if request.method == 'POST':
        # Create card object
        card = Card()
        card.card_type = request.POST['cct']

        # Credit card type checking
        if not ((card.card_type == 'Visa') or (card.card_type == 'Master')):
            context['err'] += 'Invalid card type! Visa or Master only!\n'

        # Credit card number checking
        ccn = request.POST['ccn']
        if input_check(ccn, 'int'):
            card.card_number = int(ccn)
        else:
            context['err'] += 'Invalid card number!\n'

        # Credit card expiration date checking
        date = request.POST['expire_date']
        if re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', date):
            card.card_expiration_date = date
        else:
            context['err'] += 'Invalid expiration date!\n'

        # Credit card cvv checking
        cvv = request.POST['CVV']
        if input_check(cvv, 'int'):
            card.card_CVV = int(cvv)
        else:
            context['err'] += 'Invalid cvv number! Maximum 20 digits!\n'

        # Wallet object creation
        wallet = Wallet()
        points = request.POST['points']
        if input_check(points, 'int'):
            wallet.wallet_points = points
        else:
            context['err'] += 'Invalid points number! Maximum 99999 points!\n'

        # user creation
        username = request.POST['username']
        if not input_check(username, 'str'):
            context['err'] += 'Invalid username!\n'
        password = request.POST['psw']
        if not input_check(password, 'str') and len(password) > 6:
            context['err'] += 'Invalid password! Length at least should be 6!\n'
        password_con = request.POST['psw-repeat']
        if password != password_con:
            context['err'] += 'Invalid password confirmation!\n'
        email = request.POST['email']
        if not input_check(email, 'str') or not ('@' in email):
            context['err'] += 'Invalid email!\n'

        # profile creation
        pf = Profile()
        question = request.POST['security-question']
        if re.search(r'[^0-9a-zA-Z?\s]]', question):
            context['err'] += 'Invalid security question! Letters and question mark and spaces only!\n'
        else:
            pf.user_security_question = question
        answer = request.POST['security-question-answer']
        if re.search(r'[^0-9a-zA-Z?\s]]', question):
            context['err'] += 'Invalid security answer! Letters and question mark and spaces only!\n'
        else:
            pf.user_security_answer = answer

        if User.objects.filter(username=username):
            context['err'] += 'User already exists! Try another username!'

        # If there is no error, save the data
        if context['err'] is not '':
            return render(request, "register.html", context)
        else:
            if Card.objects.filter(card_number=card.card_number):
                card = Card.objects.get(card_number=card.card_number)
            else:
                card.save()
            wallet.wallet_card = card
            wallet.save()
            user = User.objects.create_user(username=username, password=password, email=email)
            pf.user_wallet_id = wallet.wallet_id
            pf.user = user
            pf.save()
            return redirect('homepage')

    return render(request, "register.html", context)


def ok(request):
    return "ok"

def betConfirm(request, event_id, team_id):
    # Only logged in user can bet on matches
    if not request.user.id:
        return HttpResponse('You have not logged in!')
    if request.method == 'POST':
        points = request.POST['point']
        odds = request.POST['odds']
        prof = Profile.objects.get(user_id=request.user.id)
        wal = Wallet.objects.get(wallet_id=prof.user_wallet_id)
        newB = wal.wallet_points
        newB -= int(points)
        wal.wallet_points = newB
        wal.save()
        bet = Bet()
        max_bet_id = 0
        for b in Bet.objects.all():
            if b.bet_id > max_bet_id:
                max_bet_id = b.bet_id
        max_bet_id += 1
        bet.bet_id = max_bet_id
        bet.bet_amount = int(points)
        myDate = datetime.now()
        formatedDate = myDate.strftime("%Y-%m-%d")
        bet.bet_date = formatedDate
        bet.bet_event = Event.objects.get(event_id=event_id)
        bet.bet_odds = float(odds)
        bet.bet_result = False
        bet.bet_result_released = False
        bet.bet_user = request.user
        bet.save()
        return redirect('betSuccess')
    e = Event.objects.get(event_id=event_id)
    t = Team.objects.get(id=team_id)
    profile = Profile.objects.get(user_id=request.user.id)
    w = Wallet.objects.get(wallet_id=profile.user_wallet_id)

    context = {
        "event": e,
        "team": t,
        "wallet": w,
    }
    return render(request, "Bet_confirm.html",context)


def betPage(request, event_id):
    e = Event.objects.get(event_id=event_id)
    context = {
        "event": e,
    }
    return render(request, "Bet_page.html", context)


def Bet_success(request):
    return render(request, "Bet_success.html")

class RegisterFormView(View):
    form_class = UserForm
    template_name = 'register.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)
            user.profile.user_security_question = form.cleaned_data['user_security_question']
            user.profile.user_security_answer = form.cleaned_data['user_security_answer']

            if user is not None:
                if user.is_active:
                    login(request, user)

                    return redirect('addFunds')

        return render(request, self.template_name, {'form': form})


# return json object queried by keyword
def ajax_load_teams(request):
    if request.method == 'GET':
        game = request.GET.get('game')
        if game:
            events = Event.objects.filter(event_name__contains=game)
            data = list(Team.objects.filter(Q(team_name__in=events.values('event_team_a__team_name')) |
                                             Q(team_name__in=events.values('event_team_b__team_name'))).values('team_name').distinct())
            return JsonResponse(list(data), safe=False)


##################### inner funcitons ###########################

# To check the input
def input_check(str, type):
    if type == 'str':
        if re.search(r'[^0-9a-zA-Z@.\s]', str) is None:
            return True
        else:
            return False
    else:
        if re.search(r'[^0-9]', str) is None:
            return True
        else:
            return False
