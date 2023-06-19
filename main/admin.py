from django.contrib import admin
from .models import *
from django.http import HttpResponse
import pandas as pd
import xlsxwriter
from .views import enviar_email_html

def gerar_planilha_evento(modeladmin, request, queryset):
    eventos = queryset  # Eventos selecionados

    # Criar um dicionário para armazenar os dados de cada evento
    dados_eventos = {}

    for evento in eventos:
        # Filtrar os inscritos por evento
        inscritos = Inscrito.objects.filter(evento=evento)

        # Criar um dataframe com os dados dos inscritos
        data = {
            'Nº de Inscrição': [inscrito.numero_inscricao for inscrito in inscritos],
            'Nome': [inscrito.nome for inscrito in inscritos],
            'E-mail': [inscrito.email for inscrito in inscritos],
            'Telefone': [inscrito.telefone for inscrito in inscritos],
            'Curso': [inscrito.graduacao for inscrito in inscritos],
            'Instituição': [inscrito.instituicao for inscrito in inscritos],
            'Data da Inscrição': [inscrito.data_hora_inscricao for inscrito in inscritos],
            'Cursos': ['Sim' if inscrito.cursos.exists() else 'Não' for inscrito in inscritos],
        }

        df = pd.DataFrame(data)

        # Converter a coluna "Data da Inscrição" para um formato sem informações de fuso horário
        df['Data da Inscrição'] = df['Data da Inscrição'].dt.tz_localize(None)

        # Adicionar o dataframe ao dicionário de dados do evento
        nome_planilha = evento.titulo[:31]
        dados_eventos[nome_planilha] = df

    # Criar o objeto de resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Inscritos nos Eventos.xlsx"'

    # Create a Pandas Excel writer with xlsxwriter engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    workbook = writer.book

    # Save each dataframe to a separate sheet in the Excel file
    for evento_nome, df in dados_eventos.items():
        df.to_excel(writer, sheet_name=evento_nome, index=False)

        # Largura das colunas
        worksheet = writer.sheets[evento_nome]
        worksheet.set_column('A:A', 14)  # Nº de Inscrição
        worksheet.set_column('B:B', 33)  # Nome
        worksheet.set_column('C:C', 30)  # E-mail
        worksheet.set_column('D:D', 12)  # Telefone
        worksheet.set_column('E:E', 33)  # Curso
        worksheet.set_column('F:F', 18)  # Instituição
        worksheet.set_column('G:G', 18) # Data da Inscrição
        worksheet.set_column('H:H', 8) # Cursos


    # Close the Pandas Excel writer and save the Excel file
    writer.close()

    return response


gerar_planilha_evento.short_description = 'Gerar Planilha'

def gerar_planilha_curso(modeladmin, request, queryset):
    cursos = queryset  # Cursos selecionados

    # Criar um dicionário para armazenar os dados de cada curso
    dados_cursos = {}

    for curso in cursos:
        # Filtrar os inscritos por curso
        inscritos = Inscrito.objects.filter(cursos=curso)

        # Criar um dataframe com os dados dos inscritos
        data = {
            'Nº de Inscrição': [inscrito.numero_inscricao for inscrito in inscritos],
            'Nome': [inscrito.nome for inscrito in inscritos],
        }

        df = pd.DataFrame(data)

        # Adicionar o dataframe ao dicionário de dados do curso
        nome_planilha = curso.nome[:31]
        dados_cursos[nome_planilha] = df

    # Criar o objeto de resposta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Inscritos nos Cursos.xlsx"'

    # Create a Pandas Excel writer with xlsxwriter engine
    writer = pd.ExcelWriter(response, engine='xlsxwriter')
    workbook = writer.book

    # Save each dataframe to a separate sheet in the Excel file
    for curso_nome, df in dados_cursos.items():
        df.to_excel(writer, sheet_name=curso_nome, index=False)

        # Largura das colunas
        worksheet = writer.sheets[curso_nome]
        worksheet.set_column('A:A', 14)  # Nº de Inscrição
        worksheet.set_column('B:B', 33)  # Nome

    # Close the Pandas Excel writer and save the Excel file
    writer.close()

    return response


gerar_planilha_curso.short_description = 'Gerar Planilha'

def confirmar_pagamento(modeladmin, request, queryset):
    for inscrito in queryset:
        # Verificar se o pagamento já foi confirmado anteriormente
        if not inscrito.pagamento_confirmado:
            # Atualizar o status do pagamento para confirmado
            inscrito.pagamento_confirmado = True
            inscrito.save()

            # Enviar e-mail de confirmação para o inscrito
            destinatario = inscrito.email
            assunto = f'Comprovante de Inscrição - {inscrito.evento}'
            template_name = 'main/email_confirmacao.html'
            context = {
                'evento': inscrito.evento,
                'inscrito': inscrito,
            }
            enviar_email_html(destinatario, assunto, template_name, context)

    modeladmin.message_user(request, "Pagamento confirmado para os inscritos selecionados.")


class InscritoInline(admin.StackedInline):
    model = Inscrito

class EventoAdmin(admin.ModelAdmin):
    actions = [gerar_planilha_evento]
    inlines = [InscritoInline]

    def get_model_perms(self, request):
        """
        Verifica as permissões do modelo e habilita o botão apenas para usuários com permissão de alteração.
        """
        perms = super().get_model_perms(request)
        perms['gerar_planilha_evento'] = perms['change']
        return perms
    
class CursoAdmin(admin.ModelAdmin):
    actions = [gerar_planilha_curso]

    def get_model_perms(self, request):
        """
        Verifica as permissões do modelo e habilita o botão apenas para usuários com permissão de alteração.
        """
        perms = super().get_model_perms(request)
        perms['gerar_planilha_curso'] = perms['change']
        return perms

class InscritoAdmin(admin.ModelAdmin):
    actions = [confirmar_pagamento]

    def get_nome_com_evento(self, inscrito):
        return f"{inscrito.nome} - {inscrito.evento.titulo}"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('evento')  # Carregar evento relacionado em uma única consulta
        return queryset

    list_display = ['get_nome_com_evento', 'pagamento_confirmado', 'data_hora_inscricao']

admin.site.register(Index_Carousel_Item)
admin.site.register(Diretor)
admin.site.register(Sobre_Text)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Alerta)
admin.site.register(Inscrito, InscritoAdmin)
admin.site.register(Patrocinador)
admin.site.register(Curso, CursoAdmin)
