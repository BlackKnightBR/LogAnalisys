import psycopg2

views =[

totalStatus = """create view totalStatus
               select substring(cast(time as text),1,10) "time", count(*) as num from
               log group by time; """,

logFailed = """create view logFailed as
             select substring(cast(time as text),1,10) "time", count(*) as num
             from log where status = '404 not found'
             goup by time;""",

percentage = """create view percentage as
           select totalStatus.time, totalStatus.num as total,
           logFailed.num AS fail,
           logFailed.num::double precision/totalStatus.num::double precision * 100 as percentFailed
           from totalStatus,logfailed
           where totalStatus.time = logFailed.time; """
]

# Database queries
# Articles: Three most popular articles of all time.
# Authors: Most popular article authors of all time.
# ReqFailed: Which day did more than 1% of requests lead to errors.
request = [
articles = """select articles.title, count(*) as num
            from log, articles
            where log.status='200 OK'
            and articles.slug = substr(log.path, 10)
            group by articles.title
            order by num desc
            limit 3;""",

authors = """select authors.name, count(*) as num
            from articles, authors, log
            where log.status='200 OK'
            and authors.id = articles.author
            and articles.slug = substr(log.path, 10)
            group by authors.name
            order by num desc; """,

reqFailed = """select time, percentFailed
            from percentage
            where percentagefailed > 1;"""
]
