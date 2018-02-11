SELECT a.l_subreddit as Source, b.l_subreddit as Target, COUNT(*) as Weight
FROM (
  SELECT author, LOWER(subreddit) as l_subreddit, COUNT(DISTINCT(link_id)) as unique_threads
  FROM [pushshift:rt_reddit.comments]
  GROUP BY author, l_subreddit
  HAVING unique_threads >= 5) a JOIN (
  SELECT author, LOWER(subreddit) as l_subreddit, COUNT(DISTINCT(link_id)) as unique_threads
  FROM [pushshift:rt_reddit.comments]
  GROUP BY author, l_subreddit
  HAVING unique_threads >= 5) b ON a.author = b.author
GROUP BY Source, Target
HAVING Source < Target AND Weight >= 200
ORDER BY Weight DESC