# MLHouse website

Research report: **Finding prompt injections at web scale**.

This repository is private for internal review. GitHub Pages is not enabled. The complete static website is in [`site/`](site/); it needs no package installation or build step.

## Review the report

With repository access, choose **Code → Download ZIP**, extract it, and open `site/index.html` in a browser. All styling, scripts, and logos are included. Alternatively:

```sh
git clone https://github.com/MLhouse-project/website.git
cd website
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

Open <http://127.0.0.1:8765/>. Use the report's Print button to print or save a PDF. Review feedback can be left in this repository's issues or on proposed changes. Administrators can grant reviewer access under **Settings → Collaborators and teams**.

## Edit and check

- Report text: [`site/index.html`](site/index.html).
- Layout and print styles: [`site/assets/report.css`](site/assets/report.css).
- Reading enhancements: [`site/assets/report.js`](site/assets/report.js).

```sh
python3 scripts/validate_report_site.py
node --check site/assets/report.js
```

The validation workflow runs on pushes and pull requests. It checks local links, document structure, and publication contents; it does not validate research claims. Keep internal audit notes, private references, datasets, and credentials out of the website. The report presents its own methods and findings directly and cites public external sources. Dataset access is handled through the contact listed in the report.

## Publish with GitHub Pages after review

Publishing is manual; pushing or merging changes does not publish the website.

1. Complete the publication review and update the draft status in the report when agreed.
2. In **Settings → Pages → Build and deployment**, select **GitHub Actions** as the source.
3. Open **Actions → Publish website → Run workflow**, choose `main`, and check the publication confirmation. The workflow validates the files and publishes only `site/`.
4. Use the URL reported by the deployment. The default project URL is normally `https://mlhouse-project.github.io/website/`; organization domain settings can affect it.
5. Once the MLHouse domain is confirmed, configure it in **Settings → Pages**, add the required DNS records, and enable HTTPS. Add the final canonical URL and `og:url` to the document metadata. No custom domain is assumed in this repository.

GitHub Pages can publish from a private organization repository on an eligible paid plan. **Repository privacy does not make the published website private**: access-controlled Pages requires GitHub Enterprise Cloud. Keep Pages disabled during repository-only review unless private site access is explicitly configured. See [publishing-source settings](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [Pages access control](https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site), and [custom domains](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages).

## Institutional artwork

Official artwork is stored locally and used with its original colors and proportions:

- MICIU / EU co-funding / AEI: [official combined artwork](https://www.aei.gob.es/sites/default/files/inline-images/MICIU%2BCofinanciado%2BAEI.jpg), selected using the [AEI funding-publicity guidance](https://www.aei.gob.es/ayudas-concedidas/comunicacion-publicidad-ayudas-concedidas) for CPP2023/2024. Preserve the required logo order; this is FEDER support.
- BSC: the regular blue SVG from the [BSC Brand & Logo page](https://www.bsc.es/discover-bsc/brand-and-logo).
- RES: the color SVG from the [RES institutional identity page](https://www.res.es/es/imagen-institucional).
