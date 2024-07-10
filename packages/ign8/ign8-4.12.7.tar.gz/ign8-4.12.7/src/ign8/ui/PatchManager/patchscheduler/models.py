from django.db import models

# Create your models here.
# Environment are predefined
#TEST / DEV Batch 1-03
#TEST / DEV Batch 1-04
#TEST / DEV Batch 1-05
#TEST / DEV Batch 1-06
#TEST / DEV Batch 1-07
#TEST / DEV Batch 1-08
#TEST / DEV Batch 1-09
#TEST / DEV Batch 1-10
#TEST / DEV Batch 1-11
#TEST / DEV Batch 1-12
#TEST / DEV Batch 1-13
#TEST / DEV Batch 1-14
#TEST / DEV Batch 1-15
#TEST / DEV Batch 1-16
#TEST / DEV Batch 1-17
#TEST / DEV Batch 1-18
#TEST / DEV Batch 1-19
#TEST / DEV Batch 1-20
#TEST / DEV Batch 1-21
#TEST / DEV Batch 1-22
#TEST / DEV Batch 2-01
#TEST / DEV Batch 2-02
#TEST / DEV Batch 2-03
#TEST / DEV Batch 2-04
#TEST / DEV Batch 2-05
#TEST / DEV Batch 2-06
#TEST / DEV Batch 2-07
#TEST / DEV Batch 2-08
#TEST / DEV Batch 2-09
#TEST / DEV Batch 2-10
#TEST / DEV Batch 2-11
#TEST / DEV Batch 2-12
#TEST / DEV Batch 2-13
#TEST / DEV Batch 2-14
#TEST / DEV Batch 2-15
#TEST / DEV Batch 2-16
#TEST / DEV Batch 2-17
#pro

class Environment(models.Model):
    environment = models.CharField(max_length=50)
    def __str__(self):
        return self.environment
    

class Server(models.Model):
    app_id = models.CharField(max_length=10)
    server_name = models.CharField(max_length=100)
    patch_window_name = models.CharField(max_length=100)
    environment = models.CharField(max_length=50)

class PatchDate(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    january = models.DateField()
    february = models.DateField()
    march = models.DateField()
    april = models.DateField()
    may = models.DateField()
    june = models.DateField()
    july = models.DateField()
    august = models.DateField()
    september = models.DateField()
    october = models.DateField()
    november = models.DateField()
    december = models.DateField()




class PatchDates(models.Model):
    environment = models.ForeignKey(Environment, on_delete=models.CASCADE)
    patch_date_januar = models.DateField()
    patch_date_februar = models.DateField()
    patch_date_march = models.DateField()
    patch_date_april = models.DateField()
    patch_date_may = models.DateField()
    patch_date_june = models.DateField()
    patch_date_july = models.DateField()
    patch_date_august = models.DateField()
    patch_date_september = models.DateField()
    patch_date_october = models.DateField()
    patch_date_november = models.DateField()
    patch_date_december = models.DateField()

    def __str__(self):
        return self.app_id

#csv file
#APP ID,ServerName,PatchWindowName,Environment,PatchDateJuly,PatchDateAugust,PatchDateSeptember,PatchDateOctober,PatchDateNovember,PatchDateDecember
#,i09966,TEST / DEV Batch 1-03,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i09970,TEST / DEV Batch 1-04,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#i31086,TEST / DEV Batch 1-06,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31736,TEST / DEV Batch 1-07,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31737,TEST / DEV Batch 1-08,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31757,TEST / DEV Batch 1-09,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31758,TEST / DEV Batch 1-10,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31767,TEST / DEV Batch 1-11,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31768,TEST / DEV Batch 1-12,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i31976,TEST / DEV Batch 1-13,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i33384,TEST / DEV Batch 1-14,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i33905,TEST / DEV Batch 1-15,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i33906,TEST / DEV Batch 1-16,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i91296,TEST / DEV Batch 1-17,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i91298,TEST / DEV Batch 1-19,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i91299,TEST / DEV Batch 1-20,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i931012,TEST / DEV Batch 1-22,Production,04/07/2024,05/08/2024,04/09/2024,04/10/2024,05/11/2024,04/12/2024
#,i931013,TEST / DEV Batch 2-01,Production,05/07/2024,06/08/2024,05/09/2024,07/10/2024,06/11/2024,05/12/2024
#,i931014,TEST / DEV Batch 2-02,Production,05/07/2024,06/08/2024,05/09/2024,07/10/2024,06/11/2024,05/12/2024
#,i931015,TEST / DEV Batch 2-03,Production,05/07/2024,06/08/2024,05/09/2024,07/10/2024,06/11/2024,05/12/2024
#,i931016,TEST / DEV Batch 2-04,Production,05/07/2024,06/08/2024,05/09/2024,07/10/2024,06/11/2024,05/12/2024
#,i931017,TEST / DEV Batch 2-05,Production,05/07/2024,06/08/2024,05/09/2024,07/10/2024,06/11/2024,05/12/2024