from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member
from django.contrib.auth.decorators import login_required
from .forms import RegistForm, SignupForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
import datetime


# Create your views here.
def index(request):
	return redirect('memlist')

@login_required(login_url='/로그인/')
def memberlist(request):
	members = Member.objects.all().order_by('joindate')
	for f in members:
		if f.birthday == datetime.date(9999, 12, 31,):
			f.birthday = ""
	context = {'members':members}
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
	for f in members:
		if f.birthday == datetime.date(9999, 12, 31,):
			f.birthday = ""
	context = {'members':members, 'field':field, 'order':order}
	return render(request, 'member/memberlist_order.html', context)

@login_required(login_url='/로그인/')
def memberinfo(request, id):
	member = get_object_or_404(Member, pk = id)

	if request.method == "POST":
		form = RegistForm(request.POST or None, instance=member)
		if form.is_valid():
			post = form.save(commit = False)
			if not post.birthday:
				post.birthday="1111-11-11"
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
