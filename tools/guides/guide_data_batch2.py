# -*- coding: utf-8 -*-
"""Batch 2 per-installation guide facts (the 18 remaining BAH pages).

Same rules as guide_data.py: every sentence in checklist/housing/area carries source keys;
no BAH/OHA dollar figures are typed here; all facts come from the cited Military OneSource
(MilitaryINSTALLATIONS) pages read on AS_OF.  Merged into guide_data.GUIDES / SOURCES at import.
"""

# ---- part 1
MO = "https://installations.militaryonesource.mil/military-installation/%s/%s"
def src(slug, name, extra=""):
    return {
     "%s_mi" % slug: ("Military OneSource, %s housing" % name, MO % (slug, "housing/housing")),
     "%s_tl" % slug: ("Military OneSource, %s temporary housing" % name, MO % (slug, "housing/temporary-housing")),
     "%s_in" % slug: ("Military OneSource, %s check-in procedures" % name, MO % (slug, "base-essentials/check-in-procedures")),
    }
SOURCES2 = {}
GUIDES2 = {}
SOURCES2.update(src("fort-benning","Fort Benning")); SOURCES2.update(src("fort-carson","Fort Carson")); SOURCES2.update(src("fort-gordon","Fort Gordon"))
GUIDES2["fort-benning"] = dict(
  short="Fort Benning",
  lead="Fort Benning’s family housing is run by The Villages of Benning, and Military OneSource says it charges no credit check, background check, application fee or security deposit to active-duty military. Your place on the wait list is set by the day you cleared your last duty station, so start the application early.",
  lead_src=["fort-benning_mi"],
  checklist=[
   ("Sign in first. During duty hours permanent-party soldiers report to the Installation Replacement Operations Center, Ridgway Hall (Building 35), Room 239; after hours they report to post Staff Duty at McGinnis-Wickam Hall (Building 4). Military OneSource says not to report to your unit first unless you are a single soldier going to barracks.", ["fort-benning_in"]),
   ("Plan for a seven-day in-processing program touching medical, finance, transportation, housing and education. The first full day includes a four-hour briefing session that covers housing and finance, after which you get a schedule and a cohort leader.", ["fort-benning_in"]),
   ("Visit the Housing Services Office (HSO) in Ridgway Hall (Building 35), Room 385, phone 706-545-3921, for current off-post listings. Military OneSource lists hours of Monday to Wednesday and Friday 8 a.m. to 4:30 p.m. and Thursday 8 a.m. to 2:30 p.m.", ["fort-benning_mi"]),
   ("For on-post family housing, apply as soon as you can: your eligibility date is the date you signed out of your last PCS station, and it sets your place on the list but not how long you wait. Applicants who apply more than 30 days after arriving are listed with the date of their application instead.", ["fort-benning_mi"]),
   ("Bring complete documentation. Military OneSource says applicants with missing paperwork go on administrative hold and are not offered a home until everything is received, and that no availability date is guaranteed.", ["fort-benning_mi"]),
   ("Lodging while you wait: the on-post IHG hotel is Holiday Inn Express Abrams Hall (Building 167, 7350 Ingersoll Road). Military OneSource notes on-post lodging is often full, especially in summer, and Fort Benning Lodging helps with off-post rooms in Columbus.", ["fort-benning_tl"]),
   ("Single soldiers contact the Unaccompanied Housing Office (706-545-3921) or their prospective unit about barracks.", ["fort-benning_mi"]),
  ],
  housing=[
   ("On post: family homes are managed by The Villages of Benning through six community management offices, with 24-hour emergency maintenance, mowing and curbside trash pickup. The Welcome Center and leasing office is at 601 Lumpkin Street, Monday to Friday 8 a.m. to 5 p.m., 706-685-3939.", ["fort-benning_mi"]),
   ("Deposits and pets on post: no credit check, background check, application fees or security deposit for active-duty military, and no pet deposit for the first two approved pets.", ["fort-benning_mi"]),
   ("School letters are issued at the housing appointment, but only if the wait for quarters is under 90 days.", ["fort-benning_mi"]),
   ("Off post: the HSO is the contact for off-post tenant and landlord disputes and discrimination complaints, and it can point you to available temporary lodging while you wait for on-post housing.", ["fort-benning_mi"]),
  ],
  area=[
   ("Uchee Creek Campground and Marina sits on the Alabama bank of the Chattahoochee River on a 385-acre park and offers chalets, cabins and RV and tent sites to military ID holders.", ["fort-benning_tl"]),
   ("McIver Suites Historic Guest Lodging, near the golf course clubhouse, offers one- and two-bedroom suites with housekeeping.", ["fort-benning_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Benning in 2026?", "{bah_line}"),
   ("Does The Villages of Benning charge a deposit?", "Military OneSource’s Fort Benning housing page says the Villages offer no credit check, background check, application fee or security deposit for active-duty military, and no pet deposit for the first two approved pets. Confirm current terms with the leasing office before you apply."),
   ("Does my place on the Fort Benning housing wait list start when I arrive?", "No. Military OneSource says your eligibility date is the date you signed out of your last PCS station, but applicants who apply more than 30 days after arriving are listed with their application date, so apply early."),
  ],
)
GUIDES2["fort-carson"] = dict(
  short="Fort Carson",
  lead="Fort Carson’s Army housing office handles three things: off-post help, on-post community services and barracks. Military OneSource says Army regulations require you to visit the Housing Services Office after you arrive and before you commit to any permanent off-post arrangement if you receive BAH.",
  lead_src=["fort-carson_mi"],
  checklist=[
   ("Sign in at the Reception Center (Building 1456, 1783 Nelson Boulevard) at the second-floor CQ desk with a copy of your DA 31 and orders. Military OneSource says to bring five copies of your orders and amendments and five copies of your approved absence request.", ["fort-carson_in"]),
   ("Expect a 4+1 in-processing schedule; your first day varies with installation needs.", ["fort-carson_in"]),
   ("Flying in: for Colorado Springs, contact Replacement to coordinate pickup. From either Colorado Springs or Denver airport, soldiers may use ride shares or taxis and be reimbursed; receipts are not required for expenses under $75.", ["fort-carson_in"]),
   ("Report to the Housing Services Office (HSO), Building 1225, if you receive BAH. It helps with rentals and for-sale listings, complaint mediation and a volunteer realtor program, and works with landlords so homes meet government standards. Phones: 719-238-6458 or 719-725-8096.", ["fort-carson_mi"]),
   ("Ask the HSO about the Pikes Peak Association of Realtors volunteer realtors: Military OneSource says they are vetted and print rental and sale listings from the Multiple Listing Service and explain VA, FHA and conventional loan basics.", ["fort-carson_mi"]),
   ("Lodging: unaccompanied soldiers at E-5 and below are billeted by Replacement; everyone else arranges their own. On post, Candlewood Suites (IHG) gives priority to PCS families (719-526-4832 or 877-711-8326). If it is full, HSO (Building 1225, Room 189) keeps a list of military-friendly hotels with discounted rates.", ["fort-carson_tl","fort-carson_in"]),
   ("For newcomer help call Army Community Service at 719-526-0457; Military OneSource also points to a digital welcome packet.", ["fort-carson_mi","fort-carson_in"]),
  ],
  housing=[
   ("Army housing at Fort Carson has three parts: the Housing Services Office for off-post help, Residential Community Services for on-post homes, and Unaccompanied Housing for barracks.", ["fort-carson_mi"]),
   ("The HSO can also point you to HOMES.mil for listings.", ["fort-carson_mi"]),
   ("Other lodging: the Regional Training Institute hotel on post is open to active-duty members and families (with a shuttle), and Camp Hale outside Gate 6 has cabins and pull-through RV pads that are pet friendly.", ["fort-carson_tl"]),
  ],
  area=[
   ("Shuttle buses run throughout the installation, which helps if you arrive without a car.", ["fort-carson_in"]),
  ],
  faq=[
   ("What is BAH at Fort Carson in 2026?", "{bah_line}"),
   ("Do I have to see the Fort Carson Housing Services Office before renting off post?", "Military OneSource’s Fort Carson housing page says that if you receive BAH, Army regulations require you to visit the Housing Services Office before making permanent off-post living arrangements. The office is in Building 1225."),
   ("Is my airport ride to Fort Carson reimbursed?", "Military OneSource says soldiers arriving at Colorado Springs or Denver airports may use local transportation such as ride shares or taxis and be reimbursed, with no receipt needed for expenses under $75. Check your orders and call Replacement Staff Duty if you need help."),
  ],
)
GUIDES2["fort-gordon"] = dict(
  short="Fort Gordon",
  lead="Fort Gordon’s Military OneSource housing page describes an Augusta-area market with a healthy rental vacancy rate, and says the roughly 1,000 on-post family homes are all privatized. Check which county you want before you tour: Fort Gordon is in Richmond County, next to newer and pricier Columbia County.",
  lead_src=["fort-gordon_mi"],
  checklist=[
   ("If you want the allowed ten days of permissive TDY for house hunting, contact your gaining unit first so you have the right leave form; otherwise you are charged ordinary leave. After PTDY you report for duty at Darling Hall (Building 33720, Room 262) to start in-processing.", ["fort-gordon_in"]),
   ("Budget about seven days for in-processing, which includes visits to several locations and orientations. Spouses are encouraged to attend the newcomer orientation held Thursdays at 1 p.m., except federal holidays.", ["fort-gordon_in"]),
   ("Use the mobile in-processing guides Military OneSource names: the Digital Garrison and GuideOn apps, for Apple and Android.", ["fort-gordon_in"]),
   ("Army personnel must have a sponsor; if you do not, contact your gaining unit.", ["fort-gordon_in"]),
   ("Book lodging early: all on-post lodging is run by IHG Army Hotels (877-711-TEAM or online), with Griffith Hall just inside Gate 1. Gate 6 is open 24 hours for DOD ID cardholders.", ["fort-gordon_tl"]),
   ("Visit the Housing Services Office (HSO) for a list of rentals with locator maps and community information; it also handles discrimination complaints and tenant-landlord disputes.", ["fort-gordon_mi"]),
   ("Buy renters insurance: Military OneSource says the landlord’s policy covers only the building and that most local leases require renters insurance.", ["fort-gordon_mi"]),
  ],
  housing=[
   ("On post: about 1,000 family housing units, all privatized and operated by Balfour Beatty Communities (706-772-7041).", ["fort-gordon_mi"]),
   ("Off post: Military OneSource says Augusta has a healthy rental vacancy rate and that security deposits are sometimes waived for military personnel, otherwise usually one month’s rent.", ["fort-gordon_mi"]),
   ("Pets: where pets are allowed there is usually a substantial nonrefundable deposit, and many apartments limit pets to 25 pounds (Military OneSource).", ["fort-gordon_mi"]),
   ("Mobile homes are typically available and usually furnished; there is no mobile home park on the installation, so check the surroundings before signing.", ["fort-gordon_mi"]),
  ],
  area=[
   ("Local communities: Augusta and Hephzibah in Richmond County; Martinez, Evans and Grovetown in Columbia County.", ["fort-gordon_mi"]),
   ("Columbia County homes are generally newer and more expensive, and its newer schools and infrastructure can mean higher property taxes.", ["fort-gordon_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Gordon in 2026?", "{bah_line}"),
   ("Which county should I look in near Fort Gordon?", "Military OneSource says Fort Gordon is in Richmond County near the Columbia County border. Local communities include Augusta and Hephzibah in Richmond County and Martinez, Evans and Grovetown in Columbia County, where homes are generally newer and more expensive and property taxes can be higher."),
   ("Is on-post housing at Fort Gordon run by the Army?", "Military OneSource says all of Fort Gordon’s family housing, roughly 1,000 units, is privatized and operated by Balfour Beatty Communities."),
  ],
)

# ---- part 2
SOURCES2.update(src("fort-huachuca","Fort Huachuca")); SOURCES2.update(src("fort-irwin","Fort Irwin"))
GUIDES2["fort-huachuca"] = dict(
  short="Fort Huachuca",
  lead="Fort Huachuca’s family housing is privatized under the Army’s Residential Communities Initiative and managed by Mountain Vista Communities. Military OneSource says the housing and management offices share one building, and that you must sign in for duty and hold PCS orders before you can apply for an on-post home.",
  lead_src=["fort-huachuca_mi"],
  checklist=[
   ("Enter through the Van Deman Gate Welcome Center (open Monday to Friday 5:30 a.m. to 5:15 p.m.) or the Buffalo Soldier Gate, which is open 24 hours.", ["fort-huachuca_in"]),
   ("In-processing starts at your unit or activity, which books you into the Personnel Processing Center briefing on Tuesdays 7:30 a.m. to noon (908 Butler Road, Building 22420). Newcomers Orientation is Wednesdays 8 a.m. to noon at Murr Community Center (Building 51301, Cushing Street).", ["fort-huachuca_in"]),
   ("Report to the Housing Services Office (HSO) as part of in-processing if you have family members. Military OneSource says it is required, and that you need your sign-in for duty and PCS orders before applying for on-post housing.", ["fort-huachuca_mi"]),
   ("The HSO and Mountain Vista Communities offices are both in Building 52065 on Smith Street, Monday to Friday 7:30 a.m. to 4:30 p.m., phone 520-515-9000.", ["fort-huachuca_mi"]),
   ("Reserve lodging early: IHG Army Hotels’ Candlewood Suites takes reservations up to a year ahead (520-226-3800, 24 hours), pet rooms are limited and in high demand, and PCS and TDY travelers pay a portion of the Cochise County per diem, no more than the full amount.", ["fort-huachuca_tl"]),
   ("Do not wait on a Statement of Non-Availability: Military OneSource says none is needed or possible, because the lodging is privately owned.", ["fort-huachuca_tl"]),
   ("If you have pets, plan for the Pet Addendum that Mountain Vista requires, and check the restricted-breed list before you commit.", ["fort-huachuca_mi"]),
  ],
  housing=[
   ("On-post family housing is one- and two-story single-family homes and duplexes, and some homes date from 1884 in the old cavalry fort, now a state and national historic landmark.", ["fort-huachuca_mi"]),
   ("The Army’s private partner is carrying out a 50-year plan to develop, build and operate privatized family housing on post, with new construction and renovation of existing homes.", ["fort-huachuca_mi"]),
   ("Homes are open to members of all service branches assigned to Fort Huachuca; waiting time varies by rank and bedroom requirement.", ["fort-huachuca_mi"]),
   ("Pets: two per home; dogs of listed aggressive breeds (Pit Bull types, Rottweilers, Doberman Pinschers, Chows and wolf hybrids) are not permitted, and certified assistance animals are not pets under the policy.", ["fort-huachuca_mi"]),
  ],
  area=[
   ("Apache Flats RV Resort on post has 56 concrete pull-through slots for active duty, dependents, retirees and civilians; reservations open 60 days out for active duty (520-533-1335).", ["fort-huachuca_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Huachuca in 2026?", "{bah_line}"),
   ("Do I need a non-availability statement for Fort Huachuca lodging?", "Military OneSource’s Fort Huachuca temporary housing page says that if lodging is unavailable a Statement of Non-Availability is not needed or possible, because the hotel is privately owned. Ask the lodging office and your finance office how your lodging reimbursement works."),
   ("When can I apply for on-post housing at Fort Huachuca?", "Military OneSource says military personnel must sign in for duty and have their PCS orders before they can apply for on-post housing, and that all members with families must report to the Housing Services Office as part of in-processing."),
  ],
)
GUIDES2["fort-irwin"] = dict(
  short="Fort Irwin",
  lead="Fort Irwin sits far from the nearest large town, and Military OneSource says most families prefer to live on post because of the distance to Barstow and the extra cost of living there. On-post homes are often not available on arrival, so apply 60 to 90 days before your PCS date.",
  lead_src=["fort-irwin_mi"],
  checklist=[
   ("Report to the Replacement Detachment, Building 109, Langford Lake Road (open 24 hours) with your leave form, finance records, medical and dental records and five copies of your orders. After duty hours use the Command Duty Section, Building 988.", ["fort-irwin_in"]),
   ("Attend the Mandatory Newcomers Briefing, held every Friday at the Replacement Detachment; family members are encouraged to come.", ["fort-irwin_in"]),
   ("Apply for on-post housing 60 to 90 days before your PCS date. Military OneSource says the waiting list varies from 1 to 6 months.", ["fort-irwin_mi"]),
   ("If you must wait, ask the privatized housing partner to move you into a temporary home at a fixed BAH rate until your home is ready.", ["fort-irwin_mi"]),
   ("Arriving from an unaccompanied tour such as Korea earns a waiting-period adjustment equal to the months served, up to 18 months.", ["fort-irwin_mi"]),
   ("Lodging: the Landmark Inn (760-386-4040) is the only hotel within 35 miles of Fort Irwin. Military OneSource says it is often sold out months in advance during rotations, and that as a private business it does not set priorities for who may reserve. It also says a non-availability statement is not required to be reimbursed if you stay in a Barstow motel, so keep your receipts.", ["fort-irwin_tl"]),
   ("Families staying in Barstow, Victorville or Apple Valley can use the satellite Army Community Service center, the Military Connection and Resource Center at 512 Barstow Road (760-256-5751). Both it and the on-post ACS have a lending closet with kitchenware, microwaves, card tables and some baby items.", ["fort-irwin_in"]),
  ],
  housing=[
   ("On post: family housing is privatized; Michaels Management Services has been the community partner since July 2015, and leasing is at 4553 Tippecanoe in the Sandy Basin community. Homes have 2 to 4 bedrooms and some are accessible.", ["fort-irwin_mi"]),
   ("How BAH works on post: because housing is privatized, the full BAH amount shows on your LES as an entitlement and is simultaneously taken out as an allotment paid to the landlord for rent. Utilities except telephone and cable are included in the rent within the median baseline.", ["fort-irwin_mi"]),
   ("Off post: Military OneSource says apartment rents are plus utilities (it gives an undated range, so ask for current prices) and that the Housing Services Office can name reputable complexes and property managers.", ["fort-irwin_mi"]),
   ("Single members: company grade officers, warrant officers and soldiers E-6 and above drawing BAH at the without-dependents rate are not required to live on post; unaccompanied housing is available through the private partner.", ["fort-irwin_mi"]),
   ("There is no mobile home park at Fort Irwin, but there is an RV site (Outdoor Recreation, 760-380-4327).", ["fort-irwin_mi"]),
  ],
  area=[
   ("The Landmark Inn has 179 rooms, free wireless internet and a daily continental breakfast.", ["fort-irwin_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Irwin in 2026?", "{bah_line}"),
   ("Why does my full BAH go to rent on post at Fort Irwin?", "Military OneSource says Fort Irwin’s on-post housing is privatized, so your full BAH appears on your LES as an entitlement and is subtracted at the same time as an allotment paid to the housing partner for rent. Most utilities are included in the rent within the median baseline."),
   ("How long is the wait for on-post housing at Fort Irwin?", "Military OneSource says it varies from 1 to 6 months, and recommends applying 60 to 90 days before your PCS date. If you have to wait, you can ask the housing partner for a temporary home at a fixed BAH rate."),
  ],
)

# ---- part 3
SOURCES2.update(src("fort-jackson","Fort Jackson")); SOURCES2.update(src("fort-knox","Fort Knox"))
GUIDES2["fort-jackson"] = dict(
  short="Fort Jackson",
  lead="Fort Jackson’s Army Housing Office calls itself your housing community advocate and your first stop whether you live on or off post. Military OneSource also cautions against signing a lease before you arrive, and says the Columbia area has many apartment communities within about a 15-minute drive of the installation.",
  lead_src=["fort-jackson_mi"],
  checklist=[
   ("Report to Room 200, 5450 Strom Thurmond Boulevard, Monday, Wednesday and Friday 7:30 a.m. to 4:30 p.m. The office is closed on federal holidays and Tuesdays and Thursdays from 11:30 a.m. to 5 p.m.; arrive after 11:30 on those days and you report to Room 207 for a time stamp.", ["fort-jackson_in"]),
   ("Arriving after 5 p.m. with no sponsor or unit assignment on your orders: report to the front desk of the IHG hotel at 7550 Benning Road, then to Room 200 at 8 a.m. the next duty day.", ["fort-jackson_in"]),
   ("Bring your absence leave form and a copy of your PCS orders. Military OneSource warns that an administrative absence cannot run past your report date or you are charged leave for the whole period; if yours is for house hunting, visit your gaining unit or call your sponsor.", ["fort-jackson_in"]),
   ("Go through the One-Stop In-Processing (OSIP) Center before you report to your gaining command.", ["fort-jackson_in"]),
   ("Visit the Army Housing Office at 4514 8th Division Road or call 803-751-9339 before you pick a home. Military OneSource says it handles discrimination complaints, tenant-landlord disputes, lease reviews and inspections.", ["fort-jackson_mi"]),
   ("Do not sign a lease before you arrive, and visit any apartment in person. Most rentals ask for one month’s rent plus a security deposit up front, and Military OneSource says you are accountable for damage if you skip renters insurance.", ["fort-jackson_mi"]),
   ("Ask the HSO for its list of apartment complexes that are off-limits to service members.", ["fort-jackson_mi"]),
   ("Book lodging as soon as you have orders: IHG Army Hotel Fort Jackson (877-711-8326) says on-post lodging is often fully booked during PCS season.", ["fort-jackson_tl"]),
  ],
  housing=[
   ("On post: Fort Jackson Family Homes (520 Brown, 803-738-8275) manages privatized family housing. All units have central heating and air conditioning, and the average wait depends on home size and arrival date.", ["fort-jackson_mi"]),
   ("Your eligibility date is the final out date of your previous duty station; after an unaccompanied tour, it is the out date of the station before that tour, up to 14 months.", ["fort-jackson_mi"]),
   ("Single members: E-1 through E-5 without dependents must live in the Freddie Stowers Single Soldiers Complex unless granted an exception; E-6 and above may live off post.", ["fort-jackson_mi"]),
   ("Exceptional family members: a limited number of accessible homes exist; contact Fort Jackson Family Homes at 803-738-9339 as early as possible.", ["fort-jackson_mi"]),
   ("Pets on post: breeds restricted by the housing community include Akita, Chow, Doberman, Pit Bull, Rottweiler, Staffordshire terrier types and wolf hybrids.", ["fort-jackson_mi"]),
  ],
  area=[
   ("The Columbia metro area has many new apartments, condos and townhomes under construction, and many apartment communities offer military discounts.", ["fort-jackson_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Jackson in 2026?", "{bah_line}"),
   ("Should I sign a lease before I arrive at Fort Jackson?", "Military OneSource’s Fort Jackson housing page says it cautions against signing a lease before arrival and encourages you to visit the apartment or home in person. The Housing Service Office can also give you a list of complexes that are off-limits to service members."),
   ("How is my Fort Jackson housing eligibility date set?", "Military OneSource says the eligibility date is the final out date of your previous duty station, and after an unaccompanied tour it is the out date of the station before that tour, up to 14 months."),
  ],
)
GUIDES2["fort-knox"] = dict(
  short="Fort Knox",
  lead="Military OneSource’s Fort Knox housing page says all incoming soldiers must first report to Housing Services to in-process housing, and that the same office checks that leases carry military provisions. Its check-in page separately tells soldiers to report to their gaining unit on day one. On-post family housing is privatized and run by Knox Hills.",
  lead_src=["fort-knox_mi","fort-knox_in"],
  checklist=[
   ("Day one: report to your gaining unit so your arrival is recorded in IPPS-A; Military OneSource’s check-in page says to do this before the Process Control Station. If you arrive after duty hours, sign in at the Department of Emergency Services, Building 298 on Gold Vault Road (502-624-6847).", ["fort-knox_in"]),
   ("Housing: Military OneSource’s housing page says all incoming soldiers must first report to Housing Services (Housing Division Office, Building 1110A, Suite 101, Sixth Avenue) to in-process housing under AR 420-1, and that counselors give referrals and a local orientation.", ["fort-knox_mi"]),
   ("Before you rent, lease or buy off post, visit or contact the Housing Services Office (502-624-8084). Military OneSource says it can help you avoid scams, unreliable realtors and unsuitable rentals, and checks that leases have the provisions military renters need.", ["fort-knox_mi"]),
   ("Search HOMES.mil, the joint military housing listings site; Military OneSource says it marks properties approved by HSO staff and lists Rental Partnership Program offers, and that you can search without an account.", ["fort-knox_mi"]),
   ("Then complete in-processing in duty uniform: report to the Process Control Station at Rockenbach Hall, Building 2020, Room 130 no later than one duty day after your unit completes your arrival transaction, with your orders, any amendments and your corrected absence request. Processing hours are 8 a.m. to 3 p.m. Monday to Thursday and 8:30 a.m. to 3 p.m. Friday, closed 11:30 a.m. to 12:30 p.m.", ["fort-knox_in"]),
   ("You then get five duty days to visit the in-processing agencies and return to finalize your checklist.", ["fort-knox_in"]),
   ("Lodging: IHG Army Hotels, 406 N. Knox Street (502-943-1000), has five facilities and a front desk open 24 hours; Military OneSource strongly encourages reservations.", ["fort-knox_tl"]),
   ("Single and unaccompanied soldiers at E-5 and below contact the Housing Division Office at 502-624-8084.", ["fort-knox_mi"]),
  ],
  housing=[
   ("On post: Knox Hills LLC owns, operates and maintains all family housing. The leasing office is at 41 W. Chaffee Avenue (502-799-6550, Monday to Friday 8 a.m. to 5 p.m.); maintenance is at 144 S. Conroy Avenue (502-799-6565).", ["fort-knox_mi"]),
   ("Knox Hills has three community offices: Historic (41 W. Chaffee Avenue), North and South Dietz (75 Estrada Avenue) and Oak Park (101 S. Brett).", ["fort-knox_mi"]),
   ("Off post: the HSO provides listings plus local school-district information and county planning and zoning rules.", ["fort-knox_mi"]),
  ],
  area=[
   ("Camp Carlson, an outdoor recreation area, has 56 RV sites with water, electric and sewer hookups and a 90-consecutive-day stay limit, then a 72-hour break. A deposit equal to one day’s rent holds a reservation.", ["fort-knox_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Knox in 2026?", "{bah_line}"),
   ("Who owns the family housing at Fort Knox?", "Military OneSource says Fort Knox’s on-post housing is privatized and that Knox Hills LLC owns, operates and maintains all of the family housing. The leasing office is at 41 W. Chaffee Avenue."),
   ("Where do I report first at Fort Knox?", "Military OneSource’s check-in page says to report to your gaining unit on day one, then to the Process Control Station no later than one duty day after your arrival is recorded; after hours, sign in at the Department of Emergency Services (Building 298). Its housing page says all incoming soldiers must first report to Housing Services to in-process housing, and must visit or contact it before renting, leasing or buying off post."),
  ],
)

# ---- part 4
SOURCES2.update(src("fort-leavenworth","Fort Leavenworth")); SOURCES2.update(src("fort-lee","Fort Lee"))
GUIDES2["fort-leavenworth"] = dict(
  short="Fort Leavenworth",
  lead="At Fort Leavenworth living on post is voluntary for most families, and Military OneSource says your report date, not your application date, sets your place on the privatized housing waiting list, so you can apply before you arrive. Every arriving soldier must still see the Housing Services Office.",
  lead_src=["fort-leavenworth_mi"],
  checklist=[
   ("Apply for on-post housing online with Frontier Heritage Communities before you arrive; Military OneSource says all military personnel with dependents assigned to Fort Leavenworth are eligible and that the report date determines the waiting-list position. Applications can also be faxed to 913-758-1779.", ["fort-leavenworth_mi"]),
   ("Report to the Housing Services Office (HSO), 731 McClellan Avenue, Building 48 (913-684-5681 or 913-684-3052). Military OneSource says all soldiers reporting to Fort Leavenworth must do this.", ["fort-leavenworth_mi"]),
   ("If you rent off post, carry renters insurance: the owner’s policy covers the building, not your belongings.", ["fort-leavenworth_mi"]),
   ("Walk through the property with the landlord at move-in and again at move-out, and make sure both of you sign and keep a copy of the inspection.", ["fort-leavenworth_mi"]),
   ("Get everything in writing. Military OneSource warns that verbal agreements will not stand up in court, and recommends a receipt that lists each payment separately plus a copy of the lease.", ["fort-leavenworth_mi"]),
   ("Know the lease-break rule: the installation’s housing page cites the SCRA’s 30-day notice after PCS orders (or deployment orders of more than 90 days) and cautions that accepting on-post housing is not a reason to break a lease.", ["fort-leavenworth_mi"]),
   ("Lodging: IHG Army Hotels (800-854-8627 or 913-684-4091) is the post lodging office, about one mile from the front gate off Grant Avenue; PCS and TDY personnel can reserve up to 30 days ahead, and people on orders have priority over visitors.", ["fort-leavenworth_tl"]),
  ],
  housing=[
   ("On post: family housing is privatized and managed by Frontier Heritage Communities, which has ADA-approved homes for families with medical housing needs.", ["fort-leavenworth_mi"]),
   ("Pets on post: up to four dogs or cats in any combination per household, with a deposit for the first two pets; listed aggressive breeds and crosses are not allowed.", ["fort-leavenworth_mi"]),
   ("There are no mobile home parks on Fort Leavenworth.", ["fort-leavenworth_mi"]),
   ("Buying a home: the garrison offers free home-buyer seminars through the HSO, covering how to choose an agent, apply for a loan, and understand escrow and closing costs.", ["fort-leavenworth_mi"]),
  ],
  area=[
   ("The lodging office says pets are allowed in lodging, with a nonrefundable pet deposit and a daily fee after seven days.", ["fort-leavenworth_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Leavenworth in 2026?", "{bah_line}"),
   ("Is on-post housing required at Fort Leavenworth?", "Military OneSource says living on post is voluntary, except for personnel in positions the installation commander designates as key and essential. Everyone reporting to Fort Leavenworth must still visit the Housing Services Office."),
   ("How is my Fort Leavenworth housing waiting-list position set?", "Military OneSource’s Fort Leavenworth housing page says the service member’s report date determines position on the waiting list, and that you may apply in advance of your arrival through Frontier Heritage Communities."),
  ],
)
GUIDES2["fort-lee"] = dict(
  short="Fort Lee",
  lead="Fort Lee sits in Virginia’s tri-city area (Petersburg, Hopewell and Colonial Heights), about 20 miles southeast of Richmond, and Military OneSource notes that depending on which gate you use you can be in a different city or county. That matters when you compare rentals against your BAH.",
  lead_src=["fort-lee_mi"],
  checklist=[
   ("Permanent-party soldiers report to the Soldier Support Center (Building 3400, 1401 Barefoot Avenue) from 7:30 a.m. to 4:30 p.m. After hours or on weekends and holidays, sign in at the Installation Operations Center, Building 1107 (804-734-1584).", ["fort-lee_in"]),
   ("Hand-carry list from Military OneSource: orders (copy counts differ by group on that page: two at the Soldier Support Center sign-in, five on the general hand-carry list and seven for students and training courses, so ask your gaining organization), DA Form 31, DD Form 93, personnel file, proof of car insurance, children’s birth certificates and school transcripts, medical, dental and immunization records, ID cards, professional licenses, marriage certificate and wills or legal documents.", ["fort-lee_in"]),
   ("Flying into Richmond: Military OneSource says AIT students use the USO at Richmond International Airport (804-236-7234) with two copies of orders for no-cost transport to the installation.", ["fort-lee_in"]),
   ("Contact the Housing Services Office (804-765-3862 or 804-765-1597) for off-post renting or buying information.", ["fort-lee_mi"]),
   ("On-post lodging: the IHG Army Hotel is open 24 hours (877-711-8326 or 804-733-4100); Holiday Inn Express is in Building 12015, 2301 Sustainment Avenue.", ["fort-lee_tl","fort-lee_mi"]),
   ("If you are single and E-6 or above, plan to rent off post: Military OneSource says these grades without dependents are required to live off post and are authorized BAH at the without-dependents rate.", ["fort-lee_mi"]),
  ],
  housing=[
   ("On post: Fort Lee Family Housing is managed by Hunt Companies (office hours 8:30 a.m. to 5:30 p.m. weekdays). It has seven villages and two- to five-bedroom homes, with some units adaptable for special needs. Active-duty members with dependents are eligible.", ["fort-lee_mi"]),
   ("Pets are allowed in lodging for a fee; about 20% of rooms in the older lodging building are pet-friendly.", ["fort-lee_mi"]),
   ("Single members: members geographically separated from their families are not authorized to live in the barracks, and E-6 and above without dependents are required to live off post.", ["fort-lee_mi"]),
   ("Students: AIT students live in their barracks and should not bring family, and most military students are prohibited from bringing family members to Fort Lee.", ["fort-lee_mi"]),
  ],
  area=[
   ("Surrounding counties are Prince George, Chesterfield and Dinwiddie, and Williamsburg is about 45 minutes away.", ["fort-lee_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Lee in 2026?", "{bah_line}"),
   ("Can I live in the barracks at Fort Lee if my family is somewhere else?", "No. Military OneSource says soldiers who are geographically separated from their families are not authorized to live in the barracks, and that E-6 and above without dependents are required to live off post at the without-dependents BAH rate."),
   ("Who manages family housing at Fort Lee?", "Military OneSource says Fort Lee Family Housing is managed by Hunt Companies, with seven villages and homes of two to five bedrooms, open to active-duty members with dependents."),
  ],
)

# ---- part 5
SOURCES2.update(src("fort-leonard-wood","Fort Leonard Wood")); SOURCES2.update(src("fort-polk","Fort Polk"))
GUIDES2["fort-leonard-wood"] = dict(
  short="Fort Leonard Wood",
  lead="Fort Leonard Wood’s family housing is privatized and open to all ranks, in about 1,800 two-, three- and four-bedroom homes in four neighborhoods run by Balfour Beatty. Military OneSource’s page also spells out who must live off post, which decides whether you ever compare a rent against BAH.",
  lead_src=["fort-leonard-wood_mi"],
  checklist=[
   ("Active-duty Army personnel report to the Central In/Out Processing Office, Building 470, Room 2105, from 7:30 a.m. to 4:30 p.m. Soldiers arriving with family members go first to the Lodging Office inside Candlewood Suites (Building 2020), open 24 hours. Marine Corps, Navy and Air Force personnel have separate reporting points listed on Military OneSource.", ["fort-leonard-wood_in"]),
   ("Pack the documents Military OneSource lists: passports, driver’s license and military ID, naturalization papers if relevant, power of attorney, credit card information, tax records, school transcripts, employment records and references, insurance policies, car titles and registration, and sales receipts for furniture and high-value items.", ["fort-leonard-wood_in"]),
   ("Reserve lodging early: PCS families can book 60 days before arrival through the IHG Army Hotels lodging office at 3400 Nebraska Avenue (573-586-4800 or 800-677-8356).", ["fort-leonard-wood_tl"]),
   ("Watch the stay limit: Military OneSource says the maximum length of stay is 30 days without forfeiture of BAH.", ["fort-leonard-wood_tl"]),
   ("If you have pets, join the waiting list early: eight cottages on Community Drive take pets, and the page says there is a 30-day waiting list.", ["fort-leonard-wood_tl"]),
   ("Contact the Housing Referral Office for off-post help: it gives you rental lists with locator maps and community information and handles discrimination complaints and tenant-landlord disputes.", ["fort-leonard-wood_mi"]),
   ("Call the housing office at 573-329-0122 about on-post family housing, and carry renters insurance wherever you live off post.", ["fort-leonard-wood_mi"]),
  ],
  housing=[
   ("On post: Balfour Beatty took over family housing in June 2008; Military OneSource cites about 1,806 families and describes about 1,800 homes in four neighborhoods managed by Fort Leonard Wood Homes.", ["fort-leonard-wood_mi"]),
   ("Single soldiers: E-1 to E-3 are assigned space in Specker Barracks, E-4 to E-5 in renovated family quarters on Indiana Avenue, and E-6 to E-9 must live off post. Soldiers with legally supported family members and geographic bachelors also live off post.", ["fort-leonard-wood_mi"]),
   ("There are no permanent-party bachelor officer quarters on post.", ["fort-leonard-wood_mi"]),
  ],
  area=[
   ("Pets in lodging: eight post cottages on Community Drive accept pets for a per-night fee plus nonrefundable cleaning and pet fees; check the temporary housing page for the current schedule.", ["fort-leonard-wood_tl"]),
  ],
  faq=[
   ("What is BAH at Fort Leonard Wood in 2026?", "{bah_line}"),
   ("Who has to live off post at Fort Leonard Wood?", "Military OneSource says all personnel in grades E-6 to E-9 must reside off post, along with soldiers who have legally supported family members and geographic bachelors. Single soldiers in E-1 to E-5 are assigned post barracks or renovated family quarters."),
   ("Will long lodging stays cost me BAH at Fort Leonard Wood?", "Military OneSource says the maximum length of stay for PCS lodging at Fort Leonard Wood is 30 days without forfeiture of BAH. Ask the lodging office and your finance office how that applies to your orders."),
  ],
)
GUIDES2["fort-polk"] = dict(
  short="Fort Polk",
  lead="Fort Polk lets you apply for on-post housing up to 90 days before you arrive, through Corvias. Military OneSource describes the local market as medium cost of living and tells renters to insist on a military clause in the lease and to take paperwork to the Legal Assistance Office before signing.",
  lead_src=["fort-polk_mi"],
  checklist=[
   ("Apply for on-post housing up to 90 days before arrival on the Corvias website (polk.corviaspm.com) or in person; the Corvias Resident Relocation Specialist is at 337-537-5000.", ["fort-polk_mi"]),
   ("Report during duty hours to the In/Out Processing Center, Building 250 (1716 3rd Street), which handles ID and CAC, finance, medical and dental records, education, TRICARE and housing briefings in one place.", ["fort-polk_in"]),
   ("At in-processing, Corvias Family Housing gives you information on off-post housing availability and places you on the waiting list, according to Military OneSource.", ["fort-polk_in"]),
   ("Visit the Army Housing Office, 1820 Corps Road, Building 330 (337-531-6000), the liaison between residents, the installation and Corvias; it also helps with off-post leasing and mediation.", ["fort-polk_mi"]),
   ("Before you sign a lease, take the paperwork to the Legal Assistance Office and make sure the lease has a military clause that lets you end it early for deployment or PCS orders.", ["fort-polk_mi"]),
   ("Budget up front: local landlords require first and last month’s rent, and some ask you to pay part of the utilities instead of having your own meter.", ["fort-polk_mi"]),
   ("Book lodging: Holiday Inn Express Magnolia House and Cypress Inn, 7326 Utah Avenue, Building 522 (337-531-9000). Keep receipts for the Finance Office; pet-friendly rooms are offered on request and by availability.", ["fort-polk_tl"]),
  ],
  housing=[
   ("On post: Corvias manages six neighborhoods of two- to five-bedroom homes for all ranks.", ["fort-polk_mi"]),
   ("A limited number of two-bedroom homes for senior single members, warrant officers and officers is handled by the housing assistance office (337-531-6000).", ["fort-polk_mi"]),
   ("Military OneSource lists off-post hotels in Leesville and DeRidder as alternatives while you look.", ["fort-polk_tl"]),
  ],
  area=[
   ("Military OneSource describes Fort Polk as a medium-cost-of-living area and gives a broad range for local home prices and rents without utilities; ask the Army Housing Office for current figures.", ["fort-polk_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Polk in 2026?", "{bah_line}"),
   ("How early can I apply for on-post housing at Fort Polk?", "Military OneSource says incoming personnel may apply up to 90 days before arriving at Fort Polk, using the Corvias website or in person."),
   ("What should a Fort Polk lease include?", "Military OneSource says your lease should contain a military clause that lets you end it early if you deploy or receive PCS orders, and that you should take all paperwork to the Legal Assistance Office before you sign."),
  ],
)

# ---- part 6
SOURCES2.update(src("fort-rucker","Fort Rucker")); SOURCES2.update(src("fort-stewart","Fort Stewart"))
GUIDES2["fort-rucker"] = dict(
  short="Fort Rucker",
  lead="Fort Rucker’s family housing is entirely on post and entirely privatized, and Military OneSource says there are no other government housing options such as leased homes in the community. It also says you should apply as soon as you receive orders, because availability drops in peak PCS season.",
  lead_src=["fort-rucker_mi"],
  checklist=[
   ("Apply for on-post housing as soon as your orders arrive, using the Corvias online application or the Leasing and Relocation Center at 9700 Division Road (334-440-8988). Military OneSource notes availability is lower in peak PCS season.", ["fort-rucker_mi"]),
   ("Sign in during duty hours (7:30 a.m. to 4 p.m., Monday to Friday) at the Soldier Service Center, Military Personnel Division, Building 5700, Room 280, with PCS orders and your leave authorization form. Military OneSource recommends reporting during duty hours.", ["fort-rucker_in"]),
   ("Arriving after hours, on a weekend or on a holiday: report to Building 101 (the installation operations center, 334-255-3100), then go to Building 5700, Room 280 at 7:30 a.m. the first duty day in duty uniform.", ["fort-rucker_in"]),
   ("Visit the Housing Services Office (334-255-2224) in the Soldier Service Center, Building 5700, Room 160; Military OneSource calls it the soldier’s advocate.", ["fort-rucker_mi"]),
   ("Set up utilities at the Utilities Clearing House (Building 5700, Room 190, 334-255-3554), which helps soldiers and families with electricity and cable service.", ["fort-rucker_mi"]),
   ("Reserve lodging: IHG Army Hotels is in Building 308 on Sixth Avenue (877-711-TEAM or 334-598-5216), about 20 miles from Dothan Regional Airport.", ["fort-rucker_tl"]),
  ],
  housing=[
   ("On post: Corvias Military Living runs three neighborhood community centers (pool, fitness center, club room, computer lab) that residents can use at no extra cost, plus 24-hour maintenance, lawn care, pest control and refuse pickup.", ["fort-rucker_mi"]),
   ("Eligibility: accompanied and unaccompanied service members, geographic bachelors, federal civilians and military retirees can apply; children are eligible to attend DoWEA schools.", ["fort-rucker_mi"]),
   ("Single members: two- and three-bedroom homes are available to E-6 and above and are shared by two service members of the same rank and gender; unaccompanied personnel housing for staff sergeants and above is voluntary and first come, first served.", ["fort-rucker_mi"]),
   ("Pets in lodging: IHG charges a nonrefundable pet fee plus a daily fee starting the sixth night.", ["fort-rucker_tl"]),
  ],
  area=[
   ("Fort Rucker is in Alabama’s Wiregrass area; local communities include Daleville and Ozark in Dale County, Enterprise in Coffee County and Dothan in Houston County.", ["fort-rucker_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Rucker in 2026?", "{bah_line}"),
   ("Is any government housing available off post near Fort Rucker?", "No. Military OneSource says there is no government-owned or leased housing in the community and no government-operated mobile home park; all government housing is on the installation and is privatized."),
   ("Which towns are near Fort Rucker?", "Military OneSource’s Fort Rucker housing page says the post is in the Wiregrass area, with Daleville and Ozark in Dale County, Enterprise in Coffee County and Dothan in Houston County."),
  ],
)
GUIDES2["fort-stewart"] = dict(
  short="Fort Stewart",
  lead="Fort Stewart’s on-post rent is tied directly to your BAH: Military OneSource says the rent allotment for Fort Stewart Family Homes equals the soldier’s BAH entitlement for their rank. It also says every soldier reporting to the installation must process through the Housing Service Office before renting or buying off post.",
  lead_src=["fort-stewart_mi"],
  checklist=[
   ("Sign in at the installation’s reception center on Fort Stewart, even if you are assigned to Hunter Army Airfield, unless you have specific directions otherwise. Expect a few days of in-processing, and submit the proper leave request before taking permissive leave for house hunting.", ["fort-stewart_in"]),
   ("Hand-carry list: PCS orders with amendments, DA Form 31, military ID cards, marriage certificate, divorce decree, birth certificates, a household goods inventory and any other military records.", ["fort-stewart_in"]),
   ("Process through the Housing Service Office (HSO) before renting or buying off post. Military OneSource says it provides rental lists, lease reviews, inspections for suitability, mediation of landlord disputes and information on the deposit waiver program.", ["fort-stewart_mi"]),
   ("Apply for family housing online (or fax a printed application). When you arrive, bring your military ID, Leave and Earnings Statement, copy of orders and a DEERS form or birth certificates for every child in the home.", ["fort-stewart_mi"]),
   ("Apply within 30 days of leaving your last station to keep your eligibility date: Military OneSource says it is the day you left, otherwise the date of your application. From an unaccompanied tour such as Korea, you get credit from the date you departed for that tour, up to 14 months, with orders as proof.", ["fort-stewart_mi"]),
   ("If you are married and this is your first duty station, bring your Basic Training and AIT orders to confirm your eligibility date.", ["fort-stewart_mi"]),
   ("Concurrent travel with family must be authorized on your PCS orders. If you marry before you PCS or report, Military OneSource says follow the procedures exactly or the military will not pay for your spouse’s travel and housing.", ["fort-stewart_in"]),
   ("Book lodging early: Army Lodging (Building 4951, across from Club Stewart) takes PCS reservations up to a year ahead, with a 30-day first stay and extensions on request. It has 70 double rooms and 99 single rooms.", ["fort-stewart_tl","fort-stewart_in"]),
  ],
  housing=[
   ("On post: Fort Stewart Family Homes, managed by Balfour Beatty Communities, has 3,268 air-conditioned homes in 10 neighborhoods, from two to five bedrooms (912-408-2466).", ["fort-stewart_mi"]),
   ("Most homes are for active-duty Army families assigned to Fort Stewart; the page says the highest proportion is for E-1 to E-6 and the lowest for officers, and rental homes are also open to retirees, DoW civilians and the public.", ["fort-stewart_mi"]),
   ("Pets: two are allowed in family housing at no extra charge; restricted breeds and exotic pets such as snakes, rodents and reptiles are not allowed.", ["fort-stewart_mi"]),
   ("Exceptional family members: adaptable and wheelchair-accessible homes are available, but the page says generators are not provided for medical equipment.", ["fort-stewart_mi"]),
   ("There are no mobile home parks on post and no government-leased housing in the community.", ["fort-stewart_mi"]),
  ],
  area=[
   ("To check VA home-loan eligibility, Military OneSource points soldiers to the Veterans Administration at the Soldier Service Center, Building 253.", ["fort-stewart_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Stewart in 2026?", "{bah_line}"),
   ("How much rent will I pay in Fort Stewart Family Homes?", "Military OneSource says the rent allotment equals the soldier’s Basic Allowance for Housing entitlement for their rank, so check the Fort Stewart BAH table on this page for your grade and dependent status. Ask the leasing office what utilities and fees are included."),
   ("When does my Fort Stewart housing wait-list date start?", "Military OneSource says that if you apply within 30 days of leaving your previous duty station, your eligibility date is the day you left; otherwise it is your application date. A completed application is required to join the wait list."),
  ],
)

# ---- part 7
SOURCES2.update(src("fort-wainwright","Fort Wainwright")); SOURCES2.update(src("joint-base-langley-eustis","Joint Base Langley-Eustis"))
GUIDES2["fort-wainwright"] = dict(
  short="Fort Wainwright",
  lead="Fort Wainwright housing has three Alaska-specific rules worth knowing before you travel: lodging is usually fully booked from April through September, temporary lodging allowance must be validated by the Housing Services Office every 10 days, and the acceptable off-post commute is measured in extreme winter weather.",
  lead_src=["fort-wainwright_tl","fort-wainwright_mi"],
  checklist=[
   ("Reserve lodging as soon as you have orders: Military OneSource says Alaska lodging is usually 100% booked from April through September. The Holiday Inn Express on post (Building 3402, 907-370-0999) is pet-friendly; call about pet fees.", ["fort-wainwright_tl"]),
   ("Report to the Welcome Center, Building 3401 on Santiago Road, third floor, with a copy of your orders and leave form; the line at 907-353-4311 is staffed 24 hours a day. Expect five days of in-processing before you report to your unit.", ["fort-wainwright_in","fort-wainwright_mi"]),
   ("Visit the Housing Services Office (907-353-1190) before you sign any rental or sales agreement; Military OneSource says all military members must process through it first.", ["fort-wainwright_mi"]),
   ("Request Temporary Lodging Allowance (TLA) within your first five days. Only the Housing Services Office can authorize it; it comes in 10-day increments with proof of an active housing search, for up to 20 days, and the home must be ready within 60 days of sign-in.", ["fort-wainwright_tl","fort-wainwright_in"]),
   ("Check that your PCS orders authorize the Alaska Highway (and the marine highway if you will use both); if you change your route, get the orders amended to get the right travel pay.", ["fort-wainwright_in"]),
   ("For your family to travel with you, orders must say concurrent travel and list each family member; each needs Exceptional Family Member screening and command sponsorship. If orders say deferred travel, you go first and start sponsorship after you arrive.", ["fort-wainwright_in"]),
   ("Plan to keep any commute under 30 minutes: Military OneSource defines the acceptable commute as a maximum of 30 minutes measured in extreme adverse weather (cold, ice, fog or snowstorm).", ["fort-wainwright_mi"]),
  ],
  housing=[
   ("Off post: Military OneSource says about one-third of families assigned to the installation live off post for at least part of their tour, and that rentals are harder to get and cost more in summer than in winter.", ["fort-wainwright_mi"]),
   ("Preferred Tenant Program: for soldiers living off post a year or more, participating landlords offer a 3% reduction in market rent and reduced security deposits; ask the Housing Services Office for participants.", ["fort-wainwright_mi"]),
   ("Mobile homes are scarce because they are typically not insulated for extreme weather, and heating costs can rise.", ["fort-wainwright_mi"]),
   ("Pets: most rentals do not accept pets, and TLA is not extended because of pet-housing difficulties; the Housing Services Office can help find pet-friendly places.", ["fort-wainwright_mi"]),
   ("Utilities: Fairbanks-area utilities may waive the usual deposit; ask providers for the monthly average cost of a specific address before you lease.", ["fort-wainwright_mi"]),
   ("Buying: the Alaska Housing Finance Corporation’s HomeChoice workshop is free (907-330-8250).", ["fort-wainwright_mi"]),
  ],
  area=[
   ("Rent for houses is typically higher than for apartments or duplexes, and Military OneSource points to HOMES.mil for current Fairbanks-area listings.", ["fort-wainwright_mi"]),
  ],
  faq=[
   ("What is BAH at Fort Wainwright in 2026?", "{bah_line}"),
   ("How long can I get Temporary Lodging Allowance at Fort Wainwright?", "Military OneSource says TLA must be authorized within your first five days, comes in 10-day increments with proof of an aggressive housing search validated by the Housing Services Office, and is limited to 20 days to secure a rental agreement or housing offer that you can move into within 60 days of sign-in."),
   ("Does the Fort Wainwright Preferred Tenant Program save money?", "Military OneSource says it offers a 3% reduction in market rent and reduced security deposits for soldiers who will live off post for a year or more, through participating providers. Ask the Housing Services Office at 907-353-1190 for the current list."),
  ],
)
GUIDES2["joint-base-langley-eustis"] = dict(
  short="Joint Base Langley-Eustis",
  lead="Joint Base Langley-Eustis has two sides in Virginia’s Hampton Roads, and each has its own housing office, privatized community and lodging. Military OneSource says Fort Eustis soldiers with dependents who apply within 30 days of signing in get the application backdated to their departure date from the last duty station.",
  lead_src=["joint-base-langley-eustis_mi"],
  checklist=[
   ("Fort Eustis: contact the Housing Services Office, 650 Monroe Avenue, Room 114 (757-878-5579), before signing a lease or committing to housing. It is open Monday to Friday, 8 a.m. to 4:30 p.m., closed weekends and federal holidays.", ["joint-base-langley-eustis_mi"]),
   ("Apply for Fort Eustis Family Homes within 30 days of signing in: Military OneSource lists a TRICARE eligibility report showing dependents, DA Form 31, PCS orders with all amendments and, if applicable, dependent-restricted-area orders.", ["joint-base-langley-eustis_mi"]),
   ("Book General Smalls Inn (1700 Madison Avenue, Fort Eustis) for the first 3 to 7 nights; if it is full, ask for a Statement of Non-Availability so finance can reimburse an off-post hotel.", ["joint-base-langley-eustis_mi"]),
   ("In-process in duty uniform with personnel records, all PCS and DA orders, DA Form 31, and medical, dental and financial records; permanent-party soldiers at Fort Eustis report to their unit’s personnel section, which sets the appointment.", ["joint-base-langley-eustis_in"]),
   ("Langley side: Langley Inn has two facilities, Bayview Towers and VQ, with a check-in time of 2 p.m. and check-out at 11 a.m. Register every vehicle at the front desk; weapons are not allowed in quarters and can be stored at the base armory.", ["joint-base-langley-eustis_tl"]),
   ("Arriving at Langley after hours: report to the 24-hour Base Lodging Office, 44 Taylor Road (757-764-4667), then to your gaining unit on the next duty day.", ["joint-base-langley-eustis_in"]),
  ],
  housing=[
   ("Fort Eustis: Fort Eustis Family Homes (Balfour Beatty) has 881 homes, with its office at 126 Madison Avenue (757-369-8335); waits vary by availability, grade and bedrooms needed.", ["joint-base-langley-eustis_mi"]),
   ("Langley: Langley Family Housing is a Hunt Military Community open to all grades, with waits depending on grade and house type. For families with special needs, Hunt works with the Exceptional Family Member Program coordinator.", ["joint-base-langley-eustis_mi"]),
   ("Other privatized options nearby: Yorktown Naval Weapons Station is about five miles from Fort Eustis (Liberty Military Housing), and Langley Family Housing is about 15 miles away.", ["joint-base-langley-eustis_mi"]),
   ("General Smalls Inn has family suites (some pet-friendly), single rooms and six accessible rooms, with reservations by phone at any hour.", ["joint-base-langley-eustis_tl"]),
  ],
  area=[
   ("For short stays, Military OneSource says to use General Delivery mail at Langley (the mailroom is next to the Eagle Room dining facility).", ["joint-base-langley-eustis_tl"]),
  ],
  faq=[
   ("What is BAH at Joint Base Langley-Eustis in 2026?", "{bah_line}"),
   ("When should I apply for family housing at Fort Eustis?", "Military OneSource says incoming personnel should apply within 30 days of signing into Fort Eustis so the application is backdated to the departure date from the last permanent duty station."),
   ("What if General Smalls Inn is full?", "Military OneSource says to ask the inn for a Statement of Non-Availability, which lets finance reimburse a hotel off post, and that the inn may provide a list of lodging sites."),
  ],
)

# ---- part 8
SOURCES2.update(src("joint-base-lewis-mcchord","Joint Base Lewis-McChord"))
GUIDES2["joint-base-lewis-mcchord"] = dict(
  short="Joint Base Lewis-McChord",
  lead="At Joint Base Lewis-McChord, Military OneSource says Liberty Military Housing provides more than 5,370 homes in 23 communities on base. You choose a community when you apply and are placed on the wait list by rank, bedroom need and the communities you chose. The Housing Services Office also runs a Rental Partnership Program for off-base renters.",
  lead_src=["joint-base-lewis-mcchord_mi"],
  checklist=[
   ("Apply for on-base housing on the Liberty Military Housing website (active-duty members or their spouses); you must choose a community at application, and a leasing specialist is at 360-858-6097.", ["joint-base-lewis-mcchord_mi"]),
   ("Keep the Liberty leasing office informed of changes in eligibility, unit, duty and phone numbers; Military OneSource says that is your responsibility.", ["joint-base-lewis-mcchord_mi"]),
   ("Request a housing welcome packet before you arrive by emailing the Housing Services Office at the address on Military OneSource’s housing page.", ["joint-base-lewis-mcchord_mi"]),
   ("Report to the Installation Reception Center, Building 2021 on Pendleton Avenue (Lewis Main), regardless of unit assignment. If you will be late, call 253-967-7004. Expect about five days with the reception detachment.", ["joint-base-lewis-mcchord_in"]),
   ("Bring your orders, a DA Form 31 or IPPS-A absence request, and medical and dental records. Copies are made at the reception desk on arrival. Members returning to active duty after a break in service bring additional papers listed on the page.", ["joint-base-lewis-mcchord_in"]),
   ("Accompanied members arrange their own lodging at Rainier Inn on Lewis Main (253-964-0211) or Candlewood Suites on McChord Field (253-300-9200); both are pet-friendly.", ["joint-base-lewis-mcchord_in","joint-base-lewis-mcchord_tl"]),
  ],
  housing=[
   ("On base: Liberty Military Housing offers more than 5,370 homes in 23 communities, reserved for active-duty service members, with wait times in every community.", ["joint-base-lewis-mcchord_mi"]),
   ("Single soldiers: unaccompanied soldiers E-5 and below are required to live in the barracks and in-process with the barracks manager.", ["joint-base-lewis-mcchord_mi"]),
   ("Off base: the Rental Partnership Program asks landlords to give a discount of 5% or more on monthly rent and to waive security or rent deposits and credit-check fees. Call 253-967-3581.", ["joint-base-lewis-mcchord_mi"]),
   ("The Housing Services Office can brief you on your rights under the Servicemembers Civil Relief Act, answer lease questions, mediate landlord disputes, hold home-buying workshops and counsel BAH-eligible personnel before they sign a lease or purchase.", ["joint-base-lewis-mcchord_mi"]),
  ],
  area=[
   ("To compare utility providers by ZIP code, Military OneSource points to InMyArea.com.", ["joint-base-lewis-mcchord_mi"]),
  ],
  faq=[
   ("What is BAH at Joint Base Lewis-McChord in 2026?", "{bah_line}"),
   ("Who has to live in the barracks at Joint Base Lewis-McChord?", "Military OneSource says unaccompanied soldiers E-5 and below are required to reside in the barracks and in-process with their unit and the barracks manager."),
   ("What is the JBLM Rental Partnership Program?", "Military OneSource says the Housing Services Office program encourages landlords to give 5% or more off monthly rent and to waive security or rent deposits and credit-check fees. Call 253-967-3581 to ask about participating landlords."),
  ],
)

# ---- part 9
def src_as(key, urlslug, name, gov=False):
    d = {
     "%s_mi" % key: ("Military OneSource, %s housing" % name, MO % (urlslug, "housing/housing")),
     "%s_tl" % key: ("Military OneSource, %s temporary housing" % name, MO % (urlslug, "housing/temporary-housing")),
     "%s_in" % key: ("Military OneSource, %s check-in procedures" % name, MO % (urlslug, "base-essentials/check-in-procedures")),
    }
    if gov: d["%s_gh" % key] = ("Military OneSource, %s government housing" % name, MO % (urlslug, "housing/government-housing"))
    return d
SOURCES2.update(src_as("joint-base-elmendorf-richardson","joint-base-elmendorf-richardson-jber","Joint Base Elmendorf-Richardson",True))
SOURCES2.update(src_as("schofield-barracks","schofield-barracks-fort-shafter","Schofield Barracks and Fort Shafter"))
J="joint-base-elmendorf-richardson"; S="schofield-barracks"
GUIDES2[J] = dict(
  short="Joint Base Elmendorf-Richardson",
  lead="At Joint Base Elmendorf-Richardson, Military OneSource says assignment to family housing is not mandatory except for personnel in key and essential positions, but every arriving member not living in the dorms or barracks must visit the Military Housing Office within two duty days for an in-processing brief. Lodging fills quickly in summer, so reserve first.",
  lead_src=[J+"_gh", J+"_tl"],
  checklist=[
   ("Visit the Military Housing Office within two duty days of arrival if you will not live in the dorms or barracks. There are offices at Richardson (Building 600, Room 106, 907-384-3907) and Elmendorf (6346 Arctic Warrior Drive, 907-551-4439).", [J+"_gh"]),
   ("Reserve the North Star Inn (907-552-2454), which provides all temporary lodging on the base, as early as possible; Military OneSource says rooms fill quickly, especially in summer. If it is full, ask for a non-availability letter and a list of off-base hotels within Temporary Lodging Allowance (TLA) rates.", [J+"_tl"]),
   ("Apply for TLA paperwork through the Military Housing Office (907-551-4439). Claims are submitted every 15 days and need proof of aggressive house hunting, with a minimum of one home viewing per day.", [J+"_tl"]),
   ("Know the TLA limit: the maximum is 45 days, an extension is not automatic, and requests beyond 45 days go through the Military Housing Office. TLA is not authorized for single, unaccompanied service members.", [J+"_tl"]),
   ("Soldiers report directly to the Army reception point at Building 55, Chilkoot Avenue, basement Room 011, a 24-hour sign-in (907-903-4281). Military OneSource says soldiers using TLA must sign in there or they will not be reimbursed.", [J+"_in",J+"_tl"]),
   ("Call your sponsor as soon as you land at Ted Stevens International Airport in Anchorage, and tell them your arrival time before you fly.", [J+"_in"]),
   ("Apply to Aurora Military Housing before you arrive on its website, or call 907-753-1023; Military OneSource says there is no pet, move-in or application fee.", [J+"_mi"]),
  ],
  housing=[
   ("On post: Aurora Military Housing offers privatized homes in 19 neighborhoods with over 60 floor plans, appliances included, a covered-utility program, a deployed-spouse program, snow removal and 24/7 maintenance.", [J+"_mi"]),
   ("The Military Housing Office runs the Rental Partnership Program for off-base rentals, a volunteer realtor program, weekly home buying and selling seminars on Wednesdays at 1 p.m., and loaner furniture for 90 days while your household goods are in transit.", [J+"_gh"]),
   ("Barracks: Soldiers E-1 through E-5 traveling without dependents can get barracks rooms; E-6 and above must reserve lodging.", [J+"_in"]),
   ("Pets in lodging: a limited number of pet-friendly family rooms are first come, first served for an extra $10 per night; otherwise ask for a local kennel list or a non-availability letter.", [J+"_tl"]),
  ],
  area=[
   ("The base has two family camping areas, one of them open year-round, on a first-come, first-served basis.", [J+"_tl"]),
   ("The North Star Inn does not accept guest mail; Military OneSource lists separate General Delivery (HOLD) addresses for Army and for Air Force and Space Force personnel.", [J+"_tl"]),
  ],
  faq=[
   ("What is BAH at Joint Base Elmendorf-Richardson in 2026?", "{bah_line}"),
   ("How long does Temporary Lodging Allowance last at JBER?", "Military OneSource says the maximum is 45 days, an extension is not automatic, and claims are submitted every 15 days with proof of at least one home viewing a day. TLA is not authorized for single, unaccompanied service members."),
   ("Is on-post housing required at JBER?", "Military OneSource says assignment to family housing is not mandatory except for key and essential positions, but you must still visit the Military Housing Office within two duty days of arrival unless you live in the dorms or barracks."),
  ],
)
GUIDES2[S] = dict(
  short="Schofield Barracks",
  lead="Schofield Barracks is in a very high cost area, and Military OneSource’s Schofield page says all military personnel with dependents are required to report to their Housing Services Office before renting, leasing, purchasing or arranging housing on or off post. Army housing on Oahu has been privatized since 2004 through Island Palm Communities.",
  lead_src=[S+"_mi"],
  checklist=[
   ("If you have dependents, report to your Housing Services Office within five days of arrival and before renting, leasing, buying or making any housing arrangement; Military OneSource’s Schofield page says this is required. The page’s family-housing section also says you must report to housing within seven workdays of your reporting date even if you do not plan to live on post.", [S+"_mi"]),
   ("Contact the Housing Service Office (808-787-7700) about Temporary Lodging Allowance, lodging and government housing; it gives you a list of TLA-approved facilities.", [S+"_tl"]),
   ("Apply at the regional leasing office: North at Building 950, 215 Duck Road on Schofield Barracks (808-275-3700), or South at Building 1004, 111 Seventh Street on Fort Shafter (808-275-3800). Your application is processed and you are added to the waiting list.", [S+"_mi"]),
   ("When you land at Daniel K. Inouye International Airport, go to the Army replacement liaison desk in front of Baggage Claim 19 to begin in-processing.", [S+"_in"]),
   ("Hand-carry: PCS orders with all amendments, command sponsorship orders for family members, DA Form 31, your travel itinerary, your personnel file and medical and dental records.", [S+"_in"]),
   ("Budget for move-in: Military OneSource says landlords generally want the first month’s rent plus a deposit of one month’s rent, utilities are usually not included, and utility deposit waivers are usually granted to military personnel.", [S+"_mi"]),
   ("Contact the housing office for a pre-move assessment on what to ship and what to store: Hawaii is a full weight allowance area, but Military OneSource notes housing there is generally smaller than in the continental U.S.", [S+"_mi"]),
  ],
  housing=[
   ("Island Palm Communities’ North region covers Schofield Barracks, Wheeler Army Airfield and Helemano Military Reservation; the South region covers Fort Shafter, Tripler Army Medical Center, Aliamanu Military Reservation and Red Hill.", [S+"_mi"]),
   ("Military OneSource reports 7,910 homes in total and says there is normally a wait on every waiting list, so check with the leasing office for current availability.", [S+"_mi"]),
   ("Wait times: for enlisted families from immediate to one month, with officer housing up to the 60-day TLA limit; June through August is the peak season.", [S+"_mi"]),
   ("Pets: homes are pet-friendly with a two-pet maximum per family and certain restrictions, plus one-time move-in and move-out charges.", [S+"_mi"]),
   ("There are no mobile homes in Hawaii.", [S+"_mi"]),
   ("The Inn at Schofield is a pet-friendly lodging option with single and double rooms; ADA rooms can be requested at 808-839-2336.", [S+"_tl"]),
  ],
  area=[
   ("If you marry before your PCS, you must inform your command and follow the sponsorship procedures exactly; Military OneSource strongly recommends reporting unaccompanied to avoid financial hardship, with sponsorship questions to 808-787-1337.", [S+"_in"]),
  ],
  faq=[
   ("What is BAH at Schofield Barracks in 2026?", "{bah_line}"),
   ("How soon must I visit housing after arriving at Schofield Barracks?", "Military OneSource’s Schofield page says all military personnel with dependents are required to report to their Housing Services Office within five days of arrival, before renting, leasing or buying. Its family-housing section also says you must report to housing within seven workdays of your reporting date even if you do not plan to live on post."),
   ("Who manages family housing at Schofield Barracks?", "Military OneSource says Island Palm Communities manages privatized Army family housing on Oahu, in a North region (including Schofield Barracks) and a South region (including Fort Shafter), and that Army housing on the island has been privatized since 2004."),
  ],
)
