from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt


import time
import datetime
import sys
import os

sys.path.append(os.path.abspath('..'))

from polls.models import Question, Choice 


def _pollActive(pubTime, pollDuration):
	now = timezone.now()
	print(now - datetime.timedelta(days=pollDuration))
	return now - datetime.timedelta(days=pollDuration) <= pubTime

@csrf_exempt
def revealvote(request, poll_id, nounce, vote):
	# get question object
	question = get_object_or_404(Question, pk=poll_id)

	publishDate = question.pub_date

	pollDuration = 100

	if _pollActive(publishDate, pollDuration):
		return HttpResponse('poll is still active, '+
							'cannot reveal vote now.', content_type='text/plain')
	
	# need to send the poll to blockchain
	print(poll_id, nounce, vote)

	return HttpResponse('your vote has been reveal in blockchain, '+
							'hold back for results :)', content_type='text/plain')