from django.db import connection,models
from django.http import HttpResponse
from datetime import date
def getallusser(request):
    with connection.cursor() as cursor:

        sql = "SELECT * FROM userModel_user"
        cursor.execute(sql)
        result = cursor.fetchall()
        res=""

        for userRes in result:
            res+=userRes[1]+ "   " + userRes[2]
            time = userRes[4]
            res+= " "+time.strftime('%Y-%m-%d')
        return HttpResponse(res)
    return HttpResponse("ERROR")