# Annotation Guidelines

> **Note**
> version 1.0, last updated October 21, 2022

We need to train our model to recognize three entities. The entities were based
on the CoNLL 2003 Shared Task by [Tjong Kim Sang and De Meulder
(2003)](#kimsang2003conll), whereas the guidelines were lifted from the [ACE
(Automatic Content Extraction) English Annotation Guidelines for
Entities](https://www.ldc.upenn.edu/sites/www.ldc.upenn.edu/files/english-entities-guidelines-v6.6.pdf)
by the Linguistic Data Consortium.

Entities are  limited to the following types:
- [**Person (PER):**](#person) person entities are limited to humans. It may be a single individual or group (e.g., *Juan de la Cruz*)
- [**Organization (ORG):**](#organization)  organization entities are limited to corporations, agencies, and other groups of people defined by an organizational structure (e.g.,  *United Nations*, *DPWH*, *Meralco*)
- [**Location (LOC):**](#location) location entities are geographical regions, areas, and landmasses. Subtypes of geo-political entities (GPE) are also included within this group. (e.g., *Pilipinas*, *Manila*, *Luzon*)


## General guidelines

1. **Annotate with respect to semantics.** Some entities may be classified as a member
    of a particular type in isolation, but not in context. Ensure that the entity being considered
    is *actually* used on the context we label it upon.

    Examples:
    - Dumating na ang bagyong "Ondoy" sa <Maynila|LOC> (The text *Ondoy* is not marked as a Person because it's a typhoon name.)
    - Magsasampa ng kaso ang <Ombudsman|ORG> sa Miyerkules. (In this context, the Ombudsman pertains to the office rather than a specific person.)

2. **Do not annotate punctuation marks that enclose an entity.** If an entity is
    enclosed within a quotation or parenthesis, then we should ignore those marks.
    We should only annotate the entity text.

3. **Do not annotate texts that are not in Tagalog.** The TLUnified dataset has a mix
    of documents in Bisaya. If you're using Prodigy, then <kbd>REJECT</kbd> them instead.

## <a id="person"></a>Guidelines for annotating Person (PER) entities

1. **Annotate name and nominal mentions as entities.** For example, the
    following are several mentions of a single entity: *Juan de la Cruz* (name
    mention), *kapitbahay* (nominal mention).

    - Si <Juan de la Cruz|PER> ay isang OFW.
    - Nakita ng <kapitbahay|PER> ang pangyayari.

2. **Do not annotate titles when they precede a named entity.** For example, in
    the span *President Ramon Magsaysay*, only *Ramon Magsaysay* is considered a
    Person entity. This rule also holds true when the title contains an Organization
    entity; we ignore the title altogether. In the case of *DepEd Secretary Jesli A.
    Lapus*, we only annotate *Jesli A. Lapus* and ignore *DepEd*. For saints and
    religious figures (e.g., *San Jose*, *Santa Clara*, etc.), we should treat *San* and
    *Santa* as titles and ignore them.

    Examples:
    - Nilagdaan ni President <Ramon Magsaysay|PER> ang Senate Bill No. 45.
    - Marami ang nag-iiwan ng itlog para kay Santa <Clara|PER>.

3. **Annotate Person entities even if they refer to more than one person, unless
    the group meets the requirements of an Organization.** For example, *mga
    senador*, should be annotated as a Person, but a collection of them, e.g.,
    *Senado* or *Blue Ribbon Committee*, should be annotated as an Organization.

    Examples:
    - Binatikos ng <mga senador|PER> ang NBN-ZTE deal.
    - Nanguna ang <Senate Blue Ribbon Committee|ORG> sa pag-imbestiga ng korapsyon.

4. **Annotate fictional characters unless they refer to TV show titles.** For
    example, in the phrase "nilunok ni Darna ang bato," the word *Darna* is treated as
    an entity. However, in the phrase "manonood ng Darna," the word *Darna* is
    ignored.

    Examples:
    - Natuklasan ni <Super Inggo|PER> ang sikreto ni <Boy Bawang|PER>.
    - Bukas na ang huling episode ng Super Inggo!

## <a id="organization"></a>Guidelines for annotating Organization (ORG) entities

1. **Annotate organizations that fall into the following subtypes:**
    - Government: those that are of, relating to, or dealing with the structure
        or affairs of government, politics, or the state. For example: *DSWD*,
        *Malacanang*, *Commission on Human Rights*, etc.
    - Commercial: those that are focused upon providing ideas, products, or
        services for profit. For example: *SMART-PLDT*, *Meralco*, *Ayala Group of
        Companies*, etc.
    - Educational: those that are focused upon furthering or promulgation of
        learning/education. For example: *UP*, *University of the Philippines*, *Ateneo
        de Manila University*, etc.
    - Entertainment: those that are focused on entertainment as its primary
        activity. For example: *Parokya ni Edgar*, *Eraserheads*, etc.
    - Non-governmental organizations (NGO): those that are not part of a
        government or commercial organization and whose main role is advocacy,
        charity, para-military, or politics. For example: *Moro Islamic Liberation
        Front*, *Caritas Manila*, *Ayala Foundation*, *Liberal Party*, etc.
    - Media: those whose primary interest is the distribution of news or
        publications, regardless of whether the organization is privately or
        publicly owned. For example: *ABS-CBN*, *GMA News*, etc.
    - Religious: those that are primarily devoted to issues of religious
        worship. For example: *Simbahang Katoliko*, *Archdiocese of Manila*, etc.
    - Scientific Institute: those whose primary activity is the application of
        medical care or the pursuit of scientific research. For example: *FDA*,
        *Philvocs*, etc.
    - Sports: those that are primarily concerned with participating in or
        governing organized sporting events. For example: *Gilas*, *FIFA*, *PBA*

2. **Annotate the full organization name and its shorthand separately.** Some texts specify the full
    name of an organization and its acronym, usually enclosed in a parenthesis. These two should
    be annotated separately.

    Examples:
    - Ang <Department of Education|ORG> (<DepEd|ORG>) ay nag-kansela ng klase hanggang high school.
    - Ang <Philippine Atmospheric Geophysical and Astronomical Services Administration|ORG> o <PAGASA|ORG> ay nagtalaga ng Signal No. 4 sa <Marinduque|LOC>.


## <a id="location"></a>Guidelines for annotating Location (LOC) entities

1. **Annotate locations that fall into the following subtypes:**

    - Address: name of a location in a postal system, or even abstract coordinates. For example: *31°
        S, 22° W*, *Forbes Park*.
    - Celestial: a location which is otherworldly or entire-world-inclusive. For example: *sa mundo*,
        *sa araw*, etc.
    - Water Body: bodies of water, natural or artificial. For example: *Pasig River*, *Angat Dam*, etc.
    - Land Region (natural): geologically or ecosystemically designated, non-artificial locations. For example:
        *Mt. Mayon*, *Bulkang Taal*,  etc.
    - International Region: taggable non-named locations that cross national borders. For example: *Timog Africa*,
        *Gitnang Silangan*, etc.
    - General Region: taggable locations that do not cross national borders. For example: *Timog Luzon*, etc.

2. **Do not annotate places distinguished only by the occurence of an event at
    that position**. For example: *sa kanilang bahay*, *sa mall*.

3. **Do not annotate general locative phrases.** Locations should be specific. Phrases like *sa itaas*, *sa gitna*,
    *sa pagitan ng*, should be ignored.

4. **Do not tag compass points unless they refer to sections of a region.** When a compass point (*hilaga*, *kanluran*, *timog*, *silangan*),
    is used as an adjective, then they should be ignored.

5. **Annotate facilities or man-made structures that fall into the following subtypes:**

    - Airport: a facility whose primary use is an airport. For example: *NAIA*, *Ninoy Aquino International Airport*, etc.
    - Plant: buildings that are used and designated solely for industrial purposes. For example: *Bataan National Power Plant*, etc.
    - Building or Grounds: man-made buildings, outdoor spaces, and other such facilities. For example: *Enchanted Kingdom*, *SM Mall of Asia*, etc.
    - Path: a facility that allows fluids, energies, persons, or vehicles to pass from one location to the other. For example: *EDSA*, *Welcome Rotunda*, etc.

6. **Annotate the full location name and its shorthand separately.** Some texts specify the full
    name of a location and its acronym, usually enclosed in a parenthesis. These two should
    be annotated separately.

    Examples:
    - Nagdiwang sa <Ninoy Aquino International Airport|LOC> (<NAIA|LOC>)...
    - Ginanap sa <MoA|LOC> o <SM Mall of Asia|LOC> ang palabas.

7. **Annotate Geopolitical Entities (GPE) that fall into the following subtypes:**

    - Continent: entireties of any of the seven continents. For example: *Asya*, *Amerika*, *Europa*, etc.
    - Nation: entireties of any nation. For example: *Pilipinas*, *Tsina*, *Espanya*, etc.
    - State or Province: entireties of any state or province of any nation. For example: *San Francisco*, *Bulacan*, *Region III*, *CALABARZON*, etc.
    - County or District: entireties of any country, district, prefrecture, or analogous body of any state. For example: *San Juan*, *District IV*, etc.

8. **Annotate the city and province as one entity if they're presented in the form CITY, PROVINCE.** For example,
    the text *Malolos, Bulacan* should be labeled as a single entity. This is usually the case for provincial addresses in the
    Philippines.

## References

- <a id="kimsang2003conll">Erik F. Tjong Kim Sang and Fien De Meulder</a>. 2003. Introduction to the CoNLL-2003 Shared Task: Language-Independent Named Entity Recognition. In *Proceedings of the Seventh Conference on Natural Language Learning at HLT-NAACL 2003*, pages 142–147.
