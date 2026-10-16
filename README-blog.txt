BLOG — Human Skills by Sudeep Ghosh
===================================

WHAT IS HERE
------------
  blog.html                        the listing page (new posts appear here automatically)
  blog/                            one file per post
  sitemap.xml                      includes both blog pages
  new-post.py                      the generator — adds a post without editing HTML
  site.css                         your site stylesheet (the generator needs it)
  blog.css                         blog-specific styles
  posts/_sample.md                 a working example you can copy
  images/blog/sample-header.jpg    placeholder header image
  index.html, training.html, ...   your 8 pages, each with the new "07 Insights" nav item

WHERE THINGS GO IN YOUR REPO
----------------------------
  blog.html, sitemap.xml, new-post.py, site.css, blog.css, README-blog.txt   -> repo root
  index.html ... privacy.html                                               -> repo root (replaces)
  blog/                                                                     -> repo root (new folder)
  images/blog/                                                              -> inside images/ (new folder)
  posts/                                                                    -> repo root (your drafts; optional to commit)


ADDING A POST
-------------
1. Create a text file in posts/, e.g. posts/six-sigma-and-ai.md
2. Start it with a front-matter block, then write the body in markdown:

     ---
     title: Six Sigma and AI: where it actually helps
     category: Manufacturing
     date: 2026-10-25
     image: images/blog/six-sigma.jpg
     excerpt: One line that appears on the listing card.
     ---
     ## A heading

     Body text. **Bold**, *italic*, [links](https://example.com) all work.

     - bullet one
     - bullet two

     > A pull quote.

3. Run:   python3 new-post.py posts/six-sigma-and-ai.md
4. Commit and push.

That is all. The script writes blog/<slug>.html, adds the card to blog.html,
and appends the URL to sitemap.xml.

FRONT MATTER FIELDS
-------------------
  title      required   the headline
  category   required   shows on the card and in the post eyebrow
  date       required   YYYY-MM-DD
  excerpt    required   one line for the listing card
  image      optional   header image, path from the site root e.g. images/blog/foo.jpg
  slug       optional   defaults to the title, lowercased with hyphens
  read       optional   defaults to a word-count estimate

HEADER IMAGES
-------------
Yes — every post can have one, exactly like a LinkedIn article.

  - Put the file in images/blog/
  - Name it in the front matter as  image: images/blog/your-file.jpg
  - Ideal size: 1600 x 800 (2:1). Anything close works; it is scaled to fit.
  - The generator uses it three ways: the post header, og:image for social
    sharing, and the "image" property in the BlogPosting schema.
  - Leave "image" out and the post falls back to the gradient artwork, so it
    is optional per post.

WRITING TIPS THAT MATTER FOR SEARCH
-----------------------------------
  - One idea per post, and put it in the title.
  - Link to your own pages where relevant (training.html, free-resources.html).
  - Keep the category consistent with the chips on blog.html.
  - A post every few weeks beats five in one week and then nothing.

