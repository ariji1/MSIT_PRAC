function $(n) {
    return document.getElementById(n)
}

function random(n, t) {
    return t == undefined && (t = n, n = 0), 
        Math.floor(Math.random() * (t - n + 1)) + n
}

function select(n, t, i) {
    if (t == i && t == undefined) 
        return [$(n).selectionStart, $(n).selectionEnd];
    t == -1 && i == undefined && (t = $(n).value.length, i = t);
    i == undefined && t != undefined && (i = $(n).value.length);
    t > i && (t = t - i, i = t + i, t = i - t);
    $(n).selectionStart = t;
    $(n).selectionEnd = i;
    $(n).focus()
}