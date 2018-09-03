from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.contrib.auth.decorators import login_required
from .forms import RegistForm, SignupForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
import datetime

DEF_CONTEXT_IN_PAGE = 25

# Create your views here.
def index(request):
	return redirect('memlist')

@login_required(login_url='/로그인/')
def memberlist(request):
	members = Member.objects.all().order_by('joindate')

	keyword = request.GET.get('키워드','')
	if keyword:
		members = members.filter(name__icontains=keyword)

	context_in_page = ''
	if request.method == "POST":
		context_in_page = request.POST.get('members_in_page','')
		if context_in_page:
			request.session['context_in_page'] = context_in_page

	if not context_in_page:
		context_in_page = request.session.get('context_in_page')

	if not context_in_page:
		request.session['context_in_page'] = DEF_CONTEXT_IN_PAGE
		context_in_page = DEF_CONTEXT_IN_PAGE
	paginator = Paginator(members, context_in_page)
	page = request.GET.get('페이지','')
	if page:
		members = paginator.get_page(page)
	else:
		members = paginator.get_page('1')

	for f in members:
		if f.birthday == datetime.date(9999, 12, 31):
			f.birthday = ""
		if f.recentdate == datetime.date(1, 1, 1):
			f.recentdate = "없음"

	context = {'members':members}

	page_numbers_range = 5
	max_index = len(paginator.page_range)
	current_page = int(page) if page else 1

	start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
	end_index = start_index + page_numbers_range
	if end_index >= max_index:
		end_index = max_index

	page_range = paginator.page_range[start_index:end_index]
	context['page_range'] = page_range

	return render(request, 'member/memberlist.html', context)

@login_required(login_url='/로그인/')
def memberlist_order(request, field, order):
	if(field == "이름"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-name')
		else:
			members = Member.objects.all().order_by('name')
	elif(field == "성별"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-gender')
		else:
			members = Member.objects.all().order_by('gender')
	elif(field == "생일"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-birthday')
		else:
			members = Member.objects.all().order_by('birthday')
	elif(field == "거주지"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-homeplace')
		else:
			members = Member.objects.all().order_by('homeplace')
	elif(field == "직장"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-workplace')
		else:
			members = Member.objects.all().order_by('workplace')
	elif(field == "가입일자"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-joindate')
		else:
			members = Member.objects.all().order_by('joindate')
	elif(field == "최근활동일자"):
		if(order == "내림차순"):
			members = Member.objects.all().order_by('-recentdate')
		else:
			members = Member.objects.all().order_by('recentdate')
	else:
		members = Member.objects.all().order_by('joindate')
	keyword = request.GET.get('키워드','')
	if keyword:
		members = members.filter(name__icontains=keyword)

	context_in_page = ''
	if request.method == "POST":
		context_in_page = request.POST.get('members_in_page','')
		if context_in_page:
			request.session['context_in_page'] = context_in_page

	if not context_in_page:
		context_in_page = request.session.get('context_in_page')

	if not context_in_page:
		request.session['context_in_page'] = DEF_CONTEXT_IN_PAGE
		context_in_page = DEF_CONTEXT_IN_PAGE
	paginator = Paginator(members, context_in_page)
	page = request.GET.get('페이지','')
	if page:
		members = paginator.get_page(page)
	else:
		members = paginator.get_page('1')

	for f in members:
		if f.birthday == datetime.date(9999, 12, 31,):
			f.birthday = ""
		if f.recentdate == datetime.date(1, 1, 1):
			f.recentdate = "없음"

	context = {'members':members, 'field':field, 'order':order}

	page_numbers_range = 5
	max_index = len(paginator.page_range)
	current_page = int(page) if page else 1

	start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
	end_index = start_index + page_numbers_range
	if end_index >= max_index:
		end_index = max_index

	page_range = paginator.page_range[start_index:end_index]
	context['page_range'] = page_range

	return render(request, 'member/memberlist_order.html', context)

@login_required(login_url='/로그인/')
def memberinfo(request, id):
	member = get_object_or_404(Member, pk = id)

	if request.method == "POST":
		form = RegistForm(request.POST or None, instance=member)
		if form.is_valid():
			post = form.save(commit = False)
			if not post.birthday:
				post.birthday="9999-12-31"
			post.save()
			return redirect('memlist')
		else:
			return HttpResponse('<script>alert("유효하지 않은 값을 입력하셨습니다.")\nhistory.back()</script>')
	else:
		if member.birthday == datetime.date(9999,12,31):
			member.birthday = ""
		else:
			member.birthday = "{}-{:02.0f}-{:02.0f}".format(member.birthday.year, member.birthday.month, member.birthday.day)
		member.joindate = "{}-{:02.0f}-{:02.0f}".format(member.joindate.year, member.joindate.month, member.joindate.day)
		if member.recentdate == datetime.date(1,1,1):
			member.recentdate = ""
		else:		
			member.recentdate = "{}-{:02.0f}-{:02.0f}".format(member.recentdate.year, member.recentdate.month, member.recentdate.day)
		return render(request, 'member/memberinfo.html', {'member':member})

@login_required(login_url='/로그인/')
def register(request):
	if request.method == "POST":
		form = RegistForm(request.POST)
		if form.is_valid():
			post = form.save(commit = False)
			if not post.birthday:
				post.birthday="9999-12-31"
			if not post.recentdate:
				post.recentdate="0001-01-01"
			post.save()
			return redirect('memlist')
		else:
			return HttpResponse('<script>alert("유효하지 않은 값을 입력하셨습니다.")\nhistory.back()</script>')
	else:
		form = RegistForm()
		return render(request, 'member/regist.html', {'form':form})

@login_required(login_url='/로그인/')
def memberdel(request, id):
	member = get_object_or_404(Member, pk = id)
	member.delete()
	return redirect('memlist')

def signup(request):
    if request.method == 'POST':
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit = False)
            user.is_active=False
            user.save()
            return redirect('signup_done')
    else:
        signup_form = SignupForm()

    context = {
        'signup_form': signup_form,
    }
    return render(request, 'member/signup.html', context)

def signup_done(request):
	return render(request, 'member/signup_done.html')