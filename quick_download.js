// ==UserScript==
// @name         Quick Download
// @namespace    qd
// @version      1.1
// @description  Quick Download <img><video> via Middle Mouse Click
// @author       wonnebju
// @grant        GM_download
// @grant        GM_log
// @match        https://xD.com/*
// @connect      *
// ==/UserScript==

var vids = document.getElementsByTagName("video");
var imgs = document.getElementsByTagName("img");

var handler = function(e) {
    if( e.which == 2 ) {
        e.preventDefault();
        dl(this.src);
        this.removeEventListener("mousedown", handler, false);
    }
}

for (var i = 0; i < imgs.length; i++) {
    imgs[i].addEventListener("mousedown", handler, false);
}

for (var t = 0; t < vids.length; t++) {
    vids[t].addEventListener("mousedown", handler, false);
}

function dl(url) {
    var prefix = 'xD_';
    var arg = {
        url: url,
        name: prefix + url.replace(/.+\/([^/]+)$/, "$1"),
        saveAs: false
    };

    var result = GM_download(arg);
}