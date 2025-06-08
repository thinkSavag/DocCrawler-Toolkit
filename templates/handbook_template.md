{% raw %}
<!-- top of handbook_template.md -->
# {{ pages[0].title }}

*Generated on {{ timestamp }}*

---

## Table of Contents

{% for item in pages[0].toc %}
- **Level {{ item.level }}:** {{ item.text }} {% if item.link %}([link]({{ item.link }})){% endif %}
{% endfor %}

---

{% for page in pages %}
# {{ page.title }}

{% for sec in page.sections %}
## {{ sec.header }}

{{ sec.text }}

{% if sec.tables %}
| {{ sec.tables[0].headers | join(" | ") }} |
|---{% for _ in sec.tables[0].headers %}|{% endfor %}
{% for row in sec.tables[0].rows %}
| {{ row | join(" | ") }} |
{% endfor %}
{% endif %}

{% if sec.images %}
{% for img in sec.images %}
![image]({{ img }})
{% endfor %}
{% endif %}

{% endfor %}
{% endfor %}
{% endraw %}
