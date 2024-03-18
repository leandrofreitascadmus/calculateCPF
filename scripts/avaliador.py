import os
import sys
import openai
from github import Github

def main(args):
    print(args)
    print(args[6])
    pr_number = args[6]
    repository_name = args[4]
    git_token = args[2]
    openai_key = args[8]
    model = args[10]

    pr = load_pr(int(pr_number), repository_name, git_token)
    prompt = generate_prompt(pr)
    response = generate_response(model, openai_key, prompt)
    review = generate_review(pr, response)
    return review

def load_pr(number_pr, repository_name, git_token):
    git = Github(git_token)
    repository = git.get_repo(repository_name)
    pr = repository.get_pull(number_pr)
    return pr

def generate_prompt(pr):
    pr_title = pr.title
    pr_body = pr.body

    diffs = [f.patch for f in pr.get_files()]

    prompt = f'''
    Faça a revisão do PR: Titulo: {pr_title} Descrição: {pr_body} Diff: {diffs}
    Regras para Revisão de Código:
        - Idioma:
            A revisão deve ser realizada em português do Brasil.
        - Formato:
            Manter o formato Markdown durante a revisão.
        - Código:
            Em caso de problemas no código, indicar o problema utilizando o formato de código (code).
            Verificar a indentação do código para garantir legibilidade.
            Assegurar que as melhores práticas foram aplicadas.
            Identificar e corrigir possíveis erros no código.
        - Testes Unitários:
            Analisar a presença de testes unitários. Caso não existam, recomendar a inclusão para garantir a robustez do código.
        - Padrões de Codificação:
            Revisar o padrão de nomenclatura de variáveis e funções para garantir clareza e consistência.
        - Arquitetura do Projeto:
            Avaliar se as alterações propostas estão alinhadas com a arquitetura do projeto.
            Indicar se existem possibilidades de as alterações afetarem outros componentes do projeto.
        - Necessidade da Alteração:
            Esclarecer se a alteração proposta é essencial para o funcionamento do projeto.
        - Melhorias:
            Sugerir melhorias no código utilizando princípios de Clean Code para aumentar a manutenibilidade e a clareza.
        - Documentação e Comentários:
            Verificar se o código está adequadamente documentado, incluindo comentários explicativos quando necessário para facilitar o entendimento.
        - Consistência com o Design/UI:
            Se aplicável, avaliar se as mudanças estão em conformidade com os designs ou interfaces de usuário propostos, incluindo a aderência a guias de estilo.
        - Performance:
            Avaliar o impacto das mudanças na performance do sistema. Recomendar otimizações caso identifique potenciais gargalos.
        - Segurança:
            Analisar o código quanto a possíveis vulnerabilidades de segurança e recomendar práticas de codificação segura.
        - Uso de Bibliotecas e Dependências:
            Avaliar o uso de novas bibliotecas ou dependências, considerando licenças, segurança, manutenção e impacto no tamanho do projeto.
    '''

    return prompt

def generate_response(gpt_model, openai_key, prompt):
    openai.api_key = openai_key
    response = openai.chat.completions.create(
        model=gpt_model,
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content

def generate_review(pr, response):
    pr.create_review(body=response, event='COMMENT')

main(sys.argv)