import os
import asana
from asana.rest import ApiException
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint
from llm import llmstudio_enviar_prompt_especificar_pub, llmstudio_enviar_prompt_extrair_conteudo_pub
from claude import anthropic_enviar_prompt_especificar_pub_outros, anthropic_enviar_prompt_extrair_conteudo_pub, anthropic_extrair_data_audiencia, anthropic_enviar_prompt_especificar_conteudo_pub_defesa
from openai_llm import openai_enviar_prompt_especificar_pub_outros, openai_enviar_prompt_extrair_conteudo_pub, openai_extrair_data_audiencia, openai_enviar_prompt_especificar_conteudo_pub_defesa
from dados import dados

load_dotenv()



def get_project(project_gid):
    configuration = asana.Configuration()
    configuration.access_token = dados['key']
    api_client = asana.ApiClient(configuration)

    # create an instance of the API class
    projects_api_instance = asana.ProjectsApi(api_client)
    project_gid = project_gid # str | Globally unique identifier for the project.
    opts = {
        'opt_fields': "archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,owner,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
    }

    try:
        # Get a project
        api_response = projects_api_instance.get_project(project_gid, opts)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling ProjectsApi->get_project: %s\n" % e)

#copiado da documentação
def get_projects():
    configuration = asana.Configuration()
    configuration.access_token = dados['key']
    api_client = asana.ApiClient(configuration)

    # create an instance of the API class
    projects_api_instance = asana.ProjectsApi(api_client)
    workspace_gid = dados['workspace']['gid'] # str | Globally unique identifier for the workspace or organization.
    opts = {
        'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
        #'offset': "eyJ0eXAiOJiKV1iQLCJhbGciOiJIUzI1NiJ9", # str | Offset token. An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results. *Note: You can only pass in an offset that was returned to you via a previously paginated request.*
        'archived': False, # bool | Only return projects whose `archived` field takes on the value of this parameter.
        'opt_fields': "archived,color,completed,completed_at,completed_by,completed_by.name,created_at,created_from_template,created_from_template.name,current_status,current_status.author,current_status.author.name,current_status.color,current_status.created_at,current_status.created_by,current_status.created_by.name,current_status.html_text,current_status.modified_at,current_status.text,current_status.title,current_status_update,current_status_update.resource_subtype,current_status_update.title,custom_field_settings,custom_field_settings.custom_field,custom_field_settings.custom_field.asana_created_field,custom_field_settings.custom_field.created_by,custom_field_settings.custom_field.created_by.name,custom_field_settings.custom_field.currency_code,custom_field_settings.custom_field.custom_label,custom_field_settings.custom_field.custom_label_position,custom_field_settings.custom_field.date_value,custom_field_settings.custom_field.date_value.date,custom_field_settings.custom_field.date_value.date_time,custom_field_settings.custom_field.default_access_level,custom_field_settings.custom_field.description,custom_field_settings.custom_field.display_value,custom_field_settings.custom_field.enabled,custom_field_settings.custom_field.enum_options,custom_field_settings.custom_field.enum_options.color,custom_field_settings.custom_field.enum_options.enabled,custom_field_settings.custom_field.enum_options.name,custom_field_settings.custom_field.enum_value,custom_field_settings.custom_field.enum_value.color,custom_field_settings.custom_field.enum_value.enabled,custom_field_settings.custom_field.enum_value.name,custom_field_settings.custom_field.format,custom_field_settings.custom_field.has_notifications_enabled,custom_field_settings.custom_field.id_prefix,custom_field_settings.custom_field.is_formula_field,custom_field_settings.custom_field.is_global_to_workspace,custom_field_settings.custom_field.is_value_read_only,custom_field_settings.custom_field.multi_enum_values,custom_field_settings.custom_field.multi_enum_values.color,custom_field_settings.custom_field.multi_enum_values.enabled,custom_field_settings.custom_field.multi_enum_values.name,custom_field_settings.custom_field.name,custom_field_settings.custom_field.number_value,custom_field_settings.custom_field.people_value,custom_field_settings.custom_field.people_value.name,custom_field_settings.custom_field.precision,custom_field_settings.custom_field.privacy_setting,custom_field_settings.custom_field.representation_type,custom_field_settings.custom_field.resource_subtype,custom_field_settings.custom_field.text_value,custom_field_settings.custom_field.type,custom_field_settings.is_important,custom_field_settings.parent,custom_field_settings.parent.name,custom_field_settings.project,custom_field_settings.project.name,custom_fields,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.representation_type,custom_fields.text_value,custom_fields.type,default_access_level,default_view,due_date,due_on,followers,followers.name,html_notes,icon,members,members.name,minimum_access_level_for_customization,minimum_access_level_for_sharing,modified_at,name,notes,offset,owner,path,permalink_url,privacy_setting,project_brief,public,start_on,team,team.name,uri,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
    }

    try:
        # Get all projects in a workspace
        api_response = projects_api_instance.get_projects_for_workspace(workspace_gid, opts)
        for data in api_response:
            #pprint(data)
            pass
    except ApiException as e:
        print("Exception when calling ProjectsApi->get_projects_for_workspace: %s\n" % e)


def create_tasks_pubs(pubs, hoje):
    configuration = asana.Configuration()
    configuration.access_token = key
    api_client = asana.ApiClient(configuration)
    #como mostra a documentação
    tasks_api_instance = asana.TasksApi(api_client)
    i = 1
    for pub in pubs:
        #print(pub)
        body = {"data": {"name": f"pub_{i}", 
                "due_on": hoje,
                "notes": pub['texto'],
                "assignee": os.getenv('ID_SAULO'),
                "projects":  os.getenv('ID_PROJETO')#me
                }} # dict | The task to create.
        opts = {
            'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
        }

        try:
            # Create a task
            api_response = tasks_api_instance.create_task(body, opts)
            #pprint(api_response)
        except ApiException as e:
            print("Exception when calling TasksApi->create_task: %s\n" % e)
        i +=1

#algo que corresponde a como armazeno as informações de meus processos
def extrair_area_processo(dados, pub):
    numero_processo = pub[('numeroprocessocommascara')]
    df = dados['processos']
    processo_no_df = df.loc[df['numeroprocesso'] == numero_processo]
    area_processo = processo_no_df['natureza'].values[0]
    return area_processo

def criar_tarefa_geral(nome_tarefa, pub, dados, responsavel, hoje_str):
    configuration = asana.Configuration()
    configuration.access_token = os.getenv('ASANA_KEY')
    api_client = asana.ApiClient(configuration)
    tasks_api_instance = asana.TasksApi(api_client)
    df = dados['processos']
    numero_processo = pub['numeroprocessocommascara']
    processo_no_df = df.loc[df['numeroprocesso'] == numero_processo]
    parte = processo_no_df['cliente'].values[0]
    body = {"data": {"name": f"{nome_tarefa} - {numero_processo} - {parte}", 
            "due_on": hoje_str,
            "notes": pub['texto'],
            "assignee": responsavel,
            "projects": "1210522240663089"
            }} # dict | The task to create.
    opts = {
        'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
    }

    try:
        # Create a task
        api_response = tasks_api_instance.create_task(body, opts)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->create_task: %s\n" % e)
    return

def criar_tarefa_defesa(pub, dados, hoje):
    responsavel = dados['membros']['mariafernandacoleta@gmail.com']
    conteudo_pub = especificar_pub_defesa(pub['texto'], dados.get('llm_cliente', 'ANTHROPIC'))  # Configurable LLM client
    nome_tarefa = conteudo_pub
    due_on = hoje + timedelta(days=2)
    due_on_str = due_on.strftime('%Y-%m-%d')

    configuration = asana.Configuration()
    configuration.access_token = dados['key']
    api_client = asana.ApiClient(configuration)

    # create an instance of the API class
    tasks_api_instance = asana.TasksApi(api_client)
    df = dados['processos']
    numero_processo = pub['numeroprocessocommascara']
    processo_no_df = df.loc[df['numeroprocesso'] == numero_processo]
    parte = processo_no_df['cliente'].values[0]
    body = {"data": {"name": f"{nome_tarefa} - {numero_processo} - {parte}", 
            "due_on": due_on_str,
            "notes": pub['texto'],
            "assignee": responsavel,
            "projects": "1210451985447372"
            }} # dict | The task to create.
    opts = {
        'opt_fields': "actual_time_minutes,approval_status,assignee,assignee.name,assignee_section,assignee_section.name,assignee_status,completed,completed_at,completed_by,completed_by.name,created_at,created_by,custom_fields,custom_fields.asana_created_field,custom_fields.created_by,custom_fields.created_by.name,custom_fields.currency_code,custom_fields.custom_label,custom_fields.custom_label_position,custom_fields.date_value,custom_fields.date_value.date,custom_fields.date_value.date_time,custom_fields.default_access_level,custom_fields.description,custom_fields.display_value,custom_fields.enabled,custom_fields.enum_options,custom_fields.enum_options.color,custom_fields.enum_options.enabled,custom_fields.enum_options.name,custom_fields.enum_value,custom_fields.enum_value.color,custom_fields.enum_value.enabled,custom_fields.enum_value.name,custom_fields.format,custom_fields.has_notifications_enabled,custom_fields.id_prefix,custom_fields.is_formula_field,custom_fields.is_global_to_workspace,custom_fields.is_value_read_only,custom_fields.multi_enum_values,custom_fields.multi_enum_values.color,custom_fields.multi_enum_values.enabled,custom_fields.multi_enum_values.name,custom_fields.name,custom_fields.number_value,custom_fields.people_value,custom_fields.people_value.name,custom_fields.precision,custom_fields.privacy_setting,custom_fields.representation_type,custom_fields.resource_subtype,custom_fields.text_value,custom_fields.type,custom_type,custom_type.name,custom_type_status_option,custom_type_status_option.name,dependencies,dependents,due_at,due_on,external,external.data,followers,followers.name,hearted,hearts,hearts.user,hearts.user.name,html_notes,is_rendered_as_separator,liked,likes,likes.user,likes.user.name,memberships,memberships.project,memberships.project.name,memberships.section,memberships.section.name,modified_at,name,notes,num_hearts,num_likes,num_subtasks,parent,parent.created_by,parent.name,parent.resource_subtype,permalink_url,projects,projects.name,resource_subtype,start_at,start_on,tags,tags.name,workspace,workspace.name", # list[str] | This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.
    }

    try:
        # Create a task
        api_response = tasks_api_instance.create_task(body, opts)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling TasksApi->create_task: %s\n" % e)
    return

def extrair_conteudo_pub(pub, cliente):
    if cliente == "LLM_STUDIO":
        resposta = llmstudio_enviar_prompt_extrair_conteudo_pub(pub)
        return resposta
    elif cliente == "ANTHROPIC":
        resposta = anthropic_enviar_prompt_extrair_conteudo_pub(pub)
        return resposta
    elif cliente == "OPENAI":
        resposta = openai_enviar_prompt_extrair_conteudo_pub(pub)
        return resposta

def especificar_pub_outros(pub, cliente):
    if cliente == "LLM_STUDIO":
        resposta = llmstudio_enviar_prompt_especificar_pub(pub)
        return resposta
    elif cliente == "ANTHROPIC":
        resposta = anthropic_enviar_prompt_especificar_pub_outros(pub)
        return resposta
    elif cliente == "OPENAI":
        resposta = openai_enviar_prompt_especificar_pub_outros(pub)
        return resposta

def especificar_pub_defesa(pub, cliente):
    if cliente == 'ANTHROPIC':
        resposta = anthropic_enviar_prompt_especificar_conteudo_pub_defesa(pub)
        return resposta
    elif cliente == 'OPENAI':
        resposta = openai_enviar_prompt_especificar_conteudo_pub_defesa(pub)
        return resposta

def extrair_data_audiencia(pub, cliente):
    #if cliente == "LLM_STUDIO":
        #resposta = llmstudio_enviar_prompt_especificar_pub(pub)
        #return resposta
    if cliente == "ANTHROPIC":
        resposta = anthropic_extrair_data_audiencia(pub)
        return resposta
    elif cliente == "OPENAI":
        resposta = openai_extrair_data_audiencia(pub)
        return resposta