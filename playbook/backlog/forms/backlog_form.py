import time
from datetime import date
from django import forms
from django.db.models import Q
from django.forms.models import inlineformset_factory
from ...core.models import Backlog, Estimate, Event,\
    AcceptanceCriteria


class EstimateForm(forms.ModelForm):
    backlog_id = forms.CharField(widget=forms.HiddenInput())
    team_id = forms.CharField(widget=forms.HiddenInput())
    estimate = forms.CharField(
        max_length=Estimate._meta.get_field('estimate').max_length)

    class Meta:
        model = Estimate
        fields = ('backlog_id', 'team_id', 'estimate')


class BacklogUpdateForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    story_descr = forms.CharField(
        max_length=Backlog._meta.get_field('story_descr').max_length,
        label="Story Description",
        widget=forms.Textarea()
    )
    notes = forms.CharField(
        max_length=Backlog._meta.get_field('notes').max_length,
        widget=forms.Textarea()
    )
    skills = forms.CharField(
        max_length=Backlog._meta.get_field('skills').max_length
    )

    def __init__(self, *args, **kwargs):
        self.read_only = kwargs.pop('read_only', False)
        super(BacklogUpdateForm, self).__init__(*args, **kwargs)
        if self.read_only:
            self.mark_fields_as_read_only()
        self.fields['sprint'].required = False
        self.fields['sprint'].queryset = self.get_sprint_options(self.instance)
        try:
            self.fields['sprint'].initial = self.instance.sprint.id
        except Event.DoesNotExist:
            pass

    def mark_fields_as_read_only(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    def get_sprint_options(self, backlog):
        try:
            current_sprint_id = self.instance.sprint.id
        except Event.DoesNotExist:
            current_sprint_id = None
        today = date.fromtimestamp(time.time())
        # FIXME: Hitting database twice. Is it really necessary?
        sprints = Event.objects.filter(Q(schedule=backlog.project.schedule),
                                       Q(end_dttm__gte=today) |
                                       Q(id=current_sprint_id))\
            .order_by('end_dttm')
        sprints_ids = sprints.values_list('id', flat=True)[:3]
        return Event.objects.filter(id__in=sprints_ids)

    def save(self, commit=True):
        instance = super(BacklogUpdateForm, self).save(commit=False)
        if commit:
            instance.save(update_fields=['story_descr', 'skills', 'notes'])
        return instance

    class Meta:
        model = Backlog
        fields = ('id', 'story_descr', 'notes', 'skills', 'sprint')


# class AcceptanceCriteriaForm(forms.ModelForm):

#     id = forms.CharField(widget=forms.HiddenInput())
#     title = forms.CharField(
#         max_length=AcceptanceCriteria._meta.get_field('title').max_length
#     )
#     descr = forms.CharField(
#         max_length=AcceptanceCriteria._meta.get_field('descr').max_length
#     )

#     def __init__(self, read_only=False, *args, **kwargs):
#         self.read_only = kwargs.pop('read_only', False)
#         super(AcceptanceCriteriaForm, self).__init__(*args, **kwargs)
#         print 'self.read_only = %s' % self.read_only
#         if self.read_only:
#             self.mark_fields_as_read_only()

#     def mark_fields_as_read_only(self):
#         for field in self.fields:
#             self.fields[field].widget.attrs['readonly'] = True

#     def save(self, commit=True):
#         instance = super(AcceptanceCriteriaForm, self).save(commit=False)
#         if commit:
#             instance.save(update_fields=['title', 'descr'])
#         return instance

#     class Meta:
#         model = AcceptanceCriteria
#         fields = ('id', 'title', 'descr')

AcceptanceCriteriaFormSet = inlineformset_factory(Backlog, AcceptanceCriteria,
                                                  fields=('id', 'backlog',
                                                          'title', 'descr'),
                                                  extra=1,
                                                  widgets={'title': forms.Textarea(),
                                                           'descr': forms.Textarea()})
