from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import strikzilla

class CalcClass(object):

    def __init__(self, *args, **kw):
        self.N = int(args[0])
        self.M = int(args[1])

    def do_work(self):
        # Do some calculations here
        # returns a tuple ((1,2,3, ), (4,5,6,))
        sol, instr, n_start, n_middle, n_end  = strikzilla.xcrease(self.N, self.M, verbose=True)
        return sol, instr, n_start, n_middle, n_end 

class score(object):
    date   = '14/7 2016'
    ticker = 'AAPL'
    score  = 19.1

from django.shortcuts import render

class strikzilla_view(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part
        before = request.GET.get('before', 10)
        after  = request.GET.get('after', 12)

        # Any URL parameters get passed in **kw
        myClass = CalcClass(before, after, *args, **kw)
        sol, instr , n_start, n_middle, n_end  = myClass.do_work()

        p,q,res= sol
        context = {'instructions': instr.split('\n'), 
                   'before' : before,
                   'after' : after,
                   'p' : p,
                   'q' : q,
                   'n_start': n_start,
                   'n_middle': n_middle,
                   'n_end': n_end}

        return render(request, 'score/index.html', context)




class sctr_view(APIView):

    def get(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part

        # Any URL parameters get passed in **kw
        result  = (1,2,'as', request.data, request.body)#score()

        response = Response(result, status=status.HTTP_200_OK)

        return response

    def post(self, request, *args, **kw):
        # Process any get params that you may need
        # If you don't need to process get params,
        # you can skip this part

        # curl  -H "Content-Type: application/json" -X POST -d '{"data":{"NVDA":[1.1,2.4,3.0], "BBY":[1,2,3,4,5,6,7,8]}}' http://localhost:8000/score/api/sctr/?format=json

        result = []
        for tick, prices in request.data['data'].iteritems():
            result  += [{tick:sum(prices)}]

        response = Response(result, status=status.HTTP_200_OK)

        return response
        