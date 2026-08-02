
# THIRD-PARTY MODELS & LICENSES

This project integrates pretrained, open-source 2D-to-3D reconstruction models rather than training new ones — the project's own contribution is the Adaptive AI Decision Engine and orchestration layer built around them (see [`README.md`](./README.md)). The MIT License in this repository applies **only to code written by this team**. Each integrated model below is governed by its own original license, verified as of August 2026. **Always check the current LICENSE file in the model's official repository before use — license terms can and do change between versions.**

---

## TripoSR

- **Developer:** Stability AI & Tripo AI
- **Repository:** https://github.com/VAST-AI-Research/TripoSR
- **License:** MIT License
- **Commercial use:** Allowed — permissive license, allows commercial, personal, and research use with no revenue restrictions.
- **Notes:** Training data (a curated Objaverse subset) is separately licensed CC-BY; this only affects retraining, not use of the released pretrained weights.

---

## Wonder3D

- **Developer:** xxlong0 (research team, HKU-affiliated)
- **Repository:** https://github.com/xxlong0/Wonder3D
- **License:** ⚠️ **Conflicting information — verify before use.** The original repository README states the model is "under MIT license, free to use with acknowledgement." However, the newer **Wonder3D++** branch/version is explicitly licensed **AGPL-3.0**, which requires any downstream product or service (including cloud/web services) that incorporates Wonder3D code or trained weights to be open-sourced under AGPL terms.
- **Commercial use:** Depends entirely on which version/commit you pull. The original Wonder3D (MIT) is permissive; Wonder3D++ (AGPL-3.0) is strong copyleft and would require open-sourcing this entire platform if you build a hosted/commercial service on top of it.
- **Action required:** Before integration, the AI team must confirm which exact branch/commit is being used and pin it explicitly (not just "Wonder3D" — specify the commit hash), then update this entry to reflect the confirmed license. For an academic FYP kept as a public GitHub repo (not sold as a commercial service), either license is workable, but this distinction matters if the project is ever commercialized.

---

## Stable Fast 3D (SF3D)

- **Developer:** Stability AI
- **Repository:** https://github.com/Stability-AI/stable-fast-3d
- **License:** Stability AI Community License Agreement
- **Commercial use:** Free for research, non-commercial, and commercial use — **but only for individuals/organizations with under US $1,000,000 in annual revenue**. Above that threshold, a separate Stability AI Enterprise License is required.
- **Notes:** This is not a concern for a student FYP (well under the revenue threshold), but should be documented since it's a conditional license, not unconditional open-source.

---

## Hunyuan3D-2 / 2.1

- **Developer:** Tencent Hunyuan Team
- **Repository:** https://github.com/Tencent-Hunyuan/Hunyuan3D-2
- **License:** Tencent Hunyuan 3D Community License Agreement (custom license, not a standard OSI license)
- **Commercial use:** Permitted with restrictions, but **explicitly excludes the European Union, United Kingdom, and South Korea** from the license territory entirely — the model cannot be legally used in those regions under this agreement regardless of commercial/non-commercial status.
- **Notes:** There is public confusion (see Tencent-Hunyuan/Hunyuan3D-2 issue #254) between the repository's LICENSE file and some internal file headers referencing a "non-commercial" agreement — the authoritative version is the root `LICENSE` file in the repo. Since India is not in the excluded territory list, this model is usable for this project, but this exclusion is worth noting explicitly in case the project is ever deployed or demoed to an international audience.

---

## Summary Table

| Model | License | Commercial Use | Notable Restriction |
|---|---|---|---|
| TripoSR | MIT | Yes, unrestricted | None |
| Wonder3D | MIT *or* AGPL-3.0 (version-dependent) | Depends on version used | AGPL variant requires open-sourcing derivative services |
| Stable Fast 3D | Stability AI Community License | Yes, under $1M revenue | Enterprise license needed above $1M revenue |
| Hunyuan3D-2/2.1 | Tencent Hunyuan Community License | Yes, with restrictions | Excludes EU, UK, South Korea |

---

## Guidance for This Project

1. **For academic submission purposes** (non-commercial, university evaluation), all four models above are usable as-is.
2. **Pin exact versions/commits** for every integrated model in `ai/requirements.txt` or equivalent, and note the commit hash here — licenses on active research repos can change between commits, especially Wonder3D.
3. **If this project is ever extended toward a commercial product or public hosted service**, revisit this document first: Wonder3D's AGPL branch and Stable Fast 3D's revenue cap are the two terms most likely to become relevant.
4. **Attribution:** even permissively-licensed models (TripoSR, MIT-Wonder3D) expect acknowledgement — cite the original papers in your SRS/SDD References chapter and in this repository's README acknowledgements, not just in this file.

*Last verified: August 2026. Model licenses change — re-verify against each project's official repository before any submission, publication, or deployment.*
