// if (document.all){ 
// window.attachEvent('onload',initAll)//IE中 
// } 
// else{
$(document).ready(function()
    {initAll();})
// window.addEventListener('load',initAll,false);//firefox 
// }
function initAll(){
    for (var i=0;i<document.getElementsByTagName("input").length;i++)
    {  if(document.getElementsByTagName("input")[i].type=="submit" || document.getElementsByTagName("input")[i].type=="reset")
        {
        rollbutton(document.getElementsByTagName("input")[i]);
    }
    }
}
function rollbutton(obj){
    obj.moveout=new String;
    obj.moveout=obj.style.cssText;
    obj.onmouseout=function()
    {
        this.style.cssText=obj.moveout;
    }
    obj.mousedown=new String;
    obj.mousedown='color:white;background:#000;box-shadow: inset 0px 1px 0px #000, 0px 1px 0px #000;';
    obj.onmousedown=function(){
        obj.style.cssText=obj.mousedown;
    }    
    obj.mouseout=new String;
    obj.mouseout='color:orange;background:#000 ;box-shadow: inset 0px 1px 0px #000, 0px 1px 0px #000;';
    obj.onmouseup=function(){
        obj.style.cssText=obj.mouseout;
    }
    obj.moveout=new String;
    obj.moveover='color:orange;background:#000 ;box-shadow: inset 0px 1px 0px #000, 0px 1px 0px #000;';
    obj.onmouseover=function(){
        obj.style.cssText=obj.moveover;
    }
}

