
# Create your models here.
from django.db import models

class CycleRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="分析時間")
    stage_3y = models.IntegerField(null=True, blank=True, verbose_name="3年基準判定階段")
    stage_1y = models.IntegerField(null=True, blank=True, verbose_name="1年基準判定階段")
    stage_6m = models.IntegerField(null=True, blank=True, verbose_name="半年基準判定階段")
    stage_3m = models.IntegerField(null=True, blank=True, verbose_name="3個月基準判定階段")
    raw_data = models.JSONField(verbose_name="完整原始數據與趨勢")

    class Meta:
        ordering = ['-created_at'] # 預設按時間倒序排列

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d')} - 半年基準階段: {self.stage_6m}"