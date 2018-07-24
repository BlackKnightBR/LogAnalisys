import psycopg2

#views
#create view totalStatus as
#select time::date, count(*) as num from
#log group by time;
#
#create view logFailed as
#select time::date, count(*) as num
#from log where status = '404 NOT FOUND'
#group by time;
#

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

         """select (totalStatus.time = logFailed.time) as time,
            ((logFailed.num::double precision/totalStatus.num::double precision) * 100 > 1) as percent
            from totalStatus, logFailed """
        ]
]

# Request data from the database
def dbRequest (query):
    conn = psycopg2.connect(database="news")
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def quering(request):
    for title,query in request:
        print("\n\t" + title + "\n")
        response = dbRequest(query)
        for item, count in response:
            print("\t\t {} -- {}".format(item, count))

quering(request)
