# -*- coding: utf-8 -*-
"""Long-tail guide pages under /guides/.  Every factual line cites a source from guide_data.SOURCES.
Numbers on these pages come from (a) the cited official pages or (b) pages/data already in the repo."""
import html, json, re

SITE = "https://pcsvector.com"
TODAY = "2026-10-28"
E = lambda s, q=False: html.escape(s, quote=q)

def _style(read):
    h = read("bah/fort-drum/index.html")
    return re.search(r"<style>.*?</style>", h, flags=re.S).group(0)

def shell(read, slug, title, desc, h1, kick, body, crumbs, faq=None):
    url = "%s/guides/%s/" % (SITE, slug) if slug else "%s/guides/" % SITE
    ld = [{"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": url, "dateModified": TODAY},
          {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    ldh = "".join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)
    crumb_html = " › ".join('<a href="%s">%s</a>' % (u, E(n)) for n, u in crumbs[:-1]) + " › " + E(crumbs[-1][0])
    og = SITE + "/assets/og-card-2026-10-21.png"
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48"><link rel="icon" href="/favicon-192x192.png" type="image/png" sizes="192x192"><link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180"><meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>%(t)s</title>\n<meta name="description" content="%(d)s">\n<link rel="canonical" href="%(u)s">\n'
        '<meta property="og:type" content="article"><meta property="og:site_name" content="PCS Vector">\n'
        '<meta property="og:title" content="%(ot)s">\n<meta property="og:description" content="%(d)s">\n<meta property="og:url" content="%(u)s">\n'
        '<meta property="og:image" content="%(og)s">\n<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
        '<meta property="og:image:alt" content="PCS Vector — Know your BAH before you PCS — free, 2026 rates">\n'
        '<meta name="twitter:card" content="summary_large_image">\n<meta name="twitter:title" content="%(ot)s">\n<meta name="twitter:description" content="%(d)s">\n<meta name="twitter:image" content="%(og)s">\n'
        '%(style)s\n%(ld)s<script data-goatcounter="https://pcsvector.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>\n'
        '</head><body><main>\n<nav class="crumb">%(crumb)s</nav>\n<div class="kick">%(kick)s</div>\n<h1>%(h1)s</h1>\n%(body)s\n'
        '<p class="src">For Soldiers; By Soldiers. PCS Vector is an independent planning tool. It is not an official government site (not DoW, DTMO or any military service). Confirm your entitlements with your finance office. Page updated 28 Oct 2026.</p>\n</main></body></html>\n') % dict(
        t=E(title), ot=E(title.replace(" | PCS Vector", ""), True), d=E(desc, True), u=url, og=og, style=_style(read), ld=ldh, crumb=crumb_html, kick=E(kick), h1=E(h1), body=body)

def cite(GD, keys):
    out = []
    for k in keys:
        t, u = GD.SOURCES[k]
        out.append('<a href="%s" rel="noopener">%s</a>' % (E(u, True), E(t)))
    return ' <span class="note">(%s)</span>' % "; ".join(out) if out else ""

def li(GD, items, mark=""):
    return "".join("<li>%s%s%s</li>" % (mark, E(t), cite(GD, k)) for t, k in items)

def src_list(GD, keys):
    seen = []
    for k in keys:
        if k not in seen: seen.append(k)
    return ('<p class="src"><strong>Sources (read %s):</strong></p><ul class="note">%s</ul>' % (GD.AS_OF_HUMAN, "".join(
        '<li><a href="%s" rel="noopener">%s</a></li>' % (E(GD.SOURCES[k][1], True), E(GD.SOURCES[k][0])) for k in seen)))

def faq_html(faq):
    return "<h2>Quick answers</h2>" + "".join("<h3>%s</h3><p>%s</p>" % (E(q), E(a)) for q, a in faq)

def cta(slug, text):
    return '<a class="cta" href="/?utm_source=guide&amp;utm_medium=organic&amp;utm_campaign=%s">%s →</a>' % (slug, E(text))

def used(items_lists):
    ks = []
    for items in items_lists:
        for it in items:
            for k in it[1]:
                if k not in ks: ks.append(k)
    return ks

# ------------------------------------------------------------------------------------------ pages
def pages(NAMES, GUIDE_LINKS, OHA_LINKS, read, GD):
    P = {}
    CR = [("PCS Vector", "/"), ("Guides", "/guides/")]

    # ---- 1. How OHA works
    ko = read("oha/korea/index.html")
    m = re.search(r"rent ceiling of \$([\d,\.]+) \(₩([\d,]+)\) for a Sergeant \(E-5\) with dependents", ko)
    usd, krw = float(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
    rate = float(re.search(r"1 USD = ([\d,\.]+) KRW", ko).group(1).replace(",", ""))
    assert abs(krw / rate - usd) < 0.05, (krw, rate, usd)
    rows = [(1250.0, "stronger won (hypothetical)"), (rate, "rate DTMO used for 16 Oct 2026"), (1350.0, "weaker won (hypothetical)")]
    tbl = '<div class="tw"><table><thead><tr><th>Exchange rate (KRW per USD)</th><th>What it represents</th><th>Rent ceiling in USD</th></tr></thead><tbody>%s</tbody></table></div>' % "".join(
        "<tr><td>%s</td><td>%s</td><td>$%s</td></tr>" % ("{:,.2f}".format(r), E(w), "{:,.2f}".format(krw / r)) for r, w in rows)
    oha_items = {
     "parts": [("OHA is a cost-reimbursement allowance for members assigned to permanent duty overseas who lease privately owned housing. It has three components: rent, utilities/recurring maintenance, and a move-in housing allowance (MIHA).", ["dtmo_oha"])],
     "rent": [("Rental allowances are computed from actual rent payments reported through local finance systems. The maximum is set so that 80 percent of members with dependents have their rent fully reimbursed, so some members pay part of the rent themselves.", ["dtmo_oha"]),
              ("All members are reimbursed for rent up to the amount of the lease or the allowance, whichever is less. Members without dependents are entitled to 90 percent of the with-dependents rate.", ["dtmo_oha"]),
              ("Bavaria’s garrison puts it the same way for its members: you receive OHA based on your rent or the rank-based rent cap, whichever is less.", ["bav_rental"])],
     "util": [("The monthly utility/recurring maintenance allowance covers utilities paid directly to utility companies plus recurring maintenance and minor repairs. It is set to cover the 80th percentile of costs reported by members who pay their own utility bills.", ["dtmo_oha"]),
              ("If your landlord pays the utilities you do not receive this allowance; it is added to your rent allowance instead. Members without dependents who pay their own utilities get 75 percent of the with-dependents rate.", ["dtmo_oha"])],
     "miha": [("MIHA/Miscellaneous is an up-front lump sum for items that make a dwelling habitable (DTMO’s examples: transformers, supplemental heating equipment, wardrobes, electricity connection), paid with your first OHA rent payment to members with and without dependents.", ["dtmo_oha"]),
              ("MIHA/Rent is a dollar-for-dollar reimbursement of reasonable fixed, one-time, nonrefundable charges the landlord or a foreign government imposes before or when you occupy the home. Refundable deposits, advance rent and recurring costs are not included, and homeowners are ineligible.", ["dtmo_oha"]),
              ("Other components: MIHA/Security, MIHA/Infectious Disease and MIHA/Safety apply only in locations DTMO designates for them.", ["dtmo_oha"])],
     "apply": [("You apply by completing DD Form 2367 (Individual OHA Report) and returning it with a copy of your lease to the appropriate official; MIHA claims use DD Form 2556.", ["dtmo_oha"]),
               ("Authorization to live off post comes first and is decided locally. Korea, Japan and Germany garrisons each publish their own rules; see the housing-office sections on the Korea, Japan and Germany OHA pages.", ["hum_sheet","zama_move","bav_rental"])],
     "unique": [("OHA Unique Expenses reimburse excessive housing costs that a CONUS-based member does not normally have, with receipts, in listed locations. DTMO’s table lists France (mandatory habitation tax) and Denmark (refurbishing quarters on departure).", ["dtmo_oha"])],
    }
    faq1 = [
     ("Does OHA cover all of my rent overseas?", "Not always. DTMO sets the maximum rent allowance so that 80 percent of members with dependents have rent fully reimbursed, and you are reimbursed up to the lease amount or the allowance, whichever is less. Some members pay part of the rent."),
     ("Why did my OHA change when my rent did not?", "OHA is paid in U.S. dollars but rent is typically paid in foreign currency, so the dollar amount changes with the exchange rate even if the local-currency rent is the same. DTMO updates rates on a pay-period schedule."),
     ("What is MIHA?", "The Move-In Housing Allowance partially covers move-in costs for a privately leased home. The miscellaneous part is a lump sum paid with the first rent payment, and the rent part reimburses reasonable one-time nonrefundable charges."),
     ("Do I get OHA if I live in government housing overseas?", "OHA applies to members authorized to lease privately owned housing. Garrisons such as Camp Zama assign military personnel to government housing and allow off-post living only with an exception to policy, so check with the housing office before you plan around the table."),
    ]
    body = ('<p>The Overseas Housing Allowance (OHA) replaces BAH when you are authorized to rent off post overseas. The formula is different from BAH, and so are the traps: the amount moves with exchange rates, and the rules about who may rent off post depend on the garrison. This guide explains how DTMO builds OHA, and ties it to the 2026 tables on our <a href="/oha/korea/">Korea</a>, <a href="/oha/japan/">Japan</a>, <a href="/oha/okinawa/">Okinawa</a> and <a href="/oha/germany/">Germany</a> pages.%s</p>' % cite(GD, ["dtmo_oha"])
        + cta("how-oha-works", "Run your OHA numbers in the free calculator")
        + "<h2>The three parts of OHA</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["parts"])
        + "<h2>Rent: a ceiling, not a flat payment</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["rent"])
        + "<h2>Utilities and recurring maintenance</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["util"])
        + "<h2>Move-in housing allowance (MIHA)</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["miha"])
        + "<h2>Why the dollar amount moves: a worked example</h2>"
        + "<p>The Camp Humphreys rent ceiling for a Sergeant (E-5) with dependents is ₩%s on our Korea page, which DTMO converted to $%s at %s KRW per dollar for the pay period starting 16 Oct 2026. The table below is simple division on that same won ceiling. The other two rates are made-up illustrations of what a different exchange rate would do, not forecasts.%s</p>" % ("{:,}".format(krw), "{:,.2f}".format(usd), "{:,.2f}".format(rate), cite(GD, ["dtmo_oha"]))
        + tbl
        + "<p class=\"note\">If your actual rent is at or above the ceiling, your dollar reimbursement moves with the rate. If your rent is below the ceiling you are reimbursed your actual rent, converted at the rate finance uses.</p>"
        + "<h2>Applying for OHA</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["apply"])
        + "<h2>OHA unique expenses</h2><ul class=\"feat\">%s</ul>" % li(GD, oha_items["unique"])
        + "<h2>See the 2026 rates</h2><ul class=\"bases\">%s<li><a href=\"/oha/\">OHA by country</a></li></ul>" % "".join('<li><a href="%s">%s</a></li>' % (u, E(l)) for u, l in OHA_LINKS)
        + faq_html(faq1)
        + src_list(GD, ["dtmo_oha"] + used(oha_items.values())))
    P["guides/how-oha-works-overseas-pcs/index.html"] = shell(read, "how-oha-works-overseas-pcs",
        "How OHA Works for an Overseas PCS (2026): Rent, Utilities, MIHA | PCS Vector",
        "How the Overseas Housing Allowance is built: rent ceiling, utility allowance, move-in allowance, exchange-rate swings and the DD 2367 steps, cited to DTMO.",
        "How OHA works for an overseas PCS", "PCS Vector · guide", body, CR + [("How OHA works", "/guides/how-oha-works-overseas-pcs/")], faq1)

    # ---- 2. PCS cost checklist
    reimb = [
     ("Dislocation allowance (DLA) partially reimburses household-moving expenses for a PCS. You typically qualify if you move your household on PCS orders and are not assigned to single-type government housing such as barracks; most members receive only one DLA per fiscal year.", ["mos_dla"]),
     ("DLA amount depends on pay grade and dependency status; DTMO publishes the rates. File at your installation finance office.", ["mos_dla"]),
     ("You can request a DLA advance at your former installation’s finance office 10 to 15 days before the move. If approved you get 80% of the estimated payment in advance and the rest after you file at the new installation; approval is not guaranteed.", ["mos_dla"]),
     ("Temporary Lodging Expense (TLE) partially reimburses lodging and meals in temporary lodging inside CONUS during a PCS. You cannot receive both TLE and PCS per diem on the same day. Ask your local pay office.", ["mos_tle"]),
    ]
    upfront = [
     ("Security deposit. Fort Sill’s page says deposits vary and often equal one month’s rent; Fort Campbell’s says usually one month’s rent or less, or none, and that it is not an advance on your last month’s rent.", ["sill_mi","campbell_mi"]),
     ("Application and credit-check fees. Fort Campbell’s housing office warns these add up if you are denied; Fort Hood’s says local agencies require non-refundable administrative and rental/credit-history fees.", ["campbell_mi","hood_mi"]),
     ("Pet deposit. Fort Hood: non-refundable. Fort Drum: expect security deposit, first month’s rent and a pet deposit with a typical 12-month lease.", ["hood_mi","drum_mi"]),
     ("First month’s rent. In Korea, the Humphreys booklet says in most cases the landlord requires at least the first month’s rent along with a security deposit unless negotiated; get a receipt.", ["hum_hso"]),
     ("Renters insurance. Fort Sill, JBSA and the Korea housing offices recommend it, because the owner’s policy does not cover your belongings.", ["sill_mi","jbsa_mi","yc_mi"]),
     ("Utility deposits and connection: Military OneSource’s installation pages point to InMyArea.com to compare providers by ZIP code.", ["campbell_mi","jbsa_mi"]),
    ]
    saving = [
     ("Fort Campbell’s Rental Partnership Program aims to reduce the initial cost of renting through reduced or waived deposits, discounted rent and lower application fees; it requires a military allotment.", ["campbell_mi"]),
     ("Fort Riley’s Army Housing Office may be able to help get a deposit waived, depending on the property owner.", ["riley_mi"]),
    ]
    housing_pay = [
     ("BAH is not meant to cover every housing cost; DTMO says out-of-pocket costs can be higher or lower than the rate depending on the home you choose, and that rental prices generally change 2% to 5% a year.", ["dtmo_bah"]),
     ("Rate protection: a PCS ends your old rate protection. At the new station you receive any published increase but no decrease while your status stays the same.", ["dtmo_bah"]),
    ]
    overseas = [
     ("Overseas you also have MIHA (a lump sum with the first OHA payment plus reimbursement of reasonable one-time landlord charges). Bavaria’s garrison says army members may request an advance housing allowance for the first month’s rent and security deposit, which it says typically equals two months’ rent.", ["dtmo_oha","bav_rental"]),
     ("At Camp Humphreys an advance of rent or security deposit uses DA Form 4187 signed by the company commander, hand-carried to finance with a copy of the DD 2367.", ["hum_hso"]),
     ("Temporary lodging allowance (TLA) is approved by the housing office and processed by finance; Humphreys says it stops on the effective lease start date.", ["yc_mi","hum_steps"]),
    ]
    faq2 = [
     ("Do I get a security deposit back after a PCS?", "It depends on the lease. Fort Campbell’s housing office says a deposit may cover damage above normal wear and tear or unpaid rent, and that if the rental is in good shape and no rent is due you should ask for it back; it is not an advance on your last month’s rent."),
     ("Can I get my DLA before I move?", "You can request an advance 10 to 15 days before the move at your installation finance office. If approved you receive 80% of your estimated payment up front and the rest after you file at the new installation, but an advance is not guaranteed."),
     ("Does BAH cover everything about renting near a new post?", "No. DTMO says BAH is not intended to cover all of a member’s housing costs, so budget deposits, fees and utilities separately. The BAH pages on this site compare each post’s rate to planning estimates for rent and utilities."),
    ]
    body = ('<p>A PCS has two cash-flow problems: money that comes back later, and money you hand over first. This checklist separates them, with a cited source page (DTMO, Military OneSource or the installation) behind every line. Where a number depends on your rank, check the BAH page for your new post.</p>'
        + cta("pcs-cost-checklist", "See what BAH looks like against rent at your new post")
        + "<h2>Reimbursements and allowances to claim</h2><ul class=\"feat\">%s</ul>" % li(GD, reimb, "☐ ")
        + "<h2>Costs you front before the first BAH check</h2><ul class=\"feat\">%s</ul>" % li(GD, upfront, "☐ ")
        + "<h2>Ways to cut the up-front bill</h2><ul class=\"feat\">%s</ul>" % li(GD, saving, "☐ ")
        + "<h2>How the housing allowance changes with the PCS</h2><ul class=\"feat\">%s</ul>" % li(GD, housing_pay, "☐ ")
        + "<h2>If the move is overseas</h2><ul class=\"feat\">%s</ul>" % li(GD, overseas, "☐ ")
        + "<h2>Installation guides with local housing-office rules</h2><ul class=\"bases\">%s</ul>" % "".join('<li><a href="/bah/%s/#pcs-guide">%s</a></li>' % (s, E(NAMES[s].split(" (")[0])) for s in ["fort-hood","fort-campbell","fort-sill","fort-drum","fort-riley","fort-bragg","fort-bliss","joint-base-san-antonio","national-capital-region"])
        + faq_html(faq2)
        + src_list(GD, used([reimb, upfront, saving, housing_pay, overseas])))
    P["guides/pcs-cost-checklist/index.html"] = shell(read, "pcs-cost-checklist",
        "PCS Cost Checklist: Deposits, DLA, TLE and Housing Start-Up Costs | PCS Vector",
        "A cited PCS cost checklist: what DLA and TLE reimburse, which deposits and fees you front, and how BAH rate protection changes when you PCS.",
        "PCS cost checklist: what you pay up front and what comes back", "PCS Vector · guide", body, CR + [("PCS cost checklist", "/guides/pcs-cost-checklist/")], faq2)

    # ---- 3. Break a lease
    scra = [
     ("The SCRA lets a servicemember end a residential lease after receiving PCS orders, or deployment orders for at least 90 days. The lease must be signed by someone who later enters service, or by someone in service who later gets PCS or deployment orders. Separation or retirement orders also qualify.", ["doj_scra"]),
     ("How: give the landlord written notice and a copy of your orders (or a letter from your commanding officer). DOJ says the notice may be sent electronically as well as by mail or hand delivery.", ["doj_scra"]),
     ("When it ends: if you pay rent monthly, the lease terminates 30 days after the next rent payment is due once you have given proper notice and orders. That is not the same as 30 days from the day you send the notice.", ["doj_scra"]),
     ("DOJ’s position: requiring a servicemember to repay rent concessions or discounts is an early-termination fee that violates the SCRA, and mileage requirements in a lease are likely unenforceable because the SCRA has no minimum distance to the new station.", ["doj_scra"]),
     ("Waivers: the SCRA allows a waiver only as a separate instrument, during or after the relevant service period, in at least 12-point type. DOJ says waivers are invalid if they are lease addenda signed with the lease and give you nothing in return.", ["doj_scra"]),
    ]
    local = [
     ("Fort Drum: most landlords require a one-year lease, so insist on a military clause and have the Housing Services Office or Legal Assistance Office review it before you sign.", ["drum_mi"]),
     ("Fort Hood: make sure the lease contains the SCRA clause, and complete and keep a signed move-in inspection checklist to avoid repair or penalty charges when you leave. (Fort Hood’s page describes the clause as covering orders away for more than 90 days; DOJ’s summary above is the legal source, so ask a legal assistance office how it applies to you.)", ["hood_mi","doj_scra"]),
     ("Fort Riley: accepting on-post housing is not, by itself, justification to break a lease. If you hold deployment orders, call the Off Post Housing Division for help with the process.", ["riley_mi"]),
     ("Camp Humphreys: the garrison housing booklet says the lease will contain a military clause and that the service member or DA civilian gives 30 days’ written notice on receipt of orders or an offer of government quarters. The DOJ summary above does not list an offer of quarters as an SCRA ground, so treat that line as the garrison’s own guidance and confirm it with the legal assistance office.", ["hum_hso","doj_scra"]),
     ("Germany: the Wiesbaden briefing says verbal agreements with a landlord or agent are binding and that termination needs written notice with a 3-month period, so read the termination terms before you sign.", ["wies_brief"]),
    ]
    faq3 = [
     ("Does 30 days’ notice start the day I send it?", "No. For a monthly lease, DOJ says the lease ends 30 days after the next rent payment is due following delivery of your notice and a copy of your orders."),
     ("Can a landlord charge an early-termination fee when I PCS?", "DOJ’s position is that a covered servicemember who properly terminates under the SCRA may not be charged an early-termination fee, and that requiring repayment of rent concessions or discounts is such a fee. Ask your legal assistance office if a landlord pushes back."),
     ("Can I end a lease if I take on-post housing?", "Not automatically. Fort Riley’s housing information says accepting on-post housing is not justification to break a lease or rental agreement, and the DOJ summary lists orders (PCS, deployment of 90 days or more, separation or retirement), not a housing offer. Garrisons differ: the Camp Humphreys booklet lists an offer of government quarters as a reason for notice, so ask your legal assistance office about your lease."),
    ]
    body = ('<p>If your orders say you are leaving, your rental lease does not have to follow you. This guide summarizes the federal rule from the Department of Justice and the notes housing offices give new arrivals. It is general information, not legal advice; your installation’s legal assistance office is the place to ask how it applies to your lease.%s</p>' % cite(GD, ["doj_scra"])
        + "<h2>What the SCRA says about residential leases</h2><ul class=\"feat\">%s</ul>" % li(GD, scra, "")
        + "<h2>What installation offices add</h2><ul class=\"feat\">%s</ul>" % li(GD, local, "")
        + "<h2>Steps in order</h2><ol class=\"feat\"><li>Get a copy of your PCS orders (or a commander’s letter).</li><li>Write a short termination notice naming the lease, the address and the effective date you are asking for; keep a dated copy.</li><li>Deliver it to the landlord or agent by a method you can prove (mail, hand delivery or email if the landlord accepts it).</li><li>Calculate the end date: 30 days after the next rent due date after delivery, for monthly rent.</li><li>Do a move-out inspection with the landlord and keep photos of the condition you leave the home in.</li></ol>"
        + '<p class="note">The steps are a plain-language outline of the DOJ summary above, not a legal template.</p>'
        + cta("break-a-lease", "Compare your new post’s BAH with its rent")
        + faq_html(faq3)
        + src_list(GD, used([scra, local])))
    P["guides/break-a-lease-for-pcs-orders/index.html"] = shell(read, "break-a-lease-for-pcs-orders",
        "Breaking a Lease for PCS Orders: SCRA Notice Rules | PCS Vector",
        "How the SCRA lets you end a residential lease for PCS orders: the notice, the 30-day rule, early-termination fees and what installation housing offices add.",
        "Breaking a lease for PCS orders", "PCS Vector · guide", body, CR + [("Break a lease for PCS orders", "/guides/break-a-lease-for-pcs-orders/")], faq3)

    # ---- 4. BAH 2027 and PCS
    yoy = []
    for slug in NAMES:
        h = read("bah/%s/index.html" % slug)
        m2 = re.search(r"A Sergeant \(E-5\) with dependents gets (\$[\d,]+) in 2026, vs (\$[\d,]+) in 2025 \(([^/]+)/month, ([^)]+)\)", h)
        if m2: yoy.append((NAMES[slug].split(" (")[0], m2.group(2), m2.group(1), m2.group(3), m2.group(4)))
    yoy_tbl = '<div class="tw"><table><thead><tr><th>Post</th><th>E-5 w/ dep. 2025</th><th>E-5 w/ dep. 2026</th><th>Change</th><th>Percent</th></tr></thead><tbody>%s</tbody></table></div>' % "".join(
        "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % tuple(E(x) for x in r) for r in yoy)
    know = [
     ("BAH rates are set per calendar year. For 2026, coverage of the Defense Department’s 11 Dec 2025 release says new rates averaged a 4.2 percent increase (versus 5.4 percent in 2025) and took effect 1 Jan 2026, with increases varying by location.", ["asf_bah26"]),
     ("The same coverage says members who kept BAH eligibility in places where rates fell were not cut, because rate protection exists so members with long-term commitments are not penalized.", ["asf_bah26","dtmo_bah"]),
     ("DTMO says rental prices generally change 2% to 5% from year to year and housing allowances typically change accordingly.", ["dtmo_bah"]),
     ("DTMO’s BAH page does not give a 2027 publication date. Based on last year’s release (mid-December), plan for new rates around then, and treat any 2027 figure you see before that as unofficial.", ["dtmo_bah","asf_bah26"]),
    ]
    pcs_rules = [
     ("Rate protection keeps you from receiving less than the previous year’s rate while your BAH status stays the same. It ends if your status changes through a PCS, a reduction in grade or a change in dependency status.", ["dtmo_bah"]),
     ("After you arrive at the new duty station, rate protection applies again: you get any published increase but no decrease while your status stays the same.", ["dtmo_bah"]),
     ("BAH distinguishes between with-dependents and without-dependents, not the number of dependents.", ["dtmo_bah"]),
    ]
    faq4 = [
     ("When are 2027 BAH rates published?", "DTMO has not published 2027 rates as of 28 Oct 2026. The 2026 rates were announced in a Defense Department release dated 11 Dec 2025 and took effect 1 Jan 2026, so plan for new rates in mid-December."),
     ("Will my BAH drop if rates fall at my post?", "Not if your status stays the same. DTMO’s individual rate protection means you receive the rate published on 1 January or what you received on 31 December, whichever is larger, until a PCS, reduction in grade or change in dependency status."),
     ("Which BAH do I use if I PCS right after 1 January?", "Use your new duty station’s published rate for the year it applies to, and check it against DTMO’s BAH calculator for your ZIP code. This site shows the 2026 rates until DTMO publishes 2027."),
    ]
    body = ('<p>If you are planning a PCS this winter, you will probably see headlines about 2027 BAH before you see the numbers. As of 28 Oct 2026 DTMO has not published 2027 rates, and PCS Vector shows no 2027 amounts. This guide covers what is known, what the rules say about a PCS, and how to use the 2026 pages as a baseline.%s</p>' % cite(GD, ["dtmo_bah"])
        + cta("bah-2027", "Compare 2026 BAH at two posts in the calculator")
        + "<h2>What we know about the next BAH release</h2><ul class=\"feat\">%s</ul>" % li(GD, know)
        + "<h2>What a PCS does to your rate</h2><ul class=\"feat\">%s</ul>" % li(GD, pcs_rules)
        + "<h2>How much 2026 moved at eight posts</h2><p>These are DTMO’s 2025 and 2026 rates for a Sergeant (E-5) with dependents, copied from our BAH pages for the posts where we have both years. They show the size of a typical yearly swing; they do not predict 2027.</p>" + yoy_tbl
        + "<p class=\"note\">Source for the table: DTMO BAH Rate Lookup figures on each post’s page (checked 19 Oct 2026). Each linked page lists every pay grade.</p>"
        + "<ul class=\"bases\">%s</ul>" % "".join('<li><a href="/bah/%s/">%s</a></li>' % (s, E(NAMES[s].split(" (")[0])) for s in NAMES if any(NAMES[s].split(" (")[0] == r[0] for r in yoy))
        + "<h2>Using the 2026 pages as a baseline</h2><p>Look up your new post, note the E-5, E-6 or O-3 figure for your grade, then compare it with the planning rent range on that page. When DTMO publishes, the new numbers replace these, but the gap between BAH and local rent changes by far less than the rate on its own does, because rents move as well. See the <a href=\"/guides/pcs-cost-checklist/\">PCS cost checklist</a> for the one-time costs that BAH does not touch.</p>"
        + faq_html(faq4)
        + src_list(GD, ["dtmo_bah", "asf_bah26"]))
    P["guides/bah-2027-pcs/index.html"] = shell(read, "bah-2027-pcs",
        "BAH 2027: When Rates Are Published and What a PCS Does to Your Rate | PCS Vector",
        "No 2027 BAH rates exist yet. What DTMO and last year’s release tell us, how rate protection works at a PCS, and how 2026 moved at eight posts.",
        "BAH 2027 and your PCS: what we know", "PCS Vector · guide", body, CR + [("BAH 2027 and your PCS", "/guides/bah-2027-pcs/")], faq4)

    # ---- 5. Hub
    hub_items = [
     ("/guides/pcs-cost-checklist/", "PCS cost checklist", "What DLA and TLE reimburse, which deposits and fees you front, and where rate protection starts over."),
     ("/guides/break-a-lease-for-pcs-orders/", "Breaking a lease for PCS orders", "The SCRA notice rule, the 30-day timing and what installation housing offices add."),
     ("/guides/bah-2027-pcs/", "BAH 2027 and your PCS", "What is known before DTMO publishes 2027 rates, and how 2026 moved at eight posts."),
     ("/guides/how-oha-works-overseas-pcs/", "How OHA works for an overseas PCS", "Rent ceiling, utility allowance, MIHA and why the dollar amount moves with exchange rates."),
    ]
    inst = ["fort-hood","fort-campbell","fort-sill","fort-drum","fort-riley","fort-bragg","fort-bliss","joint-base-san-antonio","national-capital-region"]
    body = ("<p>Plain-language PCS guides built on official sources, each with the source and the date it was read. For rates by post, use the BAH and OHA pages; for the rules around them, start here.</p>"
        + "<h2>PCS guides</h2><ul class=\"feat\">%s</ul>" % "".join('<li><a href="%s"><strong>%s</strong></a> — %s</li>' % (u, E(t), E(d)) for u, t, d in hub_items)
        + "<h2>Installation guides (BAH posts)</h2><p>Each page below has a PCS checklist, housing options and area notes from the installation’s own housing pages.</p><ul class=\"bases\">%s</ul>" % "".join('<li><a href="/bah/%s/#pcs-guide">%s</a></li>' % (s, E(NAMES[s].split(" (")[0])) for s in inst)
        + "<h2>Overseas (OHA)</h2><p>Housing-office rules for living off post overseas.</p><ul class=\"bases\">%s</ul>" % "".join('<li><a href="%s#pcs-guide">%s</a></li>' % (u, E(l)) for u, l in OHA_LINKS[:2] + OHA_LINKS[3:])
        + '<h2>Everything else</h2><ul class="bases"><li><a href="/bah/">BAH by post (27 pages)</a></li><li><a href="/oha/">OHA by country</a></li><li><a href="/">Free PCS calculator</a></li></ul>')
    P["guides/index.html"] = shell(read, None, "PCS Guides: Costs, Leases, BAH and OHA Rules | PCS Vector",
        "PCS Vector guides: cost checklist, breaking a lease for orders, BAH 2027 and OHA basics, plus installation housing-office checklists for major posts.",
        "PCS guides", "PCS Vector · guides", body, [("PCS Vector", "/"), ("Guides", "/guides/")])
    return P
