---
title:     {{ handbook_title }}
date:      {{ date }}
version:   {{ version }}
author:    {{ author }}
---

<!-- TOC will be auto-injected here -->

## What this template does
- Renders a sequence of pages into a single handbook
- Each page must supply:
  - `title` (string)
  - `toc` (list of `{ level, text, link }`)
  - `sections` (list of `{ header, text, tables?, images? }`)

{% for page in pages %}
# {{ page.title }}

{% for entry in page.toc %}
{{ "#" * entry.level }} [{{ entry.text }}]({{ entry.link }})
{% endfor %}

{% for sec in page.sections %}
## {{ sec.header }}

{{ sec.text }}

{% if sec.tables %}
| {{ sec.tables[0].headers | join(' | ') }} |
|{{ ' --- |' * sec.tables[0].headers|length }}

{% for row in sec.tables[0].rows %}
| {{ row | join(' | ') }} |
{% endfor %}
{% endif %}
{% if sec.images %}
{% for img in sec.images %}
![image]({{ img }})
{% endfor %}
{% endif %}
{% endfor %}

{% endfor %}
