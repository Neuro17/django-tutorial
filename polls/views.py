# Create your views here.
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic

from models import Question
from models import Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#   latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')
#    context = RequestContext(request, {
#        'latest_question_list': latest_question_list,
#    })
#    return HttpResponse(template.render(context))

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

#def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk=question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question does not exist")
#    return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def recent(request, n_polls):
    try:
        selected_question = Question.objects.get(pk=request.POST['question'])
    except KeyError: #non e' una richiesta POST o non ho selezionato nessun messaggio
        question_list_ord = Question.objects.order_by('-pub_date')
        latest_question_list = []
        for q in question_list_ord:
            if q.was_published_recently():
                latest_question_list.append(q)
        if request.method == 'GET':  #caso richiesta GET
            context = {'latest_question_list': latest_question_list[:int(n_polls)]}
            return render(request, 'polls/recent.html', context)
        elif request.method == 'POST':   #caso richiesta POST con selezione non corretta
            return render(request, 'polls/recent.html', {
             'latest_question_list': latest_question_list[:int(n_polls)],
                    'error_message': "You didn't select a question.",
            })
    else:    #caso POST con scelta selezionata correttamente
        for c in selected_question.choice_set.all():
            c.votes = 0
            c.save()
            return HttpResponseRedirect(reverse('polls:results', args=(selected_question.id,)))