-- Re-upload counts by view band, same classification as content-types.sql.
-- Takes the latest snapshot per post, maps each post to a piece by caption, then types it.
-- Run: sqlite3 -header -column your.db < reupload-thresholds.sql
with latest as (
  select platform, post_id, max(captured_at) c from metric_snapshots group by 1, 2
),
ig as (
  select p.post_id, p.posted_at, p.kind, lower(p.text) t, m.views, m.saves, m.shares
  from latest l
  join metric_snapshots m on m.platform = l.platform and m.post_id = l.post_id and m.captured_at = l.c
  join posts p on p.platform = m.platform and p.post_id = m.post_id
  where p.platform = 'instagram'
),
pieced as (
  select *,
    case
      when kind = 'story' then 'story:' || post_id
      when t like '%zombie movie%' and (t like '%drops%' or t like '%trailer%') then
        case when t like '%part 2%' then 'zombie teaser p2'
             when t like '%part 3%' then 'zombie teaser p3'
             when t like '%part 4%' then 'zombie teaser p4' end
      when t like '%another piece%' then 'zombie extra'
      when t like '%zombie movie%' and (t like '%part 4%' or t like '%part four%') then 'zombie p4'
      when t like '%zombie movie%' and (t like '%part 3%' or t like '%part three%') then 'zombie p3'
      when t like '%zombie movie%' and (t like '%part 2%' or t like '%part two%') then 'zombie p2'
      when t like '%princess zombie movie%' then 'zombie p1'
      when t like '%shabang%' then 'shabang'
      when t like '%beauty machine%' then 'beauty machine'
      when t like '%eleven use%' then 'eleven psychic'
      when t like '%peter and mj%' then 'peter and mj'
      else 'one:' || post_id
    end piece
  from ig
),
ranked as (
  select *,
    row_number() over (partition by piece order by posted_at) n_upload,
    julianday(posted_at) - julianday(min(posted_at) over (partition by piece)) days_after_first
  from pieced
),
typed as (
  select *,
    case
      when kind = 'story' then '7 story'
      when n_upload > 1 then '4 re-upload of a piece already posted'
      when piece in ('zombie p1', 'zombie p2', 'zombie p3') then '1 numbered part 1-3, first upload'
      when piece = 'zombie p4' then '2 numbered part 4, first upload (disputed)'
      when piece like 'zombie teaser%' or piece = 'zombie extra' then '3 series teaser or extra clip'
      when kind = 'post' then '6 image or carousel post'
      else '5 one-off reel'
    end type
  from ranked
)
select count(*) reuploads,
  sum(views < 3300) under_3300,
  sum(views between 3300 and 49999) from_3300_to_49999,
  sum(views >= 50000) at_least_50000,
  sum(posted_at >= '2026-08-20') posted_from_aug_20,
  sum(posted_at >= '2026-08-20' and views < 3300) from_aug_20_under_3300
from typed where type like '4%';
