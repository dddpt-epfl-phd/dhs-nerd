import {
    Link,
    useParams
  } from "react-router-dom";



/*
 * Different text links:
 * - dhs-article
 * - wikipedia
 * - wikidata
 * 
 * needs:
 * - triage between the 3 different types
 * - choose to force a priority order
 * - 
 * 
 * triage:
 * - dhsArticle: has .dhsid property
 * - wikidata: has .wiki.item not null property
 * - wikipedia: has .wiki.articleLNG not null property
 * - unidentified identity: none of the above
 * 
 * 
 * 
 * 
 */

function getLinkSubProperty(textLink, property, subproperty){
    if( textLink[property] &&
        textLink[property][subproperty] &&
        textLink[property][subproperty]!="" &&
        textLink[property][subproperty]!==undefined &&
        textLink[property][subproperty]!==null
    ){
        return textLink[property][subproperty]        
    }
    return false

}

function getLinkWikiProperty(textLink, property){
    return getLinkSubProperty(TextLink,"wiki", property)
}

function getLinkAnnotationProperty(textLink, property){
    return getLinkSubProperty(TextLink,"wiki", property)
}


function getLinkAnnotationExtraField(textLink, extraField){
    const extraFields = getLinkAnnotationProperty(textLink, "extra_fields")
    return extraFields? extraFields[extraField] : false
}

export function getDhsUrlFromDhsId(dhsId, language="de"){
    return (language? "/"+language : "")+"/articles/"+dhsId
}
export function getRealDhsUrlFromDhsId(dhsId, language="de"){
    return "https://hls-dhs-dss.ch"+ (language? "/"+language : "")+"/articles/"+dhsId
}

/** dhsArticle: has .dhsid property
 * 
 * @param {*} textLink 
 * @returns {str or null}: this textLink dhs-id or false if no dhs id in this link (doesn't link to a dhs article)
 */
 export function getLinkDhsId(textLink){
    return textLink.dhsid && textLink.dhsid!="" && textLink.dhsid!==undefined && textLink.dhsid!==null? textLink.dhsid : false
}
/** dhsArticle: has .dhsid property
 * 
 * @param {*} textLink 
 * @returns {str or null}: this textLink dhs-id or false if no dhs id in this link (doesn't link to a dhs article)
 */
export function getLinkDhsUrl(textLink, language=false){
    const dhsId = getLinkDhsId(textLink)
    return dhsId? (language? "/"+language : "")+"/articles/"+dhsId : false
}

/**  wikipedia: has .wiki.articleLNG not null property
 * 
 * @param {*} textLink 
 * @returns {str or null}: this textLink wikipediaUrl or false if no wikipediaUrl in this link
 */
export function getLinkWikipediaUrl(textLink, language){
    return getLinkWikiProperty(textLink, "article"+language)
}

/**  wikidata: has .wiki.item not null property
 * 
 * @param {*} textLink 
 * @returns {str or null}: this textLink wikidataUrl or false if no wikidataUrl in this link
 */
export function getLinkWikidataUrl(textLink){
    return getLinkWikiProperty(textLink, "item")
}


export const noLinkClass = "no-text-link"
export const dhsLinkClass = "dhs-dhs-link"
export const realDhsLinkClass = "dhs-real-dhs-link"
export const wikipediaLinkClass = "dhs-wikipedia-link"
export const wikidataLinkClass = "dhs-wikidata-link"


export function NoTextLink({className="", children=[]}){
    return <span className={noLinkClass+" "+className}>{children}</span>
}



export function DhsArticleTextLink({dhsUrl = "", children=[]}){
    return <Link className={dhsLinkClass} to={dhsUrl}>{children}</Link>
}

export function DhsArticleLink({dhsId = "", children=[]}){
    const { language } = useParams();
    const dhsUrl = getDhsUrlFromDhsId(dhsId, language)
    return <Link className={dhsLinkClass} to={dhsUrl}>{children}</Link>
}
export function RealDhsArticleLink({dhsId = "", children=[]}){
    //https://hls-dhs-dss.ch/fr/articles/008015/2014-02-19/
    //const link = { pathname: getRealDhsUrlFromDhsId(dhsId) }
    const url = getRealDhsUrlFromDhsId(dhsId)
    console.log("RealDhsArticleLink url: ", url)
    return <a className={realDhsLinkClass} href={url} target="_blank">{children}</a>
}



export function WikipediaTextLink({url = "", children=[]}){
    const link = { pathname: url }
    return <Link className={wikipediaLinkClass} to={link} target="_blank">{children}</Link>
}



export function WikidataTextLink({url = "", children=[]}){
    const link = { pathname: url }
    return <Link className={wikidataLinkClass} to={link} target="_blank">{children}</Link>
}



export function TextLink({
    textlink = {},
    language="de",
    children = []
}){
    const textLink = textlink
    //console.log("<TextLink/> textLink:", textLink, "\nlanguage: ", language, "\nchildren: ", children,"\nzulu: ",zulu)
    const dhsId = getLinkDhsId(textLink)
    if(dhsId){
        return <DhsArticleLink dhsId={dhsId}>{children}</DhsArticleLink>
    }
    /*const dhsUrl = getLinkDhsUrl(textLink, language)
    if(dhsUrl){
        return <DhsArticleTextLink dhsUrl={dhsUrl}>{children}</DhsArticleTextLink>
    }*/
    const wikipediaUrl = getLinkWikipediaUrl(textLink, language)
    if(wikipediaUrl){
        return <WikipediaTextLink url={wikipediaUrl}>{children}</WikipediaTextLink>
    }
    const wikidataUrl = getLinkWikidataUrl(textLink)
    if(wikidataUrl){
        return <WikidataTextLink url={wikidataUrl}>{children}</WikidataTextLink>
    }
    return <NoTextLink>{children}</NoTextLink>
}



/* TEXT LINK EXAMPLE (with all options present):
{
    "start": 271,
    "end": 276,
    "mention": null,
    "origin": "entity_fishing",
    "annotation": {
        "wikidata_entity_id": "Q14274",
        "wikipedia_page_id": 168146,
        "wikipedia_page_title": null,
        "wikidata_entity_url": "http://www.wikidata.org/entity/Q14274",
        "grobid_tag": null,
        "extra_fields": {
            "rawName": "protestants",
            "confidence_score": 0.6095,
            "domains": [
                "Sociology",
                "Computer_Science"
            ],
            "origin": "entity_fishing"
        }
    },
    "href": "fr/articles/001620",
    "dhsid": "001620",
    "wiki": {
        "item": "http://www.wikidata.org/entity/Q14274",
        "itemLabel": "Aarau",
        "dhsid": "001620",
        "namefr": "Aarau",
        "articlefr": "https://fr.wikipedia.org/wiki/Aarau",
        "namede": "Aarau",
        "articlede": "https://de.wikipedia.org/wiki/Aarau",
        "nameit": "Aarau",
        "articleit": "https://it.wikipedia.org/wiki/Aarau",
        "nameen": "Aarau",
        "articleen": "https://en.wikipedia.org/wiki/Aarau",
        "instanceof": "http://www.wikidata.org/entity/Q14770218",
        "instanceofLabel": "capitale cantonale de Suisse",
        "gndid": "4000018-7",
        "wikidata_id": "Q14274"
    }
},

*/