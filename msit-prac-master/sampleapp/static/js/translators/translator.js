function Translator() {
    this.symbn = [];
    this.chord = [];
    this.time = [];
    this.defaults = function () {
        this.symbn = [0];
        this.chord = [""];
        this.time = [0, 0]
    };
    this.compile = function () {
        for (var t = $("s1").value, r, n = 0, i = 0, u; t.length > n;) 
            switch (t[n]) {
                case "{":
                    n++;
                    this.time[this.time.length - 1] = this.time[this.time.length - 1] + parseInt(t.substring(n, t.indexOf("}", n)));
                    n = t.indexOf("}", n) + 1;
                    break;
                default:
                    notes.w_n.indexOf(t[n]) != -1 || notes.b_n.indexOf(t[n]) != -1 ? 
                    (n != 0 && t[n - 1] != "}" && (this.time[this.time.length - 1] = this.time[this.time.length - 1] + 200), 
                    this.time[this.time.length] = this.time[this.time.length - 1], 
                    notes.w_n.indexOf(t[n]) != -1 ? this.chord[this.chord.length] = "a" + notes.w_c[notes.w_n.indexOf(t[n])] : 
                    notes.b_n.indexOf(t[n]) != -1 && (this.chord[this.chord.length] = "b" + notes.b_c[notes.b_n.indexOf(t[n])]), this.symbn[this.symbn.length] = ++n) : n++
            }
        return this.time.length != 0 && (this.time.length = this.time.length - 1), 
        u = [this.time, this.chord, this.symbn], this.defaults(), u
    }
}
var trans = new Translator;
trans.defaults();