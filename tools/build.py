#!/usr/bin/env python3
"""Build the static tutorial site from the page bodies in src/en and src/zh.

Usage (from the repository root):  python3 tools/build.py

Only the Python standard library is used. Each file in src/<lang>/<slug>.html holds the
content that goes inside <main>; this script adds the shared <head>, navigation, footer
and previous/next links, then writes <slug>.html (English) and zh/<slug>.html (Chinese).
Edit the files in src/, never the generated pages, then run the script again.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://seesaw-earth.github.io/RodentStudio-Tutorials/"
SUPPORT = "https://seesaw-earth.github.io/RodentStudio-Support/"
REPO = "https://github.com/seesaw-earth/RodentStudio-Tutorials"

# slug, nav label (en, zh), page title (en, zh), meta description (en, zh)
PAGES = [
    ("index", ("Overview", "概览"),
     ("How the RodentStudio models were built", "RodentStudio 的模型是怎么来的"),
     ("Bilingual tutorials on where the data behind RodentStudio's pose models came from, how the models were trained and tested, how they run on-device, and how to cite every source.",
      "中英双语教程：RodentStudio 姿态模型的数据从哪里来、模型如何训练和测试、如何在设备上运行，以及如何正确引用每一个来源。")),
    ("mousepose6", ("MousePose6", "MousePose6"),
     ("Tutorial 1: MousePose6 from four public datasets", "教程 1：用四个公开数据集训练 MousePose6"),
     ("How the six-keypoint top-view mouse pose model was built from ETH Zurich and JAX open-field datasets, trained with Ultralytics YOLO26 and evaluated.",
      "六关键点俯视小鼠姿态模型如何由 ETH Zurich 和 JAX 的公开数据集构建、用 Ultralytics YOLO26 训练并评估。")),
    ("cylinder-v2", ("Cylinder v2", "Cylinder v2"),
     ("Tutorial 2: Distilling DeepLabCut into CylinderMousePoseV2", "教程 2：把 DeepLabCut 蒸馏成 CylinderMousePoseV2"),
     ("How the seven-keypoint cylinder-test model was distilled from a lab DeepLabCut project with cleaned pseudo-labels and evaluated on held-out human labels.",
      "七关键点圆筒实验模型如何用清洗过的 DeepLabCut 伪标签蒸馏而来，并在留出的人工标注上评估。")),
    ("tst-detector", ("TST detector", "TST 检测器"),
     ("Tutorial 3: The tail-suspension mouse detector", "教程 3：悬尾实验小鼠检测器"),
     ("What is known about the bundled YOLO11n mouse detector for multi-chamber tail suspension, and which RodentStudio trackers use no neural network.",
      "内置 YOLO11n 多格悬尾小鼠检测器的已知信息，以及 RodentStudio 中哪些追踪方法不使用神经网络。")),
    ("app-integration", ("Into the app", "接入 App"),
     ("Tutorial 4: From a trained model to Core ML in the app", "教程 4：从训练好的模型到 App 里的 Core ML"),
     ("Exporting Ultralytics YOLO models to Core ML, inspecting the package, running it with Vision and decoding the output tensor in Swift, as RodentStudio does.",
      "按 RodentStudio 的做法：把 Ultralytics YOLO 导出为 Core ML、检查模型包、用 Vision 运行并在 Swift 中解码输出张量。")),
    ("citations", ("How to cite", "如何引用"),
     ("How to cite the datasets, papers and software", "如何引用数据集、论文和软件"),
     ("Reference list, BibTeX, licence summary and example methods text for the datasets, papers and software behind RodentStudio's models.",
      "RodentStudio 模型所用数据集、论文和软件的参考文献、BibTeX、许可汇总和方法部分示例文字。")),
]

UI = {
    "en": dict(lang="en", other="zh", other_label="中文", other_lang="zh-CN", skip="Skip to content",
               brand="RodentStudio Tutorials", support="Support site ↗", prev="Previous", next="Next",
               footer_note="Independent research software. Model outputs require scientific validation.",
               f_support="Support site", f_bib="references.bib", f_repo="Source on GitHub",
               f_legal="Legal &amp; notices", main_nav="Main navigation", suffix="RodentStudio Tutorials",
               copyright="© 2026 Ziqing Shi · Developer: Ziqing Shi"),
    "zh": dict(lang="zh-CN", other="en", other_label="English", other_lang="en", skip="跳到正文",
               brand="RodentStudio 教程", support="支持网站 ↗", prev="上一篇", next="下一篇",
               footer_note="独立科研软件。模型输出需要经过科学验证。",
               f_support="支持网站", f_bib="references.bib", f_repo="GitHub 源文件",
               f_legal="条款与声明", main_nav="主导航", suffix="RodentStudio 教程",
               copyright="© 2026 Ziqing Shi · 开发者：Ziqing Shi"),
}


def page_url(slug, lang):
    name = "" if slug == "index" else f"{slug}.html"
    return BASE + ("zh/" if lang == "zh" else "") + name


def render(i, lang):
    slug, nav, title, desc = PAGES[i]
    li = 1 if lang == "zh" else 0
    ui = UI[lang]
    up = "../" if lang == "zh" else ""
    other_href = (f"../{slug}.html" if lang == "zh" else f"zh/{slug}.html")
    support_href = SUPPORT + ("zh/" if lang == "zh" else "")
    body = (ROOT / "src" / lang / f"{slug}.html").read_text(encoding="utf-8")

    links = []
    for s, n, _, _ in PAGES:
        cur = ' aria-current="page"' if s == slug else ""
        links.append(f'<a href="{s}.html"{cur}>{n[li]}</a>')
    links.append(f'<a href="{support_href}">{ui["support"]}</a>')
    links.append(f'<a class="language" href="{other_href}" lang="{ui["other_lang"]}">{ui["other_label"]}</a>')

    pager = ""
    if "<!--PAGER-->" in body:
        parts = []
        if i > 0:
            p = PAGES[i - 1]
            parts.append(f'<a class="prev" href="{p[0]}.html"><small>← {ui["prev"]}</small>{p[2][li]}</a>')
        if i < len(PAGES) - 1:
            n_ = PAGES[i + 1]
            parts.append(f'<a class="next" href="{n_[0]}.html"><small>{ui["next"]} →</small>{n_[2][li]}</a>')
        pager = '<nav class="pager" aria-label="Pages">' + "".join(parts) + "</nav>"
        body = body.replace("<!--PAGER-->", pager)

    full_title = f"{title[li]} · {ui['suffix']}"
    head = (
        f'<!doctype html><html lang="{ui["lang"]}"><head><meta charset="utf-8">'
        f'<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<meta name="color-scheme" content="light">'
        f'<meta name="description" content="{escape(desc[li])}">'
        f'<meta name="theme-color" content="#e9f9f7">'
        f"<title>{escape(full_title)}</title>"
        f'<link rel="canonical" href="{page_url(slug, lang)}">'
        f'<link rel="alternate" hreflang="en" href="{page_url(slug, "en")}">'
        f'<link rel="alternate" hreflang="zh-CN" href="{page_url(slug, "zh")}">'
        f'<link rel="icon" href="{up}assets/favicon.png" type="image/png">'
        f'<link rel="stylesheet" href="{up}assets/styles.css">'
        f'<link rel="stylesheet" href="{up}assets/tutorial.css">'
        f'<meta property="og:type" content="article">'
        f'<meta property="og:title" content="{escape(full_title)}">'
        f'<meta property="og:description" content="{escape(desc[li])}">'
        f'<meta property="og:url" content="{page_url(slug, lang)}">'
        f'<meta property="og:image" content="{BASE}assets/app-icon.png">'
        "</head>"
    )
    header = (
        f'<body><a class="skip-link" href="#main">{ui["skip"]}</a>'
        f'<header class="nav-wrap"><nav class="nav shell" aria-label="{ui["main_nav"]}">'
        f'<a class="brand" href="index.html"><img src="{up}assets/app-icon.png" alt="" width="40" height="40"> {ui["brand"]}</a>'
        f'<div class="links">{"".join(links)}</div></nav></header>'
    )
    footer = (
        '<footer class="footer"><div class="shell footer-grid"><div>'
        f'<strong>{ui["brand"]}</strong>'
        f'<div><small>{ui["copyright"]}</small></div>'
        f'<div><small>{ui["footer_note"]}</small></div></div>'
        '<div class="footer-links">'
        f'<a href="{support_href}">{ui["f_support"]}</a>'
        f'<a href="{up}references.bib">{ui["f_bib"]}</a>'
        f'<a href="{REPO}">{ui["f_repo"]}</a>'
        f'<a href="{support_href}legal.html">{ui["f_legal"]}</a>'
        "</div></div></footer></body></html>\n"
    )
    return head + header + f'<main id="main">{body}</main>' + footer


def main():
    for i, (slug, *_rest) in enumerate(PAGES):
        for lang in ("en", "zh"):
            out = ROOT / ("zh" if lang == "zh" else "") / f"{slug}.html"
            out.parent.mkdir(exist_ok=True)
            out.write_text(render(i, lang), encoding="utf-8")
    urls = []
    for slug, *_rest in PAGES:
        for lang in ("en", "zh"):
            urls.append(
                f"<url><loc>{page_url(slug, lang)}</loc>"
                f'<xhtml:link rel="alternate" hreflang="en" href="{page_url(slug, "en")}"/>'
                f'<xhtml:link rel="alternate" hreflang="zh-CN" href="{page_url(slug, "zh")}"/></url>'
            )
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    print(f"Built {len(PAGES) * 2} pages and sitemap.xml")


if __name__ == "__main__":
    main()
