# -*- coding: utf-8 -*-
"""Per-installation guide facts for PCS Vector.

RULES (see tools/README.md):
  * Every sentence in `checklist`, `housing`, `area` carries 1+ source keys from SOURCES.
  * No figure appears here that is not on the cited page.  BAH/OHA dollar amounts are
    NOT typed here: the generator reads them from the page/data already in the repo.
  * AS_OF is the date the source pages were read.  Re-read before changing AS_OF.
To add a fort: copy a block, fill facts from the installation's official page, add its sources.
"""
AS_OF = "2026-10-28"
AS_OF_HUMAN = "28 Oct 2026"

SOURCES = {
 # ---- Fort Sill
 "sill_mi":   ("Military OneSource, Fort Sill housing", "https://installations.militaryonesource.mil/military-installation/fort-sill/housing/housing"),
 "sill_in":   ("Military OneSource, Fort Sill check-in procedures", "https://installations.militaryonesource.mil/military-installation/fort-sill/base-essentials/check-in-procedures"),
 "sill_new":  ("Fort Sill newcomers page", "https://home.army.mil/sill/my-fort/newcomers"),
 # ---- Belvoir / NCR
 "belvoir_hso": ("Fort Belvoir Housing Services Office", "https://home.army.mil/belvoir/about/Garrison/housing-services-office"),
 "belvoir_mi":  ("Military OneSource, Fort Belvoir housing", "https://installations.militaryonesource.mil/military-installation/fort-belvoir/housing/housing"),
 "belvoir_plb": ("Fort Belvoir Installation Housing Office plain-language briefing", "https://home.army.mil/belvoir/7115/9551/6586/Installation_Housing_Office_Plain_Language_Briefing.pdf"),
 # ---- JBSA
 "jbsa_pah":  ("JBSA-Fort Sam Houston privatized Army housing", "https://home.army.mil/samhouston/directorates-1/privatized-army-housing"),
 "jbsa_mi":   ("Military OneSource, JBSA housing", "https://installations.militaryonesource.mil/military-installation/joint-base-san-antonio-lackland-randolph-sam-houston/housing/housing"),
 # ---- Bliss / Riley / Campbell / Bragg / Hood / Drum
 "bliss_mi":  ("Military OneSource, Fort Bliss housing", "https://installations.militaryonesource.mil/military-installation/fort-bliss/housing/housing"),
 "riley_mi":  ("Military OneSource, Fort Riley housing", "https://installations.militaryonesource.mil/military-installation/fort-riley/housing/housing"),
 "campbell_mi": ("Military OneSource, Fort Campbell housing", "https://installations.militaryonesource.mil/military-installation/fort-campbell/housing/housing"),
 "bragg_mi":  ("Military OneSource, Fort Bragg housing", "https://installations.militaryonesource.mil/military-installation/fort-bragg/housing/housing"),
 "hood_mi":   ("Military OneSource, Fort Hood housing", "https://installations.militaryonesource.mil/military-installation/fort-hood/housing/housing"),
 "drum_mi":   ("Military OneSource, Fort Drum housing", "https://installations.militaryonesource.mil/military-installation/fort-drum/housing/housing"),
 # ---- generic
 "dtmo_bah":  ("DTMO, Basic Allowance for Housing", "https://www.travel.dod.mil/Allowances/Basic-Allowance-for-Housing/"),
 "dtmo_oha":  ("DTMO, Overseas Housing Allowance", "https://www.travel.dod.mil/Allowances/Overseas-Housing-Allowance/"),
 "doj_scra":  ("U.S. Department of Justice, Financial and Housing Rights (SCRA)", "https://www.justice.gov/servicemembers/financial-and-housing-rights-0"),
 "mos_dla":   ("Military OneSource, Dislocation Allowance FAQs", "https://www.militaryonesource.mil/benefits/military-dislocation-allowance/"),
 "mos_tle":   ("Military OneSource, Temporary Lodging Expense", "https://www.militaryonesource.mil/benefits/temporary-lodging-expense/"),
 "asf_bah26": ("Air & Space Forces Magazine, 2026 BAH and COLA release coverage (30 Dec 2025)", "https://www.airandspaceforces.com/pentagon-releases-cost-of-living-bah-rates-for-2026/"),
 # ---- Korea
 "hum_sheet": ("USAG Humphreys Housing Information Sheet (Oct 2024)", "https://home.army.mil/humphreys/3817/3093/6105/Housing_Information_Sheet_Oct._2024.pdf"),
 "hum_dpw":   ("USAG Humphreys DPW Housing Division", "https://home.army.mil/humphreys/about/garrison/directorate-public-works/housing-division"),
 "hum_steps": ("USAG Humphreys Off-Post In-processing Packet, Army (PDF dated 20 Feb 2024)", "https://home.army.mil/humphreys/3917/0901/0899/Offpost_In-processing_Packet_-_Army_20_Feb_2024.pdf"),
 "hum_hso":   ("Humphreys Housing Services Office booklet", "https://api.army.mil/e2/c/downloads/365895.pdf"),
 "yc_mi":     ("Military OneSource, USAG Yongsan-Casey housing", "https://installations.militaryonesource.mil/military-installation/usag-yongsan-casey/housing/housing"),
 # ---- Japan
 "zama_move": ("USAG Japan, moving in: on-post / off-post housing", "https://home.army.mil/japan/my-fort/newcomers/arriving-airport/post-or-post-housing-moving"),
 "zama_mi":   ("Military OneSource, Camp Zama government housing", "https://installations.militaryonesource.mil/military-installation/camp-zama/housing/government-housing"),
 "zama_faq":  ("Camp Zama housing FAQ", "https://www.housing.army.mil/Installations/Zama/FAQ.pdf"),
 # ---- Germany
 "wies_off":  ("USAG Wiesbaden off-post housing", "https://home.army.mil/wiesbaden/about/Garrison/directorate-public-works/housing-services-office/off-post-housing"),
 "wies_brief":("USAG Wiesbaden off-post housing briefing (Apr 2022)", "https://home.army.mil/wiesbaden/2316/4984/3790/Off-Post_Housing_Briefing_April_2022.pdf"),
 "bav_rental":("USAG Bavaria private rental", "https://home.army.mil/bavaria/housing/privaterental"),
 "kmc_hso":   ("USAG Rheinland-Pfalz Housing Services Office", "https://home.army.mil/rheinland-pfalz/about/directorates-support-offices/directorate-public-works-dpw/housing-services-office"),
 "army_landlord": ("Army.mil, Avoid problems with your landlord (Wiesbaden)", "https://www.army.mil/article/249890/avoid_problems_with_your_landlord_helpful_tips"),
 "ahousing":  ("Army Housing Online User Services, renting and leasing", "https://www.housing.army.mil/pages/rentingleasing.aspx"),
}

# short = display name; slug = /bah/<slug>/; kind = BAH
GUIDES = {
 "fort-sill": dict(
  short="Fort Sill",
  lead="Fort Sill sits north of Lawton, Oklahoma, about 90 miles southwest of Oklahoma City. Military OneSource says about 80% of military personnel in the Fort Sill area live off post, so the BAH-versus-rent question matters more than the on-post waitlist.",
  lead_src=["sill_new","sill_mi"],
  checklist=[
   ("In-process at the Welcome Center, Building 4700 on Mow-Way Road. Bring your PCS orders; in-processing takes 3 to 5 days.", ["sill_in","sill_new"]),
   ("Temporary lodging: unaccompanied E-5 and below get a temporary room; accompanied members and E-6 and above check with on-post lodging (IHG, Building 5676), and if no room is free you receive a statement of non-availability that allows off-post lodging in Lawton.", ["sill_in"]),
   ("Before you rent, lease or buy off post, report to the Housing Services Office (HSO), Welcome Center, Building 4700, third floor. Military OneSource says you are required to report in person before making any off-post housing arrangements.", ["sill_mi","sill_new"]),
   ("Ask the HSO for its list of rentals with locator maps and information on the surrounding communities. The newcomers page says it provides referrals, landlord mediation, fair housing information and Servicemembers Civil Relief Act (SCRA) guidance.", ["sill_mi","sill_new"]),
   ("Relocation help: the Army Community Service relocation program is on the first floor of Building 4700 (PCS planning, area orientations, settlement assistance).", ["sill_new"]),
   ("Budget the move-in costs: security deposits at Fort Sill vary and often equal one month’s rent, and the installation advises every renter to carry renters insurance because the owner’s policy does not cover your belongings.", ["sill_mi"]),
  ],
  housing=[
   ("Off post: about 80% of military personnel live off post in the Fort Sill area, in apartment complexes, mobile homes and houses for rent or sale in Lawton and nearby towns.", ["sill_mi"]),
   ("On post: family housing is privatized through Corvias Property Management (apply through its website, sill.corviaspm.com).", ["sill_mi","sill_new"]),
   ("Single E-1 to E-5 members are required to occupy barracks space; living off post at the single rate needs an approved exception to policy and a Certificate of Non-Availability.", ["sill_mi"]),
  ],
  area=[
   ("Fort Sill is about 94,000 acres, home to the Fires Center of Excellence, and sits just north of Lawton.", ["sill_new"]),
  ],
  faq=[
   ("What is BAH at Fort Sill in 2026?", "{bah_line}"),
   ("Is Fort Sill BAH the same as BAH in Oklahoma City or Tulsa?", "No. DTMO sets BAH by military housing area, and Fort Sill’s area ({mha_name}, {mha_code}) covers only the Lawton-area ZIP codes listed on this page. Oklahoma City, Tulsa and other Oklahoma ZIP codes belong to different housing areas, so look them up in DTMO’s BAH calculator instead of using these rates."),
  ],
 ),
 "national-capital-region": dict(
  short="Fort Belvoir and the DC area",
  lead="Searches for “Fort Belvoir BAH”, “DC BAH” and “O-6 BAH Washington DC” all end up at the same DTMO housing area. Fort Belvoir (ZIP 22060), Fort Myer (22211), Fort McNair (20319) and the rest of the DC metro share one rate, so inside this area your commute, not your BAH, is what changes with where you live.",
  lead_src=[],
  checklist=[
   ("Start with the Fort Belvoir Housing Services Office (HSO): Building 258, 9851 Harding Place. Its off-post division gives counseling and referrals, lists of brokers, property managers, apartment and condominium complexes, lease and rental-agreement review, and landlord-tenant mediation.", ["belvoir_hso"]),
   ("HSO hours posted by the garrison: Monday to Friday, 7:30 a.m. to 3:30 p.m.; phone 703-805-3019. Garrison Commander’s Housing Hotline (on-post housing concerns): 571-259-9867.", ["belvoir_hso"]),
   ("Ask the HSO about the services Military OneSource lists for it: rental and temporary housing listings, off-post quality housing inspections, in- and out-processing, lease review, and landlord-tenant mediation and advocacy.", ["belvoir_mi"]),
   ("If you want on-post family housing, Fort Belvoir’s privatized partner is The Villages at Belvoir; the garrison page describes the HSO, unaccompanied housing and the privatized-housing oversight office as three separate divisions.", ["belvoir_hso","belvoir_mi"]),
   ("Junior enlisted single members who report to Fort Belvoir are assigned barracks rooms through the First Sergeants Barracks Program; unaccompanied housing: 703-806-0120.", ["belvoir_hso"]),
   ("The garrison’s housing briefing notes two FY20 NDAA requirements: if a tenant cannot attend the pre-assignment walkthrough inspection, the Housing Office must attend on the tenant’s behalf, and the Housing Manager contacts residents 15 and 60 days after move-in.", ["belvoir_plb"]),
  ],
  housing=[
   ("Fort Belvoir is in Fairfax County, Virginia, but Military OneSource says families may live in surrounding counties including Alexandria, Arlington, Prince William, Prince George’s, Frederick, Montgomery and Stafford.", ["belvoir_mi"]),
   ("On post: living on post is described as including gyms, pools, a marina, golf course, field house and skate park, plus the Village Commons mixed-use area.", ["belvoir_mi"]),
  ],
  area=[
   ("Because BAH is identical in every ZIP code of this housing area, the useful comparison is rent plus commute: price a few neighborhoods against the same rate, then test the drive at your real reporting time.", []),
  ],
  faq=[
   ("What is the BAH for Fort Belvoir in 2026?", "Fort Belvoir (ZIP 22060) is in DTMO’s {mha_name} housing area ({mha_code}). In 2026 an E-5 with dependents receives {E5w}, an O-3 with dependents {O3w} and an O-6 with dependents {O6w}; without dependents the same grades receive {E5o}, {O3o} and {O6o}."),
   ("What is O-6 BAH in Washington, DC?", "For 2026 an O-6 in the {mha_name} area ({mha_code}) receives {O6w} a month with dependents and {O6o} without. Every ZIP in the area gets the same rate; DTMO’s 2026 table is on this page."),
   ("Is DC BAH different for Virginia and Maryland suburbs?", "No. DTMO lists DC, Northern Virginia and Maryland ZIP codes together under {mha_code}, so a Soldier at the same grade and dependency status receives the same BAH whether they rent in Arlington, Alexandria, Fairfax or Prince George’s County."),
  ],
 ),
 "joint-base-san-antonio": dict(
  short="JBSA (Fort Sam Houston, Lackland, Randolph)",
  lead="Joint Base San Antonio combines Fort Sam Houston, Lackland and Randolph. One DTMO housing area covers all three, so a search for “Fort Sam Houston BAH” and one for “JBSA BAH” return the same rate.",
  lead_src=[],
  checklist=[
   ("Contact the Military Housing Office (MHO) for the campus you report to: JBSA-Fort Sam Houston 210-221-0881, JBSA-Lackland 210-671-1840, JBSA-Randolph 830-483-9900.", ["jbsa_mi"]),
   ("The Fort Sam Houston MHO is at 3171 Zinn Road, Building 1161; hours listed by Military OneSource are Monday to Friday, 8 a.m. to 4 p.m.", ["jbsa_mi"]),
   ("Use the MHO for rental searches and for lease review and disputes; Military OneSource describes it as the subject-matter expert on leases, discrimination complaints and tenant-landlord disputes.", ["jbsa_mi"]),
   ("Search HOMES.mil by ZIP code: listings are reviewed by the Military Housing Office for discriminatory content and safety concerns before they are approved.", ["jbsa_mi"]),
   ("Carry renters insurance: the property owner’s policy covers the building but not your belongings.", ["jbsa_mi"]),
   ("Look up utility providers by ZIP code before you sign so you can compare deposits and connection fees.", ["jbsa_mi"]),
  ],
  housing=[
   ("Military OneSource says the San Antonio area has over 174 neighborhoods, with rents that vary considerably by style, size and location.", ["jbsa_mi"]),
   ("On-post family housing at Fort Sam Houston is privatized; see the garrison’s privatized Army housing page for how to apply.", ["jbsa_pah"]),
  ],
  area=[
   ("The three main JBSA locations each have their own housing office, so call the one that matches your report location rather than assuming one office covers the whole base.", ["jbsa_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Sam Houston in 2026?", "Fort Sam Houston, Lackland and Randolph are all in DTMO’s {mha_name} housing area ({mha_code}). In 2026 an E-5 with dependents receives {E5w} and an E-5 without dependents {E5o}; the full table by grade is on this page."),
  ],
 ),
 "fort-bliss": dict(
  short="Fort Bliss",
  lead="Fort Bliss is in El Paso, Texas, and DTMO prices it as the EL PASO housing area. On-post family housing is privatized, and the installation tells arriving members to see its Housing Services Office before arranging anything off post.",
  lead_src=["bliss_mi"],
  checklist=[
   ("Report to the Housing Services Office (HSO), Building 515B, Pershing Road, before you rent, lease or buy off post. Military OneSource lists hours of Monday to Friday, 9 a.m. to noon and 1 to 4 p.m., closed the third Thursday of each month from noon to 4 p.m.; phone 915-568-2898.", ["bliss_mi"]),
   ("Do not send deposits for housing before you have contacted the HSO.", ["bliss_mi"]),
   ("Service members are told to report to the HSO at both their current and new duty stations before making off-post arrangements, so call your losing installation’s office too.", ["bliss_mi"]),
   ("If you want on-post family housing, contact Fort Bliss Family Homes (1991 Marshall Road, El Paso): 915-564-0795 for leasing, with two-, three- and four-bedroom homes.", ["bliss_mi"]),
  ],
  housing=[
   ("On post: Fort Bliss Family Homes is a gated, privatized community with pools, playgrounds and sport courts, and is described as open first to active-duty families assigned to the base, with select homes for retirees, DoW civilians and the public.", ["bliss_mi"]),
   ("Off post: the HSO is the office to ask for rental listings and housing help before you pay any deposit.", ["bliss_mi"]),
  ],
  area=[
   ("Fort Bliss Family Homes lists El Paso, TX 79906 as its address, so the on-post option is inside the El Paso housing area DTMO uses for BAH.", ["bliss_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Bliss in 2026?", "{bah_line}"),
  ],
 ),
 "fort-riley": dict(
  short="Fort Riley",
  lead="Fort Riley’s on-post family housing is privatized and assigned by rank and bedroom qualification, and Military OneSource warns that being on the waitlist does not guarantee a home when you arrive. Plan your first weeks around that.",
  lead_src=["riley_mi"],
  checklist=[
   ("Apply for on-post housing as soon as you know you are coming; Military OneSource says service members may apply as soon as they know they will be assigned. Applying within 30 days of signing in preserves a backdated effective date to your detachment date.", ["riley_mi"]),
   ("Secure temporary lodging before you arrive and be ready to pay for lodging beyond what the Temporary Lodging Expense covers until adequate housing is found.", ["riley_mi"]),
   ("Gather the on-post application documents: orders to Fort Riley, a DD 93 or DD 1172 that is less than a year old (no handwritten copies), and a DA 31 if you took leave. Dual-military, single pregnant, restricted-tour and power-of-attorney cases have extra requirements listed on the source page.", ["riley_mi"]),
   ("Corvias Military Living’s leasing office is at 45 Barry Avenue (Main Post), 785-717-2258, Monday to Friday, 8 a.m. to 5 p.m.", ["riley_mi"]),
   ("For off-post housing, use the Army Housing Office; Military OneSource says it may be able to help get a deposit waived, depending on the property owner.", ["riley_mi"]),
   ("Do not treat an on-post offer as a reason to break a lease: the installation states that accepting on-post housing is not justification to break a lease or rental agreement. For lease questions when you hold deployment orders, call the Off Post Housing Division, 785-239-3525.", ["riley_mi"]),
  ],
  housing=[
   ("On post: five neighborhoods managed by Corvias Military Living; homes are assigned by rank and bedroom qualification and wait times vary.", ["riley_mi"]),
   ("Pets on post: at most two dogs or cats per household; several breeds are not allowed on Fort Riley or in family housing, so read the pet policy before you commit.", ["riley_mi"]),
   ("Boats and RVs may be kept in a family-housing garage with the door closed, or in the free (often full) Camp Forsyth RV lot with a waiting list.", ["riley_mi"]),
  ],
  area=[],
  faq=[
   ("What is BAH at Fort Riley in 2026?", "{bah_line}"),
  ],
 ),
 "fort-campbell": dict(
  short="Fort Campbell",
  lead="Military OneSource says rentals in Clarksville, Tennessee, and Oak Grove and Hopkinsville, Kentucky, are very affordable. That is why the housing office asks every service member, regardless of grade or marital status, to check in before signing anything.",
  lead_src=["campbell_mi"],
  checklist=[
   ("Report to the Housing Services Office (HSO), Soldier Support Center, 2702 Michigan Avenue, Suite 400, before you rent, lease or buy. Listed hours: Monday to Friday, 7:30 a.m. to 4 p.m., with a note to call on Thursday mornings; phone 270-798-3808.", ["campbell_mi"]),
   ("Ask the HSO for the rental listings, inspection of rentals for adequacy, tenant-landlord mediation, home-finding transportation and the off-limits establishment list, which is also included in each in-processing packet.", ["campbell_mi"]),
   ("Before you pay another application or credit-check fee, visit the HSO: the office says it has long-term relationships with local property managers and fees add up quickly if you are denied.", ["campbell_mi"]),
   ("Ask about the Rental Partnership Program, which aims to cut the initial cost of renting through reduced or waived security deposits, discounted rent and application fees; enrollment requires a military allotment.", ["campbell_mi"]),
   ("Make sure the lease has a military clause, and have the HSO or the Staff Judge Advocate review it before you sign.", ["campbell_mi"]),
   ("For on-post housing (Campbell Crossing LLC), apply early: advance applications are accepted online, and you need orders, a current DD 1172, a recent leave and earnings statement showing the with-dependents BAH rate, and other forms listed on the source page. Apply no later than 30 days after reporting to keep your eligibility date.", ["campbell_mi"]),
  ],
  housing=[
   ("On post: Campbell Crossing LLC manages privatized housing for all ranks, from two to five bedrooms, with waiting lists set by grade and bedroom need.", ["campbell_mi"]),
   ("Off post: there are no mobile home parks on post and no government-owned or -leased housing off post.", ["campbell_mi"]),
   ("Deposits: a landlord may ask for a security deposit usually equal to one month’s rent or less, or none; it is not an advance on your last month’s rent.", ["campbell_mi"]),
  ],
  area=[
   ("Cities named by Military OneSource for off-post rentals: Clarksville, Tennessee, and Oak Grove and Hopkinsville, Kentucky.", ["campbell_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Campbell in 2026?", "{bah_line}"),
  ],
 ),
 "fort-bragg": dict(
  short="Fort Bragg",
  lead="Fort Bragg’s housing office makes a simple rule explicit: every service member, married or single, reports to the Housing Services Office before signing a rental, lease or purchase agreement off post.",
  lead_src=["bragg_mi"],
  checklist=[
   ("Report to the Housing Services Office (HSO), Soldier Support Center, Normandy Drive, Building 4-2843, basement level (BH2) near the elevators. Phone 910-396-1022; Military OneSource lists Monday, Wednesday, Thursday and Friday 7:30 a.m. to 4 p.m., Tuesday from 9 a.m., closed 11:30 a.m. to 12:30 p.m.", ["bragg_mi"]),
   ("Ask for rental listings, maps, landlord-tenant responsibilities, North Carolina rental law information and the off-limits establishment list, all provided at the information briefings.", ["bragg_mi"]),
   ("For on-post family housing, the privatized manager is Corvias Military Housing (leasing office, 2850 Compass Court, 910-495-0878). Wait times vary with rank and bedroom count; applications are not complete without supporting documents.", ["bragg_mi"]),
   ("Single Soldiers in the rank of Staff Sergeant and below must live in the barracks, which also applies to Soldiers married to Soldiers at that rank when the spouse is stationed elsewhere; Sergeant First Class and above may live off post or ask about Randolph Point (910-764-5008).", ["bragg_mi"]),
  ],
  housing=[
   ("On post: Corvias communities are organized into enclaves for particular rank bands, from junior enlisted through field-grade officers.", ["bragg_mi"]),
   ("Off post: the HSO is the contact for discrimination complaints, tenant-landlord disputes and off-post housing questions.", ["bragg_mi"]),
  ],
  area=[],
  faq=[
   ("What is BAH at Fort Bragg in 2026?", "{bah_line}"),
  ],
 ),
 "fort-hood": dict(
  short="Fort Hood",
  lead="Fort Hood’s housing office says most local housing is in Killeen, Harker Heights and Copperas Cove, 10 to 15 minutes from post, with Temple, Belton, Gatesville and Lampasas about 30 minutes away. Living on post is voluntary except for personnel in key and essential positions.",
  lead_src=["hood_mi"],
  checklist=[
   ("In-process through the Housing Services Office (HSO) before you rent, lease or buy locally; this is mandatory. It is in the Copeland Soldier Service Center, Building 18010, B209, T.J. Mills Boulevard; phone 254-285-2313.", ["hood_mi"]),
   ("Ask the HSO for its list of registered rental agencies, and for lease review or help with any discrimination complaint or landlord-tenant dispute.", ["hood_mi"]),
   ("Budget for fees: local agencies and property managers require non-refundable administrative and rental/credit-history fees and a non-refundable pet deposit, and may require a security deposit equal to one month’s rent.", ["hood_mi"]),
   ("Do not sign until the HSO has reviewed the property, and make sure the lease contains the Servicemembers Civil Relief Act clause, which lets you end the lease if orders take you away for more than 90 days.", ["hood_mi"]),
   ("Complete the move-in inspection checklist within the allotted time and keep a signed copy to avoid penalty or repair charges when you leave.", ["hood_mi"]),
   ("To live on post, apply within 30 days of arriving to receive an eligibility date; later applications use the application date. Listed wait times range from two weeks to 12 months depending on occupancy.", ["hood_mi"]),
  ],
  housing=[
   ("On post: privatized housing in 13 villages (single-family homes and townhomes, two to five bedrooms), operated by the installation’s housing partners; applications go through the partner websites or the HSO.", ["hood_mi"]),
   ("Off post: homes and apartments in Killeen, Harker Heights, Copperas Cove, Temple, Belton, Gatesville and Lampasas, all within a 30-minute drive of Fort Hood.", ["hood_mi"]),
  ],
  area=[
   ("Commute times given by Military OneSource: Killeen, Harker Heights and Copperas Cove 10 to 15 minutes; Temple, Belton, Gatesville and Lampasas about 30 minutes.", ["hood_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Hood in 2026?", "{bah_line}"),
  ],
 ),
 "fort-drum": dict(
  short="Fort Drum",
  lead="At Fort Drum, one fact changes the BAH math: Military OneSource says the rental rate for on-post family housing covers utilities, weekly trash and recycling, and 24-hour emergency maintenance. Off post you pay utilities yourself, which in the North Country means heat.",
  lead_src=["drum_mi"],
  checklist=[
   ("Visit the Housing Services Office / Army Community Housing, Clark Hall, 10720 Mount Belvedere Boulevard, 2nd floor, room A2-54. Phone 315-772-6668; listed hours Monday to Friday, 7:30 a.m. to 4 p.m.", ["drum_mi"]),
   ("The HSO keeps a list of rentals near Fort Drum, updated weekly, and helps with discrimination and landlord-tenant disputes.", ["drum_mi"]),
   ("Expect most off-post homes to be unfurnished with a 12-month lease, plus a security deposit, first month’s rent and a pet deposit; furnished apartments are hard to find.", ["drum_mi"]),
   ("Insist on a military clause that lets you end the lease early under the Servicemembers Civil Relief Act if you deploy or get PCS orders, and have the HSO or the Legal Assistance Office review the lease.", ["drum_mi"]),
   ("If you want on-post family housing, start the advance application early with Fort Drum Mountain Community Homes (315-955-6644).", ["drum_mi"]),
   ("Need a four- or five-bedroom home? Military OneSource advises allowing more time and widening the search to single-family rentals, buying, or places farther from post.", ["drum_mi"]),
  ],
  housing=[
   ("On post: Fort Drum Mountain Community Homes maintains 3,793 homes, two to five bedrooms, with garages, private outdoor space and washer and dryer hookups.", ["drum_mi"]),
   ("Single members: those at E-5 and below who are not entitled to with-dependents BAH must live in the barracks; The Timbers has 192 one- and two-bedroom apartments for single and unaccompanied members at E-6 and above.", ["drum_mi"]),
   ("Off post: apartments, duplexes, single homes and mobile homes; Fort Drum itself has no mobile home park.", ["drum_mi"]),
  ],
  area=[
   ("For buyers, Military OneSource points to homes for sale across Jefferson, Lewis and St. Lawrence counties.", ["drum_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Drum in 2026?", "{bah_line}"),
  ],
 ),
}

# Batch 2: the 18 remaining BAH pages live in guide_data_batch2.py (same rules, same renderer).
from guide_data_batch2 import SOURCES2, GUIDES2   # noqa: E402
SOURCES.update(SOURCES2)
GUIDES.update(GUIDES2)
