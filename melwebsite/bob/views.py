from django.shortcuts import render, redirect
from .models import Project, Question
from plotly.offline import plot
import requests
import plotly.graph_objs as go

def index(request):
    return render(request, 'bob/index.html')

def projects(request):
    projects = Project.objects.all()
    return render(request, 'bob/projects.html', {'projects': projects})

def questions(request):
    if request.method == 'POST':
        question_text = request.POST.get('question')
        if question_text:
            Question.objects.create(question_text=question_text)

            return redirect('bob:answers')  # Change this to the correct URL name
    return render(request, 'bob/questions.html')

def answers(request):
    questions = Question.objects.all()
    return render(request, 'bob/answers.html', {'questions'
                                                : questions})

def graph(request):
    pokemon_names = ['pikachu', 'goomy', 'rowlet', 'espurr', 'bulbasaur',
                     'squirtle', 'lucario', 'tinkaton']
    stat_type = 'hp'
    pokemon_stats = []
    hover_labels = []

    for name in pokemon_names:
        url = f'https://pokeapi.co/api/v2/pokemon/{name}'
        r = requests.get(url)
        if r.status_code == 200:
            data = r.json()
            stat = next((s['base_stat'] for s in data['stats'] if
                         s['stat']['name'] == stat_type), None)
            if stat is not None:
                pokemon_stats.append(stat)
                hover_labels.append(f"{name.title()} -"
                                    f" {stat_type.upper()}: {stat}")

    pastel_colors = ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF',
                     '#D9BAFF', '#FFC8E1', '#C6F7FF']

    bar_chart = go.Bar(
        x=pokemon_names,
        y=pokemon_stats,
        text=hover_labels,
        marker=dict(color=pastel_colors),
        hoverinfo='text'
    )

    layout = go.Layout(
        title='Pokémon Base HP Stats',
        xaxis=dict(title='Pokémon'),
        yaxis=dict(title='HP'),
        plot_bgcolor='rgba(255,255,255,0.95)'
    )

    fig = go.Figure(data=[bar_chart], layout=layout)
    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

    return render(request, 'bob/graph.html',
                  {'plot_div': plot_div})