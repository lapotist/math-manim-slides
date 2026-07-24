# Third-Party Components

The project uses dependencies through the Pixi environment. Their code and
package contents retain their own licenses and are not covered by this
repository's CC0 dedication.

| Component | Version | License | Homepage |
| --- | --- | --- | --- |
| Manim Community | 0.20.1 | MIT | https://www.manim.community/ |
| Manim Slides | 5.6.0 | MIT | https://manim-slides.eertmans.be/ |
| Tectonic | 0.16.9 | MIT | https://tectonic-typesetting.github.io/ |
| dvisvgm | 3.6 (Fedora `texlive-dvisvgm` fallback) | GPL-3.0-or-later | https://dvisvgm.de/ |
| Potrace | 1.16 (Fedora fallback dependency) | GPL-2.0-or-later AND LGPL-2.0-or-later | http://potrace.sourceforge.net/ |
| AMSFonts / Computer Modern outlines | Fedora `texlive-amsfonts` fallback | OFL-1.1 | https://www.ams.org/open-math-notes/amsfonts |
| Tectonic default TeX bundle | bundle v33, fetched during `prepare-tex` | Mixed TeX package licenses; retained in the user cache, not redistributed | https://tectonic-typesetting.github.io/ |
| PySide6 | 6.9.3 | LGPL-3.0-only/GPL-2.0-only/GPL-3.0-only commercial alternatives; see upstream package terms | https://doc.qt.io/qtforpython-6/ |
| Noto Sans CJK | system installation | OFL-1.1 | https://github.com/notofonts/noto-cjk |

The generated offline HTML exporter may bundle Reveal.js and related assets.
Audit and preserve their notices before distributing exported HTML as a release
artifact.

The Fedora RPMs and extracted binaries are runtime downloads under ignored
`build/` paths. They are not part of the repository's CC0-covered source tree.
