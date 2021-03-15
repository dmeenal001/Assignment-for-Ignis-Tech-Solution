from django.shortcuts import  render

import pymysql as mysql

def  EventRegistration(request):
    return render(request, "EventRegistration.html", {'msg': ''})


def EventSubmit(request):

    ename = request.POST['ename']
    date = request.POST['date']
    time= request.POST['time']
    location= request.POST['location']
    file = request.FILES['image']

    try:
              dbe = mysql.connect(host="localhost", port=3306,user="root", password='admin', db="event")
              cmd = dbe.cursor()
              q = "insert into events (event_name,date,time,location,image) values('{0}','{1}','{2}','{3}','{4}')".format(ename, date, time,location, file.name)

              cmd.execute(q)
              dbe.commit()
              dbe.close()
              # upload file
              f = open("e:/Event/asset/" + file.name, "wb")
              for chunk in file.chunks():
                     f.write(chunk)
              f.close()
              return render(request,"EventRegistration.html",{'msg':'Event Registered'})
    except Exception as e:
              print(e)
              return render(request, "EventRegistration.html", {'msg': 'Failed to Register Event '})

def DisplayAllEvents(request):

    try:
              dbe = mysql.connect(host="localhost", port=3306, user="root", password='admin', db="event")

              cmd = dbe.cursor()
              q="select *  from events"
              cmd.execute(q)
              rows=cmd.fetchall()
              dbe.close()
              return render(request, "DisplayAllEvents.html",{'rows':rows})
    except Exception as e:
         print(e)
         return render(request, "DisplayAllEvents.html",{'rows':[]})


def AddToLiked(request):
    eid = request.GET['eid']

    try:

        dbe = mysql.connect(host="localhost", port=3306, user="root", password='admin', db="event")
        cmd = dbe.cursor()
        q = "update events set is_liked= 1 where eventid={0}".format(eid)
        print(q)

        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return DisplayAllEvents(request)

    except Exception as e:
              return DisplayAllEvents(request)

def LikedEvents(request):

    try:
              dbe = mysql.connect(host="localhost", port=3306, user="root", password='admin', db="event")

              cmd = dbe.cursor()
              q="select *  from events E where E.is_liked=1"
              cmd.execute(q)
              rows=cmd.fetchall()
              dbe.close()
              return render(request, "LikedEvents.html",{'rows':rows})
    except Exception as e:
         print(e)
         return render(request, "LikedEvents.html",{'rows':[]})

def Unlike(request):
    eid = request.GET['eid']

    try:

        dbe = mysql.connect(host="localhost", port=3306, user="root", password='admin', db="event")
        cmd = dbe.cursor()
        q = "update events set is_liked= 0 where eventid={0}".format(eid)
        print(q)

        cmd.execute(q)
        dbe.commit()
        dbe.close()
        return LikedEvents(request)

    except Exception as e:
              return LikedEvents(request)