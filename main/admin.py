from django.contrib import admin
from .models import *
from django.http import HttpResponse
import pandas as pd
import xlsxwriter
from .views import enviar_email_html


admin.site.site_header = 'Administração de LAVIB-PA'
admin.site.index_title = 'LAVIB-PA'
admin.site.site_title = 'Administração'


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
    readonly_fields = ['numero_inscricao', 'data_hora_inscricao']
    extra = 0

    
@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    actions = [gerar_planilha_evento]
    inlines = [InscritoInline]
    readonly_fields = ['vagas_restantes']
    save_on_top = True
    
    fieldsets = [
        ('Informações Gerais do Evento', {"fields": ['titulo', 'descricao_curta', 'imagem']}),
        ('Informações Específicas do Evento', {"fields": ['descricao', 'data_hora', 'data_hora_final', 'local', 'valor', 'carga_horaria', 'palestrantes', 'vagas', 'vagas_restantes', 'mensagem_comprovante']}),
        ('Cursos', {"fields": ['cursos']}),
        ('Descontos', {"fields": ['descontos']})
    ]

    def get_model_perms(self, request):
        """
        Verifica as permissões do modelo e habilita o botão apenas para usuários com permissão de alteração.
        """
        perms = super().get_model_perms(request)
        perms['gerar_planilha_evento'] = perms['change']
        return perms


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    actions = [gerar_planilha_curso]
    readonly_fields = ['vagas_restantes']

    def get_model_perms(self, request):
        """
        Verifica as permissões do modelo e habilita o botão apenas para usuários com permissão de alteração.
        """
        perms = super().get_model_perms(request)
        perms['gerar_planilha_curso'] = perms['change']
        return perms


class EventoTituloFilter(admin.SimpleListFilter):
    title = 'Evento'
    parameter_name = 'evento_titulo'

    def lookups(self, request, model_admin):
        eventos = set([inscrito.evento.titulo for inscrito in Inscrito.objects.all()])
        return [(evento, evento) for evento in eventos]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(evento__titulo=self.value())


@admin.register(Inscrito)
class InscritoAdmin(admin.ModelAdmin):
    ordering = ['numero_inscricao']
    actions = [confirmar_pagamento]
    list_display = ['numero_inscricao', 'nome', 'evento_titulo', 'pagamento_confirmado']
    list_filter = ['pagamento_confirmado', EventoTituloFilter]
    search_fields = ['nome']
    readonly_fields = ['numero_inscricao', 'data_hora_inscricao']
    list_display_links = ['nome']
    
    fieldsets = [
        ('Informações do Identificação', {"fields": ['numero_inscricao', 'nome']}),
        ('Informações de Contato', {"fields": ['email', 'telefone']}),
        ('Informações de Graduação', {"fields": ['graduacao', 'instituicao']}),
        ('Informações de Inscrição no Evento', {"fields": ['data_hora_inscricao', 'evento', 'cursos']}),
        ('Informações de Pagamento', {"fields": ['comprovante', 'pagamento_confirmado']}),
        ('Informações de Indicação', {"fields": ['indicacao']})
    ]

    def evento_titulo(self, obj):
        return obj.evento.titulo

    evento_titulo.short_description = 'Evento'


@admin.register(Index_Carousel_Item)
class IndexCarouselItemAdmin(admin.ModelAdmin):
    list_display = ['caption_title', 'link']


@admin.register(Diretor)
class DiretorAdmin(admin.ModelAdmin):
    ordering = ['nome']
    list_display = ['nome', 'ano']
    search_fields = ['nome']
    
    fieldsets = [
        ('Sobre o Diretor', {"fields": ['nome', 'foto', 'ano']}),
        ('Redes Sociais', {"fields": ['lattes', 'linkedin', 'instagram', 'twitter', 'facebook']})
    ]


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['email', 'telefone', 'chave_pix', 'nome_conta']
    fieldsets = [
        ('Informações da Liga', {"fields": ['email', 'telefone']}),
        ('Informações de Pagamento', {"fields": ['chave_pix', 'qrcode_pagamento', 'nome_conta']}),
        ('Alerta', {"fields": ['alerta_negrito', 'alerta_text', 'alerta_cor', 'alerta_link']}),
        ('Sobre a LAVIB-PA', {"fields": ['sobre_nos']}),
        ('Informações do Site', {"fields": ['plano_de_fundo']})
    ]


@admin.register(Patrocinador)
class PatrocinadorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'link']


@admin.register(Redes_Sociais)
class RedesSociaisAdmin(admin.ModelAdmin):
    list_display = ['nome', 'url']


@admin.register(Desconto)
class DescontoAdmin(admin.ModelAdmin):
    list_display = ['cupom', 'valor', 'cupons_restantes']
    readonly_fields = ['cupons_restantes']
    

@admin.register(Participante)
class ParticipanteAdmin(admin.ModelAdmin):
    ordering = ['nome']
    list_display = ['nome', 'descricao']