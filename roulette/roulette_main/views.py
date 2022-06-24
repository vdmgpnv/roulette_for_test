from email import message
from rest_framework import generics, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from .service import get_roll


class StartRound(generics.CreateAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundCreateSerializer


class RollTheRoulette(generics.CreateAPIView):
    queryset = Roll.objects.all()
    serializer_class = RollSerializer

    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        message = 'В следующий раз повезет'
        
        user_data = request_data["user"]

        current_round = Round.objects.filter(user=user_data).reverse().first()


        if current_round.is_finished:
            new_round = Round(user=user_data)
            new_round.save()

            current_round = new_round

        rolls = list(current_round.rolls.values())

        rolls = [Roll.objects.get(pk=roll['id']).result for roll in rolls]

    
        roll = get_roll(rolls)

        
        if roll == 11:
            current_round.is_finished = True
            current_round.is_jackpot = True
            current_round.save()
            message = 'ДЖЕПООООООООООООООООООООООООТ!!!'
        
        request_data['result'] = roll
       
        request_data = self.serializer_class(data=request_data)
        request_data.is_valid(raise_exception=True)
        request_data.save()
        
        data = {
            'data' : request_data.data,
            'message' : message
                }
        current_round.rolls.add(request_data.data["id"])
        current_round.save()

        return Response(data=data, status=status.HTTP_201_CREATED)


class EndRound(generics.UpdateAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundUpdateSerializer

    def patch(self, request, *args, **kwargs):
        request_data = dict(request.data)
        
        user_data = request_data["user"]

        current_round = Round.objects.filter(user=user_data).reverse().first()

        current_round.is_finished = True
        current_round.save()

        response_data = Round.objects.filter(user=user_data).reverse().values().first()

        return Response(data=response_data, status=status.HTTP_200_OK)


class RoundStatistics(generics.ListAPIView):
    queryset = Round.objects.all()
    serializer_class = RoundDetailSerializer

    def get(self, request, *args, **kwargs):

        def sort_func(value):
            return value["games"]

        results = list(Round.objects.all().values())
        print(results)

        if not results:
            return Response(data={"Error": "No data"}, status=status.HTTP_204_NO_CONTENT)

        roll_dict = {}
        roll_dict['users'] = []

        for result in results:

            if len(roll_dict['users']) == 0:
                roll_dict['users'].append(
                    {
                        'user': result['user'],
                        'games': 1,
                        'rolls': result['rolls_count']
                    }
                )

            else:
                isFound = False
                for iter in roll_dict['users']:

                    if iter['user'] == result['user']:
                        iter['games'] += 1
                        iter['rolls'] += result['rolls_count']
                        isFound = True

                if not isFound:
                    roll_dict['users'].append(
                        {
                            'user': result['user'],
                            'games': 1,
                            'rolls': result['rolls_count']
                        }
                    )   

        roll_dict = {'users': sorted(roll_dict['users'], key=sort_func, reverse=True)}

        if 'user_stat' in request.GET:

            for user in roll_dict['users']:
                user['avg_rolls'] = user['rolls'] // user['games']
                
            return Response(data=roll_dict, status=status.HTTP_200_OK)

        max_round = roll_dict['users'][0]['games']

        statistics = {}

        for game in range(1, max_round + 1):
            user_list = []
            kol = 0
            for user in roll_dict['users']:

                if user['games'] >= game:
                    user_list += user['user']
                    kol += 1

            statistics[game] = kol
            

        return Response(data=statistics, status=status.HTTP_200_OK)