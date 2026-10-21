# RodentStudio Tutorials

Bilingual (English / 中文) tutorials on the models bundled with RodentStudio: where their data and labels came from, how they were trained and tested, how they became Core ML packages, how the app runs them, and how to cite every dataset, paper and software package correctly.

Site: https://seesaw-earth.github.io/RodentStudio-Tutorials/ (once GitHub Pages is enabled)

| Page | English | 中文 |
|---|---|---|
| Overview | `index.html` | `zh/index.html` |
| Tutorial 1 · MousePose6 | `mousepose6.html` | `zh/mousepose6.html` |
| Tutorial 2 · CylinderMousePoseV2 | `cylinder-v2.html` | `zh/cylinder-v2.html` |
| Tutorial 3 · TST MouseDetector | `tst-detector.html` | `zh/tst-detector.html` |
| Tutorial 4 · Core ML in the app | `app-integration.html` | `zh/app-integration.html` |
| How to cite | `citations.html` | `zh/citations.html` |

`references.bib` holds all 24 references. `CITATION.cff` describes how to cite the tutorials themselves.

## Editing

The pages are static HTML with no JavaScript and no third-party requests. Page bodies live in `src/en/` and `src/zh/`; the shared head, navigation, footer and previous/next links are added by a standard-library Python script:

```bash
python3 tools/build.py        # writes *.html, zh/*.html and sitemap.xml
```

Edit the files in `src/`, never the generated pages, then rebuild and commit both. Styles: `assets/styles.css` is copied unchanged from the RodentStudio-Support site; tutorial-specific additions are in `assets/tutorial.css`.

## Publishing on GitHub Pages

1. Create the repository `seesaw-earth/RodentStudio-Tutorials` and push this folder to `main`.
2. Settings → Pages → Build and deployment → Source: *Deploy from a branch*, Branch: `main`, folder `/ (root)`.
3. `.nojekyll` is included so the files are served as they are.

## Sources and verification status

Numbers come from the original Colab notebooks, the metadata inside each shipped `.mlpackage`, and the app source in `seesaw-earth/RodentStudio-Support/source`. Bibliographic details and licences were checked on 2026-10-20 against Zenodo, DataCite, Crossref, arXiv and publisher pages.

Licence finding: the two JAX datasets on Harvard Dataverse (doi:10.7910/DVN/SAPNJG v1.2, doi:10.7910/DVN/RQYI04 v1.0) are CC BY-NC-SA 4.0, so MousePose6 should be treated as non-commercial unless JAX grants permission.

Still open:

- Permission from JAX for commercial use of MousePose6, or a retrained model without the JAX data.
- Whether the lab's cylinder recordings used for CylinderMousePoseV2 are published.
- Training data, settings and evaluation of the bundled TST MouseDetector.
- Results of `validate_on_mac.py` (PyTorch vs. Core ML INT8 parity) for the shipped MousePose6 package.

The licence of the tutorial text itself has not been chosen yet.
