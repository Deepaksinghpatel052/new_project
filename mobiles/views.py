from mobiles.models import Mobile
from rest_framework import viewsets
from rest_framework import permissions
from mobiles.serializers import MobileSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest


# @csrf_exempt
def getMobileList(request):
    location = request.GET.get('location', '')
    page = request.GET.get('page', 1)
    items = request.GET.get('items', 10)
    searchedMobiles = Mobile.objects.filter(location__icontains=location).order_by('-user__pk')
    mobileList = []
    paginator = Paginator(searchedMobiles, items)
    searchedMobiles = paginator.page(page)

    for item in searchedMobiles:
        mobileList.append({
            "name": item.name,
            "description": item.description,
            "user": item.user.pk,
            "location": item.location
        })

    return JsonResponse({
        "mobiles": mobileList,
        "page": page,
        "items": items,
        "totalPages": paginator.num_pages,
        "totalItems": paginator.count,
    })


class MobileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows mobiles to be viewed or edited.
    """
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        mobile = self.get_object()
        mobile_serializer = MobileSerializer(mobile, data=request.data, partial=True)
        if mobile_serializer.is_valid():
            mobile_serializer.save()
            return HttpResponse(mobile_serializer.data)
        else:
           return HttpResponseBadRequest()