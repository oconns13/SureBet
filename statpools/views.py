from django.http import JsonResponse
from django.views.generic import ListView, FormView
from django.shortcuts import render
from . import forms
import requests
import json
from . import models
from django.shortcuts import redirect
from statpools.stores.statpoolsstore import StatPoolsStore
from statpools.stores.scoringstore import ScoringStore
from . import tasks
# Create your views here.

class HomeListView(ListView):
	template_name = 'home.html'
	User = None

	def get(self, request):
		self.User = request.user
		return super().get(request)
	
	def get_queryset(self):
		return

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if (self.User.is_authenticated):
			context['mypools'] = StatPoolsStore().GetStatPoolData(self.User)
			context['user_stats'] = StatPoolsStore.GetUserStats(self.User)
		return context
	
class ViewListView(ListView):
	template_name = 'view.html'
	model = models.StatPoolCategory
	Categories = []
	StatPoolUser = None

	def get_queryset(self):
		qs = super().get_queryset() 
		self.Categories = qs.filter(stat_pool_id=self.kwargs['statpoolid'])
		return self.Categories
	
	def get(self, request, statpoolid):
		if ('user' in request.GET):
			self.StatPoolUser = models.StatPoolUser.objects.filter(id=request.GET['user']).first()
			if self.StatPoolUser.user_id == request.user:
				return redirect('statpoolsview', statpoolid=statpoolid)
		else:
			self.StatPoolUser = models.StatPoolUser.objects.filter(user_id__username=request.user, stat_pool_id__id=statpoolid).first()
		return super().get(request, statpoolid)
	
	def post(self, request, *args, **kwargs):
		if 'setpick' in request.POST:
			self.set_pick(request)
		return redirect('statpoolsview', statpoolid=self.kwargs['statpoolid'])
	
	def set_pick(self, request):
		category = models.StatPoolCategory.objects.filter(id=request.POST['setpick']).first()
		user = models.User.objects.filter(username=request.user).first()
		statpooluser = models.StatPoolUser.objects.filter(user_id=user, stat_pool_id=category.stat_pool).first()
		pick = models.StatPoolUserPick.objects.filter(stat_pool_user=statpooluser).filter(stat_pool_category=category).first()
		if not pick:
			pick = models.StatPoolUserPick.objects.create(stat_pool_user=statpooluser, stat_pool_category=category)
		pick.value = request.POST['statpick']
		pick.save()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = StatPoolsStore.GetCategoriesData(self.Categories, self.StatPoolUser)
		context['statpool'] = models.StatPool.objects.filter(id=self.kwargs['statpoolid']).first()
		context['users'] = models.StatPoolUser.objects.filter(stat_pool_id=context['statpool']).order_by('score')
		context['picksUser'] = self.StatPoolUser.user_id.username
		return context

class CreateFormView(FormView):
	template_name = 'create.html'
	form_class = forms.CreateStatPoolForm
	Categories = []
	Users = []

	def get(self, request):
		return super().get(request)

	def post(self, request, *args, **kwargs):
		if 'add' in request.POST:
			self.add_category(request)
		elif 'remove' in request.POST:
			self.remove_category(int(request.POST['remove']))
		elif 'create' in request.POST:
			self.create(request)
			return redirect('statpoolshome')
		return redirect('statpoolscreate')
	
	def add_category(self, request):
		game = json.loads(request.POST['gameSelectedInput'])
		playerSplit = request.POST['playerSelectedInput'].split('|')
		player = {
			'id':playerSplit[0], 'pos':playerSplit[1], 'num':playerSplit[2], 
			'name':playerSplit[3], 'img':playerSplit[4]
		}
		stat_id = request.POST['statSelectedInput']
		stat = {'id':stat_id,'desc': StatPoolsStore.GetStatByKey(stat_id)['desc']}
		self.Categories.append({'player': player,'stat':stat, 'game': game})

	def remove_category(self, idx):
		self.Categories.remove(self.Categories[idx])

	def create(self, request):
		statpool = models.StatPool.objects.create(name=request.POST['name'], owner=request.user)
		for cat in self.Categories:
			models.StatPoolCategory.objects.create(
				stat_pool = statpool,
				player_id = cat['player']['id'],
				game_id = cat['game']['id'],
				game_desc = cat['game']['away'] + " @ " + cat['game']['home'],
				game_datetime = cat['game']['date'],
				game_status = "scheduled",
				stat_id = cat['stat']['id']
			)
		models.StatPoolUser.objects.create(
			stat_pool_id = statpool,
			user_id = request.user
		)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['categories'] = self.Categories
		return context

class AddCategoryFormView(FormView):
	template_name = 'addcategory.html'
	form_class = forms.CreateStatPoolCategoryForm
	#
	Games = []

	def get(self, request):
		self.Games = StatPoolsStore.GetCurrentWeekGames()
		return super().get(request)
	
	def get_players(self, gameid):
		return JsonResponse({'data': StatPoolsStore.GetGamePlayers(gameid) })
	
	def get_stats(self, pos):
		return JsonResponse({'data': StatPoolsStore.GetStatOptions(pos) })
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['games'] = self.Games
		context['dict'] = { 'id':'test', 'second':'test' }
		return context
	
class AddStatPoolFormView(FormView):
	template_name = 'addstatpool.html'
	form_class = forms.CreateStatPoolForm

	def get(self, request):
		return super().get(request)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = forms.CreateStatPoolForm()
		return context
	
class AddStatPoolUserFormView(FormView):
	template_name = 'adduser.html'
	form_class = forms.AddUserForm
	StatPoolId = None

	def get(self, request):
		self.StatPoolId = request.GET['statpoolid']
		return super().get(request)
	
	def post(self, request, *args, **kwargs):
		form = forms.AddUserForm(request.POST, request=request)
		if form.is_valid():
			user = models.User.objects.filter(username=request.POST["username"]).first()
			statpool = models.StatPool.objects.filter(id=request.POST["statpoolid"]).first()
			models.StatPoolUser.objects.create(
				stat_pool_id = statpool,
				user_id = user
			)
			form = forms.AddUserForm()
		context = self.get_context_data(**kwargs)
		context['form'] = form
		return render(request, self.template_name, context)
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = forms.AddUserForm()
		context['statpoolid'] = self.StatPoolId
		return context