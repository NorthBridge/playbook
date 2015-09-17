import time
from datetime import date
from django import forms
from django.db.models import Q
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory
from .util import queued_status_id
from apps.shared.models import (Backlog, Estimate, Event,
                           AcceptanceCriteria)


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
            mark_fields_as_read_only(self)
        self.fields['sprint'].required = False
        self.fields['sprint'].queryset = self.get_sprint_options(self.instance)
        if self.instance.sprint:
            self.fields['sprint'].initial = self.instance.sprint.id

    def clean(self):
        if is_backlog_queued(self.instance):
            raise forms.ValidationError("A queued backlog cannot be edited.",
                                        code='not_editable')

    def get_sprint_options(self, backlog):
        if self.instance.sprint:
            current_sprint_id = self.instance.sprint.id
        else:
            current_sprint_id = None

        today = date.fromtimestamp(time.time())

        # event.schedule == backlog.project.schedule and
        #  (event.end_dttm >= today or event.id == backlog.sprint.id)
        sprints = Event.objects.filter(
            Q(schedule=backlog.project.schedule),
            Q(end_dttm__gte=today) | Q(id=current_sprint_id))\
            .order_by('end_dttm')

        # Returns only the first three sprints in the list
        return sprints[:3]

    def save(self, commit=True):
        instance = super(BacklogUpdateForm, self).save(commit=False)
        if commit:
            instance.save(update_fields=['story_descr', 'skills', 'notes'])
        return instance

    class Meta:
        model = Backlog
        fields = ('id', 'story_descr', 'notes', 'skills', 'sprint')


class AcceptanceCriteriaForm(forms.ModelForm):

    id = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(
        max_length=AcceptanceCriteria._meta.get_field('title').max_length,
        widget=forms.Textarea()
    )
    descr = forms.CharField(
        max_length=AcceptanceCriteria._meta.get_field('descr').max_length,
        widget=forms.Textarea()
    )
    backlog = forms.CharField(
        max_length=AcceptanceCriteria._meta.get_field('descr').max_length,
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        super(AcceptanceCriteriaForm, self).__init__(*args, **kwargs)
        if self.instance.id and is_backlog_queued(self.instance.backlog):
            mark_fields_as_read_only(self)

    def save(self, commit=True):
        instance = super(AcceptanceCriteriaForm, self).save(commit=False)
        if commit:
            instance.save(update_fields=['title', 'descr'])
        return instance

    class Meta:
        model = AcceptanceCriteria
        fields = ('id', 'backlog', 'title', 'descr')


class CustomAcceptanceCriteriaFormSet(BaseInlineFormSet):

    def __init__(self, data=None, files=None, instance=None,
                 save_as_new=False, prefix=None, queryset=None, **kwargs):
        super(CustomAcceptanceCriteriaFormSet, self).__init__(
            data=data, files=files, instance=instance, save_as_new=save_as_new,
            prefix=prefix, queryset=queryset, **kwargs)
        if is_backlog_queued(self.instance):
            self.extra = 0

    def clean(self):
        if is_backlog_queued(self.instance):
            raise forms.ValidationError("A queued backlog cannot be edited.",
                                        code='not_editable')

AcceptanceCriteriaFormSet = inlineformset_factory(
    Backlog, AcceptanceCriteria, extra=1, form=AcceptanceCriteriaForm,
    formset=CustomAcceptanceCriteriaFormSet)


def is_backlog_queued(backlog):
    return backlog.id and\
        backlog.status.id == queued_status_id()


def mark_fields_as_read_only(form):
    for field in form.fields:
        form.fields[field].widget.attrs['readonly'] = True
