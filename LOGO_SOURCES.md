# Institution logo sources

Retrieved and checked on **2026-09-18**. These files identify the institutions in Cristiano's experience and education. The logo artwork belongs to the respective institutions.

| Local asset | Official source | Notes |
| --- | --- | --- |
| `static/images/institutions/nvidia.svg` | [NVIDIA SIL site header](https://research.nvidia.com/labs/sil/shared/index.html) | Extracted the complete `n24-nvidia-logo` SVG symbol into a standalone SVG, retaining its original viewBox, paths, transforms, and colors. Green eye and black horizontal wordmark. |
| `static/images/institutions/naver-labs-europe.png` | [NAVER LABS Europe logo](https://europe.naverlabs.com/wp-content/uploads/2019/01/logo-europe-naver-labs-noir.png), referenced by the [official homepage](https://europe.naverlabs.com/) | Original transparent PNG, 373 × 68 pixels; black LABS wordmark with NAVER LABS EUROPE underneath. |
| `static/images/institutions/tum.svg` | [Technical University of Munich homepage](https://www.tum.de/en/) | Extracted the complete inline SVG from `page__header-logo`, retaining its original viewBox and path. Its `currentColor` fill defaults to black when loaded as an image. |
| `static/images/institutions/unitn.svg` | [University of Trento SVG](https://www.unitn.it/themes/custom/unitn_eventi/logointerno.svg), referenced by the [official brand identity page](https://www.unitn.it/it/brand-identity) | Original SVG with the red seal and black wordmark. Visually cross-checked against the color logo shown on the official brand identity page. |

All four assets were rendered and visually inspected at both large size and a 70-pixel display width. Use a **white logo tile in both light and dark themes**, preserving the original artwork's contrast and proportions. Do not apply CSS filters or crop the marks.

The current lab link is [NVIDIA Spatial Intelligence Lab (SIL)](https://research.nvidia.com/labs/sil/). Its [public main page](https://research.nvidia.com/labs/sil/main.html) confirms the lab name and states that DVL and other research groups have joined forces there. Cristiano's current lab affiliation follows his explicit correction.

## Personal robot icon

`static/images/favicon.svg` is the site's original winking robot artwork, also used in the header. The 32-pixel favicon, 180-pixel touch icon, and root `static/favicon.ico` (16, 32, and 48 pixels) are rasterizations of that same SVG. Browser icon links use Hugo content fingerprints so replacing the artwork changes its URL and bypasses stale browser favicon caches.
