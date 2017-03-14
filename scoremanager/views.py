import json

from json.decoder import JSONDecodeError

from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render

from .models import ScoreboardEntry

from . import validators

def submit_score(request):
	if request.method != 'POST': # check that the request is using the required POST method
		return HttpResponseNotAllowed(permitted_methods = ['POST']) # HTTP 405 Method Not Allowed; does not need to be handled by front-end (except for debugging purposes)

	if not ('serialized_score') in request.POST: # check that the POST data contains the required field
		return HttpResponseBadRequest("POST data must include 'serialized_score' field") # HTTP 400 Bad Request; does not need to be handled by front-end (except for debugging purposes)

	try:
		parsed_score = json.loads(request.POST['serialized_score']) # parse the JSON contained in the POST request
	except JSONDecodeError: # if the POST request's JSON was invalid
		return HttpResponseBadRequest("'serialized_score' must be a valid JSON string") # HTTP 400 Bad Request; does not need to be handled by front-end (except for debugging purposes)

	if not ('score' and 'balls_dropped') in parsed_score: # if the necessary fields are not in the parsed JSON dict
		return HttpResponseBadRequest("'serialized_score' JSON must contain 'score' and 'balls_dropped' fields") # HTTP 400 Bad Request; does not need to be handled by front-end (except for debugging purposes)

	# TODO: decryption/deobfuscation here

	submitted_score = parsed_score['score']
	submitted_balls_dropped = parsed_score['balls_dropped']

	if not isinstance(submitted_score, int): # if serialized_score.score was not serialized as an integer
		return HttpResponseBadRequest("'serialized_score.score' must be an integer") # HTTP 400 Bad Request; does not need to be handled by front-end (except for debugging purposes)

	if not isinstance(submitted_balls_dropped, int): # if serialized_score.submitted_balls_dropped was not serialized as an integer
		return HttpResponseBadRequest("'serialized_score.submitted_balls_dropped' must be an integer") # HTTP 400 Bad Request; does not need to be handled by front-end (except for debugging purposes)

	if not validators.run_validator(validators.score_max_validator, submitted_score): # check whether the submitted score will fit into a PositiveIntegerField
		return HttpResponseBadRequest("'serialized_score.score' must be a value >=" + validators.SCORE_MAXIMUM) # HTTP 400 Bad Request; may need to be handled in case of incredibly large legit scores

	if not validators.run_validator(validators.balls_dropped_max_validator, submitted_balls_dropped): # check whether the submitted balls dropped will fit into a PositiveIntegerField
		return HttpResponseBadRequest("'serialized_score.submitted_balls_dropped' must be a value >=" + validators.BALLS_DROPPED_MAXIMUM) # HTTP 400 Bad Request; may need to be handled in case of incredibly large legit balls dropped

	ScoreboardEntry.create_new_scoreboard_entry(score = submitted_score, balls_dropped = submitted_balls_dropped)
	return HttpResponse() # HTTP 200 OK; should be handled by front-end as a successful submission


def get_top_scores(request):
	if request.method != 'GET': # check that the request is using the required GET method
			return HttpResponseNotAllowed(permitted_methods = ['GET']) # HTTP 405 Method Not Allowed; does not need to be handled by front-end (except for debugging purposes)

	# TODO: header 'X-Top-Score-Count' to change the number of scores returned

	top_scores = ScoreboardEntry.objects.all()[:5] # return the top 5 ScoreboardEntries, pre-ordered by its Meta class
	top_scores_dict = {'response':
		[ # create an ordered list of dicts for each top score in the retrieved list
			{
			'score': top_score.score,
			'balls_dropped': top_score.balls_dropped
			}
			for top_score in top_scores
		]
	}

	return JsonResponse(top_scores_dict)
