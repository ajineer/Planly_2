from rest_framework import viewsets, permissions
from ..models.calendarModel import Calendar
from ..serializers import calendarSerializer


class CalendarViews(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = calendarSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_calendars(self):
        return self.queryset.filter(user=self.request.user)

    def create_calendar(self, serializer):
        serializer.save(user=self.request.user)
