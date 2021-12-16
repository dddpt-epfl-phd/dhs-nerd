

# Linking the DHS

## 1) Introduction

The Historical Dictionary of Switzerland (HDS) is a valuable source for historians and the general public on the History of Switzerland. It is the result of 30 years of dedicated work by historians with a vision for a detailed encyclopedia of Switzerland. Today it boasts a growing collection of 36'000 articles.

It was also at the forefront of the use of digital technologies in History. It offered its first online portal in 2006. It is actively participating in the push for linked data as part of the metagrid.ch consortium. Today, most of its articles are linked to wikidata.

The Dictionary was intended for publication as a paper encyclopedia. Its digital twin has been an evolution from this format. As a result, it still lacks some features that are hallmarks of born-digital encyclopedias.

Notably, cross-linking is a defining feature of Wikipedia. On a Wikipedia page, any entity that has its own article is directly linked to this article, offering an easy and enticing exploration experience.

Cross-linking of articles is currently in the process of being implemented in HDS articles. This project aims at making this process faster by automating using NLP techniques.

In this project, we will perform automated named entity recognition and disambiguation on the whole HDS, use it to link the articles among themselves and provide a demonstration interface for a linked HDS.

The rest of this report is organized as follows: in section 2), the methodology and techologies used are presented; in section 3), the results, evaluation and statistics are presented; finally, section 4) concludes and proposes future avenues to continue this work.

## 1) The Historical Dictionary of Switzerland

HDS articles are classified in 4 main categories: people, families, spatial and themes.

![articles lengths by category](./figures/articles_lengths_by_category.png "articles lengths by category")

A HDS article has many components:
1) article text
2) media components (images, maps, data tables)
3) a list of historical and bibliographic sources
4) links to the same entity on other linked databases (GND, VIAF, Swiss diplomatic documents, etc.)
5) structured data (birth and death dates, alternative names, etc.)
6) thematic indexation (categories such as "Elites before 1800", "Cantonal parliaments", etc.)

Components "1) article text", "3) sources" and "6) thematic indexation" are present in all articles. Component "4) links to other linked databases" is present in most articles while presence of the components "2) media" and "5) structured data" vary a lot.

Two examples of articles with most of the above components are the [city of Zurich](https://hls-dhs-dss.ch/articles/000171) and [Gustave Ador](https://hls-dhs-dss.ch/articles/003848/). [Schneckenbundgericht](https://hls-dhs-dss.ch/articles/029462/2016-11-23/) or [Schmerikon](https://hls-dhs-dss.ch/articles/001373/2011-08-10/)are typical sparse articles, without external links, media or structured data.

All articles are versioned, for example Bioley-Orjulaz just got updated from an [older version](https://hls-dhs-dss.ch/articles/002356/2004-09-30/) to [a new one](https://hls-dhs-dss.ch/articles/002356/2021-11-08/). It clearly shows that the question of cross-linking is currently being adressed at the HDS, at the same time this project has been going.

## 2) Methodology

The main steps of the projects are as follows:
1) downloading the whole HDS;
2) doing named entity recognition and disambiguation;
3) augmenting the HDS articles with the recognized entities; 
4) creating a demonstration interface for a linked HDS.

### 2.1) HDS articles extraction

We created a python scraper to download and parse the whole HDS.

Of the 6 type of components mentionned in section 1), the scraper gathers all of them except media components which squarely fall out of the scope of this project.



### 2.2) Named Entity Recognition and Disambiguation with entity-fishing

The main task of this project is named entities recognition and disambiguation.

Based on the result of the CLEF-HIPE 2020 challenge,

### 2.3) Demonstration Interface for a linked HDS

For this work

## 3) Results

## 4) Conclusion and future works