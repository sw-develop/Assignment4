from django_filters import CharFilter, FilterSet, DateFilter

from .models        import TradeLog


class TradeLogListFilter(FilterSet):
    
    start = DateFilter(lookup_expr='gte', field_name='created_at')
    end   = DateFilter(lookup_expr='lte', field_name='created_at')
    code = CharFilter(lookup_expr='exact', field_name='code')

    class Meta:
        model  = TradeLog
        fields = '__all__'