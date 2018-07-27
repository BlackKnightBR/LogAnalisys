#!/usr/bin/env python

import psycopg2

# views
#  create view totalStatus as
#  select substring(cast(time as text) from 1 for 10) "day",
#  count(*) as num from
#  log group by day;
#
#  create view logFailed as
#  select substring(cast(time as text) from 1 for 10) "day", count(*) as num
#  from log where status != '200 OK'
#  group by day;
#
#  create view percentage as
#  select logFailed.day,
#  (logFailed.num::double precision/totalStatus.num::double precision)
#  * 100 as percent
#  from logFailed
#  inner join totalStatus on logFailed.day = totalStatus.day;

# Titles of requests and queries
request = [
        [
         """Three most popular articles of all time.""",

         """select articles.title, count(*) as num
            from log, articles
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            group by articles.title
            order by num desc
            limit 3;"""
        ],

        [
         """Most popular article authors of all time.""",

         """select authors.name, count(*) as num
            from articles, authors, log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = substr(log.path, 10)
            group by authors.name
            order by num desc; """
        ],

        [
         """Which day did more than 1% of requests lead to errors.""",

         """select day, round(cast(percentage.percent as numeric),2) as percent
            from percentage
            where percent > 1.0"""
        ]
]


# Request data from the database
def dbRequest(query):
    try:
        conn = psycopg2.connect(database="news")
    except psycopg2.Error as e:
        print("Unable to reach database")
        print(e.pgerror)
        print(e.diag.message_detail)
        sys.exit(1)
    else:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results


def quering(request):
    for title, query in request:
        print("\n\t" + title + "\n")
        response = dbRequest(query)
        for item, count in response:
            print("\t\t {} -- {}".format(item, count))


quering(request)
