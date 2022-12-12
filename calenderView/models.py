from django.contrib.contenttypes import fields
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django_project.settings import USE_FULLCALENDAR
from calenderView.utils import EventListManager


class CalendarManager(models.Manager):
    """
    >>> user1 = User(username='tony')
    >>> user1.save()
    """

    def get_calendar_for_object(self, obj, distinction=""):
        """
        This function gets a calendar for an object.  It should only return one
        calendar.  If the object has more than one calendar related to it (or
        more than one related to it under a distinction if a distinction is
        defined) an AssertionError will be raised.  If none are returned it will
        raise a DoesNotExistError.
        >>> user = User.objects.get(username='tony')
        >>> try:
        ...     Calendar.objects.get_calendar_for_object(user)
        ... except Calendar.DoesNotExist:
        ...     print("failed")
        ...
        failed
        Now if we add a calendar it should return the calendar
        >>> calendar = Calendar(name='My Cal')
        >>> calendar.save()
        >>> calendar.create_relation(user)
        >>> Calendar.objects.get_calendar_for_object(user)
        <Calendar: My Cal>
        Now if we add one more calendar it should raise an AssertionError
        because there is more than one related to it.
        If you would like to get more than one calendar for an object you should
        use get_calendars_for_object (see below).
        >>> calendar = Calendar(name='My 2nd Cal')
        >>> calendar.save()
        >>> calendar.create_relation(user)
        >>> try:
        ...     Calendar.objects.get_calendar_for_object(user)
        ... except AssertionError:
        ...     print("failed")
        ...
        failed
        """
        calendar_list = self.get_calendars_for_object(obj, distinction)
        if len(calendar_list) == 0:
            raise Calendar.DoesNotExist("Calendar does not exist.")
        elif len(calendar_list) > 1:
            raise AssertionError("More than one calendars were found.")
        else:
            return calendar_list[0]

    def get_or_create_calendar_for_object(self, obj, distinction="", name=None):
        """
        >>> user = User(username="jeremy")
        >>> user.save()
        >>> calendar = Calendar.objects.get_or_create_calendar_for_object(user, name = "Jeremy's Calendar")
        >>> calendar.name
        "Jeremy's Calendar"
        """
        try:
            return self.get_calendar_for_object(obj, distinction)
        except Calendar.DoesNotExist:
            if name is None:
                calendar = self.model(name=str(obj))
            else:
                calendar = self.model(name=name)
            calendar.slug = slugify(calendar.name)
            calendar.save()
            calendar.create_relation(obj, distinction)
            return calendar

    def get_calendars_for_object(self, obj, distinction=""):
        """
        This function allows you to get calendars for a specific object
        If distinction is set it will filter out any relation that doesnt have
        that distinction.
        """
        ct = ContentType.objects.get_for_model(obj)
        if distinction:
            dist_q = Q(calendarrelation__distinction=distinction)
        else:
            dist_q = Q()
        return self.filter(
            dist_q,
            calendarrelation__content_type=ct,
            calendarrelation__object_id=obj.id,
        )


class Calendar(models.Model):
    """
    This is for grouping events so that batch relations can be made to all
    events.  An example would be a project calendar.
    name: the name of the calendar
    events: all the events contained within the calendar.
    >>> calendar = Calendar(name = 'Test Calendar')
    >>> calendar.save()
    >>> data = {
    ...         'title': 'Recent Event',
    ...         'start': datetime.datetime(2008, 1, 5, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 10, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Upcoming Event',
    ...         'start': datetime.datetime(2008, 1, 1, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 4, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Current Event',
    ...         'start': datetime.datetime(2008, 1, 3),
    ...         'end': datetime.datetime(2008, 1, 6)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    """

    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=191, unique=True)
    objects = CalendarManager()

    class Meta:
        verbose_name = _("calendar")
        verbose_name_plural = _("calendars")

    def __str__(self):
        return self.name

    @property
    def events(self):
        return self.event_set

    def create_relation(self, obj, distinction="", inheritable=True):
        '''
        Creates a CalendarRelation between self and obj.
        if Inheritable is set to true this relation will cascade to all events
        related to this calendar.
        '''
        CalendarRelation.objects.create_relation(self, obj, distinction, inheritable)

    def get_recent(self, amount=5):
        '''
        This shortcut function allows you to get events that have started
        recently.
        amount is the amount of events you want in the queryset. The default is
        5.
        '''
        return self.events.order_by("-start").filter(start__lt=timezone.now())[:amount]

    def occurrences_after(self, date=None):
        return EventListManager(self.events.all()).occurrences_after(date)

    def get_absolute_url(self):
        if USE_FULLCALENDAR:
            return reverse("fullcalendar", kwargs={"calendar_slug": self.slug})
        return reverse("calendar_home", kwargs={"calendar_slug": self.slug})


