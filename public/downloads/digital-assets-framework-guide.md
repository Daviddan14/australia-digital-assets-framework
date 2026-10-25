# The Digital Assets Framework Act, in plain words

_What Australia’s new platform licensing law means for issuers, for holders, and for Tokeniser on Redbelly Network_

Sources checked 25 October 2026.

> **General information, not legal advice.** This guide describes an Australian law and public documents in everyday language. It is not legal, financial or tax advice, it does not recommend any product, and it does not tell any business whether it needs a licence. Several ASIC documents used here are drafts released for consultation, so the final versions may differ [3]. ASIC’s own draft guide says it is not legal advice and that anyone unsure should seek legal or regulatory advice [5].

Numbers in square brackets point to the source list at the end. Text under **What the law says** and **What the companies say** reports the sources; text under **What this means** and **Not settled** is analysis.

## The short version

**What does the Act do?** It treats two kinds of custody business as financial products. In a **digital asset platform**, a business keeps digital tokens on behalf of others. In a **tokenised custody platform**, a business looks after a real asset and issues one token that stands for it [1].

**When does it start?** On **8 April 2027** [1][4]. A business already running such a platform has until **7 October 2027** to apply for a licence, and can keep operating while ASIC decides [4].

**Who needs a licence?** The operator of the platform, unless an exemption applies [5]. Small digital asset platforms are exempt if they hold no financial products, handle no more than $10 million of transactions a year, keep each client’s holdings within $5,000 (valued when tokens are added), and notify ASIC [1].

**What changes for issuers?** Less than many expect. When a fund keeps its primary register of unit holders on chain, ASIC’s draft guide would usually treat it as a managed investment scheme rather than a tokenised custody platform [5]. The new rules bite hardest on whoever holds investors’ tokens or assets.

**Where does Redbelly fit?** Its identity and eligibility tools match the Act’s requirement for transparent, non-discriminatory eligibility rules [1][10]. Whether the network counts as public digital token infrastructure, which sits outside licensing, is not settled [1][4].

## 1. What the Act is, and why it exists

_A short law with a large reach. It adds two financial products and leaves most of the detail to ASIC._

### What the law says

Its full name is the Corporations Amendment (Digital Assets Framework) Act 2026, numbered No. 38 of 2026 [1]. Parliament passed it on 1 April 2026 and it received Royal Assent on 8 April 2026 [1][4].

It amends the law on corporations and financial services: the Corporations Act 2001, and also the ASIC Act [1].

Its central change is to add two new kinds of **financial product**: a digital asset platform and a tokenised custody platform, in each case unless the platform is a managed investment scheme [1]. If a facility is one of these and no exemption applies, its operator needs an Australian financial services (AFS) licence [5].

When the Bill was introduced, the Government said it was meant to help unlock innovation and protect Australians investing in digital assets [2]. It pointed to a gap: a business could look after any amount of its clients’ digital assets with no financial-law safeguards in place, and collapses overseas had shown what weak oversight costs [2].

ASIC describes the Act as addressing regulatory gaps and uncertainty about digital assets, with the aim of fostering innovation, competition and growth [4]. Its Commissioner summed up ASIC’s approach as “same activity, same risk, same regulatory outcome” [3].

### What this means

Read together, the definitions point to one idea: **the licence follows custody**. A business comes into the new rules by holding tokens, or holding real assets behind tokens, on behalf of other people. Using a blockchain, issuing a token or keeping your own tokens is not, by itself, what the definitions describe [1][5].

The Act sets the frame and leaves the working detail to ASIC standards, ASIC guidance and Government regulations that are still being written. Most of that detail is due in 2027 [4][5].

## 2. Six terms that do most of the work

_The Act turns on a handful of defined words. These are the ones worth knowing._

### What the law says

**Key terms in the Act**

| Term | What it means | Section |
| --- | --- | --- |
| Digital token | An electronic record that someone can factually control: they can move it, block others from moving it, and prove they can do both [1]. | s 761GB |
| Possess | What counts is what a person can do in fact, not their legal rights [1]. A person does not jointly possess a token if they need someone else’s cooperation and that other person can act alone [1]. | s 761GB(3), s 86 |
| Digital asset platform (DAP) | A facility where an operator possesses digital tokens for or on behalf of another person [1]. | s 761GC |
| Tokenised custody platform (TCP) | A facility where an operator holds an asset other than money and creates a single token for each asset. Holding the token gives a right to redeem the asset or direct its delivery [1]. A TCP cannot also be a DAP [1]. | s 761GD |
| Public digital token infrastructure (PDTI) | Open source, publicly accessible protocols that work without discretion, let any person contribute to running the network, and do not depend on one critical participant [1]. PDTI is not a financial product [1]. | s 9E, s 765A |
| Platform rules | The operator’s rules for a licensed platform. They must include transparent and non-discriminatory criteria for who can become a client [1]. | s 912BG |

### What this means

“Possess” carries much of the weight. If investors alone control the keys to their tokens, nobody else possesses those tokens for them, so that part of an arrangement does not look like a DAP. If a business controls the keys for them, it may well be one [1].

## 3. Licences, who is in and who is out

_The operator of a platform needs one, unless an exemption fits. Several exemptions do._

### What the law says

If a facility is a DAP or TCP and no exemption applies, the operator must hold an AFS licence that authorises it to issue that type of platform [5]. ASIC says related services, such as dealing in or advising about DAPs and TCPs, will also need a licence [4].

The platform is a financial product in its own right, separate from the tokens or assets held through it [5]. Whether a token is itself a financial product is a different question, which ASIC answers in its existing guide, INFO 225 [5].

**Small digital asset platforms.** The Act exempts the issue of a DAP when four conditions are all met: none of the group’s platforms holds financial products; transactions through them total no more than $10 million over the last 12 months; whenever a token is added for a client, the client’s holdings across the platforms total no more than $5,000, with each token valued at the time it was added; and the operator has lodged a notice with ASIC [1]. The Government called these “smaller, low-risk platforms” [2].

Regulations can raise those amounts [1], and ASIC’s draft guide says the tests will rise with inflation [5]. The exemption is written for digital asset platforms only [1].

**Pointing people to a platform.** A business that only tells people a DAP or TCP exists, or arranges for them to use one, does not need a licence for that if it does so in the ordinary course of its business and those services are not a significant part of the business [1].

**Validators.** Running consensus on public digital token infrastructure is not a financial service, and the infrastructure itself is not a financial product [1].

**Exemptions still to come.** ASIC expects Government regulations to extend some existing custody exemptions to DAPs and TCPs, subject to Government processes [5]. An exemption from licensing does not stop an arrangement being a DAP or TCP [5].

**Arrangements outside the definitions.** Merely possessing tokens is not enough; they must be possessed for a client [5]. A facility may also fall outside both definitions if the client cannot direct how the assets are dealt with [5], although it may then be another kind of financial product [5].

#### A rough self-check

1. Do you, or someone acting for you, possess digital tokens for another person? That describes a DAP [1].
2. Do you hold an asset other than money and create one token for it that lets the holder redeem it? That describes a TCP [1].
3. Does an exemption fit, such as the small platform exemption or the advise and arrange exemption [1]?
4. If not, the operator needs an AFS licence [5]. A business already operating must apply by 7 October 2027 [4].

_This is a summary to help you find the right questions, not a legal test. ASIC’s draft guide says that if you are unsure, seek legal or regulatory advice [5]._

### What this means

**Where some common roles are likely to sit (this guide’s reading)**

| Role | Likely position | Why |
| --- | --- | --- |
| An exchange or app that holds customers’ tokens | Likely a DAP, so a licence is needed unless an exemption fits | It possesses tokens for clients [1][5] |
| A business that holds gold bars and issues one redeemable token per bar | Likely a TCP | An asset other than money, one token each, redeemable [1] |
| A token for a mixed basket of assets | Not a TCP on ASIC’s draft view; other rules may apply | ASIC’s example is a token for 1 gram of gold and 1 kg of silver [5] |
| A wallet app where only the user controls the keys | Not a DAP on that basis alone | Nobody else possesses the tokens [1] |
| A fund that issues its units as tokens and keeps the unit holder register on chain | Generally a managed investment scheme, not a TCP, on ASIC’s draft view | ASIC’s note on native tokenisation [5] |
| A validator on a public network | Not providing a financial service, if the network is PDTI | Consensus on PDTI is excluded [1] |
| A website that refers users to a platform as a minor sideline | May fit the advise and arrange exemption | Not a significant part of the business [1] |

## 4. The dates that matter

_Royal Assent in April 2026, a year’s wait, then six months for existing businesses to apply._

### What the law says

| Date | What happens |
| --- | --- |
| 26 November 2025 | The Bill is introduced, and the Minister’s second reading speech is made in the House of Representatives [1][2] |
| 5 February 2026 | Second reading speech in the Senate [1] |
| 1 April 2026 | Parliament passes the Act [4] |
| 8 April 2026 | Royal Assent [1] |
| April 2026 | ASIC publishes its implementation roadmap [3] |
| 30 June 2026 | Original deadline to apply for a licence under ASIC’s no-action position for businesses already covered by current law [7] |
| 30 September 2026 | Extended deadline for that no-action position [3] |
| 15 October 2026 | ASIC releases Consultation Paper 392 with its draft guide and standards [4] |
| 27 November 2026 | ASIC’s consultation closes at 5pm AEDT [3][4] |
| March 2027 | ASIC plans to publish its final instruments and guidance [4] |
| 8 April 2027 | The Act commences and licence applications open [1][4] |
| 8 April to 7 October 2027 | Six-month transition period for businesses already operating [1][4] |
| From 8 October 2027 | Operators need a DAP or TCP authorisation unless an exemption applies [4] |

During the transition period, a business already providing these services can apply to ASIC. If it does, the new rules do not apply to that service until the day after ASIC decides the application [1]. If it does not apply in time, the new rules apply as soon as the transition period ends [1].

ASIC is considering publishing a list of firms that apply by 7 October 2027, so the public can see who may keep operating while their application is decided [4]. ASIC says it has already recorded over 140 applications from businesses seeking to provide digital asset-related financial services [3].

#### 8 April or 9 April 2027?

Some documents give 9 April 2027 as the start date, including ASIC’s roadmap, an earlier ASIC news item and the TASK-30 brief [6][7][20].

The Act sets its start as the day after the end of the 12 months beginning on the day of Royal Assent [1]. Royal Assent was given on 8 April 2026 [1], so the 12 months run to 7 April 2027 and the Act starts on 8 April 2027. The commencement table records 8 April 2027 [1]; that column is not formally part of the Act [1], but it matches the rule. ASIC’s October 2026 documents also use 8 April 2027 [3][4]. This guide uses 8 April 2027.

### What this means

ASIC says the Act provides for an 18-month implementation timeline [6]. On this guide’s reading, that is the 12 months before the Act starts plus the six-month transition [1].

## 5. Issuers on Tokeniser, and what actually changes for them

_For many issuers, less than expected. The new rules mostly land on whoever holds tokens or assets for investors._

### What the law says

Tokenising an asset does not by itself create a TCP. ASIC’s draft guide says not every arrangement that tokenises an existing asset is one [5]. Its examples include a token for a mixed pool of assets, and an arrangement where the operator makes investment decisions for the client [5].

For funds, ASIC’s draft view is direct: where each token is a unit in a unit trust and the blockchain is the primary register of unit holders, the arrangement would generally be a managed investment scheme rather than a TCP [5]. A platform that is a managed investment scheme is not one of the two new products [1].

Where a TCP is used, its underlying assets can include financial products, including tokens that are financial products [5]. For a TCP to stay outside the managed investment scheme rules, the Act requires, among other things, that all its underlying assets are of the same class and that a token is only as divisible as the asset can be physically delivered in parts [1].

An issuer that makes a securities offer needing a disclosure document through a DAP or TCP must promptly tell the platform operator and each custodian about key events [1], such as a supplementary or replacement document being lodged [1]. The disclosure document does not have to describe the platform itself [1].

Any licensed platform must have platform rules with transparent, non-discriminatory eligibility criteria, and must tell potential clients whether and how their purchases will be recorded in any legal or technical register [1].

### What the companies say

Tokeniser says it operates on Redbelly Network, which it calls Australia’s public digital token infrastructure [16], and that funds can run their registry and investor lifecycle on it [19].

It describes its product as “engineered to align with Australia’s Digital Assets Framework, operating under your existing licence” [18]. It says trades that fail an eligibility check do not proceed [18], and that eligibility, identity and the target market determination are enforced at the point of transfer [17].

Asked in its technology FAQ whether a new licence is needed to use the infrastructure, Tokeniser answers “No”, saying the protocol layer is designed to sit outside markets, clearing and settlement, and custody licensing [17]. These are the company’s own statements about its product.

### What this means

For a fund manager that uses Tokeniser to keep its unit register on chain, ASIC’s draft view suggests the fund remains a managed investment scheme [5]. The rules that already govern the fund keep applying, and the new platform regime is not the main question for the fund itself.

The new regime matters at the edges. If the manager, Tokeniser or a wallet provider controls investors’ tokens for them, that party could be operating a DAP. If someone holds a separate asset and issues one redeemable token for it, that could be a TCP [1].

**Questions an issuer may want to put to its own advisers**

- Who controls the private keys for investors’ tokens: the investor, the issuer, Tokeniser or a custodian?
- Is the on-chain record the legal register of holders, or a copy of a register kept elsewhere?
- Does anyone hold an underlying asset and issue one redeemable token for it?
- Who makes the investment decisions?
- Are the eligibility rules transparent and non-discriminatory, and do they match the fund’s target market?
- How will secondary trading happen, and who runs that venue?

### Not settled

The Tokeniser pages this guide relied on do not say who controls investors’ keys, so whether any part of the service is a DAP cannot be told from them. Its “no new licence” answer also rests on Redbelly being public digital token infrastructure, which the next section shows is not settled.

## 6. Redbelly against the new rules, what fits and what is open

_Strong on identity and eligibility. The open question is whether the network itself counts as public digital token infrastructure._

### What the companies say

Redbelly describes Receptor as its native digital identity and verifiable credential protocol [10]. Its verifier module is used to “define eligibility criteria” and check users’ credentials [10], so that only eligible users can access particular products and services [10].

Every participant must prove who they are before gaining access to the network [8]. For an access credential, a user proves through an accredited issuer that they hold a valid passport, checked biometrically [9]. Businesses can be verified too [8].

The Eligibility SDK lets developers run checks such as age and KYC using privacy-preserving proofs [11], and the onboarding SDK covers wallet authentication, KYC and on-chain permission setup [12].

Redbelly states that “Redbelly is Digital Public Token Infrastructure” [14] and that its finality means transactions cannot be reversed [14]. It was selected for the Reserve Bank of Australia’s Project Acacia pilot [15].

**The new rules beside Redbelly’s design**

| What the rules call for | What Redbelly offers | This guide’s reading |
| --- | --- | --- |
| Platform rules with transparent, non-discriminatory eligibility criteria [1] | Verifiable credentials and a verifier that defines and checks eligibility at the point of trade [10][14] | **Lines up.** The tools can enforce criteria. The operator still has to write criteria that are transparent and non-discriminatory; a tool does not make them so. |
| Platform rules that set out the settlement method [1] | Deterministic finality [14] | **Lines up.** Final settlement gives the operator something definite to describe. The duty to describe it stays with the operator. |
| Knowing who is on the platform, so eligibility can be applied | Identity proof for every participant, with passport and biometric checks [8][9] | **Lines up.** It is a starting point only. Whatever obligations a licensee has stay with the licensee. |
| Saying whether and how purchases are recorded in a legal or technical register [1] | A shared ledger, with Tokeniser offering on-chain registries [19] | **Partly.** The chain can be the technical record. Whether it is also the legal register is the issuer’s choice, and that choice affects how ASIC may classify a fund. |
| Asset-holding standards on safeguarding, records and reconciliation [1] | Not described in the Redbelly pages this guide relied on | **Not covered.** Custody is done by whoever controls the keys, not by the network. |
| Being public digital token infrastructure, outside licensing [1] | Redbelly says it is PDTI; Tokeniser says it is designed to meet the three statutory tests [14][17] | **Not settled.** See below. |

### Not settled

The Act’s second test asks whether the protocols “permit any person to contribute” to running the infrastructure [1]. ASIC’s draft guidance says infrastructure where “only select persons” can conduct consensus is not PDTI, and that this could include KYC restrictions; minimum staking or hardware requirements that apply to everyone are unlikely to count against it [4]. ASIC gives public permissionless blockchains as an example of PDTI [4].

On Redbelly’s own pages, node operator applicants “will be selected based upon their previous experience, location and commitment to the Redbelly Project” [13], and applications were closed when this guide checked [13]. Every network participant must also prove their identity [8]. The 100,000 RBNT stake applies to all nodes [13], which is the kind of universal threshold ASIC’s draft says is unlikely to matter.

Two different things are being gated here. Identity checks for users decide who can transact; selection of node operators decides who can help run the network. The PDTI test is about the second, so node selection is the closer fit to ASIC’s concern, while the KYC point could matter too because ASIC names it.

No regulator has said whether Redbelly is PDTI in any source this guide found, and ASIC’s guidance is still a draft. ASIC also says licensing is assessed at a point in time, not on a future expected state [4], so the answer could change as the network’s design changes.

Why it matters: if Redbelly is PDTI, running it is not a financial service and the network is not a financial product [1]. If it is not, activities on and around it would have to be assessed under the ordinary rules. That would not mean anyone is acting unlawfully. It means the answer is not yet known.

## 7. What holders get from the new rules

_The protections attach to platforms that hold assets for you._

### What the law says

A licensed operator must give a retail client a DAP/TCP Guide before issuing the platform to them [1]. It must include what a person would reasonably need to understand the platform and its risks [1], and the method and extent of all charges [1].

The platform rules act as a contract under seal between the licensee and each client [1].

ASIC’s standards must require money held under a platform, other than its underlying assets, to be held in trust for clients [1]. They must not stop an operator holding many clients’ tokens in one wallet if its own accounts identify which tokens are each client’s [1].

The Government listed access to dispute resolution and compensation among the core obligations that come with the licence [2].

### What this means

A holder who keeps their own keys is not a client of any platform for those tokens, so these protections do not apply to them. The protections matter when someone else holds the keys.

## 8. What is still open

_Several pieces arrive between now and April 2027._

### What this means

- ASIC’s final guide and standards, planned for March 2027 [4].
- Government regulations for further exemptions [5].
- The financial requirements for licensees, including net tangible assets, which are part of ASIC’s consultation [3].
- Whether identity-gated networks with selected node operators, such as Redbelly, count as PDTI [4].
- Whether ASIC will publish a list of businesses that applied in time [4].
- Anyone can comment on ASIC’s proposals until 5pm AEDT on 27 November 2026 [3].

## 9. How this guide was checked

_Every statement of fact can be traced to a passage in a saved copy of its source._

### What this means

Every factual statement cites the passage it relies on, and the [source list](sources.html) quotes each passage word for word with a link to the source.

Primary sources come first: the Act as made, then the Government’s own statement and ASIC’s papers. Company pages are used only to report what the companies say about themselves.

Each source was saved as plain text on 25 October 2026 with a SHA-256 fingerprint. A script checks that every quoted passage appears in its saved copy, that every statement of law cites a source, and that no sentence says Redbelly, Tokeniser or any issuer is licensed or compliant.

The Explanatory Memorandum to the Bill is not cited directly because its host blocked automated download. Where ASIC quotes it, this guide cites ASIC.

Text under “What this means” and “Not settled” is this guide’s analysis. Text under “What the law says” and “What the companies say” reports the sources.

## Sources

**[1] Corporations Amendment (Digital Assets Framework) Act 2026 (No. 38, 2026), as made**  
Federal Register of Legislation · <https://www.legislation.gov.au/C2026A00038/asmade/text>  
Saved copy: `evidence/snapshots/act.txt`

- “No. 38, 2026” (Title page)
- “[Assented to 8 April 2026]” (Long title)
- “The day after the end of the period of 12 months beginning on the day this Act receives the Royal Assent.” (Section 2, commencement table)
- “8 April 2027” (Section 2, commencement table, column 3)
- “Any information in column 3 of the table is not part of this Act.” (Subsection 2(2))
- “An Act to amend the law relating to corporations and financial services, and for related purposes” (Long title)
- “Part 7—Amendment of the ASIC Act” (Schedule 1, Part 7)
- “House of Representatives on 26 November 2025 Senate on 5 February 2026” (End note)
- “the person can (whether alone or jointly with one or more other persons): (a) transfer the electronic record; and (b) exclude one or more other persons from transferring the electronic record; and (c) demonstrate that the person can do the things in paragraphs (a) and (b).” (New s 761GB(1) and (2))
- “it only matters what the person can do as a matter of fact rather than law” (New s 761GB(3))
- “the person needs the express cooperation of another person in order to be able to satisfy paragraph 761GB(2)(a), (b) or (c) for the electronic record; and (b) that other person can unilaterally satisfy that paragraph for the electronic record.” (New s 86(3))
- “A digital asset platform is a facility under which: (a) a person (the operator) possesses one or more digital tokens (the underlying assets); and (b) the underlying assets are so possessed for or on behalf of another person” (New s 761GC(1))
- “a person (the operator) identifies one or more assets other than money (the underlying assets); and (b) for each underlying asset: (i) the operator creates a single digital token; and (ii) possessing the digital token confers a right to redeem, or direct the delivery of, the underlying asset” (New s 761GD(1))
- “Despite subsection (1), a tokenised custody platform cannot be a digital asset platform.” (New s 761GC(4))
- “(la) a digital asset platform, unless the platform is a managed investment scheme; (lb) a tokenised custody platform, unless the platform is a managed investment scheme;” (New s 764A(1)(la) and (lb))
- “(iv) all of the underlying assets must belong to the same class of asset; and (v) the digital token created for an underlying asset can only be divisible to the same extent that the underlying asset is reasonably capable of being divisible in a way that each part can be physically delivered;” (New para (md) of the definition of managed investment scheme, s 9)
- “(a) the protocols are a set of open source and publicly accessible standards for transmitting, processing and recording electronic records in a non-discretionary manner; (b) the protocols permit any person to contribute to the integrity, functionality and reliability of the infrastructure by conducting activities involving transmitting, processing and recording such electronic records; (c) the protocols are not reliant on any participant having a role so critical that the transmitting, processing, or recording of such electronic records cannot happen without the participant;” (New s 9E(2))
- “(xa) public digital token infrastructure;” (New s 765A(1)(xa))
- “None of the following is the provision of a financial service: (a) a person's conduct done in the course of work of a kind ordinarily done by clerks or cashiers; (b) conducting activities described in paragraph 9E(2)(b) (about consensus activities involving public digital token infrastructure).” (New s 766A(3))
- “(i) no financial products are held under any digital asset platform (a relevant platform) issued by a member of the person's closely-related group; and (ii) the total value of transactions in the last 12 months through all relevant platforms does not exceed $10 million; and (iii) whenever a digital token begins to be an underlying asset of a relevant platform for a client (whether directly or through a nominee), the total of the entry values of all underlying assets of all relevant platforms for the client does not exceed $5,000; and (iv) the person has lodged with ASIC, in the prescribed form, notice that the person intends to rely on the exemption in this paragraph for digital asset platforms;” (New s 911A(2)(ja))
- “An amount in the exemption under paragraph (2)(ja) is taken to be replaced by any higher amount prescribed in, or worked out using a method prescribed in, regulations made for the purposes of this subsection.” (New s 911A(4B))
- “(i) advising another person about the existence of a digital asset platform or tokenised custody platform; (ii) arranging for another person to use a digital asset platform or tokenised custody platform; and when the person provides the service: (iii) the person does so in the ordinary course of the person's business; and (iv) such services are not a significant part of the person's business;” (New s 911A(2)(jb))
- “possessing and safeguarding the underlying assets of the platforms; or (ii) recordkeeping, reconciliation and reporting for the underlying assets of the platforms; or (iii) using the underlying assets of the platforms;” (New s 912BE(1))
- “requires any money held under a digital asset platform or tokenised custody platform (that is not an underlying asset of the platform) to be held in trust for, or on behalf of, a client under the platform” (New s 912BE(2)(b))
- “in one wallet; if the licensee's internal accounting system identifies the digital tokens as the client's” (New s 912BE(2)(e))
- “transparent and non-discriminatory eligibility criteria for identifying who can become a client under the platform” (New s 912BG(1)(a))
- “the method (the settlement method) for executing client instructions to execute and settle transactions involving the acquisition or disposal of underlying assets of the platform” (New s 912BG(1)(c))
- “whether and how a client's acquisition of an underlying asset of the platform will be recorded in any legal or technical register” (New s 912BG(1)(d)(v))
- “The platform rules of a digital asset platform or tokenised custody platform have effect as a contract under seal: (a) between the licensee and each client under the platform” (New s 912BG(2))
- “The licensee must, before issuing a digital asset platform or tokenised custody platform to a person as a retail client under the platform, give the person a DAP/TCP Guide” (New s 1020AN(1))
- “understand the nature of the platform and any risks associated with participation in the platform” (New s 1020AO(1))
- “understand the method and extent of all charges associated with the platform” (New s 1020AO(1)(c))
- “must promptly notify the operator of the platform, and each custodian for the platform, if any of the following events happens” (New s 741A(1))
- “Nothing in Part 6D.2 or 6D.3 requires a disclosure document for offers of securities under a digital asset platform or tokenised custody platform to include information about: (a) the platform” (New s 741A(2))
- “Division 1—Main amendments Corporations Act 2001” (Schedule 1, Part 1, Division 1)
- “a supplementary or replacement document is lodged with ASIC in relation to the disclosure document” (New s 741A(1)(d) and (f))
- “transition period means the 6-month period starting on commencement.” (New s 1730)
- “the DAP/TCP amendments do not apply in relation to the provision of the service until the day after the day ASIC makes a decision described in that paragraph in response to the application.” (New s 1732(3))
- “If the responsible person fails to apply during the transition period, then the DAP/TCP amendments will start to apply immediately after the transition period.” (Note to new s 1732(3))

**[2] New digital asset laws to unlock innovation and safeguard investment (media release, 26 November 2025)**  
Treasury Ministers · <https://ministers.treasury.gov.au/ministers/daniel-mulino-2025/media-releases/new-digital-asset-laws-unlock-innovation-and-safeguard>  
Saved copy: `evidence/snapshots/treasury-mr.txt`

- “The Albanese Government has introduced new legislation to the Parliament to help unlock innovation and protect Australians investing in digital assets.” (Opening paragraph)
- “Currently, businesses can hold unlimited client digital assets without financial law safeguards. Recent collapses overseas have shown the consequences of inadequate oversight.” (Body)
- “Providing accessible dispute resolution and compensation if things go wrong.” (List of core obligations)
- “Smaller, low‑risk platforms – those holding less than $5,000 per customer and facilitating less than $10 million in transactions per year – will be exempt” (Body)

**[3] 26-245MR ASIC consults on implementation of new digital asset laws**  
ASIC · <https://www.asic.gov.au/about-asic/news-centre/find-a-media-release/2026-releases/26-245mr-asic-consults-on-implementation-of-new-digital-asset-laws>  
Saved copy: `evidence/snapshots/asic-26-245mr.txt`

- “ASIC has today commenced consultation on guidance and standards to implement new laws for digital asset platforms and tokenised custody platforms commencing on 8 April 2027.” (Opening paragraph)
- “Our approach is based on the principle of “same activity, same risk, same regulatory outcome” to align Australia with the approach of comparable overseas jurisdictions.” (Quote from ASIC Commissioner Alan Kirkland)
- “apply for (or vary) an Australian financial services licence, provide customer disclosure documents and platform rules, and comply with asset-holding standards, transactional and settlement standards, and net tangible asset requirements, where relevant.” (Body)
- “ASIC’s consultation is open until 5pm AEDT 27 November 2026.” (Body)
- “In April 2026, ASIC set out its roadmap for implementing the new regime to support industry.” (Body)
- “In June 2026, ASIC clarified and expanded the full scope and conditions of its no-action position and extended the deadline to 30 September 2026” (Body)
- “ASIC has recorded over 140 applications from businesses seeking to provide digital asset-related financial services.” (Body)

**[4] Consultation Paper 392, Digital asset law reform implementation: Proposed standards and guidance (15 October 2026)**  
ASIC · <https://download.asic.gov.au/media/0pqj5lgc/cp392-published-15-october-2026.pdf>  
Saved copy: `evidence/snapshots/asic-cp392.txt`

- “On 1 April 2026, Parliament passed the DAF Act. It received Royal Assent on 8 April 2026.” (Paragraph 1)
- “The DAF Act addresses regulatory gaps and consequent uncertainty regarding digital assets, and some infrastructure and arrangements that support them. It aims to foster innovation, enhance competition and growth, and strengthen Australia’s position in the global digital asset ecosystem.” (Paragraph 3)
- “The DAF Act commences on 8 April 2027. If you are currently operating a platform that will be considered a DAP or TCP on 8 April 2027, you must apply for an Australian financial services (AFS) licence or variation by 7 October 2027. You can continue operating while we assess your application.” (Background, key points)
- “15 October 2026 Consultation paper released” (What will happen next, stage 1)
- “27 November 2026 Feedback due on the consultation paper” (What will happen next, stage 2)
- “March 2027 Publication of instruments and guidance” (What will happen next, stage 4)
- “8 April 2027 The DAF Act commences and licence applications open” (What will happen next, stage 5)
- “7 October 2027 Close of transition window for existing firms to make a licence application (new application or variation)” (What will happen next, stage 6)
- “from 8 October 2027, DAP and TCP operators (and certain other financial services providers) will require an appropriate DAP or TCP-related licence authorisation to carry on a financial services business in Australia, unless covered by a licensing exemption” (Paragraph 39)
- “Related financial services will also require an AFS licence (e.g. to deal in other than issue, or provide advice about DAPs and TCPs).” (Paragraph 41)
- “we are considering publishing a list of firms that apply for or vary an AFS licence by 7 October 2027 (and can therefore continue operating until their application is decided).” (Paragraph after proposal A3)
- “This includes public permissionless blockchain networks as well as decentralised applications on those networks.” (Proposed guidance on PDTI)
- “Infrastructure where ‘only select persons became able to conduct consensus activities’ is not PDTI (paragraph 1.340). This could include restrictions for KYC requirements, but is unlikely to include consideration of base hardware requirements or minimum staking thresholds if those apply universally” (Proposed guidance on PDTI)
- “an entity’s licensing requirements are assessed at a point in time, and not based on any future expected state.” (Proposed guidance on PDTI)

**[5] Attachment 1 to CP 392: draft Regulatory Guide 000, Digital asset platforms and tokenised custody platforms**  
ASIC · <https://download.asic.gov.au/media/a3cpo5ds/attachment-1-to-cp392-published-15-october-2026.pdf>  
Saved copy: `evidence/snapshots/asic-draft-rg.txt`

- “This guide does not constitute legal advice.” (Disclaimer)
- “If you are unsure, seek legal or regulatory advice.” (Figure 1, final step)
- “INFO 225 explains when a digital asset or related arrangement is itself a financial product and whether an exemption or exclusion applies.” (RG 000.23)
- “A DAP or TCP is a financial product, separate from any digital asset or underlying asset made available or held through the DAP or TCP.” (RG 000.20)
- “Not every arrangement that tokenises or digitally represents an already existing asset is a TCP.” (RG 000.35)
- “a token that represents a claim to 1 gram of gold and 1 kg of silver is not a TCP” (RG 000.35(a))
- “the operator makes investment decisions for the client” (RG 000.35(b))
- “a ‘direct’ or ‘native’ tokenisation arrangement (where each token represents a unit in a unit trust using the blockchain as the primary unit-holder register) would generally be a managed investment scheme rather than a TCP.” (Note to RG 000.35)
- “Underlying assets of a TCP can include financial products and can include digital tokens that are financial products.” (RG 000.33)
- “Merely possessing digital tokens does not make a facility a DAP—the operator must possess them for or on behalf of a client or their nominee.” (RG 000.37)
- “A facility may not be a DAP or TCP where the client cannot direct how the underlying assets are dealt with.” (RG 000.56)
- “Depending on its terms, the facility may be a derivative, a facility for making a financial investment or another financial product.” (RG 000.56)
- “An exemption from the requirement to hold an AFS licence does not mean that the arrangement ceases to be a DAP or TCP.” (RG 000.76)
- “The anticipated regulations (subject to Government processes) also extend specified licensing exemptions that apply to custodial or depository service arrangements to equivalent DAP and TCP arrangements.” (RG 000.75)
- “The client value and transaction value tests increase over time with the rate of inflation.” (Table 3, low-value DAP exemption)
- “If a facility is a DAP or TCP, and an exemption does not apply, the operator must hold an AFS licence with relevant authorisations to issue that type of platform” (RG 000.78)

**[6] ASIC’s roadmap for digital assets law reform implementation**  
ASIC · <https://www.asic.gov.au/about-asic/news-centre/news-items/asics-roadmap-for-digital-assets-law-reform-implementation>  
Saved copy: `evidence/snapshots/asic-roadmap.txt`

- “passed Parliament on 1 April 2026, received Royal Assent on 8 April 2026, and will commence on 9 April 2027. The DAF Act provides for an 18-month implementation timeline.” (Opening paragraph)

**[7] Deadline looms for digital asset businesses to apply for a licence**  
ASIC · <https://www.asic.gov.au/about-asic/news-centre/news-items/deadline-looms-for-digital-asset-businesses-to-apply-for-a-licence>  
Saved copy: `evidence/snapshots/asic-deadline.txt`

- “apply by 30 June 2026, before ASIC’s no-action position expires.” (Opening paragraph)
- “will commence on 9 April 2027” (Closing paragraphs)

**[8] Identity and participation on the network**  
Redbelly Network developer portal · <https://vine.redbelly.network/identity/>  
Saved copy: `evidence/snapshots/rb-identity.txt`

- “To ensure a baseline of accountability, all network participants MUST prove they are who they say they are before gaining access, a process facilitated by Receptor, Redbelly's native identity protocol.” (Identity and participation on the network)
- “organisations can be verified to ensure that other network parties can be confident that they're interacting with licensed entities, official representatives and official smart contracts on chain.” (Identity and participation on the network)

**[9] User access**  
Redbelly Network developer portal · <https://vine.redbelly.network/identity/user-access/>  
Saved copy: `evidence/snapshots/rb-user-access.txt`

- “users must work with their chosen accredited issuer to prove they possess a valid photo identity document (passport) which is verified via biometric checks.” (User access)

**[10] Receptor**  
Redbelly Network technical documentation · <https://docs.redbelly.network/pages/receptor/>  
Saved copy: `evidence/snapshots/rb-receptor.txt`

- “Receptor is Redbelly's native digital identity and verifiable credential protocol.” (Receptor overview)
- “Verifier: Use to define eligibility criteria, surface requests of those criteria to users, and verify the authenticity and validity of the claims made by users based on their verifiable credentials.” (Receptor modules)
- “ensuring that only eligible users can access particular products and services” (Receptor overview)

**[11] Eligibility SDK for Redbelly Network**  
Redbelly Network technical documentation · <https://docs.redbelly.network/pages/eligibility-sdk/eligibility-sdk/>  
Saved copy: `evidence/snapshots/rb-eligibility-sdk.txt`

- “This SDK enables developers to perform eligibility checks (e.g., age, KYC) with privacy-preserving proof submissions” (Eligibility SDK overview)

**[12] Individual onboarding, overview**  
Redbelly Network technical documentation · <https://docs.redbelly.network/pages/eligibility-sdk/onboarding/individual/overview/>  
Saved copy: `evidence/snapshots/rb-onboarding.txt`

- “It includes wallet authentication, KYC verification, and Redbelly on-chain permission setup.” (Overview)

**[13] Become an operator**  
Redbelly Network developer portal · <https://vine.redbelly.network/nodes/become-operator/>  
Saved copy: `evidence/snapshots/rb-node-operator.txt`

- “Applicants will be selected based upon their previous experience, location and commitment to the Redbelly Project.” (Submissions)
- “all nodes must stake 100,000 RBNT in order to participate.” (Requirements)
- “Submissions currently closed” (Submissions)

**[14] Asset tokenisation on Redbelly Network**  
Redbelly Network · <https://redbelly.network/asset-tokenisation>  
Saved copy: `evidence/snapshots/rb-tokenisation.txt`

- “Redbelly is Digital Public Token Infrastructure” (Section heading)
- “Deterministic finality ensures transactions are confirmed once and cannot be reversed” (Infrastructure features)
- “verifiable credentials enable tokenised investment products with defined investor eligibility, enforced at the point of trade.” (Asset issuers)

**[15] Redbelly Network selected for the Reserve Bank of Australia’s Project Acacia**  
Redbelly Network · <https://redbelly.network/projectacacia>  
Saved copy: `evidence/snapshots/rb-acacia.txt`

- “Redbelly Network has been selected for The Reserve Bank of Australia's (RBA) latest tokenization pilot, Project Acacia” (Announcement)

**[16] Tokeniser home page**  
Tokeniser · <https://tokeniser.com>  
Saved copy: `evidence/snapshots/tk-home.txt`

- “Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure” (Home page)

**[17] Our technology**  
Tokeniser · <https://tokeniser.com/technology>  
Saved copy: `evidence/snapshots/tk-technology.txt`

- “Redbelly is a public network designed to meet the three statutory tests for public digital token infrastructure under Australian law” (Common questions)
- “No. The protocol layer is designed to sit outside markets, clearing and settlement, and custody licensing.” (Common questions)
- “Eligibility, identity and your target market determination are enforced at the point of transfer, every time.” (Compliance built into the protocol)

**[18] Automated compliance**  
Tokeniser · <https://tokeniser.com/product/superpowers/automated-compliance>  
Saved copy: `evidence/snapshots/tk-compliance.txt`

- “Engineered to align with Australia's Digital Assets Framework, operating under your existing licence.” (Automated compliance)
- “Trades that fail a check do not proceed, and every check is logged.” (Automated compliance)

**[19] Tokeniser for funds**  
Tokeniser · <https://tokeniser.com/solutions/funds>  
Saved copy: `evidence/snapshots/tk-funds.txt`

- “Run your registry and investor lifecycle on Tokeniser today” (Funds)

**[20] TASK-30 brief: Australia’s Digital Assets Framework Act, what it means for Tokeniser**  
Redbelly DAO Community Task Board · <https://taskboard.redbellydao.network/tasks/TASK-30>  
Saved copy: `evidence/snapshots/task-brief.txt`

- “received Royal Assent on 8 April 2026 and commences on 9 April 2027” (Brief)
