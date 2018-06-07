function ReTranslator() {
    this.compile = function () {
        var e = "",i;
        for (i = 1; i < piano.chord.length; i++) 
        {
            e += "{" + (piano.time[i] - piano.time[i - 1]) + "}";
            if(notes.w_c.indexOf(parseInt(piano.chord[i].substr(1))) != -1)
                e += notes.w_n[notes.w_c.indexOf(parseInt(piano.chord[i].substr(1)))];
            else
                e += notes.b_n[notes.b_c.indexOf(parseInt(piano.chord[i].substr(1)))];
        }
        e = e.substr(3)
        $("s1").value = e;
    }
}
var retrans = new ReTranslator;
trans.defaults();