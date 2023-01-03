import os

import requests
from settings import (
    BOND_ASSET_OUTPUT,
    BOND_FOOTER,
    BOND_HEADER,
    BOND_SCRIPT,
    BOND_STYLESHEET,
)

DESCRIPTION = """
<div class="fr {classes} normal">
    <p class="measure f5 ma0 pa0 lh-copy tl">
        Browse the international development organisations that are members of 
        <a href="https://www.bond.org.uk/about-us" target="_blank" class="bond-red link underline bond-link b">the Bond network</a>,
        and see which countries they work in and which Sustainable Development Goals they focus on.
    </p>
    <p class="measure f5 ma0 pa0 lh-copy tl">
        If you have any feedback on this directory, please 
        <a href="https://www.bond.org.uk/contact-us" target="_blank" class="bond-red link underline bond-link b">get in touch</a>.
    </p>
</div>
"""
HEADING = """
<h1 class="bond-mid-grey header-text b f1 f2 mt0 mb3 w100 w-50-l">
    Members Directory
</h1>
"""


def fetch_header_and_footer():
    r = requests.get(BOND_HEADER)
    r.raise_for_status()
    header = r.text

    r = requests.get(BOND_FOOTER)
    r.raise_for_status()
    footer = r.text

    with open(os.path.join(BOND_ASSET_OUTPUT, "template/index.html"), "r") as f:
        template = f.read()

    with open(os.path.join(BOND_ASSET_OUTPUT, "index.html"), "w") as f:
        f.write(
            template.replace("<%= HEADER %>", header)
            .replace("<%= FOOTER %>", footer)
            .replace("<%= BOND_CSS %>", BOND_STYLESHEET)
            .replace("<%= BOND_SCRIPT %>", BOND_SCRIPT)
            .replace('href="/join"', 'href="https://www.bond.org.uk/join/"')
            # .replace(
            #     '<div class="site-branding">',
            #     '<div class="site-branding">' + DESCRIPTION.format(classes="dn db-l"),
            # )
            # .replace(
            #     "</div><!-- .site-branding -->",
            #     HEADING
            #     + DESCRIPTION.format(classes="db dn-l")
            #     + "</div><!-- .site-branding -->",
            # )
        )
