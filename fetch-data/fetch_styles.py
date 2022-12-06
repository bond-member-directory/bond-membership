import os

import requests
from settings import BOND_ASSET_OUTPUT, BOND_FOOTER, BOND_HEADER, BOND_STYLESHEET

DESCRIPTION = """
<div class="fr">
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


def fetch_header_and_footer():
    header = requests.get(BOND_HEADER).text
    footer = requests.get(BOND_FOOTER).text

    with open(os.path.join(BOND_ASSET_OUTPUT, "template/index.html"), "r") as f:
        template = f.read()

    with open(os.path.join(BOND_ASSET_OUTPUT, "index.html"), "w") as f:
        f.write(
            template.replace("<%= HEADER %>", header)
            .replace("<%= FOOTER %>", footer)
            .replace("<%= BOND_CSS %>", BOND_STYLESHEET)
            .replace(
                '<div class="site-branding">',
                '<div class="site-branding">' + DESCRIPTION,
            )
            .replace(
                "</div><!-- .site-branding -->",
                '<h1 class="bond-mid-grey header-text normal f1 f2 mt0 mb3 w100 w-50-l" data-v-ad84f3a8="">Members Directory</h1></div><!-- .site-branding -->',
            )
        )
