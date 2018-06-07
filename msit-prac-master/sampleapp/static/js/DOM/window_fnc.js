function Windows_FNC() {
    
    this.coos = ["0px", "5px"];
    
    this.stop = function () {
        piano.stp = !0;
        $("sheet_stop").style.visibility = "hidden";
        $("sheet_stop_sep").style.visibility = "hidden"
    };
    this.viewer = function () {
        var i = $("win");
        (i.style.visibility = "visible",
         (piano.stp = !0, $("s1").value = ""), 
         $("s1").style.top = "92px", 
         $("s1").style.height = "270px", 
         $("s1").readOnly = !1, 
         $("rec_bkg_title").innerHTML = "Recorder",
         $("recplay").style.visibility = "visible",  
         $("rec_tb3").style.visibility = "visible");
    };
    this.hider = function () {
        $("sheet_play").value = "► Play";
        $("sheet_stop").style.visibility = "hidden";
        $("sheet_stop_sep").style.visibility = "hidden"
    }
}
var win_fnc = new Windows_FNC;