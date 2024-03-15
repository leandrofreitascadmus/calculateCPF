import os
import openai
from github import Github
from dotenv import load_dotenv

load_dotenv()

GPT_MODEL = os.getenv('GPT_MODEL')
openai.api_key = os.getenv('OPENAI_API_KEY')
git = Github(os.getenv('GITHUB_TOKEN'))


def main(pr_number):
    pr = load_pr(pr_number)
    prompt = generate_prompt(pr)
    response = generate_response(prompt)
    review = generate_review(pr, response)
    return review

def load_pr(number_pr):
    repository = git.get_repo('leandrofreitascadmus/calculateCPF')
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

def generate_response(prompt):
    response = openai.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )

    return response.choices[0].message.content

def generate_review(pr, response):
    pr.create_review(body=response, event='COMMENT')

main(1)