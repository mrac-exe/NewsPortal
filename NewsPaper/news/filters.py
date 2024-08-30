from django import forms
import django_filters
from django_filters import FilterSet
from .models import Author


class DateInput(forms.DateInput):
    input_type = 'date'


class PostFilter(FilterSet):
    author = django_filters.filters.ModelChoiceFilter(queryset=Author.objects.all(), lookup_expr='exact',
                                              label='Выберите автора')
    title = django_filters.CharFilter(lookup_expr='icontains', label='Поиск по словам в заголовке новости')
    date_time = django_filters.DateFilter(widget=DateInput(attrs={'type': 'date'}),
                                          label='Показать все новости, размещенные позднее',
                                          lookup_expr='date__gt')