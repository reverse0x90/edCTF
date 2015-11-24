from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from edctf.api.models import ctf
from edctf.api.serializers import ctfSerializer


class ctfView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, id=None, format=None):
        """
        Get all ctfs
        or get by id via ctfs/:id
        or get all live ctfs via GET parameter, i.e. live=true
        """
        if id:
            ctfs = ctf.objects.filter(id=id)
        else:
            if 'live' in request.query_params:
                if request.query_params['live'] == 'true':
                    ctfs = ctf.objects.filter(live=True)
                else:
                    ctfs = ctf.objects.filter(live=False)
            else:
                ctfs = ctf.objects.all()
        serializer = ctfSerializer(ctfs, many=True, context={'request': request})
        return Response({
            "ctfs": serializer.data,
        })