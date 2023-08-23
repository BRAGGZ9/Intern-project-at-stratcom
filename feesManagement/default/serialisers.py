from rest_framework import serializers
from . models import *

class StudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Students
        fields = "__all__"
    

class AllPaymentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AmountPaid
        fields = "__all__"

    def all_students():
        returned = []
        all_stds = AmountPaid.objects.all()
        for x in all_stds:
            returned.append({
                "id": x.id,
                "amount": x.amount,
                "date": x.date,
                "name": x.student.name,
                "level": x.level.name,
                "student_id":x.student.id,
                "level_id":x.level.id
            })
        return returned









    #email = serializers.CharField(source = "user.email")
    #user_id = serializers.CharField(source = "user.id")
    #first_name = serializers.CharField(source = "user.first_name")
    #last_name = serializers.CharField(source = "user.last_name")