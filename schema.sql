-- Run this in the Supabase SQL editor

-- Articles table
create table articles (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  summary text,
  content text,
  source_url text not null unique,
  source_name text not null,
  category text,
  ministry text,
  state text default 'Central',
  language text default 'en',
  published_at timestamptz,
  scraped_at timestamptz default now(),
  url_hash text unique,
  is_duplicate boolean default false,
  tags text[]
);

-- Sources registry table
create table sources (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  base_url text not null,
  feed_url text,
  scraper_type text,        -- 'rss' | 'html' | 'api'
  category text,
  state text default 'Central',
  is_active boolean default true,
  last_scraped_at timestamptz,
  created_at timestamptz default now()
);

-- Seed initial sources
insert into sources (name, base_url, feed_url, scraper_type, category, state) values
  ('PIB', 'https://pib.gov.in', 'https://pib.gov.in/RssMain.aspx?ModId=6&Lang=1&Regid=3', 'rss', 'Press Release', 'Central'),
  ('PIB Hindi', 'https://pib.gov.in', 'https://pib.gov.in/RssMain.aspx?ModId=6&Lang=2&Regid=3', 'rss', 'Press Release', 'Central'),
  ('India.gov.in', 'https://www.india.gov.in', null, 'html', 'General', 'Central'),
  ('myScheme', 'https://www.myscheme.gov.in', null, 'html', 'Schemes', 'Central');

-- Full text search index
create index articles_fts on articles using gin(to_tsvector('english', coalesce(title,'') || ' ' || coalesce(summary,'')));

-- Category and filter indexes
create index articles_category_idx on articles(category);
create index articles_state_idx on articles(state);
create index articles_published_idx on articles(published_at desc);
