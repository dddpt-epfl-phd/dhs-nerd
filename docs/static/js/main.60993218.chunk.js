(this["webpackJsonpdhs-nerd-frontend"]=this["webpackJsonpdhs-nerd-frontend"]||[]).push([[0],{80:function(e,t,n){},81:function(e,t,n){"use strict";n.r(t);var r=n(0),i=n(24),c=n.n(i),s=(n(71),n(25)),a=n(7),l=n(6),d=n(89),o=n(1);function h(e,t,n){return!(!e[t]||!e[t][n]||""==e[t][n]||void 0===e[t][n]||null===e[t][n])&&e[t][n]}function j(e,t){return h(e,"annotation",t)}function u(e){var t=!(!e.dhsid||""==e.dhsid||void 0===e.dhsid||null===e.dhsid)&&e.dhsid;return t||(t=!(!e.href||""==e.href||void 0===e.href||null===e.href)&&function(e){return e.match(/\/(\w+)?\/?articles\/(.+?)\/(\d{4}-\d{2}-\d{2})?/)}(e.href)[2]),t}var b=function(e,t){return"https://<LNG>.wikipedia.org/?curid=".replace("<LNG>",e)+t};var x="dhs-dhs-link",g="dhs-original-dhs-link",O="dhs-wikipedia-link";function v(e){var t=e.className,n=void 0===t?"":t,r=e.children,i=void 0===r?[]:r;return Object(o.jsx)("span",{className:"no-text-link "+n,children:i})}function f(e){var t=e.dhsId,n=void 0===t?"":t,r=e.children,i=void 0===r?[]:r,c=e.originalLink,l=void 0!==c&&c,d=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"de";return(t?"/"+t:"")+"/articles/"+e}(n,Object(a.x)().language);return Object(o.jsx)(s.Link,{className:"dhs-dhs-link "+(l?g:""),to:d,children:i})}function p(e){var t=e.dhsId,n=void 0===t?"":t,r=e.language,i=void 0===r?"de":r,c=e.children,s=void 0===c?[]:c,a=function(e){var t=arguments.length>1&&void 0!==arguments[1]?arguments[1]:"de";return"https://hls-dhs-dss.ch"+(t?"/"+t:"")+"/articles/"+e}(n,i);return Object(o.jsx)("a",{className:"dhs-real-dhs-link",href:a,target:"_blank",children:s})}function m(e){var t=e.url,n=void 0===t?"":t,r=e.children,i=void 0===r?[]:r;return Object(o.jsx)("a",{className:O,href:n,target:"_blank",children:i})}function k(e){var t=e.url,n=void 0===t?"":t,r=e.children,i=void 0===r?[]:r;return Object(o.jsx)("a",{className:"dhs-wikidata-link",href:n,target:"_blank",children:i})}function w(e){var t=e.textlink,n=void 0===t?{}:t,r=e.language,i=void 0===r?"de":r,c=e.children,s=void 0===c?[]:c,a=n,l=u(a);if(l)return Object(o.jsx)(f,{dhsId:l,originalLink:"entity_fishing"!==a.origin,children:s});var d=function(e,t){var n=j(e,"wikipedia_page_id");return!!n&&b(t,n)}(a,i);if(d)return Object(o.jsx)(m,{url:d,children:s});var h=function(e){return j(e,"wikidata_entity_url")}(a);return h?Object(o.jsx)(k,{url:h,children:s}):Object(o.jsx)(v,{children:s})}var N=n(87),L=n(88),_=n(64),I=n(61),A=n(90),C=n(91),S=n(93),y=n(59),D=function(e){Object(I.a)(e);var t=Object(a.x)().language,n=["de","fr","it"].filter((function(e){return e!=t})).map((function(e){var n=(window.location+"").replace(t,e);return Object(o.jsx)(y.LinkContainer,{to:n,children:Object(o.jsx)(A.a.Item,{children:e.toUpperCase()})},e)}));return Object(o.jsx)(A.a,{className:"language-chooser",title:t.toUpperCase(),id:"basic-nav-dropdown",children:n})},T=function(){var e=Object(a.x)(),t=e.language;e.dhsId;return Object(o.jsxs)(C.a,{bg:"light",expand:"lg",children:[Object(o.jsx)(C.a.Toggle,{"aria-controls":"basic-navbar-nav"}),Object(o.jsx)(C.a.Collapse,{id:"basic-navbar-nav",children:Object(o.jsxs)(S.a,{className:"mr-auto",children:[Object(o.jsx)(y.LinkContainer,{to:"/"+t+"/articles",children:Object(o.jsx)(S.a.Link,{children:"Articles"})}),Object(o.jsx)(D,{})]})})]})};n(80);function E(e){var t=e.children;return Object(o.jsxs)("div",{className:"main",children:[Object(o.jsx)(T,{}),Object(o.jsx)(N.a,{className:"centered-article-container",children:Object(o.jsx)(L.a,{className:"justify-content-md-center",children:Object(o.jsx)(_.a,{lg:"7",className:"justify-content-md-center centered-article-content",children:t})})})]})}var H=function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:"";return console.log("CopyrightFooter originalPageLink: ",e),Object(o.jsxs)("div",{id:"copyright-footer",children:["The content of all HDS articles presented on this website are the work of their respective author from the original HDS. ",[e]," ",Object(o.jsx)("br",{}),"This work is available under the ",Object(o.jsx)("a",{href:"https://creativecommons.org/licenses/by-sa/4.0/",target:"_blank",children:"Creative Common Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0) "})]})};function G(e){var t=e.text,n=e.textLinks,r=void 0===n?[]:n,i=e.language,c=void 0===i?"de":i;if(0==r.length)return t;r.sort((function(e,t){return e.start-t.start}));var s={start:0,end:0},a=r.map((function(e,n){if(e.start>=s.end){var r=s.end;return s=e,[t.substring(r,e.start),Object(o.jsx)(w,{textlink:e,language:c,children:t.substring(e.start,e.end)},n)]}return console.warn("Overlapping text links\npreviousTextLink:",s,"\ntextLink: ",e),!1})).filter((function(e){return e})).flat();return a.push(t.substring(s.end,t.length)),a}function U(e){var t=e.tag,n=void 0===t?"p":t,r=e.textLinks,i=void 0===r?[]:r,c=e.children,s=void 0===c?"":c,a=e.language,l=void 0===a?"de":a,d=s[0];switch(n){case"h1":return Object(o.jsx)("h1",{children:s});case"h2":return Object(o.jsx)("h2",{children:s});case"h3":return Object(o.jsx)("h3",{children:s});case"h4":return Object(o.jsx)("h4",{children:s});case"p":return Object(o.jsx)("p",{children:Object(o.jsx)(G,{text:d,textLinks:i,language:l})});default:return Object(o.jsx)("div",{children:Object(o.jsx)(G,{text:d,textLinks:i,language:l})})}}function B(e){var t=e.article,n=void 0===t?{}:t,r=e.language,i=void 0===r?"de":r,c=e.baseurl,s=void 0===c?"":c;console.log("DhsArticleContent baseurl:",s),n.text_blocks&&n.text_blocks.length>0&&(n.text_blocks[0][1]=n.search_result_name);var a="20px",d=!!n.wikipedia_page_title&&b(i,n.wikipedia_page_title),h=!!n.wikidata_url&&n.wikidata_url,j=d?Object(o.jsx)(m,{url:d,children:Object(o.jsx)("img",{src:s+"/wikipedia.png",width:a,height:a})},"wk-tl"):"",u=h?Object(o.jsx)(k,{url:h,children:Object(o.jsx)("img",{src:s+"/wikidata.svg",width:a,height:a})},"wdt-l"):"",x=Object(o.jsxs)("span",{children:[Object(o.jsxs)(p,{dhsId:n.id,language:i,children:[" ",Object(o.jsx)("img",{src:s+"/hds.png",className:"real-dhs-article-external-link",width:a,height:a})]},"r-dhs-tl"),j,u]}),g=n.text_blocks?n.text_blocks.map((function(e,t){var r=Object(l.a)(e,2),c=r[0],s=r[1];return Object(o.jsx)(U,{tag:c,textLinks:n.text_links[t],language:i,children:[s," ",0==t?x:""]},t)})):"Loading...",O=Object(o.jsx)(p,{dhsId:n.id,children:"Original article"});return Object(o.jsxs)("div",{className:"dhs-article",children:[g,Object(o.jsx)(H,{originalPageLink:O})]})}function F(e){var t=e.baseurl,n=void 0===t?"":t,i=Object(a.x)(),c=i.language,s=i.dhsId,h=n+"/data/"+c+"/"+s+".json",j=Object(r.useState)({id:!0}),u=Object(l.a)(j,2),b=u[0],g=u[1];return Object(r.useEffect)((function(){fetch(h).then((function(e){return e.json()})).then((function(e){g(e)})).catch((function(e){console.warn("DhsArticle problem loading article: ",e),g({lastArticle:b})}))}),[h]),console.log("DhsArticle.js language",c,"dhsId:",s,", article:",b),b.id?Object(o.jsxs)(E,{children:[Object(o.jsxs)(d.a,{className:"dhs-article-info",variant:"info",children:[Object(o.jsx)("a",{className:x,children:"Blue links"})," point to other HDS articles.",Object(o.jsx)("br",{}),Object(o.jsx)("a",{className:O,children:"Green links"})," point to Wikipedia articles.",Object(o.jsx)("br",{}),Object(o.jsx)("a",{className:"dhs-dhs-link dhs-original-dhs-link",children:"Underdashed blue links"})," are links coming from the original HDS.",Object(o.jsx)("br",{})]}),Object(o.jsx)(B,{article:b,language:c,baseurl:n})]}):Object(o.jsx)(P,{lastArticle:b.lastArticle})}function P(e){var t=e.lastArticle,n=void 0===t?{}:t,r=Object(a.x)(),i=r.language,c=r.dhsId;return Object(o.jsxs)(E,{children:[Object(o.jsx)("h1",{children:"Error 404: Article not found"}),Object(o.jsxs)("p",{children:["Oops, it seems this article is missing. Are you sure the article id is correct?",Object(o.jsx)("br",{})]}),Object(o.jsx)("p",{children:Object(o.jsxs)("a",{href:"#",onClick:function(){return window.history.back()},children:["Go back ",n.title?"("+n.title+")":""]})}),c?Object(o.jsx)("p",{children:Object(o.jsx)(p,{dhsId:c,language:i,children:"Visit the original HDS article"})}):""]})}var J=n(92),R=n(62);function V(e){var t=e.articleTitle,n=e.dhsId;return Object(o.jsx)("div",{className:"dhs-articles-list-item",children:Object(o.jsxs)(f,{dhsId:n,children:[Object(o.jsx)("span",{className:"dhs-articles-list-item-id",children:n+" "}),Object(o.jsx)("span",{className:"dhs-articles-list-item-title",children:t})]})})}function W(e){var t=e.baseurl,n=void 0===t?"":t,i=Object(a.x)().language;console.log("ArticlesList.js language",i);var c=n+"/data/indices/"+i+".json",s=Object(r.useState)([]),d=Object(l.a)(s,2),h=d[0],j=d[1],u=Object(r.useState)([]),b=Object(l.a)(u,2),x=b[0],g=b[1];Object(r.useEffect)((function(){fetch(c).then((function(e){return e.json()})).then((function(e){g(e),j(e)}))}),[c]);return Object(o.jsxs)(E,{children:[Object(o.jsxs)(J.a,{id:"dhs-article-search",onSubmit:function(e){var t=document.getElementById("dhs-article-text-search").value;j(function(e,t){var n=t.toLowerCase();return e.filter((function(e){return-1!=e[1].toLowerCase().indexOf(n)}))}(x,t)),e.preventDefault(),e.stopPropagation()},children:[Object(o.jsx)(J.a.Group,{className:"mb-3",controlId:"dhs-article-text-search",children:Object(o.jsx)(J.a.Control,{type:"text",placeholder:"Search in articles' titles..."})}),Object(o.jsx)(R.a,{variant:"primary",type:"submit",children:"Search"})]}),h.filter((function(e,t){return t<100})).map((function(e,t){return Object(o.jsx)(V,{dhsId:e[0],articleTitle:e[1]},t)}))]})}var Y=function(e){var t=e.tadu,n=void 0===t?"DEFAULT":t;return Object(o.jsxs)("div",{children:["THIS IS A ",n," ROUTE"]})};function q(){return Object(o.jsx)(o.Fragment,{children:Object(o.jsx)(s.HashRouter,{children:Object(o.jsxs)(a.f,{basename:"/dhs-nerd",children:[Object(o.jsx)(a.d,{path:"/:language/articles/:dhsId",element:Object(o.jsx)(F,{baseurl:"/dhs-nerd"})}),Object(o.jsx)(a.d,{path:"/:language",element:Object(o.jsx)(W,{baseurl:"/dhs-nerd"})}),Object(o.jsx)(a.d,{path:"/:language/articles",element:Object(o.jsx)(W,{baseurl:"/dhs-nerd"})}),Object(o.jsx)(a.d,{exact:!0,path:"/",element:Object(o.jsx)(a.b,{to:"/fr"})}),Object(o.jsx)(a.d,{path:"*",element:Object(o.jsx)(Y,{})})]})})})}c.a.render(Object(o.jsx)(q,{}),document.getElementById("root"))}},[[81,1,2]]]);
//# sourceMappingURL=main.60993218.chunk.js.map