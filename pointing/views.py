import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import transaction

# Create your views here.
from pointing.models import Presence, PrecenceItem
from pointing import utils
from authentication.models import User



@login_required
def add_presence(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file')
        if file_path:
            date_month, data = utils.get_presence_data(file_path)
            data_json = json.dumps(data, indent=4, ensure_ascii=False)
            all_data = json.loads(data_json)

            for item in all_data:
                for name, value in item.items():
                    try:
                        with transaction.atomic():
                            user = User.objects.get(identifier=name, company=request.user.company)
                            presence = Presence.objects.create(
                                user=user,
                                month=date_month
                            )

                            for precence_item in value:
                                PrecenceItem.objects.create(
                                    presence=presence,
                                    user=user,
                                    state=precence_item['Etat du Ptg'],
                                    times=precence_item['Temps'],
                                    date=precence_item['Date'],
                                    identifier=precence_item['Prénom']
                                )
                    except :
                        pass


    return render(request, 'frontend/pointing/add_precence.html')
