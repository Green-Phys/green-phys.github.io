
# Green website

This repository builds <https://green-phys.org/>, the shared documentation site
for the Green project.

Coding agents and downstream users can start from
[`llms.txt`](https://green-phys.org/llms.txt), which routes to the maintained
installation, workflow, data-format, troubleshooting, and contribution pages.
The index is validated during the site build by `scripts/check-ai-docs.py`.

Bibliographic metadata and citation mappings are owned by
[`Green-Phys/green-citations`](https://github.com/Green-Phys/green-citations).
`scripts/sync-citations.py` imports one resolved commit into the publication
page and BibTeX download; generated citation files must not be edited here.

# Acknowledgements

This work is supported by the US National Science Foundation as part of the NSF CSSI program under the award NSF OAC-2310582

