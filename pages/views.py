from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home.html"

class MonthlyCalenderView(TemplateView):
    template_name = "calenderView/fullcalendar.html"
# Create your views here.
