from flask import Flask, request, Response
from flask_cors import CORS
from predict import doPredict
import logging
from logging.handlers import RotatingFileHandler
from IPython import embed

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def main():
	aux = request.values
	#embed()
	print(len(request.values))
	title = aux.to_dict(flat = False)['title'][0]
	body = aux.to_dict(flat = False)['body'][0]
	s = body.find(title)
	if s == -1:
		body = "*"
	else:
		body = body[s:]
	

	#["Agrees", "Disagrees", "Discusses", "Unrelated"]


	print("Title of the new: ", title)
	#title = request.args['title']
	#body = request.args.post('body')
	result = doPredict(title, body)
	print("Probabilities: ", result[0])
	print("Most probable category: ", result[1])
	print("Clickbaity title? : ", result[2])

	resp = Response(result, status=200, mimetype='application/json')
	return "resp"
	#logger.info('This error output', file=sys.stderr)
	#logger.info(title, file=sys.stdout)
	#logger.info("Hi", file=sys.stdout)

	#return print("Hello")
	
if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
	logging.basicConfig(format='%(asctime)s %(module)s %(message)s', level=logging.INFO)
	logger = logging.getLogger(__name__)
