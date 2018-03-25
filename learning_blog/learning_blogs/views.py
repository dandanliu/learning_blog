from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404

#reverse提示错误，将下面的第一行代码换为第二个
#1、from django.core.urlresolvers import reverse
from django.urls import reverse

from .models import Topic,Entry
from .forms import TopicForm,EntryForm

#限制对topics 页面的访问
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
	"""学习笔记的主页"""
	return render(request,'learning_blogs/index.html')

"""限制对topics 页面的访问"""
@login_required
def topics(request):
	"""显示所有的主题"""
	#topics = Topic.objects.order_by('date_added')

	#只允许用户访问自己的主题
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')


	context = {'topics':topics}
	return render(request,'learning_blogs/topics.html',context)


@login_required
def topic(request,topic_id):
	"""显示单个主题及其所有的条目"""
	topic = Topic.objects.get(id=topic_id)

	#确认请求的主题属于当前用户
	if topic.owner != request.user:
		raise Http404

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request,'learning_blogs/topic.html',context)

def new_topic(request):
	"""添加新的主题"""
	if request.method != 'POST':
		#未提交数据，创建一个新表单
		form = TopicForm()
	else:
		#POST提交的数据，对数据进行处理
		form = TopicForm(request.POST)
		if form.is_valid():

			#form.save()

			#将新主题关联到当前用户
			new_topic = form.save(commit=False)
			new_topic.owner = request.user
			new_topic.save()

			return HttpResponseRedirect('/learning_blogs/topics')

	context = {'form':form}
	return render(request,'learning_blogs/new_topic.html',context)


@login_required
def new_entry(request,topic_id):

	"""在特定的主题中添加新条目"""
	topic = Topic.objects.get(id=topic_id)

	if request.method != 'POST':
		#未提交数据，创建一个新表单
		form = EntryForm()
	else:
		#POST提交的数据，对数据进行处理
		form = EntryForm(data=request.POST)

		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.topic = topic

			# 确认请求的主题属于当前用户
			if topic.owner != request.user:
				raise Http404

			new_entry.save()

			#return HttpResponseRedirect('/learning_blogs/topics')
			#return redirect(reverse('/learning_blogs/topics', args=[topic_id]))
			return HttpResponseRedirect(reverse('learning_blogs:topic', args=[topic_id]))

	context = {'topic':topic, 'form':form}
	return render(request,'learning_blogs/new_entry.html',context)


@login_required
def edit_entry(request, entry_id):
	"""编辑既有条目"""
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	topic_id = topic.id

	# 确认请求属于当前用户
	if topic.owner != request.user:
		raise Http404

	if request.method != "POST":
		#初次请求，使用当前条目填充
		form = EntryForm(instance=entry)
	else:
		#Post提交数据，对数据进行处理
		form = EntryForm(instance=entry, data=request.POST)

		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_blogs:topic', args=[topic_id]))
			#return HttpResponseRedirect(reverse('learning_blogs:topics'))


	context = {'entry':entry, 'topic':topic, 'form':form}
	return render(request,'learning_blogs/edit_entry.html',context)