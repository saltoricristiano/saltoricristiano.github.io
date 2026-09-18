# Publication GIF audit

Checked on **18 September 2026** for all **14 publications currently listed on the website**.

**Result:** two distinct, relevant animated GIFs are available from the official CoSMix and GIPSO repository READMEs. They are used by three publication entries, because the CoSMix repository explicitly covers both the ECCV conference paper and its TPAMI extension. Eight other entries have a public repository but no GIF was found in the checked branches or README references. For the remaining three entries, no official public implementation repository was linked from the checked paper/project sources.

The existing static images remain available for every publication. The GIFs are stored locally, avoiding a runtime dependency on GitHub image hosting. A GIF marked as available below is a verified animation, not a badge, logo, or static file with a `.gif` extension.

## Per-publication results

| Website entry | Official sources checked | Result |
| --- | --- | --- |
| Efficient Multi-Camera Tokenization with Triplanes for End-to-End Driving (RA-L 2025) | [NVIDIA publication](https://research.nvidia.com/labs/avg/publication/ivanovic.saltori.etal.ral2025/), [paper](https://arxiv.org/html/2506.12251v1), and a title-based repository search. | No official public implementation repository or GIF linked from these sources. An independently authored implementation found in search was not treated as an author-provided source. Static image retained. |
| Towards Learning to Complete Anything in Lidar (ICML 2025) | [Official project page](https://research.nvidia.com/labs/dvl/projects/complete-anything-lidar/) and [paper](https://arxiv.org/abs/2504.12264). | No public implementation repository or GIF linked. The project page contains an actual [MP4 qualitative demo](https://research.nvidia.com/labs/dvl/projects/complete-anything-lidar/assets/CAL_qualitative_video.mp4), which was not converted to a GIF or added in this update. Static image retained. |
| Cross-Modal and Uncertainty-Aware Agglomeration for Open-Vocabulary 3D Scene Understanding (CVPR 2025) | [CUA_O3D repository](https://github.com/TyroneLi/CUA_O3D), `main` recursive tree and README; [project page](https://tyroneli.github.io/CUA_O3D/). | No GIF found. Repository/project figures are static. Static image retained. |
| Novel Class Discovery Meets Foundation Models for 3D Semantic Segmentation (IJCV 2025) | [SNOPS repository](https://github.com/LuigiRiz/SNOPS), `main` recursive tree and README. | No GIF found. README teaser is `assets/teaser.png`. Static image retained. |
| Unsupervised Point Cloud Representation Learning by Clustering and Neural Rendering (IJCV 2024) | [CluRender repository](https://github.com/gfmei/clurender), `master` and `main` recursive trees and root README files. | No GIF found in either branch or README references. Static image retained. |
| Walking Your LiDOG: A Journey Through Multiple Domains for LiDAR Semantic Segmentation (ICCV 2023) | [LiDOG repository](https://github.com/saltoricristiano/lidog), `main` and `pages` recursive trees and README/HTML; [project page](https://saltoricristiano.github.io/lidog/). | No GIF found. README teaser is `assets/teaser.png`. Static image retained. |
| Novel Class Discovery for 3D Point Cloud Semantic Segmentation (CVPR 2023) | [NOPS repository](https://github.com/LuigiRiz/NOPS), `main` recursive tree and README. | No GIF found. README teaser is `assets/NOPS_teaser.jpg`. Static image retained. |
| Compositional Semantic Mix for Domain Adaptation in Point Cloud Segmentation (TPAMI 2023) | [CoSMix repository README](https://github.com/saltoricristiano/cosmix-uda/blob/main/README.md), `main` recursive tree. | **GIF available and added.** The README identifies both the conference and journal titles above the shared demo and documents the journal extension. This is a shared CoSMix method visualization, not a separate visualization of the journal's one-shot SSDA results. Uses the same local `cosmix.gif` as the conference entry. |
| Overlap-guided Gaussian Mixture Models for Point Cloud Registration (WACV 2023) | [OGMM repository](https://github.com/gfmei/ogmm), `main` recursive tree and README. | No GIF found. Static image retained. |
| CoSMix: Compositional Semantic Mix for Domain Adaptation in 3D LiDAR Segmentation (ECCV 2022) | [CoSMix repository README](https://github.com/saltoricristiano/cosmix-uda/blob/main/README.md), `main` recursive tree. | **GIF available and added.** The README embeds the author-uploaded LiDAR segmentation comparison via GitHub's `user-images` host; it is not a file in the repository tree itself. |
| GIPSO: Geometrically Informed Propagation for Online Adaptation in 3D LiDAR Segmentation (ECCV 2022) | [GIPSO repository README](https://github.com/saltoricristiano/gipso-sfouda/blob/main/README.md), `main` recursive tree. | **GIF available and added.** The README embeds the author-uploaded source/GIPSO/ground-truth comparison via GitHub's `user-images` host; it is not a file in the repository tree itself. |
| Data Augmentation-free Unsupervised Learning for 3D Point Cloud Understanding (BMVC 2022) | [SoftClu repository](https://github.com/gfmei/softclu), `master` and `main` recursive trees and root README files. | No GIF found. README method figure is `figures/main_frame.png`. Static image retained. |
| SF-UDA³D: Source-Free Unsupervised Domain Adaptation for LiDAR-Based 3D Object Detection (3DV 2020) | [Paper](https://iris.unitn.it/retrieve/handle/11572/286980/399788/2010.0824.pdf), which links the [official SF-UDA-3DV repository](https://github.com/saltoricristiano/SF-UDA-3DV); `main` recursive tree and README. | No GIF found. The public repository contains a placeholder README announcing a future code release, so no new Code button was added. Static image retained. |
| Regularized Evolutionary Algorithm for Dynamic Neural Topology Search (ICIAP 2019) | [NVIDIA publication](https://research.nvidia.com/labs/dvl/publication/saltori2019regularized/), [paper record](https://arxiv.org/abs/1905.06252), [author's public repositories](https://github.com/saltoricristiano?tab=repositories), and a title-based repository search. | No official public implementation repository or GIF linked from the checked sources. Static image retained. |

## Downloaded assets and verification

Both files were downloaded without modification from the official README references. First and middle frames were visually inspected; both show moving, paper-relevant LiDAR segmentation scenes.

| Local file | Original source | Dimensions | Frames / duration | File size |
| --- | --- | --- | --- | --- |
| `static/images/publications/cosmix.gif` | [Author's CoSMix GIF](https://user-images.githubusercontent.com/56728964/179716779-09e4b4bb-a7b3-4364-83ec-e876ca359adf.gif) | 550 × 309 | 139 / 5.56 seconds | 8,588,792 bytes |
| `static/images/publications/gipso.gif` | [Author's GIPSO GIF](https://user-images.githubusercontent.com/56728964/179717597-2af96b9e-208e-4bc6-9a8f-fbc954cef681.gif) | 800 × 175 | 146 / 5.84 seconds | 9,114,669 bytes |

Validation checked the `GIF89a` signature, logical screen dimensions, complete GIF block structure, image-frame counts, frame delays, and terminating trailer. FFmpeg successfully decoded representative frames.

## Audit scope and future updates

Ten distinct public repositories were inspected. GitHub recursive tree responses were complete (`truncated: false`). All reported branches were checked: `main` for most repositories, both `master`/`main` for CluRender and SoftClu, and `main`/`pages` for LiDOG. README links were checked because GitHub-hosted GIF attachments do not appear in repository trees.

“No GIF found” means none was found in those public branches, README links, and relevant linked project pages at the audit date. It does not claim that no private, unreleased, historical, or otherwise unlinked animation exists. The site keeps static figures when a suitable author-provided GIF could not be verified.

To add a newly released animation, download the relevant author-provided GIF to `static/images/publications/`, retain the publication's existing `image` and `image_alt`, and add `animation` plus `animation_alt` to its frontmatter. Update the row above with the source and verification date.
