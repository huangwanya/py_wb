from django.contrib import admin
from keshihua.models import *
from openpyxl import Workbook
from django.http import HttpResponse
# Register your models here.

admin.site.site_header = '微博舆情可视化系统'
admin.site.site_title = "微博舆情可视化系统"

class ExportExcelMixin(object):
    def export_as_excel(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='application/msexcel')
        response['Content-Disposition'] = f'attachment; filename={meta}.xlsx'
        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for obj in queryset:
            for field in field_names:
                data = [f'{getattr(obj, field)}' for field in field_names]
            row = ws.append(data)

        wb.save(response)
        return response
    export_as_excel.short_description = '导出Excel'


@admin.register(Case_item)
class Case_item_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("fabu_name", "fabushijian", "content", "status","possibility",)
    actions = ['export_as_excel']
    search_fields = ("fabu_name", "content",)
    list_filter = ['status']


@admin.register(Yonghu)
class Yonghu_Admin(admin.ModelAdmin, ExportExcelMixin):
    list_display = ("username", "email", "set", "age")
    actions = ['export_as_excel']
    search_fields = ("username",)