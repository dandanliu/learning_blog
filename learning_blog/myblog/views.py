from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    # article = models.Article.objects.get(pk=2)
    articles = models.Article.objects.all()
    return render(request,'myblog/index.html',{'articles':articles})

def article_page(request,article_id):
    article = models.Article.objects.get(pk=article_id)
    return render(request,'myblog/article_page.html',{'article':article})

def edit_page(request,article_id):
    if str(article_id) == '0':
        return render(request,'myblog/edit_page.html')
    article = models.Article.objects.get(pk=article_id)
    return render(request, 'myblog/edit_page.html', {'article': article})

#编辑响应函数
def edit_action(request):
    title = request.POST.get('title','TITLE')
    content = request.POST.get('content','CONTENT')
    article_id = request.POST.get('article_id','0')

    if article_id == "0":

        #如果ID等于0且不为空，创建对象
        if title != None and content != None:
            models.Article.objects.create(title=title, content=content)
        articles = models.Article.objects.all()
        return HttpResponseRedirect('/myblog/index')

    #如果不为0，查询当前ID的title，content,并修改报存
    article = models.Article.objects.get(pk=article_id)
    article.title = title
    article.content = content
    article.save()
    #跳转至文章页面
    return render(request, 'myblog/article_page.html', {'article': article})