from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import logout
from users.models import User
from matchmaking.models import matchmaking
from allauth import socialaccount
from allauth.socialaccount.models import SocialAccount
import time
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponseBadRequest,HttpResponseRedirect
from django.shortcuts import render
from django.http import Http404
from functools import wraps
from django.db.models import F
from users.models import User
def home(request):
    return render(request,'home.html')
def update_ranks():
    users = User.objects.order_by('-wins','-winrate','-score','-pscore','username')
    for rank, user in enumerate(users, start=1):
        user.rank = rank
        user.save()

    return users



def require_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, 'unauthorized.html', status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
from django.contrib.auth.decorators import user_passes_test

def require_superuser(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Not found")
        return view_func(request, *args, **kwargs)
    
    return wrapper

@require_auth
def comingsoon(request):
    return render(request,'comingsoon.html')

@require_superuser
def rerank(request):
    updated_players = update_ranks()
    zen=[]
    for player in updated_players:
        zen.append(f"Player: {player.username}, Rank: {player.rank}")
    return HttpResponseBadRequest(zen)
@csrf_exempt
@require_auth
def delmatch(request):
    if request.method == 'POST':
        player_id = request.POST.get('playerID')
        category = request.POST.get('category')

        try:
            matchmaking_obj = matchmaking.objects.get(player_id=player_id, category=category)
            matchmaking_obj.delete()
            return JsonResponse({'success': True})
        except matchmaking.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Matchmaking entry does not exist.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@require_auth
def settings(request):
    return render(request,'settings.html')
@require_auth
def suggest(request):
    return render(request,'suggest.html')

@require_auth
def reset(request):
    current_user = User.objects.get(pk=request.user)
    current_user.score = 0
    current_user.wins=0
    current_user.winrate=0.0
    current_user.pscore=0
    current_user.total=0
    current_user.lscore=0
    current_user.save()
    update_ranks()
    return redirect('/settings')
@require_auth
def matchup(request):
    category = request.GET.get('category')
    context = {
        'category': category
    }
    return render(request, 'matchmaking.html', context)


@require_auth
def join_game(request):
    try:
        if request.method == 'GET':
            person = User.objects.get(username=request.user.username)
            player_id = person.uid
            playername = request.user.first_name
            category = request.GET.get('category')
            try:
                player = matchmaking.objects.create(player_id=player_id, category=category, playername=playername)
            except:
                player = matchmaking.objects.filter(player_id=player_id)
                player.delete()
                player = matchmaking.objects.create(player_id=player_id, category=category,playername=playername)
            opponent = None
            t=0
            while not opponent and t!=6:
                opponent = matchmaking.objects.filter(category=category).exclude(player_id=player_id).first()
                if not opponent:
                    t+=1
                    time.sleep(2)
                    pass
            if t==6 and not opponent:
                player = matchmaking.objects.filter(player_id=player_id)
                player.delete()
                print('request dropped')
                return JsonResponse({'opponentID': 'dont multi task bro', 'oppnentCategory': 'i know u bad', 'show': False})
            elif opponent:
                response_data = {
                    'opponentID': opponent.player_id,
                    'opponentname':  opponent.playername,
                    'opponentCategory': opponent.category,
                    'show': True
                }
                return JsonResponse(response_data)
            else:
                return JsonResponse({'opponentID': 'dont multi task bro', 'oppnentCategory': 'i know u bad', 'show': False})
        else:
            return HttpResponseBadRequest("Invalid request method.")
    except Exception as e:
        pass
@require_auth
def join_global(request):
    if request.method == 'GET':
        username = request.GET.get('username')
        if username:
            response_data = {
                'username':username,
                'status':True
            }
        else:
            response_data={
                'username': 'null',
                'status': False
            }
        return JsonResponse(response_data)
@require_auth
def mid(request):
    if request.method == 'GET':
        person = User.objects.get(username=request.user.username)
        player_id = person.uid
        opponent_id = request.GET.get('oid')
        opponentname = request.GET.get('oname')
        category = request.GET.get('category')
        room_name = f"{player_id}_{opponent_id}_{category}"
        room_name_alt = f"{opponent_id}_{player_id}_{category}"
        
        room = get_object_or_404(matchmaking, player_id=player_id, category=category)
        room.delete()
                
        if not cache.get(room_name) and not cache.get(room_name_alt):
            cache.set(room_name, True, timeout=120)
        elif not cache.get(room_name) and  cache.get(room_name_alt):
            room_name=room_name_alt
            cache.delete(room_name)
            
        nurl = f"/game?pid={player_id}&roomname={room_name}&playername={request.user.username}&oname={opponentname}"
        return HttpResponseRedirect(nurl)

@require_auth
def gchatmid(request):
    if request.method == 'GET':
        nurl = f"/globalchat"
        return HttpResponseRedirect(nurl)
@require_auth
def logout_now(request):
    logout(request)
    return redirect('/')

@require_auth
def perm_delete(request):
    current_user = request.user
    person = User.objects.get(username=request.user.username)
    person.delete()
    current_user.delete()
    logout(request)
    update_ranks()
    return redirect('/')

@require_auth
def google_login_callback(request):
    google_account = SocialAccount.objects.get(user=request.user, provider='google')
    user_id = request.user.id
    rank = User.objects.count() + 1
    try:
        person = User.objects.get(username=request.user.username)
    except User.DoesNotExist:
        person = User.objects.create(
            email=google_account.extra_data['email'],
            uid = google_account.extra_data['sub'],
            rank=rank,
            score=0,
            username=request.user.username,
            wins=0,
        )

    person.save()
    return redirect('/')
@csrf_exempt
@require_auth
def leaderboard(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        if query:
            leaderboard_data = User.objects.filter(username__icontains=query)
        else:
            leaderboard_data = User.objects.all()
    else:        
        leaderboard_data = User.objects.all()
    context = {
        'leaderboard_data': leaderboard_data
    }

    return render(request, 'leaderboard.html', context)




@require_auth
def game_view(request):
    player_id = request.GET.get('player_id')
    room_name = request.GET.get('room_name')

    context = {
        'player_id': player_id,
        'room_name': room_name,
    }

    return render(request, 'game.html', context)


@require_auth
def chat_view(request):
    username = request.user.username
    context = {
        'username':username
    }
    print(request)
    return render(request,'gchat.html',context)
@csrf_exempt
@require_auth
def update_score(request):
    if request.method == 'POST':
        winner_id = request.POST.get('winner')
        winner_id = winner_id.split(',')[0].strip()
        player1_id = request.POST.get('player1_id')
        player1_score = int(request.POST.get('player1_score'))
        if winner_id == player1_id:
            winner = get_object_or_404(User, uid=winner_id)
            winner.score += player1_score
            winner.wins +=1
            winner.total +=1
            winner.winrate = round(((winner.wins) / (winner.total)) * 100, 1)
            winner.pscore = int((winner.winrate*winner.lscore)/100)
            winner.lscore = player1_score
            winner.save()
        elif winner_id != player1_id:
            player1 = get_object_or_404(User, uid=player1_id)
            player1.score += player1_score
            player1.total += 1
            player1.winrate = round(((player1.wins)/(player1.total))*100,1)
            player1.pscore = int((player1.winrate)*(player1.lscore)/100)
            player1.lscore = player1_score
            player1.save()
        updated_players = update_ranks()
        return JsonResponse({'message': 'Game results handled successfully'})
    else:
        pass
@csrf_exempt
@require_auth
def surrender_score(request):
    if request.method == 'POST':
        winnerid = request.POST.get('winnerid')
        winnerscore = int(request.POST.get('winnerscore'))
        youid = request.POST.get('youid')
        youscore = int(request.POST.get('youscore'))
        winner = get_object_or_404(User, uid=winnerid)
        winner.score += winnerscore
        winner.total +=1
        winner.wins += 1
        winner.winrate = round(((winner.wins)/(winner.total))*100,1)
        winner.pscore = int((winner.winrate*winner.lscore)/100)
        winner.lscore = winnerscore
        winner.save()
        youone = get_object_or_404(User, uid=youid)
        youone.score += youscore
        youone.total += 1
        youone.winrate = round(((youone.wins)/(youone.total))*100,1)
        youone.pscore = int((youone.winrate*youone.lscore)/100)
        youone.lscore = youscore
        youone.save()
        updated_players = update_ranks()
        return JsonResponse({'message': 'Scores updated successfully'})
    else:
        pass
@csrf_exempt
@require_auth
def left_score(request):
    if request.method == 'POST':
        winnerid = request.POST.get('winnerid')
        winnerscore = int(request.POST.get('winnerscore'))
        youid = request.POST.get('youid')
        youscore = int(request.POST.get('youscore'))
        winner = get_object_or_404(User, uid=winnerid)
        winner.score += winnerscore
        winner.wins += 1
        winner.total +=1
        winner.winrate = round(((winner.wins)/(winner.total))*100,1)
        winner.pscore = int((winner.winrate*winner.lscore)/100)
        winner.lscore = winnerscore
        winner.save()
        youone = get_object_or_404(User, uid=youid)
        youone.score -= (100-youscore)
        if youone.score<0:
            youone.score=0
        youone.wins-=1
        if youone.wins<0:
            youone.wins=0
        youone.total += 1
        youone.winrate = round(((youone.wins)/(youone.total))*100,1)
        youone.pscore = int((youone.winrate*youone.lscore)/100)
        youone.lscore = (0)
        youone.save()
        updated_players = update_ranks()
        return JsonResponse({'message': 'Scores updated successfully'})
    else:
        pass

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

