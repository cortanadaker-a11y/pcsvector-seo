# -*- coding: utf-8 -*-
"""Overseas guide blocks for /oha/korea/, /oha/japan/, /oha/germany/ (facts cited; read 28 Oct 2026).
The dollar figures on those pages come from DTMO data already in the repo; nothing numeric is
restated here except what a cited housing office page prints."""
OHA_GUIDES = {
 "korea": dict(
  title="Moving to Korea: housing-office rules before you sign",
  lead="OHA only pays if you are authorized to live off post, and in Korea that is decided by the garrison housing office, not by you or the landlord. These are the rules the housing offices themselves publish.",
  lead_src=["hum_sheet","yc_mi"],
  blocks=[
   ("Is off-post housing open to you?", [
     ("Camp Humphreys: the Housing Information Sheet (Oct 2024) says off-post housing is authorized only if the occupancy rate for government housing is above 95%, and that personnel on unaccompanied tours receiving the dependent-location BAH rate must live in available unaccompanied housing. The garrison’s housing page says about 40 percent of command-sponsored military families at Humphreys live on post.", ["hum_sheet","hum_dpw"]),
     ("Camp Casey and Camp Hovey: the USAG Yongsan-Casey page on Military OneSource states, “No Military Personnel will be authorized to live off post at CP Casey/Hovey, as UPH Quarters are available.” The Camp Casey OHA table on this page is shown for reference; confirm with the Casey housing office before you plan around it.", ["yc_mi"]),
   ]),
   ("Order of operations at Camp Humphreys", [
     ("Do not make lease arrangements without prior approval from the Housing Office. Attend the mandatory off-post housing briefing (Tuesday and Thursday at 1400 per the Oct 2024 sheet) before you deal with realtors, and bring your PCS orders and amendments.", ["hum_sheet"]),
     ("Use the USAG Humphreys Registered Realtor List. Every off-post home must pass a safety inspection by the Housing Office, which you can schedule through the realtor.", ["hum_steps","hum_sheet"]),
     ("Select housing within 15 days of arrival: the sheet says TLA can be terminated for failure to do so without a valid reason.", ["hum_sheet"]),
     ("Lease processing is by appointment only; the housing office warns that TLA or TQSA stops on the effective lease start date, and that after signing, changes or addenda need Housing Office approval.", ["hum_steps"]),
     ("Arrange government loaner furniture before household goods delivery; the sheet says to schedule the furniture pickup before arranging HHG delivery and that each member is entitled to one pickup during the tour.", ["hum_sheet","hum_steps"]),
   ]),
   ("Lease terms to check anywhere in Korea", [
     ("Bring the realtor or landlord to the housing office before signing so the unit’s fair market value is checked; the safety inspection must be done before the lease is signed.", ["yc_mi"]),
     ("Rent is paid in won while OHA is paid in dollars, and a move-in housing allowance (MIHA) is paid on signing the lease; you may also be eligible for dislocation allowance.", ["yc_mi","dtmo_oha"]),
     ("Give the landlord written notice at least 30 days before you terminate, and make sure all bills are paid before termination. A military clause protects you under the Servicemembers Civil Relief Act (30 days’ written notice after receiving orders, per the Humphreys HSO booklet).", ["yc_mi","hum_hso"]),
     ("Electricity is billed in tiers, so usage drives cost: Military OneSource says $1,000 a month for electricity alone is “not unreasonable” in summer if energy is not conserved, and members with negotiated utility caps should monitor usage. Compare that with the utility allowance in the table before you accept a lease without caps.", ["yc_mi"]),
     ("Apartment management fees (security, cleaning, elevators) are typically billed with electricity, water and oil; water off post is not potable for cooking or drinking.", ["yc_mi"]),
   ]),
  ],
 ),
 "japan": dict(
  title="Moving to Camp Zama: why OHA may not apply to you",
  lead="The OHA table below is DTMO’s rate for the locality. Whether you receive it at Camp Zama depends on a housing assignment policy that is stricter than most U.S. posts.",
  lead_src=["zama_move","zama_faq"],
  blocks=[
   ("Camp Zama housing policy", [
     ("USAG Japan states that family and unaccompanied housing in Japan is built by the Government of Japan under the SOFA and managed by the garrison, so military personnel are mandatorily assigned to family housing or unaccompanied housing.", ["zama_move"]),
     ("The Camp Zama housing FAQ says you can live off post only with an approved Exception to Policy (ETP), and that housing under the Mandatory On-Post Housing Assignment Policy is assigned to incoming members when available.", ["zama_faq"]),
     ("Military OneSource describes a different group: accompanied service members at E-7 and above assigned by orders to Sagami General Depot, Yokohama North Dock, NAF Atsugi and Akasaka Press Center (installations other than Camp Zama proper) may reside off post without an ETP, and unaccompanied officers and E-7 to E-9 reside off base unless in key and essential positions. The two pages are not worded the same way, so ask the Housing Office which applies to your orders.", ["zama_mi"]),
   ]),
   ("Order of operations", [
     ("Report to the Housing Office, Building 671, within 2 working days of arriving in Japan. Family housing applications use DD Form 1746 plus your orders and DA 31 or DA 137-2; no advance applications are accepted.", ["zama_move"]),
     ("Do not secure off-base housing before you arrive: the garrison says all off-post housing must be approved by the Housing Office to meet DoW suitability standards.", ["zama_move","zama_mi"]),
     ("The FAQ lists a typical wait for family housing of 30 to 60 days (subject to change) and says lodging is available meanwhile, but the garrison says an extension of a hotel stay because of a delayed housing assignment will not be authorized.", ["zama_faq","zama_move"]),
     ("If you are approved to live off post you receive OHA instead of BAH, and the dollar amount varies with the yen rate.", ["zama_faq"]),
   ]),
   ("What changes in the move", [
     ("Voltage in Japan is 100V at 50 Hz, so check appliances before shipping.", ["zama_move"]),
     ("Camp Zama is a weight-restricted area: the garrison says to ask your Transportation Office for your authorized allowance, and that furnishings that do not fit are stored at your expense. The Housing Office provides limited full-tour furniture, and Army Community Service has a lending closet for kitchen basics.", ["zama_move"]),
     ("This page also lists Yokota and Yokosuka rates from DTMO, but those installations’ off-post rules are not covered here; use their own housing offices.", []),
   ]),
  ],
 ),
 "germany": dict(
  title="Moving to Germany: do not sign anything before the housing brief",
  lead="Every garrison in Germany says the same thing in different words: attend the housing brief and in-process first, and have the housing office review the lease before you sign it. German rental law also makes verbal agreements binding.",
  lead_src=["wies_off","bav_rental"],
  blocks=[
   ("Who can live off post", [
     ("USAG Bavaria states the Army in Europe assignment policy: service members on PCS orders are mandatorily assigned to government housing to maintain optimum occupancy.", ["bav_rental"]),
     ("USAG Rheinland-Pfalz (Kaiserslautern, Baumholder) says Soldiers of all ranks are required to live on post until a 95% occupancy rate is reached, that private rental needs a statement of non-availability or an exception to policy, and that the wait for government housing is one to eight weeks depending on bedrooms. In the Kaiserslautern Military Community the Air Force Housing Office manages accompanied housing.", ["kmc_hso"]),
     ("Unaccompanied E-1 to E-6 at Kaiserslautern live in barracks; E-7 and above are entitled to off-post housing and report to the Air Force Housing Office (Vogelweh Housing, Building 1001).", ["kmc_hso"]),
   ]),
   ("Wiesbaden checklist", [
     ("Report to the Housing Office within 48 hours of arrival, attend the in-person Housing Brief (Wednesdays at 09:00, Building 1023W, Room 210 per the garrison page; schedule subject to change), complete in-processing, then start house-hunting.", ["wies_off"]),
     ("Before you arrive, browse HOMES.mil to compare home sizes and prices and decide how much furniture to ship or store.", ["wies_off"]),
     ("Negotiate and sign the lease at the Housing Services Office with the landlord and a counselor; bilingual agreements are preferred. The April 2022 briefing warns that verbal agreements in Germany are binding and that termination requires written notice with a 3-month period.", ["wies_brief"]),
     ("Ask the counselor whether your landlord is on the Non-Referral or Restricted Sanction list; the briefing says signing with a landlord on the Restricted Sanctions List (entries are for validated discrimination) is not recommended.", ["wies_brief"]),
     ("Complete a move-in inspection. A garrison article advises recording any damage on the inspection form with photos and giving the landlord a copy, so move-out goes smoothly.", ["wies_off","army_landlord"]),
   ]),
   ("Bavaria (Grafenwoehr, Vilseck, Hohenfels) checklist", [
     ("Do not enter a rental contract, written or verbal, before the housing brief and in-processing. Use HOMES.mil, searching “USAG Bavaria”.", ["bav_rental"]),
     ("Contract review: you and the landlord sign the contract cover sheet, then you schedule a review with the housing office within two business days of the landlord signing; the appointment takes about 60 minutes on average.", ["bav_rental"]),
     ("How OHA is paid: the garrison says you receive the lesser of your rent or the rank-based rent cap, plus a monthly utility allowance. MIHA includes a one-time miscellaneous payment for items such as transformers and curtains; realtor fees may be authorized for special housing needs (for example five or more bedrooms or Exceptional Family Member needs).", ["bav_rental"]),
     ("Army members can request an advance housing allowance for the first month’s rent and security deposit, which the page says typically equals two months’ rent; take your signed contract to your unit S1.", ["bav_rental"]),
     ("Know the house rules: landlords may choose their tenants (including meeting a dog), and quiet hours run 10 p.m. to 6 a.m., 1 to 3 p.m., and all day Sundays and German federal holidays.", ["bav_rental"]),
     ("Square-meter prices are high and some units cost more than the OHA rent cap; apartments, townhouses and duplexes are generally less expensive and easier to find than large single-family homes.", ["bav_rental"]),
   ]),
   ("Not covered here", [
     ("Stuttgart and Ansbach have the same OHA tables above, but this page has no verified housing-office rules for them; ask the USAG Stuttgart or USAG Ansbach housing office before signing.", []),
   ]),
  ],
 ),
}
