def build_site(dist, origin, public_build):
    # Generate the general research archive index; no Baniyas chronology page is published.
    for lang in LANGS:
        u = UI[lang]
        shell_page(dist,lang,ARCHIVE_ROUTE,u["archive_title"],u["archive_desc"],archive_index_html(lang),public_build)
    # Preserve the root-level research archive alias; its canonical points to /en/.
    route = ARCHIVE_ROUTE
    source = dist / "en" / route.strip("/") / "index.html"
    target = dist / route.strip("/") / "index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"),encoding="utf-8")
    enrich_existing_pages(dist,public_build)
    write_root_gateway(dist,public_build)
    css = dist / "style.css"
    extra = """
/* Knowledge archive and encyclopedic record layout */
.archive-lead{font-size:1.12rem;max-width:55rem;margin-block:1rem 1.6rem!important}
.archive-card{grid-template-columns:9rem 1fr}
.archive-card h2{font-size:1.35rem;margin:0 0 .25rem}
.archive-infobox{border:1px solid var(--line);padding:1rem 1.2rem;margin:1.5rem 0;max-width:34rem;background:var(--surface)}
.archive-infobox h2{font-size:1.35rem}
.archive-infobox dl{display:grid;grid-template-columns:minmax(7rem,9rem) 1fr;gap:.35rem .8rem;margin:.5rem 0 0}
.archive-infobox dt{font-weight:650;color:var(--muted)}
.archive-infobox dd{margin:0}
.timeline{border-inline-start:2px solid var(--line);margin:1.2rem 0 1.5rem;padding-inline-start:1.1rem}
.timeline-entry{display:grid;grid-template-columns:minmax(8rem,10rem) 1fr;gap:1rem;padding:1rem 0;border-bottom:1px solid var(--line)}
.timeline-date{font-weight:700;color:var(--red)}
.timeline-entry h3{font:600 1.2rem/1.4 var(--serif);margin:0 0 .4rem}
.timeline-entry p{margin:.3rem 0}
.source-basis{font-size:.85rem;color:var(--muted);font-weight:650}
.citation{font-size:.78em;vertical-align:super;margin-inline-start:.12rem}
.citation a{text-decoration:none;color:var(--red)}
.references{padding-inline-start:1.7rem}
.references li{padding:.35rem 0;border-bottom:1px solid var(--line);overflow-wrap:anywhere}
.ref-number{font-weight:700;color:var(--red);margin-inline-end:.3rem}
.gateway{display:grid;grid-template-columns:minmax(10rem,17rem) minmax(0,1fr);gap:2.5rem;align-items:center;padding:3rem 0}
.gateway figure img{width:100%;height:auto;border-radius:.5rem}
.gateway h1{font-size:clamp(3rem,8vw,5.5rem)}
.gateway-desc{color:var(--muted);font-size:1.1rem;max-width:38rem}
.language-choices{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.8rem;margin-top:1rem}
.language-choice{border:1px solid var(--line);padding:1rem;text-decoration:none;display:flex;flex-direction:column;gap:.35rem;border-radius:.45rem}
.language-choice:hover{border-color:var(--red);color:var(--red)}
.language-choice span{font-size:.9rem;color:var(--muted)}
.toc,.profile-toc{border:1px solid var(--line);padding:1rem 1.25rem;margin:1.5rem 0;max-width:32rem;background:var(--surface)}
.toc h2,.profile-toc h2{font-size:1.35rem;margin:0 0 .45rem}
.toc ol,.profile-toc ol{margin:.25rem 0;padding-inline-start:1.4rem}
.toc li,.profile-toc li{padding:.15rem 0}
.profile-infobox{border:1px solid var(--line);padding:1rem 1.2rem;margin:1.5rem 0;max-width:36rem;background:var(--surface)}
.profile-infobox h2{font-size:1.35rem}
.profile-infobox dl{display:grid;grid-template-columns:minmax(7rem,9rem) 1fr;gap:.35rem .8rem;margin:.5rem 0 0}
.profile-infobox dt{font-weight:650;color:var(--muted)}
.profile-infobox dd{margin:0}
.profile-identifiers{border-top:1px solid var(--line);margin-top:2rem;padding-top:1rem}
.profile-identifiers ul{padding-inline-start:1.4rem}
@media(max-width:680px){.timeline-entry{grid-template-columns:1fr;gap:.25rem}.archive-infobox dl,.profile-infobox dl{grid-template-columns:1fr;gap:.1rem}.archive-infobox dd,.profile-infobox dd{margin-bottom:.55rem}.gateway{grid-template-columns:1fr;gap:1rem}.gateway figure{width:min(100%,12rem);margin-inline:auto}.language-choices{grid-template-columns:1fr}}
"""
    current = css.read_text(encoding="utf-8")
    if "Knowledge archive and encyclopedic record layout" not in current:
        css.write_text(current + "\n" + extra,encoding="utf-8")

def write_sitemap(dist, origin):
    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    xns = "http://www.w3.org/1999/xhtml"
    ET.register_namespace("",ns)
    ET.register_namespace("xhtml",xns)
    root = ET.Element(f"{{{ns}}}urlset")
    paths = set()
    for lang in LANGS:
        base = dist / lang
        for file in base.rglob("index.html"):
            route_parts = file.parent.relative_to(base).parts
            route = "/" + "/".join(route_parts) + "/" if route_parts else "/"
            paths.add(route)
    paths.add("/")
    for route in sorted(paths):
        # The root language selector is its own URL; each translated page also gets a URL entry.
        urls_for_route = [origin + "/"] if route == "/" else []
        urls_for_route.extend(origin + f"/{lang}" + route for lang in LANGS)
        for loc in urls_for_route:
            url_node = ET.SubElement(root,f"{{{ns}}}url")
            ET.SubElement(url_node,f"{{{ns}}}loc").text = loc
            for lang in LANGS:
                href = origin + f"/{lang}" + route
                ET.SubElement(url_node,f"{{{xns}}}link",{
                    "rel":"alternate","hreflang":lang,"href":href
                })
            ET.SubElement(url_node,f"{{{xns}}}link",{
                "rel":"alternate","hreflang":"x-default","href":origin+"/"
            })
    ET.ElementTree(root).write(dist/"sitemap.xml",encoding="utf-8",xml_declaration=True)

