from flask import Flask, request, render_template_string

app = Flask(__name__)

# Import the project module
import ProjectManager as project

# Default project data
projectData = {
    'projectName': None,
    'technologies': None,
    'summary': None,
    'path': None,
    'difficulty': "Undefined",
    'tags': [],
    'templates': []
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'createProject' in request.form:
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Create Project</title>
                    <style>
                        /* Inline CSS for create project form */
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f0f0f0;
                            padding: 20px;
                        }
                        form {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        }
                        input[type=text], textarea {
                            width: 100%;
                            padding: 8px;
                            margin-bottom: 10px;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                        }
                        button {
                            background-color: #4CAF50;
                            color: white;
                            padding: 10px 20px;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                        }
                        button:hover {
                            background-color: #45a049;
                        }
                    </style>
                </head>
                <body>
                    <h1>Create Project</h1>
                    <form method="post">
                        Project Name: <input type="text" name="projectName"><br>
                        Technologies: <input type="text" name="technologies"><br>
                        Summary: <input type="text" name="summary"><br>
                        Path: <input type="text" name="path"><br>
                        Difficulty: <input type="text" name="difficulty" value="Undefined"><br>
                        Tags: <input type="text" name="tags"><br>
                        Templates: <input type="text" name="templates"><br>
                        <button type="submit" name="submitProject">Submit Project</button>
                    </form>
                </body>
                </html>
            ''')

        elif 'submitProject' in request.form:
            save_project_data(request.form)
            kwargs = {
                'technologies': projectData['technologies'],
                'summary': projectData['summary'],
                'difficulty': projectData['difficulty'],
                'tags': projectData['tags'],
                'templates': projectData['templates']
            }
            if projectData['path']:
                kwargs['path'] = projectData['path']

            project.CreateProject(projectData['projectName'], **kwargs)
            return f"Project data stored and function called: {projectData}"

        elif 'searchProject' in request.form:
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Search Project</title>
                    <style>
                        /* Inline CSS for search project form */
                        body {
                            font-family: Arial, sans-serif;
                            background-color: #f0f0f0;
                            padding: 20px;
                        }
                        form {
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #fff;
                            padding: 20px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0,0,0,0.1);
                        }
                        input[type=text] {
                            width: 100%;
                            padding: 8px;
                            margin-bottom: 10px;
                            border: 1px solid #ccc;
                            border-radius: 4px;
                        }
                        button {
                            background-color: #007bff;
                            color: white;
                            padding: 10px 20px;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                        }
                        button:hover {
                            background-color: #0056b3;
                        }
                    </style>
                </head>
                <body>
                    <h1>Search Project</h1>
                    <form method="post">
                        <label>Keywords:</label>
                        <input type="text" name="keywords">
                        <button type="submit" name="submitSearch">Search</button>
                    </form>
                </body>
                </html>
            ''')

        elif 'submitSearch' in request.form:
            keywords = request.form.get('keywords', None)
        
            if keywords:
                search_results = project.SearchProject(keywords)
                results_list = []
                for result in search_results:
                    results_list.append(result)
                print(results_list)
                return render_template_string('''
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Search Results</title>
                        <style>
                            /* Inline CSS for search results */
                            body {
                                font-family: Arial, sans-serif;
                                background-color: #f0f0f0;
                                padding: 20px;
                            }
                            ul {
                                list-style-type: none;
                                padding: 0;
                            }
                            li {
                                background-color: #fff;
                                padding: 10px;
                                margin-bottom: 10px;
                                border-radius: 4px;
                                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                            }
                        </style>
                    </head>
                    <body>
                        <h1>Search Results</h1>
                        <ul>
                            {% for result in results_list %}
                                <li>Project Name: {{ result }}</li>
                            {% endfor %}
                        </ul>
                    </body>
                    </html>
                ''', results_list=results_list)
            else:
                return '<h2>No keywords entered for search</h2>'

    return render_template_string('''
        <form method="post">
            <button type="submit" name="createProject">Create Project</button>
            <button type="submit" name="searchProject">Search Project</button><br><br>
        </form>
    ''')

def save_project_data(form):
    global projectData
    projectData = {
        'projectName': form.get('projectName', None),
        'technologies': form.get('technologies', None),
        'summary': form.get('summary', None),
        'path': form.get('path', None) if form.get('path') else None,
        'difficulty': form.get('difficulty', "Undefined"),
        'tags': form.get('tags', '').split(',') if form.get('tags') else [],
        'templates': form.get('templates', '').split(',') if form.get('templates') else []
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
