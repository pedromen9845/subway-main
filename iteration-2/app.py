from flask import Flask, render_template, request
from generate_map import generate_map, stations_info
import networkx as nx
import time


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['DEBUG'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/map', methods=['POST'])
def map():
    source = request.form['source']
    target = request.form['target']

    # Check if source and target stations are empty strings
    if not source or not target:
        return render_template('error.html', message="Please enter a valid source and target station.")

    # Check if source and target stations exist in stations_info
    if source not in stations_info or target not in stations_info:
        return render_template('error.html', message="Invalid source or target station. Please try again.")

    try:
        result = generate_map(source, target)

        return render_template('map.html', result=result)
    except nx.NetworkXNoPath:
        return render_template('error.html', message="Sorry, there is no path between {} and {}.".format(source, target))
    except Exception as e:
        # print the exception message for debugging purposes
        print("An error occurred: {}".format(str(e)))
        return render_template('error.html', message="An error occurred: {}".format(str(e)))


if __name__ == '__main__':
    app.run(debug=True)
