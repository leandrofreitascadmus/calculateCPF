import os
import sys
import openai
from github import Github

def main(args):
    pr_number = args[2]
    repository_name = args[1]
    git_token = args[0]
    openai_key = args[3]
    model = args[4]

    pr = load_pr(pr_number, repository_name, git_token)
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
    Regras para revisão:
        - A revisão tem que manter o idioma português do Brasil
        - A revisão tem que manter o formato markdown
        - Em caso de problemas no código, listar no comentário qual é o problema em formato code
    '''

    return prompt

def generate_response(gpt_model, openai_key, prompt):
    openai.api_key = os.getenv(openai_key)
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