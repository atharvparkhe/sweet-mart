// navbar collapse
var menuitem = document.getElementById("menuitem")
menuitem.style.maxHeight = "0px";
function menutoggle() {
    if (menuitem.style.maxHeight == "0px") {
        menuitem.style.maxHeight = "200px";
    }
    else {
        menuitem.style.maxHeight = "0px";
    }
}
// toast message
let x;
let toast = document.getElementById("toast");
function showToast(){
    clearTimeout(x);
    toast.style.transform = "translateX(0)";
    x = setTimeout(()=>{
        toast.style.transform = "translateX(400px)"
    }, 4000);
}
function closeToast(){
    toast.style.transform = "translateX(400px)";
}