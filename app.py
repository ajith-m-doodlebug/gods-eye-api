from flask import Flask, request
from github import Github

app = Flask(__name__)


@app.route('/api', methods=['GET'])
def hello():
    query = str(request.args['id'])

    g = Github("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")
    repo = g.get_user().get_repo("CoolMe")
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "xlsx":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open('Book1.xlsx', 'rb') as file:
        content = file.read()

    # Upload to github
    git_file = '{}.xlsx'.format(query)
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha)
        print(git_file + ' UPDATED')
        return git_file + ' UPDATED'
    else:
        repo.create_file(git_file, "committing files", content)
        print(git_file + ' CREATED')
        return git_file + ' CREATED'

    # try:

    # except:


if __name__ == '__main__':
    app.run()
