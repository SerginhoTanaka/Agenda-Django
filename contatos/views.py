from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.http import Http404
from .models import Contato
from django.db.models import Q, Value 
from django.db.models.functions import Concat
from django.contrib import messages 
from accounts.models import FormContato

def index(request):
    contatos = Contato.objects.order_by('nome').filter(
        mostrar = True
    )
    paginator = Paginator(contatos, 10)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos':contatos
    })

def ver_contato(request,contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato,id=contato_id)
    if not contato.mostrar:
        raise Http404()
    return render(request, 'contatos/ver_contato.html', {
    'contato':contato
        })

def busca(request):
    termo = request.GET.get('termo')
    if termo is None or not termo:
        messages.add_message(request,
                             messages.ERROR,
                            'Campo termo não pode ficar vazio'
                            )
        return redirect('index')
        

    campos = Concat('nome',Value(' '),'sobrenome')

    contatos = Contato.objects.annotate(
        nome_completo = campos
        ).filter(
            Q(nome_completo__icontains = termo) | Q(telefone__icontains = termo)
        )
    
    paginator = Paginator(contatos, 2)

    page = request.GET.get('p')
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos':contatos
    })  


def editar(request, contato_id):
    # Obter o registro do banco de dados com o ID fornecido
    contato = get_object_or_404(Contato, pk=contato_id)
    
    if request.method != 'POST':
        # Renderizar o formulário com os dados existentes preenchidos
        form = FormContato(instance=contato)
        return render(request, 'contatos/editar.html',{'form':form})

    form = FormContato(request.POST, request.FILES, instance=contato)

    if not form.is_valid():
        messages.error(request, 'Erro ao enviar o formulário')
        return render(request, 'contatos/editar.html',{'form':form})
    
    descricao = request.POST.get('descricao')

    if len(descricao) < 5:
        messages.error(request, 'Descrição precisa ter mais de 5 caracteres')
        return render(request, 'contatos/editar.html',{'form':form})
    
    form.save()
    return redirect('index')

def excluir(request, contato_id):
    # Obter o registro do banco de dados com o ID fornecido
    contato = get_object_or_404(Contato, pk=contato_id)
    contato.delete()
    
    

    return redirect('index')