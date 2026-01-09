# serializers.py (Live app)
from rest_framework import serializers
from .models import Batting, Extra, Match, Over  # relative import

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'  
class OverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Over
        fields = '__all__'
class BattingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batting
        fields = '__all__'
class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'