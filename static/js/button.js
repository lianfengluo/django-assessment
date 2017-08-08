// if (document.all){ 
// window.attachEvent('onload',initAll)//IE中 
// } 
// else{
// $(document).ready(function() {
//         initAll();
//         // $('form').h5Validate();

//     })
// window.addEventListener('load',initAll,false);//firefox 
// }

$(function() {
    for (var i = 0; i < document.getElementsByTagName("button").length; i++) {
        if (document.getElementsByTagName("button")[i].type == "submit" || document.getElementsByTagName("button")[i].type == "reset") {
            rollbutton(document.getElementsByTagName("button")[i]);
        }
    }
});


function rollbutton(obj) {
    obj.moveout = new String;
    obj.moveout = obj.style.cssText;
    obj.onmouseout = function() {
        obj.style.cssText = obj.moveout;
    }
    obj.moveover = new String;
    obj.moveover = 'color:black;background:white;width:90%';
    obj.onmouseover = function() {
        obj.style.cssText = obj.moveover;
    }
}