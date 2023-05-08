from django.db import models

class LekiRefundowane(models.Model):
    lp = models.IntegerField(unique=True, null=False)
    substancja_czynna = models.TextField(default="", null=False)
    nazwa = models.TextField(default="", null=False)
    postac = models.TextField(default="", null=False)
    dawka = models.TextField(default="", null=False)    
    zawartosc_opakowania = models.TextField(default="", null=False)
    ean = models.BigIntegerField(null=False)
    grupa_limitowana = models.TextField(default="", null=False)
    cena_hurtowa = models.IntegerField(default=0, null=False)
    cena_detaliczna = models.IntegerField(default=0, null=False)
    wysokosc_limitu = models.IntegerField(default=0, null=False)
    zakres_wskazan = models.TextField(default="", null=False)
    poziom_odplatnosci = models.CharField(max_length=10, default="", null=False)   
    wysokosc_doplaty = models.IntegerField(default = 0, null=False) 


class LicznikWyszukan(models.Model):
    ean = models.BigIntegerField(default="")
    ctr = models.IntegerField(default=0)