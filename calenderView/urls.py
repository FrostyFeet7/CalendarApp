from django.urls.conf import path
from django.views.generic.list import ListView

from models import Calendar
from schedule.periods import Day, Month, Week, Year
from calenderView.views import (
    CalendarByPeriodsView,
    CalendarView,
    CancelOccurrenceView,
    CreateEventView,
    CreateOccurrenceView,
    DeleteEventView,
    EditEventView,
    EditOccurrenceView,
    EventView,
    FullCalendarView,
    OccurrencePreview,
    OccurrenceView,
    api_move_or_resize_by_code,
    api_occurrences,
    api_select_create,
)

urlpatterns = [
    path(r"^$", ListView.as_view(model=Calendar), name="calendar_list"),
    path(
        r"^calendar/year/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_year.html"),
        name="year_calendar",
        kwargs={"period": Year},
    ),
    path(
        r"^calendar/tri_month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_tri_month.html"),
        name="tri_month_calendar",
        kwargs={"period": Month},
    ),
    path(
        r"^calendar/compact_month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(
            template_name="schedule/calendar_compact_month.html"
        ),
        name="compact_calendar",
        kwargs={"period": Month},
    ),
    path(
        r"^calendar/month/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_month.html"),
        name="month_calendar",
        kwargs={"period": Month},
    ),
    path(
        r"^calendar/week/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_week.html"),
        name="week_calendar",
        kwargs={"period": Week},
    ),
    path(
        r"^calendar/daily/(?P<calendar_slug>[-\w]+)/$",
        CalendarByPeriodsView.as_view(template_name="schedule/calendar_day.html"),
        name="day_calendar",
        kwargs={"period": Day},
    ),
    path(
        r"^calendar/(?P<calendar_slug>[-\w]+)/$",
        CalendarView.as_view(),
        name="calendar_home",
    ),
    path(
        r"^fullcalendar/(?P<calendar_slug>[-\w]+)/$",
        FullCalendarView.as_view(),
        name="fullcalendar",
    ),
    # Event paths
    path(
        r"^event/create/(?P<calendar_slug>[-\w]+)/$",
        CreateEventView.as_view(),
        name="calendar_create_event",
    ),
    path(
        r"^event/edit/(?P<calendar_slug>[-\w]+)/(?P<event_id>\d+)/$",
        EditEventView.as_view(),
        name="edit_event",
    ),
    path(r"^event/(?P<event_id>\d+)/$", EventView.as_view(), name="event"),
    path(
        r"^event/delete/(?P<event_id>\d+)/$",
        DeleteEventView.as_view(),
        name="delete_event",
    ),
    # paths for already persisted occurrences
    path(
        r"^occurrence/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$",
        OccurrenceView.as_view(),
        name="occurrence",
    ),
    path(
        r"^occurrence/cancel/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$",
        CancelOccurrenceView.as_view(),
        name="cancel_occurrence",
    ),
    path(
        r"^occurrence/edit/(?P<event_id>\d+)/(?P<occurrence_id>\d+)/$",
        EditOccurrenceView.as_view(),
        name="edit_occurrence",
    ),
    # paths for unpersisted occurrences
    path(
        r"^occurrence/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$",
        OccurrencePreview.as_view(),
        name="occurrence_by_date",
    ),
    path(
        r"^occurrence/cancel/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$",
        CancelOccurrenceView.as_view(),
        name="cancel_occurrence_by_date",
    ),
    path(
        r"^occurrence/edit/(?P<event_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<hour>\d+)/(?P<minute>\d+)/(?P<second>\d+)/$",
        CreateOccurrenceView.as_view(),
        name="edit_occurrence_by_date",
    ),
    # api paths
    path(r"^api/occurrences", api_occurrences, name="api_occurrences"),
    path(
        r"^api/move_or_resize/$", api_move_or_resize_by_code, name="api_move_or_resize"
    ),
    path(r"^api/select_create/$", api_select_create, name="api_select_create"),
    path(r"^$", ListView.as_view(queryset=Calendar.objects.all()), name="schedule"),
]